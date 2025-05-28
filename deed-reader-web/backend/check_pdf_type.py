#!/usr/bin/env python3
"""
Check if PDF is text-based or image-based (scanned)
"""

import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
import io
import os

def check_pdf_type(pdf_path):
    """Check if PDF contains text or is image-based."""
    print(f"Analyzing PDF: {pdf_path}")
    print("=" * 50)
    
    # Check with PyPDF2
    print("\n1. PyPDF2 Analysis:")
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"   Number of pages: {num_pages}")
            
            text_found = False
            total_text_length = 0
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text and len(page_text.strip()) > 0:
                    text_found = True
                    total_text_length += len(page_text)
                    print(f"   Page {i+1}: {len(page_text)} characters")
                else:
                    print(f"   Page {i+1}: No text found")
            
            if text_found:
                print(f"   Total text extracted: {total_text_length} characters")
            else:
                print("   ❌ No text found - likely a scanned document")
                
    except Exception as e:
        print(f"   Error with PyPDF2: {e}")
    
    # Check with PyMuPDF for images
    print("\n2. PyMuPDF Analysis:")
    try:
        pdf_document = fitz.open(pdf_path)
        print(f"   Number of pages: {pdf_document.page_count}")
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            
            # Check for text
            text = page.get_text()
            print(f"   Page {page_num + 1}:")
            print(f"     Text length: {len(text.strip())} characters")
            
            # Check for images
            image_list = page.get_images()
            print(f"     Images found: {len(image_list)}")
            
            # If page has images but no text, it's likely scanned
            if len(image_list) > 0 and len(text.strip()) < 10:
                print(f"     ⚠️  Likely a scanned page (images but no text)")
        
        pdf_document.close()
        
    except Exception as e:
        print(f"   Error with PyMuPDF: {e}")
    
    print("\n" + "=" * 50)
    print("Conclusion: This PDF appears to be a scanned document that needs OCR.")

if __name__ == "__main__":
    pdf_path = "uploads/tint_rd.pdf"
    if os.path.exists(pdf_path):
        check_pdf_type(pdf_path)
    else:
        print(f"PDF not found at: {pdf_path}") 