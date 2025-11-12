import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '../App';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Search, Home, DollarSign, Bed, Bath, CheckCircle, MapPin, Calendar, Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

export default function MLSPage() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState(false);
  const [properties, setProperties] = useState([]);
  const [selectedProperties, setSelectedProperties] = useState(new Set());
  
  // Search filters
  const [filters, setFilters] = useState({
    city: 'Las Vegas',
    state: 'NV',
    zipcode: '',
    price_min: '',
    price_max: '',
    beds: '',
    baths: '',
    property_type: '',
    limit: 50
  });

  // Check if user is enterprise/admin
  useEffect(() => {
    if (user && user.plan !== 'Enterprise' && user.plan !== 'Professional') {
      toast.error('MLS access is only available for Enterprise users');
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const handleSearch = async () => {
    try {
      setLoading(true);
      setSelectedProperties(new Set());
      
      // Build search params
      const searchParams = {
        city: filters.city || undefined,
        state: filters.state || undefined,
        zipcode: filters.zipcode || undefined,
        price_min: filters.price_min ? parseFloat(filters.price_min) : undefined,
        price_max: filters.price_max ? parseFloat(filters.price_max) : undefined,
        beds: filters.beds ? parseInt(filters.beds) : undefined,
        baths: filters.baths ? parseFloat(filters.baths) : undefined,
        property_type: filters.property_type || undefined,
        limit: filters.limit || 50
      };
      
      const response = await axios.post(`${API}/mls/search`, searchParams);
      
      if (response.data.success) {
        setProperties(response.data.properties || []);
        toast.success(`Found ${response.data.count} properties`);
      } else {
        toast.error(response.data.error || 'Search failed');
      }
    } catch (error) {
      console.error('MLS search error:', error);
      toast.error(error.response?.data?.detail || 'Failed to search MLS properties');
    } finally {
      setLoading(false);
    }
  };

  const togglePropertySelection = (mlsId) => {
    const newSelected = new Set(selectedProperties);
    if (newSelected.has(mlsId)) {
      newSelected.delete(mlsId);
    } else {
      newSelected.add(mlsId);
    }
    setSelectedProperties(newSelected);
  };

  const handleImport = async () => {
    if (selectedProperties.size === 0) {
      toast.error('Please select at least one property to import');
      return;
    }

    try {
      setImporting(true);
      const response = await axios.post(`${API}/mls/import`, {
        property_ids: Array.from(selectedProperties)
      });

      if (response.data.success) {
        toast.success(response.data.message);
        setTimeout(() => navigate('/deals'), 1500);
      }
    } catch (error) {
      console.error('Import error:', error);
      toast.error(error.response?.data?.detail || 'Failed to import properties');
    } finally {
      setImporting(false);
    }
  };

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(value);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">MLS Property Search</h1>
              <p className="text-gray-600">Las Vegas GLVAR MLS - Enterprise Access</p>
            </div>
            <Badge className="bg-purple-100 text-purple-800 text-sm px-4 py-2">
              {user?.plan || 'Enterprise'}
            </Badge>
          </div>
        </div>

        {/* Search Filters */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Search className="w-5 h-5" />
              <span>Search Filters</span>
            </CardTitle>
            <CardDescription>Search Las Vegas area properties</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <Label htmlFor="city">City</Label>
                <Input
                  id="city"
                  value={filters.city}
                  onChange={(e) => setFilters({...filters, city: e.target.value})}
                  placeholder="Las Vegas"
                  className="mt-2"
                />
              </div>

              <div>
                <Label htmlFor="zipcode">ZIP Code</Label>
                <Input
                  id="zipcode"
                  value={filters.zipcode}
                  onChange={(e) => setFilters({...filters, zipcode: e.target.value})}
                  placeholder="89101"
                  className="mt-2"
                />
              </div>

              <div>
                <Label htmlFor="price_min">Min Price</Label>
                <Input
                  id="price_min"
                  type="number"
                  value={filters.price_min}
                  onChange={(e) => setFilters({...filters, price_min: e.target.value})}
                  placeholder="200000"
                  className="mt-2"
                />
              </div>

              <div>
                <Label htmlFor="price_max">Max Price</Label>
                <Input
                  id="price_max"
                  type="number"
                  value={filters.price_max}
                  onChange={(e) => setFilters({...filters, price_max: e.target.value})}
                  placeholder="500000"
                  className="mt-2"
                />
              </div>

              <div>
                <Label htmlFor="beds">Min Beds</Label>
                <Input
                  id="beds"
                  type="number"
                  value={filters.beds}
                  onChange={(e) => setFilters({...filters, beds: e.target.value})}
                  placeholder="3"
                  className="mt-2"
                />
              </div>

              <div>
                <Label htmlFor="baths">Min Baths</Label>
                <Input
                  id="baths"
                  type="number"
                  step="0.5"
                  value={filters.baths}
                  onChange={(e) => setFilters({...filters, baths: e.target.value})}
                  placeholder="2"
                  className="mt-2"
                />
              </div>

              <div>
                <Label htmlFor="property_type">Property Type</Label>
                <select
                  id="property_type"
                  value={filters.property_type}
                  onChange={(e) => setFilters({...filters, property_type: e.target.value})}
                  className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="">All Types</option>
                  <option value="Residential">Residential</option>
                  <option value="Condo">Condo</option>
                  <option value="Townhouse">Townhouse</option>
                  <option value="Multi-Family">Multi-Family</option>
                </select>
              </div>

              <div>
                <Label htmlFor="limit">Results Limit</Label>
                <Input
                  id="limit"
                  type="number"
                  value={filters.limit}
                  onChange={(e) => setFilters({...filters, limit: e.target.value})}
                  placeholder="50"
                  className="mt-2"
                />
              </div>
            </div>

            <div className="mt-6 flex space-x-4">
              <Button
                size="lg"
                onClick={handleSearch}
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-5 w-5" />
                    Search MLS
                  </>
                )}
              </Button>

              {selectedProperties.size > 0 && (
                <Button
                  size="lg"
                  onClick={handleImport}
                  disabled={importing}
                  className="bg-green-600 hover:bg-green-700"
                >
                  {importing ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Importing...
                    </>
                  ) : (
                    <>
                      <CheckCircle className="mr-2 h-5 w-5" />
                      Import {selectedProperties.size} Selected
                    </>
                  )}
                </Button>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        {properties.length === 0 && !loading && (
          <Card>
            <CardContent className="py-12 text-center">
              <Home className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 text-lg">No properties found. Try adjusting your search filters.</p>
            </CardContent>
          </Card>
        )}

        {properties.length > 0 && (
          <div>
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">
                {properties.length} Properties Found
              </h2>
              <p className="text-sm text-gray-600">
                {selectedProperties.size} selected
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {properties.map((property) => {
                const address = property.address || {};
                const propertyData = property.property || {};
                const isSelected = selectedProperties.has(property.mlsId);

                return (
                  <Card
                    key={property.mlsId}
                    className={`cursor-pointer transition-all ${
                      isSelected ? 'ring-2 ring-blue-500 border-blue-500' : 'hover:shadow-lg'
                    }`}
                    onClick={() => togglePropertySelection(property.mlsId)}
                  >
                    {property.photos && property.photos.length > 0 && (
                      <img
                        src={property.photos[0]}
                        alt="Property"
                        className="w-full h-48 object-cover rounded-t-lg"
                      />
                    )}
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <MapPin className="w-4 h-4 text-gray-500" />
                            <p className="font-semibold text-gray-900 text-sm">
                              {address.streetNumber} {address.streetName}
                            </p>
                          </div>
                          <p className="text-xs text-gray-600">
                            {address.city}, {address.state} {address.postalCode}
                          </p>
                        </div>
                        {isSelected && (
                          <CheckCircle className="w-5 h-5 text-blue-600 flex-shrink-0" />
                        )}
                      </div>

                      <div className="flex items-center space-x-2 mb-3">
                        <DollarSign className="w-5 h-5 text-green-600" />
                        <span className="text-xl font-bold text-gray-900">
                          {formatCurrency(property.listPrice || 0)}
                        </span>
                      </div>

                      <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                        <div className="flex items-center space-x-1">
                          <Bed className="w-4 h-4" />
                          <span>{propertyData.bedrooms || 0} bd</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Bath className="w-4 h-4" />
                          <span>{propertyData.bathsFull || 0} ba</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Home className="w-4 h-4" />
                          <span>{propertyData.area ? propertyData.area.toLocaleString() : 0} sqft</span>
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <Badge variant="outline" className="text-xs">
                          {propertyData.type || 'Residential'}
                        </Badge>
                        {property.daysOnMarket && (
                          <div className="flex items-center space-x-1 text-xs text-gray-500">
                            <Calendar className="w-3 h-3" />
                            <span>{property.daysOnMarket} days</span>
                          </div>
                        )}
                      </div>

                      {property.listingId && (
                        <p className="text-xs text-gray-500 mt-2">
                          MLS#: {property.listingId}
                        </p>
                      )}
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
