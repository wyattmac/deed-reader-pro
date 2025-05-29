#!/usr/bin/env python3
"""
Direct test of PDF processing without server
"""

import os
import sys
import PyPDF2
from services.ocr_service import OCRService
from services.claude_service import ClaudeService
from core.deed_parser import AdvancedDeedParser

def test_pdf_extraction():
    """Test PDF text extraction directly."""
    pdf_path = "uploads/tint_rd.pdf"
    
    print("🧪 Testing PDF Processing Directly")
    print("=" * 50)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ PDF file not found at: {pdf_path}")
        return False
    
    print(f"✅ Found PDF file: {pdf_path}")
    print(f"   File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
    
    # 1. Test standard PDF text extraction
    print("\n1. Testing standard PDF text extraction...")
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            print(f"   PDF has {len(pdf_reader.pages)} pages")
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                    print(f"   Page {i+1}: Extracted {len(page_text)} characters")
                else:
                    print(f"   Page {i+1}: No text extracted")
        
        print(f"\n   Total standard extraction: {len(text)} characters")
        if text.strip():
            print("\n   Text preview (first 300 chars):")
            print("   " + "-" * 40)
            print("   " + text[:300].replace('\n', '\n   '))
    except Exception as e:
        print(f"❌ Standard extraction failed: {e}")
        text = ""
    
    # 2. Test OCR extraction if needed
    if len(text.strip()) < 100:
        print("\n2. PDF appears to be scanned, testing OCR extraction...")
        try:
            ocr_text = OCRService.extract_text_from_pdf(pdf_path)
            print(f"   OCR extraction: {len(ocr_text)} characters")
            if ocr_text:
                print("\n   OCR text preview (first 300 chars):")
                print("   " + "-" * 40)
                print("   " + ocr_text[:300].replace('\n', '\n   '))
                text = ocr_text
        except Exception as e:
            print(f"❌ OCR extraction failed: {e}")
    
    # 3. Test Claude enhancement if available
    if text and ClaudeService.is_available():
        print("\n3. Testing Claude text enhancement...")
        try:
            enhanced_text = ClaudeService.enhance_ocr_text(text)
            if enhanced_text:
                print(f"   Enhanced text: {len(enhanced_text)} characters")
                text = enhanced_text
        except Exception as e:
            print(f"❌ Claude enhancement failed: {e}")
    
    # 4. Test deed parsing
    if text:
        print("\n4. Testing deed parsing...")
        try:
            parser = AdvancedDeedParser(enable_filtering=True, filter_mode='hybrid')
            calls = parser.parse_deed_text(text)
            print(f"   Found {len(calls)} deed calls")
            
            summary = parser.get_call_summary()
            print(f"\n   Parsing Summary:")
            for key, value in summary.items():
                print(f"   - {key}: {value}")
        except Exception as e:
            print(f"❌ Deed parsing failed: {e}")
    
    return text

if __name__ == "__main__":
    # Initialize Claude if API key is available
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("Initializing Claude service...")
        ClaudeService.initialize()
    
    # Run the test
    extracted_text = test_pdf_extraction()
    
    if extracted_text:
        print("\n✅ PDF processing test completed successfully!")
    else:
        print("\n❌ PDF processing test failed!")