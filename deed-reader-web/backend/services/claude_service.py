"""
Claude Service for Deed Reader Pro
---------------------------------
Handles all Claude (Anthropic) API interactions for deed analysis and OCR enhancement.
"""

import os
import json
import logging
import base64
from typing import Dict, List, Optional, Any
import anthropic
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ClaudeService:
    """Service for Claude API interactions."""
    
    _client: Optional[anthropic.Anthropic] = None
    _model: str = "claude-3-5-sonnet-20241022"  # Using latest Claude 3.5 Sonnet for best performance
    _vision_model: str = "claude-3-5-sonnet-20241022"  # Claude 3.5 Sonnet with enhanced vision capabilities
    
    @classmethod
    def initialize(cls, api_key: Optional[str] = None):
        """Initialize the Claude client."""
        if not api_key:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not found. Claude features will be disabled.")
            return False

        try:
            cls._client = anthropic.Anthropic(api_key=api_key)
            # Test the connection
            test_message = cls._client.messages.create(
                model=cls._model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Test"}]
            )
            logger.info("Claude client initialized successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Claude client: {e}")
            cls._client = None
            return False
    
    @classmethod
    def is_available(cls) -> bool:
        """Check if Claude service is available."""
        return cls._client is not None
    
    @classmethod
    def enhance_ocr_text(cls, ocr_text: str) -> Optional[str]:
        """Use Claude to enhance and correct OCR-extracted text from deed documents."""
        if not cls.is_available() or not ocr_text:
            return ocr_text
            
        try:
            prompt = f"""This text was extracted from a scanned deed document using OCR. Please clean up and correct any obvious OCR errors while preserving the original structure and information.

Focus on:
- Fixing misrecognized characters (e.g., O vs 0, I vs 1)
- Correcting bearing formats (e.g., "N 45 30 15 E" to "N45°30'15"E")
- Fixing common deed terms that may have been misread
- Correcting obvious spelling errors in legal/surveying terms
- Preserving exact measurements and legal descriptions

Return ONLY the corrected text without any commentary.

OCR Text:
{ocr_text}"""

            message = cls._client.messages.create(
                model=cls._model,
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            enhanced_text = message.content[0].text
            logger.info(f"Claude OCR enhancement successful. Input: {len(ocr_text)} chars, Output: {len(enhanced_text)} chars")
            return enhanced_text.strip()
            
        except Exception as e:
            logger.error(f"Failed to enhance OCR text with Claude: {e}")
            return ocr_text
    
    @classmethod
    def extract_text_from_image(cls, image_path: str) -> Optional[str]:
        """Extract text from image using Claude's vision capabilities."""
        if not cls.is_available():
            return None
            
        try:
            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Determine image type
            image_type = "image/png"
            if image_path.lower().endswith(('.jpg', '.jpeg')):
                image_type = "image/jpeg"
            
            message = cls._client.messages.create(
                model=cls._vision_model,
                max_tokens=4000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user", 
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract all text from this scanned deed document. Focus on preserving exact formatting, especially for metes and bounds descriptions, bearings, distances, names, dates, and legal descriptions. Return only the extracted text."
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": image_type,
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ]
            )
            
            extracted_text = message.content[0].text
            logger.info(f"Claude vision OCR successful. Extracted {len(extracted_text)} characters")
            return extracted_text
            
        except Exception as e:
            logger.error(f"Failed to extract text from image with Claude: {e}")
            return None
    
    @classmethod
    def analyze_deed_document(cls, text: str) -> Dict[str, Any]:
        """Comprehensive analysis of deed document using Claude."""
        if not cls.is_available():
            return {"error": "Claude service not available"}
            
        try:
            prompt = f"""As an expert surveyor and legal document analyst, analyze this deed document and extract key information in JSON format.

Deed Document:
{text}

Return a comprehensive analysis in this exact JSON structure:
{{
    "summary": "Brief summary of the deed",
    "property_description": {{
        "legal_description": "Full legal description",
        "acres": "Acreage if mentioned",
        "lot_block": "Lot and block if applicable",
        "subdivision": "Subdivision name if applicable"
    }},
    "parties": {{
        "grantor": "Person/entity granting the deed",
        "grantee": "Person/entity receiving the deed"
    }},
    "metes_and_bounds": [
        {{
            "call_number": 1,
            "bearing": "Bearing direction",
            "distance": "Distance with units",
            "description": "Full call description"
        }}
    ],
    "monuments": [
        {{
            "type": "Type of monument",
            "description": "Description of monument",
            "action": "found/set/referenced"
        }}
    ],
    "dates": {{
        "deed_date": "Date of deed",
        "recording_date": "Date recorded if mentioned"
    }},
    "references": {{
        "book_page": "Book and page reference",
        "deed_book": "Deed book reference",
        "plat_references": "Any plat references"
    }},
    "key_findings": [
        "Important findings or notable aspects"
    ],
    "confidence_score": 0.95
}}

Provide 'null' for any information not clearly present. If not a deed, return: {{"error": "Invalid document type"}}"""

            message = cls._client.messages.create(
                model=cls._model,
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = message.content[0].text
            
            # Try to extract JSON from the response
            try:
                # Find JSON in the response (might be wrapped in markdown)
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                elif "{" in result_text:
                    json_start = result_text.find("{")
                    json_end = result_text.rfind("}") + 1
                    result_text = result_text[json_start:json_end]
                
                parsed_result = json.loads(result_text)
                logger.info(f"Claude deed analysis successful")
                return parsed_result
                
            except json.JSONDecodeError as json_e:
                logger.error(f"Failed to parse JSON from Claude response: {json_e}")
                return {
                    "error": "Invalid JSON response from Claude",
                    "raw_response": result_text
                }
                
        except Exception as e:
            logger.error(f"Failed to analyze deed with Claude: {e}")
            return {
                "error": "Claude analysis failed",
                "message": str(e)
            }
    
    @classmethod
    def extract_coordinates(cls, text: str) -> Dict[str, Any]:
        """Extract coordinate information from deed text using Claude."""
        if not cls.is_available():
            return {"error": "Claude service not available"}
            
        try:
            prompt = f"""Extract all coordinate information from this deed document and return it in structured JSON format.

Look for:
- Bearings (e.g., N45°30'15"E, South 28 degrees West)
- Distances (with units: feet, chains, poles, etc.)
- Curve data (radius, delta, chord bearings)
- Coordinate points if present

Deed Document:
{text}

Return in this exact JSON format:
{{
    "bearings": [
        {{"bearing": "N45°30'15\"E", "normalized": "45.504167", "quadrant": "NE"}}
    ],
    "distances": [
        {{"distance": "125.75", "units": "feet", "in_feet": 125.75}}
    ],
    "curves": [
        {{"radius": "50.0", "delta": "45°30'", "chord_bearing": "N67°45'E"}}
    ],
    "coordinate_points": [
        {{"point": "Point A", "coordinates": "x, y if present"}}
    ]
}}

If no coordinate information found, return structure with empty lists."""

            message = cls._client.messages.create(
                model=cls._model,
                max_tokens=3000,
                temperature=0.0,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result_text = message.content[0].text
            
            # Parse JSON response
            try:
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end].strip()
                elif "{" in result_text:
                    json_start = result_text.find("{")
                    json_end = result_text.rfind("}") + 1
                    result_text = result_text[json_start:json_end]
                
                parsed_result = json.loads(result_text)
                logger.info(f"Claude coordinate extraction successful")
                return parsed_result
                
            except json.JSONDecodeError as json_e:
                logger.error(f"Failed to parse coordinate JSON from Claude: {json_e}")
                return {
                    "error": "Invalid JSON response from Claude for coordinates",
                    "raw_response": result_text
                }
                
        except Exception as e:
            logger.error(f"Failed to extract coordinates with Claude: {e}")
            return {
                "error": "Claude coordinate extraction failed",
                "message": str(e)
            }
    
    @classmethod
    def answer_question(cls, document_text: str, question: str, chat_history: Optional[List[Dict]] = None) -> str:
        """Answer questions about the deed document using Claude."""
        if not cls.is_available():
            return "Claude service is not available."
            
        try:
            # Build conversation context
            conversation = f"""You are an expert surveyor and legal assistant helping users understand deed documents.

Here is the deed document for reference:
{document_text}

Answer questions clearly and accurately based on the document content. If information is not in the document, clearly state that. Provide specific references to the document when possible."""

            # Add chat history if provided
            if chat_history:
                conversation += "\n\nPrevious conversation:\n"
                for entry in chat_history[-3:]:  # Limit to last 3 exchanges
                    role = entry.get("role", "user")
                    content = entry.get("content", "")
                    conversation += f"{role}: {content}\n"
            
            conversation += f"\nUser question: {question}"

            message = cls._client.messages.create(
                model=cls._model,
                max_tokens=1000,
                temperature=0.2,
                messages=[{"role": "user", "content": conversation}]
            )
            
            answer = message.content[0].text
            logger.info(f"Claude Q&A successful for question: '{question[:50]}...'")
            return answer.strip()
            
        except Exception as e:
            logger.error(f"Failed to answer question with Claude: {e}")
            return f"Sorry, I encountered an error while processing your question: {str(e)}" 