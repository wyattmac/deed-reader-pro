#!/usr/bin/env python3
"""
Test script for Tiny RD Deed PDF
"""

import requests
import json
import os
import sys
from pathlib import Path

def test_tiny_rd_deed():
    """Test the Tiny RD Deed PDF processing."""
    base_url = "http://localhost:5000"
    pdf_path = "uploads/tint_rd.pdf"
    
    print("🧪 Testing Tiny RD Deed PDF Processing")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found at: {pdf_path}")
        return False
    
    print(f"✅ Found PDF file: {pdf_path}")
    print(f"   File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
    
    # Test 1: Upload PDF
    print("\n1. Uploading Tiny RD Deed PDF...")
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': ('tint_rd.pdf', f, 'application/pdf')}
            response = requests.post(f"{base_url}/api/documents/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ PDF uploaded successfully!")
            print(f"   Filename: {data.get('filename')}")
            print(f"   File type: {data.get('file_type')}")
            print(f"   Text length: {data.get('text_length')} characters")
            print(f"   Upload ID: {data.get('upload_id')}")
            
            # Save extracted text for analysis
            extracted_text = data.get('extracted_text', '')
            
            # Show preview of extracted text
            if extracted_text:
                print("\n📄 Extracted Text Preview (first 500 chars):")
                print("-" * 40)
                print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
                print("-" * 40)
            
            return data
        else:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"   Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

    # Test 2: Validate Document
    print("\n2. Validating deed document...")
    try:
        if extracted_text:
            response = requests.post(
                f"{base_url}/api/documents/validate",
                json={'text': extracted_text}
            )
            
            if response.status_code == 200:
                validation = response.json()
                print("✅ Validation complete!")
                print(f"   Is valid: {validation.get('is_valid')}")
                print(f"   Score: {validation.get('score', 0) * 100:.0f}%")
                print("   Checks:")
                for check, result in validation.get('checks', {}).items():
                    print(f"     - {check}: {'✅' if result else '❌'}")
                
                if validation.get('issues'):
                    print("   Issues found:")
                    for issue in validation['issues']:
                        print(f"     ⚠️  {issue}")
            else:
                print(f"❌ Validation failed: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Validation error: {e}")

    print("\n" + "=" * 50)
    print("✅ Test completed!")
    return True

if __name__ == "__main__":
    try:
        result = test_tiny_rd_deed()
        if result:
            print("\n🎉 Tiny RD Deed PDF processed successfully!")
            print("You can now use the web interface to:")
            print("  - Analyze the document")
            print("  - Plot the deed boundaries")
            print("  - Ask questions about the property")
        else:
            print("\n❌ Test failed. Check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"❌ Test error: {e}")
        sys.exit(1) 