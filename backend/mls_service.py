"""
MLS Integration Service using SimplyRETS
For Las Vegas GLVAR MLS integration
"""
import requests
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class MLSService:
    """Service for MLS property search and import"""
    
    def __init__(self, api_key: str = "simplyrets", api_secret: str = "simplyrets"):
        """
        Initialize MLS service with SimplyRETS credentials
        Default credentials are for demo/testing
        """
        self.base_url = "https://api.simplyrets.com"
        self.auth = (api_key, api_secret)
        
    def search_properties(
        self,
        city: Optional[str] = None,
        state: Optional[str] = "NV",
        zipcode: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        beds: Optional[int] = None,
        baths: Optional[float] = None,
        property_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search MLS properties with filters
        
        Args:
            city: City name (e.g., "Las Vegas")
            state: State code (default "NV" for Nevada)
            zipcode: ZIP code
            price_min: Minimum price
            price_max: Maximum price
            beds: Minimum bedrooms
            baths: Minimum bathrooms
            property_type: Property type (Residential, Commercial, etc.)
            limit: Number of results (max 500)
            offset: Pagination offset
            
        Returns:
            Dict with properties list and metadata
        """
        try:
            # Build query parameters
            params = {
                "limit": min(limit, 500),  # SimplyRETS max is 500
                "offset": offset
            }
            
            if city:
                params["cities"] = city
            if state:
                params["state"] = state
            if zipcode:
                params["postalCodes"] = zipcode
            if price_min:
                params["minprice"] = int(price_min)
            if price_max:
                params["maxprice"] = int(price_max)
            if beds:
                params["minbeds"] = int(beds)
            if baths:
                params["minbaths"] = float(baths)
            if property_type:
                params["type"] = property_type
            
            # Make request
            response = requests.get(
                f"{self.base_url}/properties",
                auth=self.auth,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            properties = response.json()
            
            logger.info(f"MLS search returned {len(properties)} properties")
            
            return {
                "success": True,
                "count": len(properties),
                "properties": properties,
                "filters": params
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"MLS search error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "properties": []
            }
    
    def get_property_details(self, mls_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific property
        
        Args:
            mls_id: The SimplyRETS property ID
            
        Returns:
            Property details or None if not found
        """
        try:
            response = requests.get(
                f"{self.base_url}/properties/{mls_id}",
                auth=self.auth,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching property {mls_id}: {str(e)}")
            return None
    
    def convert_to_deal(self, mls_property: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert MLS property data to our deal format
        
        Args:
            mls_property: Property data from SimplyRETS
            
        Returns:
            Deal data compatible with our analyzer
        """
        # Extract nested data safely
        property_data = mls_property.get('property', {})
        address_data = mls_property.get('address', {})
        listing_data = mls_property.get('listPrice', 0)
        
        # Build deal data
        deal = {
            # Basic info
            'address': self._format_address(address_data),
            'price': listing_data,
            'mls_id': mls_property.get('mlsId', ''),
            'listing_id': mls_property.get('listingId', ''),
            
            # Property details
            'property_type': property_data.get('type', 'residential').lower(),
            'beds': property_data.get('bedrooms', 0),
            'baths': property_data.get('bathsFull', 0) + property_data.get('bathsHalf', 0) * 0.5,
            'sqft': property_data.get('area', 0),
            'lot_size_acres': property_data.get('lotSize', 0) / 43560 if property_data.get('lotSize') else 0,
            'units': 1,
            
            # Financial (will be calculated by analyzer)
            'arv': 0,
            'estimated_rehab': 0,
            'monthly_rent': 0,
            'gross_income_annual': 0,
            
            # MLS specific
            'year_built': property_data.get('yearBuilt', 0),
            'days_on_market': mls_property.get('daysOnMarket', 0),
            'status': mls_property.get('listingStatus', ''),
            
            # Location
            'city': address_data.get('city', ''),
            'state': address_data.get('state', ''),
            'zipcode': address_data.get('postalCode', ''),
            
            # Additional
            'photos': [photo.get('url') for photo in mls_property.get('photos', [])],
            'description': mls_property.get('remarks', ''),
            'mls_source': 'SimplyRETS - Las Vegas GLVAR'
        }
        
        return deal
    
    def _format_address(self, address_data: Dict[str, Any]) -> str:
        """Format address from MLS data"""
        parts = []
        
        if address_data.get('streetNumber'):
            parts.append(str(address_data['streetNumber']))
        if address_data.get('streetName'):
            parts.append(address_data['streetName'])
        if address_data.get('city'):
            parts.append(address_data['city'])
        if address_data.get('state'):
            parts.append(address_data['state'])
        if address_data.get('postalCode'):
            parts.append(address_data['postalCode'])
        
        return ', '.join(parts) if parts else 'Address Not Available'
    
    def bulk_import_properties(self, property_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Import multiple properties by their IDs
        
        Args:
            property_ids: List of SimplyRETS property IDs
            
        Returns:
            List of converted deal data
        """
        deals = []
        
        for prop_id in property_ids:
            prop_data = self.get_property_details(prop_id)
            if prop_data:
                deal = self.convert_to_deal(prop_data)
                deals.append(deal)
        
        logger.info(f"Bulk imported {len(deals)} properties from MLS")
        return deals
