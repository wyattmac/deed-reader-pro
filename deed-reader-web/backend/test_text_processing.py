#!/usr/bin/env python3
"""
Text Processing Debug Test
"""
import requests
import json

def test_text_processing():
    """Test the text processing endpoint specifically."""
    base_url = "http://localhost:5000"
    
    sample_text = """GENERAL WARRANTY DEED

BEGINNING at an iron pin found at the southwest corner;

THENCE North 45 degrees 30 minutes East 150.00 feet to an iron pin set;

THENCE North 45 degrees 30 minutes West 200.00 feet to an iron pin set;

THENCE South 45 degrees 30 minutes West 150.00 feet to an iron pin set;

THENCE South 45 degrees 30 minutes East 200.00 feet to the POINT OF BEGINNING."""
    
    print("🔍 Testing Text Processing Endpoint")
    print("=" * 50)
    print(f"Sample text ({len(sample_text)} characters)")
    print("=" * 50)
    
    try:
        # Test the /api/documents/text endpoint
        response = requests.post(
            f"{base_url}/api/documents/text",
            json={"text": sample_text},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Text processing successful!")
            print(f"   Success: {data.get('success')}")
            print(f"   Text length: {data.get('text_length')}")
            print(f"   Upload ID: {data.get('upload_id')}")
            print(f"   Message: {data.get('message')}")
        else:
            print("❌ Text processing failed!")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown')}")
                print(f"   Message: {error_data.get('message', 'No message')}")
                print(f"   Details: {error_data.get('details', 'No details')}")
            except:
                print(f"   Raw response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot connect to backend server")
        print("   Make sure the Flask server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_text_processing() 