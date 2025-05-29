#!/usr/bin/env python3
"""
Quick PDF test with minimal dependencies
"""

import os

pdf_path = "uploads/tint_rd.pdf"
print(f"Testing PDF: {pdf_path}")
print(f"File exists: {os.path.exists(pdf_path)}")
print(f"File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")

# Try PyPDF2 (already installed)
try:
    import PyPDF2
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        print(f"\nPDF has {len(pdf_reader.pages)} pages")
        
        text = ""
        for i, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            text += page_text
            print(f"Page {i+1}: {len(page_text)} characters extracted")
        
        print(f"\nTotal text extracted: {len(text)} characters")
        if text.strip():
            print("\nFirst 500 characters:")
            print("-" * 40)
            print(text[:500])
        else:
            print("\n⚠️ No text extracted - this is likely a scanned PDF that needs OCR")
except Exception as e:
    print(f"Error: {e}")

# Check if .env is loaded
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    print(f"\nAPI Key configured: {'Yes' if api_key else 'No'}")
    if api_key:
        print(f"API Key starts with: {api_key[:15]}...")
except:
    print("\nCouldn't check API key")