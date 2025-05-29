#!/usr/bin/env python3
"""
Test Claude Vision API for PDF OCR
"""

import os
import sys
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_claude_vision():
    """Test Claude Vision on the PDF"""
    pdf_path = "uploads/tint_rd.pdf"
    
    print("🧪 Testing Claude Vision for PDF OCR")
    print("=" * 50)
    
    # Initialize Claude
    from services.claude_service import ClaudeService
    
    if ClaudeService.initialize():
        print("✅ Claude initialized successfully")
        
        # Convert first page of PDF to image for Claude
        try:
            import fitz  # PyMuPDF
            pdf_document = fitz.open(pdf_path)
            page = pdf_document[0]  # First page
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x resolution
            img_data = pix.tobytes("png")
            
            # Save temporarily
            temp_image = "temp_page_0.png"
            with open(temp_image, "wb") as f:
                f.write(img_data)
            
            print(f"\n📄 Extracting text from page 1 using Claude Vision...")
            text = ClaudeService.extract_text_from_image(temp_image)
            
            if text:
                print(f"✅ Extracted {len(text)} characters")
                print("\nFirst 500 characters:")
                print("-" * 40)
                print(text[:500])
            else:
                print("❌ No text extracted")
            
            # Clean up
            os.remove(temp_image)
            pdf_document.close()
            
        except ImportError:
            print("❌ PyMuPDF not available - would work if installed")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("❌ Claude initialization failed")

if __name__ == "__main__":
    test_claude_vision()