"""
OCR Service for Deed Reader Pro
-------------------------------
Handles optical character recognition for scanned deed documents.
"""

import os
import io
import logging
import tempfile
from typing import List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
import fitz  # PyMuPDF
import re
import subprocess

logger = logging.getLogger(__name__)

# Try to import pytesseract, but don't fail if it's not available
try:
    import pytesseract
    # Check if tesseract is installed
    try:
        subprocess.run(['tesseract', '--version'], capture_output=True, check=True)
        TESSERACT_AVAILABLE = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        TESSERACT_AVAILABLE = False
        logger.warning("Tesseract OCR is not installed. Will use Claude Vision as fallback.")
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("pytesseract module not available. Will use Claude Vision as fallback.")

from .claude_service import ClaudeService

class OCRService:
    """Service for extracting text from scanned documents."""
    
    @staticmethod
    def preprocess_image(image):
        """Preprocess image for better OCR results."""
        # Convert PIL Image to OpenCV format
        open_cv_image = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
        
        # Apply thresholding to get better contrast
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.medianBlur(thresh, 1)
        
        # Convert back to PIL Image
        return Image.fromarray(denoised)
    
    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """Extract text from a single image using OCR."""
        try:
            # If Tesseract is not available, use Claude Vision
            if not TESSERACT_AVAILABLE:
                logger.info("Using Claude Vision for OCR (Tesseract not available)")
                if ClaudeService.is_available():
                    text = ClaudeService.extract_text_from_image(image_path)
                    if text:
                        return OCRService.clean_ocr_text(text)
                else:
                    logger.error("Neither Tesseract nor Claude is available for OCR")
                    return ""
            
            # Load image
            image = Image.open(image_path)
            
            # Preprocess for better OCR
            processed_image = OCRService.preprocess_image(image)
            
            # Perform OCR
            text = pytesseract.image_to_string(processed_image, lang='eng')
            
            # Clean up extracted text
            text = OCRService.clean_ocr_text(text)
            
            logger.info(f"Successfully extracted {len(text)} characters from image")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """Extract text from a scanned PDF using OCR."""
        extracted_text = ""
        temp_dir = None
        
        # If Tesseract is not available, use Claude Vision
        if not TESSERACT_AVAILABLE:
            logger.info("Using Claude Vision for PDF OCR (Tesseract not available)")
            if ClaudeService.is_available():
                try:
                    pdf_document = fitz.open(pdf_path)
                    for page_num in range(pdf_document.page_count):
                        page = pdf_document[page_num]
                        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                        img_data = pix.tobytes("png")
                        temp_image_path = f"temp_page_{page_num}.png"
                        
                        with open(temp_image_path, "wb") as f:
                            f.write(img_data)
                        
                        page_text = ClaudeService.extract_text_from_image(temp_image_path)
                        if page_text:
                            extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                        
                        # Clean up temp file
                        if os.path.exists(temp_image_path):
                            os.remove(temp_image_path)
                    
                    pdf_document.close()
                    if extracted_text:
                        enhanced_text = ClaudeService.enhance_ocr_text(extracted_text)
                        return enhanced_text if enhanced_text else extracted_text
                    return ""
                except Exception as e:
                    logger.error(f"Claude PDF OCR failed: {e}")
                    return ""
            else:
                logger.error("Neither Tesseract nor Claude is available for OCR")
                return ""
        
        try:
            # First, try to extract any embedded text
            pdf_document = fitz.open(pdf_path)
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text()
                
                # If page has substantial text, use it
                if len(text.strip()) > 50:
                    logger.info(f"Page {page_num + 1} has embedded text")
                    extracted_text += f"\n--- Page {page_num + 1} ---\n{text}"
                else:
                    # Page needs OCR
                    logger.info(f"Page {page_num + 1} needs OCR")
                    
                    # Extract page as image
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_data = pix.tobytes("png")
                    
                    # Convert to PIL Image
                    image = Image.open(io.BytesIO(img_data))
                    
                    # Preprocess and OCR
                    processed_image = OCRService.preprocess_image(image)
                    page_text = pytesseract.image_to_string(processed_image, lang='eng')
                    
                    if page_text.strip():
                        extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            pdf_document.close()
            
            # Clean up the entire extracted text
            extracted_text = OCRService.clean_ocr_text(extracted_text)
            
            logger.info(f"Successfully extracted {len(extracted_text)} characters from PDF")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    @staticmethod
    def clean_ocr_text(text: str) -> str:
        """Clean and normalize OCR-extracted text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Fix common OCR mistakes in deed documents
        replacements = {
            r'\bTHENCE\b': 'THENCE',
            r'\bNORTH\b': 'NORTH',
            r'\bSOUTH\b': 'SOUTH',
            r'\bEAST\b': 'EAST',
            r'\bWEST\b': 'WEST',
            r'\bBEARING\b': 'BEARING',
            r'\bDEED\b': 'DEED',
            r'\bGRANTOR\b': 'GRANTOR',
            r'\bGRANTEE\b': 'GRANTEE',
            r'\bfeet\b': 'feet',
            r'\bdegrees\b': 'degrees',
            r'\bminutes\b': 'minutes',
            r'\bseconds\b': 'seconds',
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Fix degree symbols
        text = re.sub(r'(\d+)\s*[°o]\s*', r'\1° ', text)
        
        # Fix common number/letter confusion
        text = re.sub(r'\bO\b(?=\d)', '0', text)
        text = re.sub(r'(?<=\d)O\b', '0', text)
        
        return text.strip()
    
    @staticmethod
    def enhance_deed_text(text: str) -> str:
        """Enhance deed text with specific deed-related corrections."""
        if not text:
            return ""
        
        # Use Claude to enhance the text if available
        if ClaudeService.is_available():
            enhanced = ClaudeService.enhance_ocr_text(text)
            if enhanced:
                return enhanced
        
        # Fallback: basic enhancements
        bearing_pattern = r'([NS])\s*(\d+)\s*[°o]?\s*(\d+)?\s*[\']?\s*(\d+)?\s*["]?\s*([EW])'
        
        def fix_bearing(match):
            parts = match.groups()
            direction1 = parts[0]
            degrees = parts[1]
            minutes = parts[2] or '00'
            seconds = parts[3] or '00'
            direction2 = parts[4]
            return f"{direction1} {degrees}° {minutes}' {seconds}\" {direction2}"
        
        text = re.sub(bearing_pattern, fix_bearing, text, flags=re.IGNORECASE)
        text = re.sub(r'(\d+\.?\d*)\s*ft\.?', r'\1 feet', text, flags=re.IGNORECASE)
        
        return text
    
    @staticmethod
    def is_ocr_needed(file_path: str, file_type: str) -> bool:
        """Check if OCR is needed for the file."""
        if file_type in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
            return True
        
        if file_type == 'pdf':
            try:
                pdf_document = fitz.open(file_path)
                total_text = ""
                
                for page in pdf_document:
                    total_text += page.get_text()
                
                pdf_document.close()
                return len(total_text.strip()) < 100
                
            except Exception as e:
                logger.error(f"Error checking PDF for text: {e}")
                return True
        
        return False 