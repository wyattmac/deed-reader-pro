#!/usr/bin/env python3
"""
Simple test of PDF processing to identify the issue
"""

import os
import sys

def test_pdf_basics():
    """Test basic PDF operations."""
    pdf_path = "uploads/tint_rd.pdf"
    
    print("🧪 Simple PDF Test")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found at: {pdf_path}")
        return False
    
    print(f"✅ Found PDF file: {pdf_path}")
    print(f"   File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
    
    # Check what modules are available
    print("\n📦 Checking available modules:")
    
    try:
        import PyPDF2
        print("✅ PyPDF2 is available")
    except ImportError:
        print("❌ PyPDF2 is NOT available")
    
    try:
        import fitz
        print("✅ PyMuPDF (fitz) is available")
    except ImportError:
        print("❌ PyMuPDF (fitz) is NOT available")
    
    try:
        import cv2
        print("✅ OpenCV (cv2) is available")
    except ImportError:
        print("❌ OpenCV (cv2) is NOT available")
    
    try:
        import anthropic
        print("✅ Anthropic is available")
    except ImportError:
        print("❌ Anthropic is NOT available")
    
    # Try basic PDF reading with PyPDF2
    print("\n📄 Testing basic PDF reading:")
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"✅ PDF has {num_pages} pages")
            
            # Try to extract text from first page
            if num_pages > 0:
                first_page_text = pdf_reader.pages[0].extract_text()
                text_length = len(first_page_text)
                print(f"✅ First page text length: {text_length} characters")
                
                if text_length > 0:
                    print("\n   First 200 characters:")
                    print("   " + "-" * 40)
                    print("   " + first_page_text[:200].replace('\n', '\n   '))
                else:
                    print("⚠️  No text extracted from first page - might be a scanned PDF")
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
    
    # Check if it's a scanned PDF by trying PyMuPDF
    print("\n🔍 Checking if PDF is scanned:")
    try:
        import fitz
        pdf_document = fitz.open(pdf_path)
        total_text = ""
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            total_text += text
        
        pdf_document.close()
        
        if len(total_text.strip()) < 50:
            print("⚠️  PDF appears to be scanned (very little embedded text)")
            print("   This PDF will need OCR to extract text")
        else:
            print(f"✅ PDF has embedded text: {len(total_text)} characters total")
    except Exception as e:
        print(f"❌ Could not check with PyMuPDF: {e}")

if __name__ == "__main__":
    test_pdf_basics()