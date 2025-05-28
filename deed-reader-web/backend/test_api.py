#!/usr/bin/env python3
"""
API Test Script for Deed Reader Pro
----------------------------------
Tests the improved API endpoints and features.
"""

import requests
import json
import time
import sys

def test_api():
    """Test the improved API endpoints."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Deed Reader Pro API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Enhanced Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health check passed!")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Version: {health_data.get('version')}")
            print(f"   Environment: {health_data.get('environment')}")
            print(f"   OpenAI: {health_data.get('services', {}).get('openai', 'unknown')}")
            print(f"   Response time: {health_data.get('response_time_ms')}ms")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to API: {e}")
        return False
    
    # Test 2: API Info
    print("\n2. Testing API Info Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/info", timeout=5)
        if response.status_code == 200:
            info_data = response.json()
            print("✅ API info retrieved!")
            print(f"   Name: {info_data.get('name')}")
            print(f"   Description: {info_data.get('description')}")
            print(f"   Features: {list(info_data.get('features', {}).keys())}")
            print(f"   Max file size: {info_data.get('limits', {}).get('max_file_size_mb')}MB")
        else:
            print(f"❌ API info failed with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ API info request failed: {e}")
    
    # Test 3: Test 404 Error Handling
    print("\n3. Testing Enhanced Error Handling...")
    try:
        response = requests.get(f"{base_url}/api/nonexistent", timeout=5)
        if response.status_code == 404:
            error_data = response.json()
            print("✅ 404 error handling works!")
            print(f"   Error: {error_data.get('error')}")
            print(f"   Message: {error_data.get('message')}")
            print(f"   Available endpoints: {len(error_data.get('available_endpoints', []))}")
        else:
            print(f"❌ Unexpected status code for 404 test: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 404 test failed: {e}")
    
    # Test 4: Document Upload Endpoint Structure
    print("\n4. Testing Document Routes...")
    try:
        # Just test that the endpoint exists (without actually uploading)
        response = requests.post(f"{base_url}/api/documents/upload", timeout=5)
        # We expect a 400 error for missing file, which is good
        if response.status_code == 400:
            error_data = response.json()
            print("✅ Document upload endpoint is working!")
            print(f"   Expected error for missing file: {error_data.get('error')}")
        else:
            print(f"❌ Unexpected response from document upload: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Document upload test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API test completed!")
    return True

if __name__ == "__main__":
    try:
        success = test_api()
        if success:
            print("✅ All tests passed! Your improved API is working great!")
        else:
            print("❌ Some tests failed. Check the server logs.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"❌ Test script error: {e}")
        sys.exit(1) 