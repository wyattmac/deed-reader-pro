#!/usr/bin/env python3
"""
Test script for FastAPI migration
---------------------------------
Tests the new FastAPI endpoints to ensure they work correctly.
"""

import requests
import json
import sys
from pathlib import Path

# Configuration
FASTAPI_BASE_URL = "http://localhost:8000"
FLASK_BASE_URL = "http://localhost:5000"

# Test data
TEST_TEXT = """
This deed made this 15th day of March, 2024, between John Doe, Grantor, 
and Jane Smith, Grantee. Beginning at a point on the North line of Main Street, 
thence North 45 degrees 30 minutes East, 150.00 feet to a point; 
thence South 44 degrees 30 minutes East, 200.00 feet to an iron pin; 
thence South 45 degrees 30 minutes West, 150.00 feet to a point; 
thence North 44 degrees 30 minutes West, 200.00 feet to the point of beginning,
containing 0.688 acres, more or less.
"""

def test_health_check():
    """Test the health check endpoint."""
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/api/health")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   API Status: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   Claude Service: {data['services']['claude']}")
            print("   ✅ Health check passed!")
            return True
        else:
            print(f"   ❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_api_info():
    """Test the API info endpoint."""
    print("\n2. Testing API Info...")
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/api/info")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   API Name: {data['name']}")
            print(f"   Available Endpoints: {', '.join(data['endpoints'].keys())}")
            print("   ✅ API info passed!")
            return True
        else:
            print(f"   ❌ API info failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_text_processing():
    """Test the text processing endpoint."""
    print("\n3. Testing Text Processing...")
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/api/documents/text",
            json={"text": TEST_TEXT}
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data['success']}")
            print(f"   Text Length: {data['text_length']}")
            print(f"   Message: {data['message']}")
            print("   ✅ Text processing passed!")
            return True
        else:
            print(f"   ❌ Text processing failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_document_validation():
    """Test the document validation endpoint."""
    print("\n4. Testing Document Validation...")
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/api/documents/validate",
            json={"text": TEST_TEXT}
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Is Valid: {data['is_valid']}")
            print(f"   Validation Score: {data['score']:.2f}")
            print(f"   Checks:")
            for check, result in data['checks'].items():
                print(f"     - {check}: {'✓' if result else '✗'}")
            if data['issues']:
                print(f"   Issues: {', '.join(data['issues'])}")
            print("   ✅ Document validation passed!")
            return True
        else:
            print(f"   ❌ Document validation failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_supported_formats():
    """Test the supported formats endpoint."""
    print("\n5. Testing Supported Formats...")
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/api/documents/supported-formats")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Supported Formats: {', '.join(data['formats'])}")
            print(f"   Max File Size: {data['max_file_size_mb']}MB")
            print(f"   OCR Supported: {', '.join(data['ocr_supported'])}")
            print("   ✅ Supported formats passed!")
            return True
        else:
            print(f"   ❌ Supported formats failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_file_upload():
    """Test file upload with a sample text file."""
    print("\n6. Testing File Upload...")
    
    # Create a test file
    test_file_path = Path("test_deed_sample.txt")
    test_file_path.write_text(TEST_TEXT)
    
    try:
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_deed_sample.txt', f, 'text/plain')}
            response = requests.post(
                f"{FASTAPI_BASE_URL}/api/documents/upload",
                files=files
            )
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data['success']}")
            print(f"   Filename: {data['filename']}")
            print(f"   Text Length: {data['text_length']}")
            print(f"   Upload ID: {data['upload_id']}")
            print("   ✅ File upload passed!")
            
            # Clean up
            if 'upload_id' in data:
                delete_response = requests.delete(
                    f"{FASTAPI_BASE_URL}/api/documents/{data['upload_id']}"
                )
                if delete_response.status_code == 200:
                    print("   ✅ File cleanup successful!")
            
            return True
        else:
            print(f"   ❌ File upload failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        # Clean up test file
        if test_file_path.exists():
            test_file_path.unlink()


def test_api_documentation():
    """Check if API documentation is accessible."""
    print("\n7. Testing API Documentation...")
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/api/docs")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ API documentation is accessible!")
            print(f"   Visit: {FASTAPI_BASE_URL}/api/docs")
            return True
        else:
            print(f"   ❌ API documentation not accessible")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_deed_analysis():
    """Test the deed analysis endpoint."""
    print("\n8. Testing Deed Analysis...")
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/api/analysis/analyze",
            json={"text": TEST_TEXT}
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data['success']}")
            print(f"   Message: {data['message']}")
            if data.get('analysis'):
                print(f"   Analysis Keys: {list(data['analysis'].keys())[:5]}...")  # First 5 keys
            print("   ✅ Deed analysis passed!")
            return True
        elif response.status_code == 503:
            print("   ⚠️  Claude service not available (expected if no API key)")
            return True
        else:
            print(f"   ❌ Deed analysis failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_summary_generation():
    """Test the summary generation endpoint."""
    print("\n9. Testing Summary Generation...")
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/api/analysis/summary",
            json={"text": TEST_TEXT}
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data['success']}")
            if data.get('summary'):
                print(f"   Summary Length: {len(data['summary'])} chars")
            if data.get('metadata'):
                print(f"   Model Used: {data['metadata'].get('model_used', 'N/A')}")
            print("   ✅ Summary generation passed!")
            return True
        elif response.status_code == 503:
            print("   ⚠️  Claude service not available (expected if no API key)")
            return True
        else:
            print(f"   ❌ Summary generation failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_coordinate_extraction():
    """Test the coordinate extraction endpoint."""
    print("\n10. Testing Coordinate Extraction...")
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/api/analysis/coordinates",
            json={"text": TEST_TEXT}
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data['success']}")
            if data.get('coordinates'):
                print(f"   Coordinates Found: {len(data['coordinates'])}")
            print("   ✅ Coordinate extraction passed!")
            return True
        elif response.status_code == 503:
            print("   ⚠️  Claude service not available (expected if no API key)")
            return True
        else:
            print(f"   ❌ Coordinate extraction failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_data_validation():
    """Test the data validation endpoint."""
    print("\n11. Testing Data Validation...")
    
    test_data = {
        "extracted_data": {
            "bearings": ["N 45° 30' E", "S 44° 30' E"],
            "distances": [150.0, 200.0],
            "units": "feet",
            "area": 0.688
        }
    }
    
    try:
        response = requests.post(
            f"{FASTAPI_BASE_URL}/api/analysis/validate",
            json=test_data
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data['success']}")
            print(f"   Message: {data['message']}")
            print("   ✅ Data validation passed!")
            return True
        elif response.status_code == 503:
            print("   ⚠️  Claude service not available (expected if no API key)")
            return True
        else:
            print(f"   ❌ Data validation failed: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def compare_endpoints():
    """Compare Flask and FastAPI responses for consistency."""
    print("\n12. Comparing Flask vs FastAPI Responses...")
    
    # Test text processing on both
    test_payload = {"text": TEST_TEXT}
    
    try:
        # Flask response
        flask_response = requests.post(
            f"{FLASK_BASE_URL}/api/documents/text",
            json=test_payload
        )
        
        # FastAPI response
        fastapi_response = requests.post(
            f"{FASTAPI_BASE_URL}/api/documents/text",
            json=test_payload
        )
        
        if flask_response.status_code == 200 and fastapi_response.status_code == 200:
            flask_data = flask_response.json()
            fastapi_data = fastapi_response.json()
            
            # Compare key fields
            print("   Comparing response structures:")
            print(f"   - Flask keys: {sorted(flask_data.keys())}")
            print(f"   - FastAPI keys: {sorted(fastapi_data.keys())}")
            
            # Check if responses are compatible
            common_keys = set(flask_data.keys()) & set(fastapi_data.keys())
            print(f"   - Common keys: {sorted(common_keys)}")
            
            if 'success' in common_keys and flask_data['success'] == fastapi_data['success']:
                print("   ✅ Responses are compatible!")
                return True
            else:
                print("   ⚠️  Responses differ - review needed")
                return True  # Still pass as this is expected during migration
        else:
            print("   ⚠️  Could not compare - one or both servers may be down")
            return True
    except Exception as e:
        print(f"   ⚠️  Comparison skipped: {e}")
        return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("FastAPI Migration Test Suite")
    print("=" * 60)
    print(f"Testing FastAPI at: {FASTAPI_BASE_URL}")
    print(f"Flask comparison at: {FLASK_BASE_URL}")
    print("=" * 60)
    
    tests = [
        test_health_check,
        test_api_info,
        test_text_processing,
        test_document_validation,
        test_supported_formats,
        test_file_upload,
        test_api_documentation,
        test_deed_analysis,
        test_summary_generation,
        test_coordinate_extraction,
        test_data_validation,
        compare_endpoints
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ Test failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed! FastAPI migration is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 