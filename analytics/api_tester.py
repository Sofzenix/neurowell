"""
api_tester.py
Test API endpoints for analytics module
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5001"

def print_response(response, endpoint):
    """Print formatted API response"""
    print(f"\n{'='*60}")
    print(f"Testing: {endpoint}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response:")
        print(json.dumps(data, indent=2))
        
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        print(f"Response: {response.text}")
        return False

def test_all_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing Neurowell Analytics APIs")
    print(f"Base URL: {BASE_URL}")
    
    # Wait for server to start
    time.sleep(2)
    
    # Test 1: Health check
    response = requests.get(f"{BASE_URL}/api/analytics/health")
    print_response(response, "/api/analytics/health")
    
    # Test 2: Dashboard data
    response = requests.get(f"{BASE_URL}/api/analytics/dashboard?user_id=1")
    print_response(response, "/api/analytics/dashboard")
    
    # Test 3: Profile data
    response = requests.get(f"{BASE_URL}/api/analytics/profile?user_id=1")
    print_response(response, "/api/analytics/profile")
    
    # Test 4: Radar chart
    response = requests.get(f"{BASE_URL}/api/analytics/charts/radar?user_id=1")
    print_response(response, "/api/analytics/charts/radar")
    
    # Test 5: Bar chart
    response = requests.get(f"{BASE_URL}/api/analytics/charts/bar?user_id=1")
    print_response(response, "/api/analytics/charts/bar")
    
    # Test 6: Pie chart
    response = requests.get(f"{BASE_URL}/api/analytics/charts/pie?user_id=1")
    print_response(response, "/api/analytics/charts/pie")
    
    # Test 7: Progress bars
    response = requests.get(f"{BASE_URL}/api/analytics/progress?user_id=1")
    print_response(response, "/api/analytics/progress")
    
    # Test 8: Statistics
    response = requests.get(f"{BASE_URL}/api/analytics/stats?user_id=1")
    print_response(response, "/api/analytics/stats")
    
    # Test 9: Emotion detection (POST)
    payload = {
        "user_id": 1,
        "text": "I feel happy and excited today!",
        "source": "text"
    }
    response = requests.post(f"{BASE_URL}/api/analytics/analyzer/detect", 
                           json=payload)
    print_response(response, "/api/analytics/analyzer/detect")
    
    # Test 10: Generate report (POST)
    payload = {
        "user_id": 1,
        "report_type": "weekly"
    }
    response = requests.post(f"{BASE_URL}/api/analytics/report/generate",
                           json=payload)
    print_response(response, "/api/analytics/report/generate")
    
    print("\n" + "="*60)
    print("✅ API Testing Complete!")

if __name__ == "__main__":
    # First check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/health", timeout=5)
        if response.status_code == 200:
            test_all_endpoints()
        else:
            print("❌ Server is not responding. Please start the server first:")
            print("   python run_server.py")
    except requests.ConnectionError:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python run_server.py")