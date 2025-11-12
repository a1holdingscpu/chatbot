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

class DealiQBackendTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = {}
        self.uploaded_deals = []
        self.test_deal_id = None
        self.test_session_id = None
        
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
                if "DealiQ Pro API" in data.get("message", ""):
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
        print("=" * 60)
        
        # Test sequence based on priority
        test_sequence = [
            ("Root Endpoint", self.test_root_endpoint),
            ("Excel Upload", self.test_excel_upload),
            ("Get All Deals", self.test_get_all_deals),
            ("Get Single Deal", self.test_get_single_deal),
            ("Get Stats", self.test_get_stats),
            ("AI Analysis", self.test_ai_analysis),
            ("Create Checkout", self.test_create_checkout),
            ("Payment Status", self.test_payment_status),
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