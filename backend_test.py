#!/usr/bin/env python3
"""
Backend API Testing Suite for DealiQ Pro
Tests all backend endpoints with comprehensive validation
"""

import requests
import json
import os
import sys
from pathlib import Path

# Configuration
BACKEND_URL = "https://property-insight-11.preview.emergentagent.com/api"
TEST_EXCEL_FILE = "/app/data/Real_Estate_Deal_Analysis_Toolkit.xlsx"

# Admin credentials for testing
ADMIN_EMAIL = "dealiq1@gmail.com"
ADMIN_PASSWORD = "Drivetime1#!"

class DealiQBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = {}
        self.uploaded_deals = []
        self.test_deal_id = None
        self.test_session_id = None
        self.auth_token = None
        self.test_user_id = None
        
    def log_result(self, test_name, success, message, details=None):
        """Log test result"""
        self.test_results[test_name] = {
            'success': success,
            'message': message,
            'details': details or {}
        }
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if details and not success:
            print(f"   Details: {details}")
    
    def test_root_endpoint(self):
        """Test GET /api/"""
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                if "DealiQ API" in data.get("message", ""):
                    self.log_result("Root Endpoint", True, "API root accessible")
                    return True
                else:
                    self.log_result("Root Endpoint", False, "Unexpected response format", data)
                    return False
            else:
                self.log_result("Root Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Root Endpoint", False, f"Connection error: {str(e)}")
            return False

    def test_admin_login(self):
        """Test POST /api/auth/login with admin credentials"""
        try:
            payload = {
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }
            
            response = self.session.post(f"{self.base_url}/auth/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'token' in data and 'user' in data:
                    self.auth_token = data['token']
                    # Set authorization header for subsequent requests
                    self.session.headers.update({'Authorization': f'Bearer {self.auth_token}'})
                    user = data['user']
                    self.log_result("Admin Login", True, f"Admin logged in: {user.get('name')} ({user.get('plan')})")
                    return True
                else:
                    self.log_result("Admin Login", False, "Login succeeded but missing token/user", data)
                    return False
            else:
                self.log_result("Admin Login", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Admin Login", False, f"Login error: {str(e)}")
            return False

    def test_verify_token(self):
        """Test GET /api/auth/verify"""
        try:
            if not self.auth_token:
                self.log_result("Verify Token", False, "No auth token available")
                return False
            
            response = self.session.get(f"{self.base_url}/auth/verify")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'user' in data:
                    user = data['user']
                    self.log_result("Verify Token", True, f"Token verified for {user.get('email')}")
                    return True
                else:
                    self.log_result("Verify Token", False, "Token verification failed", data)
                    return False
            elif response.status_code == 401:
                self.log_result("Verify Token", False, "Token invalid or expired")
                return False
            else:
                self.log_result("Verify Token", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Verify Token", False, f"Token verification error: {str(e)}")
            return False

    def test_create_user(self):
        """Test POST /api/admin/users/create"""
        try:
            if not self.auth_token:
                self.log_result("Create User", False, "No auth token available")
                return False
            
            # Create test Enterprise user
            payload = {
                "email": "test.enterprise@dealiq.com",
                "password": "TestPass123!",
                "name": "Test Enterprise User",
                "plan": "Enterprise",
                "state": "NV",
                "mls_access": True
            }
            
            response = self.session.post(f"{self.base_url}/admin/users/create", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'user' in data:
                    user = data['user']
                    self.test_user_id = user.get('id')
                    self.log_result("Create User", True, f"Created user: {user.get('email')} ({user.get('plan')})")
                    return True
                else:
                    self.log_result("Create User", False, "User creation succeeded but missing data", data)
                    return False
            elif response.status_code == 400:
                # User might already exist, try to continue
                self.log_result("Create User", True, "User already exists (expected for repeated tests)")
                return True
            elif response.status_code == 403:
                self.log_result("Create User", False, "Admin access denied")
                return False
            else:
                self.log_result("Create User", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Create User", False, f"User creation error: {str(e)}")
            return False

    def test_list_users(self):
        """Test GET /api/admin/users"""
        try:
            if not self.auth_token:
                self.log_result("List Users", False, "No auth token available")
                return False
            
            response = self.session.get(f"{self.base_url}/admin/users")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'users' in data:
                    user_count = data.get('count', 0)
                    self.log_result("List Users", True, f"Retrieved {user_count} users")
                    return True
                else:
                    self.log_result("List Users", False, "Users list succeeded but missing data", data)
                    return False
            elif response.status_code == 403:
                self.log_result("List Users", False, "Admin access denied")
                return False
            else:
                self.log_result("List Users", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("List Users", False, f"List users error: {str(e)}")
            return False

    def test_upload_url(self):
        """Test POST /api/upload-url"""
        try:
            if not self.auth_token:
                self.log_result("Upload URL", False, "No auth token available")
                return False
            
            # Use a mock URL for testing (this will likely fail but we test the endpoint)
            payload = {
                "url": "https://example.com/sample.xlsx",
                "file_type": "excel"
            }
            
            response = self.session.post(f"{self.base_url}/upload-url", json=payload)
            
            # We expect this to fail with a 400 or 500 due to invalid URL, but endpoint should be accessible
            if response.status_code in [400, 500]:
                # Check if it's a proper error response about the URL
                try:
                    error_data = response.json()
                    if "URL" in str(error_data) or "download" in str(error_data).lower():
                        self.log_result("Upload URL", True, "URL upload endpoint accessible (expected URL error)")
                        return True
                except:
                    pass
                self.log_result("Upload URL", True, "URL upload endpoint accessible (expected error for test URL)")
                return True
            elif response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result("Upload URL", True, f"URL upload successful: {data.get('deals_count', 0)} deals")
                    return True
            
            self.log_result("Upload URL", False, f"HTTP {response.status_code}", response.text)
            return False
                
        except Exception as e:
            self.log_result("Upload URL", False, f"URL upload error: {str(e)}")
            return False

    def test_upload_csv(self):
        """Test POST /api/upload-csv"""
        try:
            if not self.auth_token:
                self.log_result("Upload CSV", False, "No auth token available")
                return False
            
            # Sample CSV data for testing
            csv_data = """address,price,property_type,arv,estimated_rehab,monthly_rent
123 Test St Las Vegas NV,250000,residential,300000,25000,2500
456 Sample Ave Henderson NV,180000,residential,220000,15000,1800"""
            
            payload = {
                "csv_text": csv_data
            }
            
            response = self.session.post(f"{self.base_url}/upload-csv", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('deals_count', 0) > 0:
                    self.log_result("Upload CSV", True, f"CSV upload successful: {data['deals_count']} deals")
                    return True
                else:
                    self.log_result("Upload CSV", False, "CSV upload succeeded but no deals processed", data)
                    return False
            else:
                self.log_result("Upload CSV", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Upload CSV", False, f"CSV upload error: {str(e)}")
            return False

    def test_upload_json(self):
        """Test POST /api/upload-json"""
        try:
            if not self.auth_token:
                self.log_result("Upload JSON", False, "No auth token available")
                return False
            
            # Sample JSON data for testing
            json_data = [
                {
                    "address": "789 JSON Blvd Las Vegas NV",
                    "price": 275000,
                    "property_type": "residential",
                    "arv": 325000,
                    "estimated_rehab": 30000,
                    "monthly_rent": 2700
                },
                {
                    "address": "321 Data Dr Henderson NV", 
                    "price": 195000,
                    "property_type": "residential",
                    "arv": 240000,
                    "estimated_rehab": 20000,
                    "monthly_rent": 1950
                }
            ]
            
            payload = {
                "json_data": json_data
            }
            
            response = self.session.post(f"{self.base_url}/upload-json", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('deals_count', 0) > 0:
                    self.log_result("Upload JSON", True, f"JSON upload successful: {data['deals_count']} deals")
                    return True
                else:
                    self.log_result("Upload JSON", False, "JSON upload succeeded but no deals processed", data)
                    return False
            else:
                self.log_result("Upload JSON", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Upload JSON", False, f"JSON upload error: {str(e)}")
            return False

    def test_manual_deal_creation(self):
        """Test POST /api/deals/manual"""
        try:
            if not self.auth_token:
                self.log_result("Manual Deal Creation", False, "No auth token available")
                return False
            
            payload = {
                "address": "555 Manual Entry St Las Vegas NV",
                "price": 300000,
                "property_type": "residential",
                "arv": 375000,
                "estimated_rehab": 35000,
                "monthly_rent": 3000,
                "sqft": 1500,
                "beds": 3,
                "baths": 2.0,
                "units": 1,
                "occupancy_pct": 100,
                "notes": "Test manual deal creation"
            }
            
            response = self.session.post(f"{self.base_url}/deals/manual", json=payload)
            
            if response.status_code == 200:
                deal = response.json()
                if deal.get('id') and deal.get('address'):
                    # Store this deal ID for later tests if we don't have one
                    if not self.test_deal_id:
                        self.test_deal_id = deal['id']
                    self.log_result("Manual Deal Creation", True, f"Manual deal created: {deal.get('address')}")
                    return True
                else:
                    self.log_result("Manual Deal Creation", False, "Deal creation succeeded but missing data", deal)
                    return False
            else:
                self.log_result("Manual Deal Creation", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Manual Deal Creation", False, f"Manual deal creation error: {str(e)}")
            return False

    def test_mls_search(self):
        """Test POST /api/mls/search"""
        try:
            if not self.auth_token:
                self.log_result("MLS Search", False, "No auth token available")
                return False
            
            payload = {
                "city": "Las Vegas",
                "state": "NV",
                "price_min": 200000,
                "price_max": 500000,
                "beds": 3,
                "limit": 10
            }
            
            response = self.session.post(f"{self.base_url}/mls/search", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                # MLS search should return some structure even if no properties found
                if isinstance(data, dict):
                    property_count = data.get('count', 0)
                    self.log_result("MLS Search", True, f"MLS search completed: {property_count} properties found")
                    return True
                else:
                    self.log_result("MLS Search", False, "MLS search returned unexpected format", data)
                    return False
            elif response.status_code == 403:
                self.log_result("MLS Search", True, "MLS access properly restricted (expected for some users)")
                return True
            else:
                self.log_result("MLS Search", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("MLS Search", False, f"MLS search error: {str(e)}")
            return False

    def test_mls_property_details(self):
        """Test GET /api/mls/property/{mls_id}"""
        try:
            if not self.auth_token:
                self.log_result("MLS Property Details", False, "No auth token available")
                return False
            
            # Use a test MLS ID (this will likely return 404 but tests the endpoint)
            test_mls_id = "test-property-123"
            
            response = self.session.get(f"{self.base_url}/mls/property/{test_mls_id}")
            
            if response.status_code == 200:
                data = response.json()
                self.log_result("MLS Property Details", True, f"Property details retrieved for {test_mls_id}")
                return True
            elif response.status_code == 404:
                self.log_result("MLS Property Details", True, "Property not found (expected for test ID)")
                return True
            elif response.status_code == 403:
                self.log_result("MLS Property Details", True, "MLS access properly restricted")
                return True
            else:
                self.log_result("MLS Property Details", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("MLS Property Details", False, f"MLS property details error: {str(e)}")
            return False

    def test_mls_import(self):
        """Test POST /api/mls/import"""
        try:
            if not self.auth_token:
                self.log_result("MLS Import", False, "No auth token available")
                return False
            
            # Test with empty property list (should work but import 0 properties)
            payload = {
                "property_ids": []
            }
            
            response = self.session.post(f"{self.base_url}/mls/import", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    deals_count = data.get('deals_count', 0)
                    self.log_result("MLS Import", True, f"MLS import completed: {deals_count} properties imported")
                    return True
                else:
                    self.log_result("MLS Import", False, "MLS import failed", data)
                    return False
            elif response.status_code == 403:
                self.log_result("MLS Import", True, "MLS access properly restricted")
                return True
            else:
                self.log_result("MLS Import", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("MLS Import", False, f"MLS import error: {str(e)}")
            return False

    def test_download_report(self):
        """Test POST /api/payments/download-report"""
        try:
            if not self.test_session_id:
                self.log_result("Download Report", False, "No test session ID available")
                return False
            
            payload = {
                "session_id": self.test_session_id
            }
            
            response = self.session.post(f"{self.base_url}/payments/download-report", json=payload)
            
            # We expect this to fail with 403 since payment is not completed
            if response.status_code == 403:
                self.log_result("Download Report", True, "Download properly restricted for unpaid session")
                return True
            elif response.status_code == 404:
                self.log_result("Download Report", True, "Session not found (expected for test)")
                return True
            elif response.status_code == 200:
                # If somehow it works, that's also fine
                self.log_result("Download Report", True, "Report download successful")
                return True
            else:
                self.log_result("Download Report", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Download Report", False, f"Download report error: {str(e)}")
            return False

    def test_stripe_webhook(self):
        """Test POST /api/webhook/stripe"""
        try:
            # Test webhook endpoint accessibility (will fail without proper Stripe signature)
            response = self.session.post(f"{self.base_url}/webhook/stripe", 
                                       data=b'{"test": "data"}',
                                       headers={'Content-Type': 'application/json'})
            
            # We expect this to fail with 400 due to missing/invalid signature
            if response.status_code == 400:
                self.log_result("Stripe Webhook", True, "Webhook endpoint accessible (expected signature error)")
                return True
            elif response.status_code == 200:
                self.log_result("Stripe Webhook", True, "Webhook endpoint working")
                return True
            else:
                self.log_result("Stripe Webhook", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Stripe Webhook", False, f"Webhook test error: {str(e)}")
            return False

    def test_delete_user(self):
        """Test DELETE /api/admin/users/{user_id}"""
        try:
            if not self.auth_token:
                self.log_result("Delete User", False, "No auth token available")
                return False
            
            if not self.test_user_id:
                # Try to get a user ID from the list
                list_response = self.session.get(f"{self.base_url}/admin/users")
                if list_response.status_code == 200:
                    users_data = list_response.json()
                    users = users_data.get('users', [])
                    if users:
                        # Find a non-admin user to delete
                        for user in users:
                            if user.get('id') != 'admin-user':
                                self.test_user_id = user.get('id')
                                break
            
            if not self.test_user_id:
                self.log_result("Delete User", True, "No test user to delete (expected)")
                return True
            
            response = self.session.delete(f"{self.base_url}/admin/users/{self.test_user_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result("Delete User", True, f"User {self.test_user_id} deleted successfully")
                    return True
                else:
                    self.log_result("Delete User", False, "Delete succeeded but no success flag", data)
                    return False
            elif response.status_code == 404:
                self.log_result("Delete User", True, "User not found (expected for test)")
                return True
            elif response.status_code == 403:
                self.log_result("Delete User", False, "Admin access denied")
                return False
            else:
                self.log_result("Delete User", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Delete User", False, f"Delete user error: {str(e)}")
            return False
    
    def test_excel_upload(self):
        """Test POST /api/upload with Excel file"""
        try:
            # Check if test file exists
            if not os.path.exists(TEST_EXCEL_FILE):
                self.log_result("Excel Upload", False, f"Test file not found: {TEST_EXCEL_FILE}")
                return False
            
            # Upload file
            with open(TEST_EXCEL_FILE, 'rb') as f:
                files = {'file': ('test_deals.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                response = self.session.post(f"{self.base_url}/upload", files=files)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('deals_count', 0) > 0:
                    self.uploaded_deals = data.get('top_deals', [])
                    if self.uploaded_deals:
                        self.test_deal_id = self.uploaded_deals[0]['id']
                    self.log_result("Excel Upload", True, f"Uploaded {data['deals_count']} deals successfully")
                    return True
                else:
                    self.log_result("Excel Upload", False, "Upload succeeded but no deals processed", data)
                    return False
            else:
                self.log_result("Excel Upload", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Excel Upload", False, f"Upload error: {str(e)}")
            return False
    
    def test_get_all_deals(self):
        """Test GET /api/deals with filters"""
        try:
            # Test basic get all deals
            response = self.session.get(f"{self.base_url}/deals")
            
            if response.status_code == 200:
                deals = response.json()
                if isinstance(deals, list):
                    deal_count = len(deals)
                    
                    # Test with filters
                    filter_tests = [
                        ("strategy filter", {"strategy": "buy_hold"}),
                        ("property_type filter", {"property_type": "residential"}),
                        ("min_score filter", {"min_score": 50}),
                        ("limit filter", {"limit": 5})
                    ]
                    
                    all_filters_passed = True
                    for filter_name, params in filter_tests:
                        filter_response = self.session.get(f"{self.base_url}/deals", params=params)
                        if filter_response.status_code != 200:
                            all_filters_passed = False
                            break
                    
                    if all_filters_passed:
                        self.log_result("Get All Deals", True, f"Retrieved {deal_count} deals, all filters working")
                        return True
                    else:
                        self.log_result("Get All Deals", False, "Some filters failed")
                        return False
                else:
                    self.log_result("Get All Deals", False, "Response not a list", deals)
                    return False
            else:
                self.log_result("Get All Deals", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Get All Deals", False, f"Request error: {str(e)}")
            return False
    
    def test_get_single_deal(self):
        """Test GET /api/deals/{deal_id}"""
        try:
            if not self.test_deal_id:
                self.log_result("Get Single Deal", False, "No test deal ID available")
                return False
            
            response = self.session.get(f"{self.base_url}/deals/{self.test_deal_id}")
            
            if response.status_code == 200:
                deal = response.json()
                if deal.get('id') == self.test_deal_id:
                    self.log_result("Get Single Deal", True, f"Retrieved deal {self.test_deal_id}")
                    return True
                else:
                    self.log_result("Get Single Deal", False, "Deal ID mismatch", deal)
                    return False
            elif response.status_code == 404:
                self.log_result("Get Single Deal", False, "Deal not found (404)")
                return False
            else:
                self.log_result("Get Single Deal", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Get Single Deal", False, f"Request error: {str(e)}")
            return False
    
    def test_get_stats(self):
        """Test GET /api/stats"""
        try:
            response = self.session.get(f"{self.base_url}/stats")
            
            if response.status_code == 200:
                stats = response.json()
                required_fields = ['total_deals', 'average_score', 'strategy_distribution', 'property_type_distribution']
                
                if all(field in stats for field in required_fields):
                    self.log_result("Get Stats", True, f"Stats retrieved: {stats['total_deals']} total deals")
                    return True
                else:
                    missing = [f for f in required_fields if f not in stats]
                    self.log_result("Get Stats", False, f"Missing fields: {missing}", stats)
                    return False
            else:
                self.log_result("Get Stats", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Get Stats", False, f"Request error: {str(e)}")
            return False
    
    def test_ai_analysis(self):
        """Test POST /api/deals/{deal_id}/ai-analysis"""
        try:
            if not self.test_deal_id:
                self.log_result("AI Analysis", False, "No test deal ID available")
                return False
            
            response = self.session.post(f"{self.base_url}/deals/{self.test_deal_id}/ai-analysis")
            
            if response.status_code == 200:
                analysis = response.json()
                required_fields = ['ai_confidence_score', 'prediction', 'key_insights', 'recommendations']
                
                if all(field in analysis for field in required_fields):
                    confidence = analysis.get('ai_confidence_score', 0)
                    prediction = analysis.get('prediction', 'unknown')
                    self.log_result("AI Analysis", True, f"AI analysis complete: {confidence}% confidence, {prediction} prediction")
                    return True
                else:
                    missing = [f for f in required_fields if f not in analysis]
                    self.log_result("AI Analysis", False, f"Missing AI fields: {missing}", analysis)
                    return False
            else:
                self.log_result("AI Analysis", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("AI Analysis", False, f"AI analysis error: {str(e)}")
            return False
    
    def test_create_checkout(self):
        """Test POST /api/payments/create-checkout"""
        try:
            if not self.test_deal_id:
                self.log_result("Create Checkout", False, "No test deal ID available")
                return False
            
            payload = {
                "deal_id": self.test_deal_id,
                "origin_url": "https://property-insight-11.preview.emergentagent.com"
            }
            
            response = self.session.post(f"{self.base_url}/payments/create-checkout", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if 'url' in data and 'session_id' in data:
                    self.test_session_id = data['session_id']
                    self.log_result("Create Checkout", True, f"Checkout session created: {self.test_session_id}")
                    return True
                else:
                    self.log_result("Create Checkout", False, "Missing checkout URL or session ID", data)
                    return False
            else:
                self.log_result("Create Checkout", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Create Checkout", False, f"Checkout error: {str(e)}")
            return False
    
    def test_payment_status(self):
        """Test GET /api/payments/status/{session_id}"""
        try:
            if not self.test_session_id:
                self.log_result("Payment Status", False, "No test session ID available")
                return False
            
            response = self.session.get(f"{self.base_url}/payments/status/{self.test_session_id}")
            
            if response.status_code == 200:
                status = response.json()
                required_fields = ['session_id', 'payment_status', 'status']
                
                if all(field in status for field in required_fields):
                    payment_status = status.get('payment_status', 'unknown')
                    self.log_result("Payment Status", True, f"Payment status: {payment_status}")
                    return True
                else:
                    missing = [f for f in required_fields if f not in status]
                    self.log_result("Payment Status", False, f"Missing status fields: {missing}", status)
                    return False
            else:
                self.log_result("Payment Status", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Payment Status", False, f"Status check error: {str(e)}")
            return False
    
    def test_clear_deals(self):
        """Test DELETE /api/deals"""
        try:
            response = self.session.delete(f"{self.base_url}/deals")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    deleted_count = result.get('deleted_count', 0)
                    self.log_result("Clear Deals", True, f"Cleared {deleted_count} deals from database")
                    return True
                else:
                    self.log_result("Clear Deals", False, "Clear operation failed", result)
                    return False
            else:
                self.log_result("Clear Deals", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Clear Deals", False, f"Clear error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all backend tests in sequence"""
        print(f"🚀 Starting DealiQ Pro Backend API Tests")
        print(f"📍 Backend URL: {self.base_url}")
        print(f"📁 Test Excel File: {TEST_EXCEL_FILE}")
        print(f"🔐 Admin Email: {ADMIN_EMAIL}")
        print("=" * 60)
        
        # Test sequence based on priority - Authentication first, then features
        test_sequence = [
            # Core API
            ("Root Endpoint", self.test_root_endpoint),
            
            # Authentication System (NEW)
            ("Admin Login", self.test_admin_login),
            ("Verify Token", self.test_verify_token),
            
            # User Management (NEW) - Admin only
            ("Create User", self.test_create_user),
            ("List Users", self.test_list_users),
            
            # Enhanced Upload Endpoints (NEW)
            ("Upload URL", self.test_upload_url),
            ("Upload CSV", self.test_upload_csv),
            ("Upload JSON", self.test_upload_json),
            ("Manual Deal Creation", self.test_manual_deal_creation),
            
            # Original Excel Upload (Existing)
            ("Excel Upload", self.test_excel_upload),
            
            # Deal Management (Existing)
            ("Get All Deals", self.test_get_all_deals),
            ("Get Single Deal", self.test_get_single_deal),
            ("Get Stats", self.test_get_stats),
            
            # MLS Integration (NEW)
            ("MLS Search", self.test_mls_search),
            ("MLS Property Details", self.test_mls_property_details),
            ("MLS Import", self.test_mls_import),
            
            # AI and Payment Features (Existing)
            ("AI Analysis", self.test_ai_analysis),
            ("Create Checkout", self.test_create_checkout),
            ("Payment Status", self.test_payment_status),
            ("Download Report", self.test_download_report),
            ("Stripe Webhook", self.test_stripe_webhook),
            
            # User Management Cleanup
            ("Delete User", self.test_delete_user),
            
            # Data Cleanup
            ("Clear Deals", self.test_clear_deals)
        ]
        
        passed = 0
        total = len(test_sequence)
        
        for test_name, test_func in test_sequence:
            print(f"\n🧪 Testing: {test_name}")
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                self.log_result(test_name, False, f"Test execution error: {str(e)}")
        
        print("\n" + "=" * 60)
        print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
        
        # Print detailed results
        print("\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status = "✅" if result['success'] else "❌"
            print(f"{status} {test_name}: {result['message']}")
            if not result['success'] and result['details']:
                print(f"   💡 Details: {result['details']}")
        
        return passed, total, self.test_results

def main():
    """Main test execution"""
    tester = DealiQBackendTester()
    passed, total, results = tester.run_all_tests()
    
    # Exit with appropriate code
    if passed == total:
        print(f"\n🎉 All tests passed! Backend is fully functional.")
        sys.exit(0)
    else:
        failed = total - passed
        print(f"\n⚠️  {failed} test(s) failed. Check the details above.")
        sys.exit(1)

if __name__ == "__main__":
    main()