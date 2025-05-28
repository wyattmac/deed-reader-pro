"""
OCR Fallback Service using OpenAI Vision
---------------------------------------
Fallback OCR using OpenAI's vision capabilities when Tesseract is not available.
"""

import os
import logging
import base64
from typing import Optional
from PIL import Image
import io
import fitz  # PyMuPDF
from openai import OpenAI

logger = logging.getLogger(__name__)

class OCRFallbackService:
    """Fallback OCR service using OpenAI's vision capabilities."""
    
    @staticmethod
    def encode_image(image_path: str) -> str:
        """Encode image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    @staticmethod
    def encode_pil_image(pil_image: Image.Image) -> str:
        """Encode PIL Image to base64 string."""
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    @staticmethod
    def extract_text_from_image_with_vision(image_path: str, client: OpenAI) -> Optional[str]:
        """Extract text from image using OpenAI's vision capabilities."""
        try:
            base64_image = OCRFallbackService.encode_image(image_path)
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at reading scanned deed documents. Extract all text from the image exactly as it appears, preserving formatting and structure. Focus especially on legal descriptions, bearings, distances, and property information."
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract all text from this scanned deed document. Preserve the exact formatting and structure. Include all legal descriptions, bearings, distances, names, dates, and any other text visible in the document."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4000,
                temperature=0.1
            )
            
            extracted_text = response.choices[0].message.content
            logger.info(f"Successfully extracted {len(extracted_text)} characters using OpenAI Vision")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error using OpenAI Vision for OCR: {e}")
            return None
    
    @staticmethod
    def extract_text_from_pdf_with_vision(pdf_path: str, client: OpenAI) -> Optional[str]:
        """Extract text from PDF pages using OpenAI's vision capabilities."""
        extracted_text = ""
        
        try:
            pdf_document = fitz.open(pdf_path)
            
            for page_num in range(pdf_document.page_count):
                logger.info(f"Processing page {page_num + 1} of {pdf_document.page_count} with OpenAI Vision")
                
                page = pdf_document[page_num]
                
                # Convert page to image
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x scale for better quality
                img_data = pix.tobytes("png")
                pil_image = Image.open(io.BytesIO(img_data))
                
                # Encode image
                base64_image = OCRFallbackService.encode_pil_image(pil_image)
                
                # Extract text using vision
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert at reading scanned deed documents. Extract all text from the image exactly as it appears, preserving formatting and structure."
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Extract all text from page {page_num + 1} of this scanned deed document. Preserve exact formatting, especially for metes and bounds descriptions, bearings, and distances."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=4000,
                    temperature=0.1
                )
                
                page_text = response.choices[0].message.content
                if page_text:
                    extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                    
            pdf_document.close()
            
            logger.info(f"Successfully extracted {len(extracted_text)} characters from PDF using OpenAI Vision")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF with OpenAI Vision: {e}")
            return None 