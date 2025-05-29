"""
Document Router for Deed Reader Pro - FastAPI
--------------------------------------------
Handles file upload, OCR, and document processing with async support.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import aiofiles
import PyPDF2
from PIL import Image

from services.ocr_service import OCRService
from services.claude_service import ClaudeService

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Constants
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Pydantic models for request/response
class TextProcessRequest(BaseModel):
    """Model for text processing requests."""
    text: str = Field(..., min_length=10)

class TextProcessResponse(BaseModel):
    """Model for text processing responses."""
    success: bool
    text_length: int
    extracted_text: str
    upload_id: str
    message: str

class DocumentValidationRequest(BaseModel):
    """Model for document validation requests."""
    text: str = Field(..., min_length=1)

class DocumentValidationResponse(BaseModel):
    """Model for document validation responses."""
    is_valid: bool
    checks: Dict[str, bool]
    issues: List[str]
    suggestions: List[str]
    score: float

class DocumentUploadResponse(BaseModel):
    """Model for document upload responses."""
    success: bool
    filename: str
    file_type: str
    text_length: int
    extracted_text: str
    upload_id: str
    message: str


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secure_filename(filename: str) -> str:
    """Secure a filename by removing potentially dangerous characters."""
    # Remove any path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    # Keep only alphanumeric, dash, underscore, and dot
    import re
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    # Ensure it has an extension
    if '.' not in filename:
        filename = filename + '.txt'
    return filename


async def extract_text_from_pdf_async(file_path: str) -> str:
    """Extract text from PDF file asynchronously."""
    try:
        # Run CPU-intensive PDF extraction in thread pool
        loop = asyncio.get_event_loop()
        
        def sync_extract():
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                if not pdf_reader.pages:
                    logger.warning(f"PDF file has no pages: {file_path}")
                    return ""
                    
                for i, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                        else:
                            logger.warning(f"No text extracted from page {i+1}")
                    except Exception as page_e:
                        logger.error(f"Error extracting text from page {i+1}: {page_e}")
                
                return text.strip()
        
        # Extract text in thread pool
        text = await loop.run_in_executor(None, sync_extract)
        
        # If no text found or very little text, try OCR
        if len(text.strip()) < 100:
            logger.info(f"PDF appears to be scanned. Using OCR...")
            ocr_text = await loop.run_in_executor(
                None, 
                OCRService.extract_text_from_pdf, 
                file_path
            )
            
            if ocr_text and len(ocr_text) > len(text):
                text = ocr_text
                
                # Use Claude to enhance the OCR text if available
                if ClaudeService.is_available():
                    logger.info("Using Claude to enhance OCR text...")
                    enhanced_text = await loop.run_in_executor(
                        None,
                        ClaudeService.enhance_ocr_text,
                        text
                    )
                    if enhanced_text:
                        text = enhanced_text
        
        return text
        
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to extract text from PDF: {str(e)}"
        )


async def extract_text_from_image_async(file_path: str) -> str:
    """Extract text from image using OCR asynchronously."""
    logger.info(f"Attempting to extract text from image: {file_path}")
    try:
        # Run OCR in thread pool
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(
            None,
            OCRService.extract_text_from_image,
            file_path
        )
        
        if not text:
            logger.warning(f"No text extracted from image: {file_path}")
            return ""
            
        # Use Claude to enhance the OCR text if available
        if ClaudeService.is_available():
            logger.info("Using Claude to enhance OCR text from image...")
            enhanced_text = await loop.run_in_executor(
                None,
                ClaudeService.enhance_ocr_text,
                text
            )
            if enhanced_text:
                text = enhanced_text
                
        logger.info(f"Successfully extracted {len(text)} characters from image")
        return text
        
    except Exception as e:
        logger.error(f"Error extracting text from image {file_path}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text from image: {str(e)}"
        )


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload")
) -> DocumentUploadResponse:
    """
    Upload and process a document file.
    
    Supports: PDF, TXT, PNG, JPG, JPEG, TIFF, BMP
    Max size: 50MB
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Supported types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Secure filename and prepare path
    filename = secure_filename(file.filename)
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    file_path = upload_dir / filename
    
    try:
        # Save file asynchronously
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(contents)
        
        logger.info(f"File '{filename}' saved successfully")
        
        # Extract text based on file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        extracted_text = ""
        
        if file_extension == 'txt':
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                extracted_text = await f.read()
                
        elif file_extension == 'pdf':
            extracted_text = await extract_text_from_pdf_async(str(file_path))
            
        elif file_extension in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
            extracted_text = await extract_text_from_image_async(str(file_path))
            
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_extension}"
            )
        
        # Validate extracted text
        if not extracted_text or len(extracted_text.strip()) < 10:
            raise HTTPException(
                status_code=400,
                detail="No readable text found in document"
            )
        
        # Return successful response
        return DocumentUploadResponse(
            success=True,
            filename=filename,
            file_type=file_extension,
            text_length=len(extracted_text),
            extracted_text=extracted_text,
            upload_id=filename.replace('.', '_'),
            message="Document uploaded and processed successfully"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing document: {e}", exc_info=True)
        # Clean up file if error occurred
        if file_path.exists():
            try:
                file_path.unlink()
            except:
                pass
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )


@router.post("/text", response_model=TextProcessResponse)
async def process_text(request: TextProcessRequest) -> TextProcessResponse:
    """Process raw text input."""
    text = request.text.strip()
    
    if len(text) < 10:
        raise HTTPException(status_code=400, detail="Text too short or empty")
    
    return TextProcessResponse(
        success=True,
        text_length=len(text),
        extracted_text=text,
        upload_id="text_input",
        message="Text processed successfully"
    )


@router.post("/validate", response_model=DocumentValidationResponse)
async def validate_document(request: DocumentValidationRequest) -> DocumentValidationResponse:
    """
    Validate document format and readability.
    
    Checks for:
    - Sufficient length
    - Deed-related keywords
    - Coordinate information
    """
    text = request.text.lower()
    
    # Define deed keywords
    deed_keywords = [
        'deed', 'grantor', 'grantee', 'bearing', 'feet', 
        'thence', 'metes', 'bounds', 'parcel', 'tract'
    ]
    
    coordinate_patterns = ['°', 'degrees', 'north', 'south', 'east', 'west', "n", "s", "e", "w"]
    
    # Validation checks
    checks = {
        'length': len(text) >= 50,
        'contains_deed_keywords': any(keyword in text for keyword in deed_keywords),
        'has_coordinates': any(pattern in text for pattern in coordinate_patterns),
        'readable_format': True
    }
    
    issues = []
    suggestions = []
    
    # Check for issues
    if not checks['length']:
        issues.append('Document is too short to be a complete deed')
        suggestions.append('Ensure the complete deed text is included')
    
    if not checks['contains_deed_keywords']:
        issues.append('Document may not be a deed - missing common deed keywords')
        suggestions.append('Verify this is a deed document')
    
    if not checks['has_coordinates']:
        issues.append('No coordinate information found')
        suggestions.append('Check if this deed contains metes and bounds descriptions')
    
    # Calculate validation score
    score = sum(checks.values()) / len(checks)
    is_valid = len(issues) == 0
    
    return DocumentValidationResponse(
        is_valid=is_valid,
        checks=checks,
        issues=issues,
        suggestions=suggestions,
        score=score
    )


# Additional utility endpoints
@router.get("/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats."""
    return {
        "formats": list(ALLOWED_EXTENSIONS),
        "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
        "ocr_supported": ['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'],
        "text_extraction": ['pdf', 'txt']
    }


@router.delete("/{upload_id}")
async def delete_document(upload_id: str):
    """Delete an uploaded document."""
    # Convert upload_id back to filename
    filename = upload_id.replace('_', '.')
    file_path = Path("uploads") / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        file_path.unlink()
        return {"message": f"Document {filename} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting document {filename}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        ) 