"""
Document Routes for Deed Reader Pro
----------------------------------
Handles file upload, OCR, and document processing.
"""

import os
import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import PyPDF2
from PIL import Image
import io
import traceback
from services.ocr_service import OCRService
from services.claude_service import ClaudeService

logger = logging.getLogger(__name__)

document_bp = Blueprint('documents', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF file."""
    try:
        # First try standard text extraction
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
                        logger.warning(f"No text extracted from page {i+1} of PDF: {file_path}")
                except Exception as page_e:
                    logger.error(f"Error extracting text from page {i+1} of PDF {file_path}: {page_e}", exc_info=True)
            
            # If no text found or very little text, try OCR
            if len(text.strip()) < 100:
                logger.info(f"PDF appears to be scanned or has minimal text. Using OCR...")
                ocr_text = OCRService.extract_text_from_pdf(file_path)
                if ocr_text and len(ocr_text) > len(text):
                    logger.info(f"OCR extracted {len(ocr_text)} characters vs {len(text)} from standard extraction")
                    text = ocr_text
                    
                    # Use Claude to enhance the OCR text if available
                    if ClaudeService.is_available():
                        logger.info("Using Claude to enhance OCR text...")
                        enhanced_text = ClaudeService.enhance_ocr_text(text)
                        if enhanced_text:
                            text = enhanced_text
            
            return text.strip()
    except FileNotFoundError:
        logger.error(f"PDF file not found: {file_path}")
        raise Exception(f"File not found: {file_path}")
    except PyPDF2.errors.PdfReadError as pdf_err:
        logger.error(f"Error reading PDF, attempting OCR: {file_path} - {pdf_err}")
        # Try OCR as fallback
        try:
            ocr_text = OCRService.extract_text_from_pdf(file_path)
            if ocr_text:
                logger.info(f"OCR successfully extracted {len(ocr_text)} characters from problematic PDF")
                return ocr_text
        except Exception as ocr_e:
            logger.error(f"OCR also failed: {ocr_e}")
        raise Exception(f"Failed to read PDF. It might be corrupted or password-protected: {os.path.basename(file_path)}")
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}", exc_info=True)
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def extract_text_from_image(file_path):
    """Extract text from image using OCR."""
    logger.info(f"Attempting to extract text from image: {file_path}")
    try:
        # Use OCR service to extract text
        text = OCRService.extract_text_from_image(file_path)
        
        if not text:
            logger.warning(f"No text extracted from image: {file_path}")
            return ""
            
        # Use Claude to enhance the OCR text if available
        if ClaudeService.is_available():
            logger.info("Using Claude to enhance OCR text from image...")
            enhanced_text = ClaudeService.enhance_ocr_text(text)
            if enhanced_text:
                text = enhanced_text
                
        logger.info(f"Successfully extracted {len(text)} characters from image")
        return text
        
    except FileNotFoundError:
        logger.error(f"Image file not found: {file_path}")
        raise Exception(f"Image file not found: {file_path}")
    except Exception as e:
        logger.error(f"Error extracting text from image {file_path}: {e}", exc_info=True)
        raise Exception(f"Failed to extract text from image: {str(e)}")

@document_bp.route('/upload', methods=['POST'])
def upload_document():
    """Upload and process a document file."""
    try:
        # Check if file is present
        if 'file' not in request.files:
            logger.warning("File upload attempt with no file part in request.")
            return jsonify({'error': 'No file provided', 'message': 'The request must include a file part.'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            logger.warning("File upload attempt with an empty filename.")
            return jsonify({'error': 'No file selected', 'message': 'Please select a file to upload.'}), 400
        
        # Log original filename
        logger.info(f"Received file upload attempt: Original filename '{file.filename}'")
        
        if not allowed_file(file.filename):
            logger.warning(f"File upload attempt with disallowed file type: {file.filename}")
            return jsonify({
                'error': 'File type not allowed',
                'message': f'File type {file.filename.rsplit(".", 1)[-1] if "." in file.filename else "unknown"} is not supported. Supported types are: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)
        if not filename:
            logger.error(f"Could not secure a valid filename from '{file.filename}'")
            return jsonify({'error': 'Invalid filename', 'message': 'The provided filename is not valid or not allowed.'}), 400
        
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        logger.info(f"Processing file: '{filename}', saving to '{file_path}'")
        
        # Save the file
        try:
            file.save(file_path)
            logger.info(f"File '{filename}' saved successfully to '{file_path}'")
        except Exception as e:
            logger.error(f"Failed to save uploaded file '{filename}' to '{file_path}': {e}", exc_info=True)
            return jsonify({
                'error': 'File save failed',
                'message': f'Could not save file to server. Please try again or contact support if the issue persists. Details: {str(e)}'
            }), 500
        
        # Extract text based on file type
        file_extension = filename.rsplit('.', 1)[1].lower()
        extracted_text = ""
        
        if file_extension == 'txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
                logger.info(f"Successfully extracted text from TXT file: {filename}")
            except FileNotFoundError:
                logger.error(f"TXT file not found after saving: {file_path}")
                return jsonify({'error': 'File processing error', 'message': 'File was saved but could not be found for processing.'}), 500
            except Exception as e:
                logger.error(f"Error reading TXT file {filename}: {e}", exc_info=True)
                return jsonify({'error': 'Text extraction failed', 'message': f"Could not extract text from TXT file. Details: {str(e)}"}), 500
        elif file_extension == 'pdf':
            try:
                extracted_text = extract_text_from_pdf(file_path)
                logger.info(f"Successfully called PDF text extraction for: {filename}")
            except Exception as e:  # Catch specific exception from extract_text_from_pdf
                logger.error(f"Error extracting text from PDF wrapper for {filename}: {e}", exc_info=True)
                # The exception from extract_text_from_pdf is already user-friendly
                return jsonify({'error': 'PDF text extraction failed', 'message': str(e)}), 500
        elif file_extension in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
            try:
                extracted_text = extract_text_from_image(file_path)
                logger.info(f"Successfully called Image text extraction for: {filename}")
                # Check if OCR is placeholder
                if "OCR functionality not yet implemented" in extracted_text:
                    logger.warning(f"OCR not implemented for image file: {filename}")
                    return jsonify({
                        'error': 'OCR not implemented',
                        'message': extracted_text  # Return the placeholder message
                    }), 400  # Use 400 as it's a known limitation, not a server error
            except Exception as e:  # Catch specific exception from extract_text_from_image
                logger.error(f"Error extracting text from Image wrapper for {filename}: {e}", exc_info=True)
                return jsonify({'error': 'Image text extraction failed', 'message': str(e)}), 500
        else:
            # This case should ideally not be reached if allowed_file works correctly
            logger.error(f"Encountered unhandled file extension '{file_extension}' for file '{filename}' after passing checks.")
            return jsonify({'error': 'Unsupported file type', 'message': f"The file type '{file_extension}' is not supported for text extraction."}), 400
        
        # Basic validation
        if not extracted_text or len(extracted_text.strip()) < 10:
            return jsonify({
                'error': 'No readable text found in document',
                'message': 'The document appears to be empty or the text could not be extracted.'
            }), 400
        
        # Return the result
        result = {
            'success': True,
            'filename': filename,
            'file_type': file_extension,
            'text_length': len(extracted_text),
            'extracted_text': extracted_text,
            'upload_id': filename.replace('.', '_'),  # Simple ID for tracking
            'message': 'Document uploaded and processed successfully'
        }
        
        logger.info(f"Successfully processed document: {filename}, text length: {len(extracted_text)}")
        return jsonify(result)
        
    except Exception as e:
        # This is a general catch-all for the /upload route itself
        tb_str = traceback.format_exc()
        logger.error(f"Unhandled error in /upload route for file '{request.files.get('file').filename if 'file' in request.files else 'Unknown file'}': {e}\nTraceback:\n{tb_str}")
        return jsonify({
            'error': 'Document processing failed unexpectedly',
            'message': 'An unexpected error occurred during document processing. Please check server logs.',
            'details': str(e)  # Provide generic error in production, or more details if debug mode is on
        }), 500

@document_bp.route('/text', methods=['POST'])
def process_text():
    """Process raw text input."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if not text or len(text.strip()) < 10:
            return jsonify({'error': 'Text too short or empty'}), 400
        
        result = {
            'success': True,
            'text_length': len(text),
            'extracted_text': text,
            'upload_id': 'text_input',
            'message': 'Text processed successfully'
        }
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing text input: {e}")
        return jsonify({
            'error': 'Text processing failed',
            'message': str(e)
        }), 500

@document_bp.route('/validate', methods=['POST'])
def validate_document():
    """Validate document format and readability."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        # Basic validation checks
        validation_results = {
            'is_valid': True,
            'checks': {
                'length': len(text) >= 50,
                'contains_deed_keywords': any(keyword in text.lower() for keyword in [
                    'deed', 'grantor', 'grantee', 'bearing', 'feet', 'thence', 'metes', 'bounds'
                ]),
                'has_coordinates': any(pattern in text for pattern in ['°', 'degrees', 'north', 'south', 'east', 'west']),
                'readable_format': True  # Basic check - could be enhanced
            },
            'issues': [],
            'suggestions': []
        }
        
        # Check for issues
        if not validation_results['checks']['length']:
            validation_results['issues'].append('Document is too short to be a complete deed')
            validation_results['suggestions'].append('Ensure the complete deed text is included')
        
        if not validation_results['checks']['contains_deed_keywords']:
            validation_results['issues'].append('Document may not be a deed - missing common deed keywords')
            validation_results['suggestions'].append('Verify this is a deed document')
        
        if not validation_results['checks']['has_coordinates']:
            validation_results['issues'].append('No coordinate information found')
            validation_results['suggestions'].append('Check if this deed contains metes and bounds descriptions')
        
        # Overall validation
        validation_results['is_valid'] = len(validation_results['issues']) == 0
        validation_results['score'] = sum(validation_results['checks'].values()) / len(validation_results['checks'])
        
        return jsonify(validation_results)
        
    except Exception as e:
        logger.error(f"Error validating document: {e}")
        return jsonify({
            'error': 'Document validation failed',
            'message': str(e)
        }), 500 