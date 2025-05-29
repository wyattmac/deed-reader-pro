"""
Analysis Router for Deed Reader Pro - FastAPI Implementation
-----------------------------------------------------------
Handles AI-powered document analysis using Claude with async support.
"""

import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from services.claude_service import ClaudeService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/analysis",
    tags=["analysis"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response validation
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to analyze")

class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to summarize")

class CoordinatesRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to extract coordinates from")

class ValidateRequest(BaseModel):
    extracted_data: Dict[str, Any] = Field(..., description="Extracted data to validate")

class ParseRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to parse with legacy parser")

class CompareRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to compare analysis methods")

class AnalysisResponse(BaseModel):
    success: bool
    analysis: Optional[Dict[str, Any]] = None
    message: str

class SummaryResponse(BaseModel):
    success: bool
    summary: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    message: str

class CoordinatesResponse(BaseModel):
    success: bool
    coordinates: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None
    message: str

class ValidationResponse(BaseModel):
    success: bool
    validation: Optional[Dict[str, Any]] = None
    message: str

class ParseResponse(BaseModel):
    success: bool
    parsed_calls: Optional[List[Dict[str, Any]]] = None
    summary: Optional[Dict[str, Any]] = None
    message: str

class CompareResponse(BaseModel):
    success: bool
    comparison: Optional[Dict[str, Any]] = None
    message: str


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_deed(request: AnalyzeRequest):
    """
    Perform comprehensive AI analysis of deed document.
    
    This endpoint uses Claude AI to analyze deed text and extract:
    - Property boundaries and bearings
    - Legal descriptions
    - Monument information
    - Property ownership details
    """
    try:
        # Check if Claude is available
        if not ClaudeService.is_available():
            raise HTTPException(
                status_code=503,
                detail={
                    'error': 'AI analysis not available',
                    'message': 'Claude service is not configured'
                }
            )
        
        # Perform AI analysis
        analysis_result = ClaudeService.analyze_deed_document(request.text)
        
        # Add metadata
        analysis_result['analysis_metadata'] = {
            'text_length': len(request.text),
            'token_count': len(request.text.split()),
            'analysis_timestamp': None,  # Could add timestamp
            'model_used': ClaudeService._model
        }
        
        return AnalysisResponse(
            success=True,
            analysis=analysis_result,
            message='Deed analysis completed successfully'
        )
        
    except Exception as e:
        logger.error(f"Error in deed analysis: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                'error': 'Analysis failed',
                'message': str(e)
            }
        )


@router.post("/summary", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """
    Generate a concise summary of the deed document.
    
    Returns a brief overview of the deed including:
    - Property location
    - Key boundaries
    - Important legal information
    """
    try:
        # Check if Claude is available
        if not ClaudeService.is_available():
            raise HTTPException(
                status_code=503,
                detail={
                    'error': 'AI summary not available',
                    'message': 'Claude service is not configured'
                }
            )
        
        # Generate summary
        summary = ClaudeService.generate_summary(request.text)
        
        return SummaryResponse(
            success=True,
            summary=summary,
            metadata={
                'text_length': len(request.text),
                'summary_length': len(summary),
                'model_used': ClaudeService._model
            },
            message='Summary generated successfully'
        )
        
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                'error': 'Summary generation failed',
                'message': str(e)
            }
        )


@router.post("/coordinates", response_model=CoordinatesResponse)
async def extract_coordinates(request: CoordinatesRequest):
    """
    Extract coordinate information from deed text.
    
    Extracts:
    - Bearings and distances
    - Starting points
    - Monument locations
    - Boundary descriptions
    """
    try:
        # Check if Claude is available
        if not ClaudeService.is_available():
            raise HTTPException(
                status_code=503,
                detail={
                    'error': 'AI coordinate extraction not available',
                    'message': 'Claude service is not configured'
                }
            )
        
        # Extract coordinates
        coordinates = ClaudeService.extract_coordinates(request.text)
        
        return CoordinatesResponse(
            success=True,
            coordinates=coordinates,
            metadata={
                'text_length': len(request.text),
                'model_used': ClaudeService._model
            },
            message='Coordinate extraction completed successfully'
        )
        
    except Exception as e:
        logger.error(f"Error extracting coordinates: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                'error': 'Coordinate extraction failed',
                'message': str(e)
            }
        )


@router.post("/validate", response_model=ValidationResponse)
async def validate_analysis(request: ValidateRequest):
    """
    Validate extracted deed data using AI.
    
    Checks for:
    - Closure errors
    - Bearing consistency
    - Distance accuracy
    - Legal description completeness
    """
    try:
        # Check if Claude is available
        if not ClaudeService.is_available():
            raise HTTPException(
                status_code=503,
                detail={
                    'error': 'AI validation not available',
                    'message': 'Claude service is not configured'
                }
            )
        
        # Validate data
        validation_result = ClaudeService.validate_deed_data(request.extracted_data)
        
        return ValidationResponse(
            success=True,
            validation=validation_result,
            message='Data validation completed successfully'
        )
        
    except Exception as e:
        logger.error(f"Error validating data: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                'error': 'Data validation failed',
                'message': str(e)
            }
        )


@router.post("/parse", response_model=ParseResponse)
async def parse_deed_legacy(request: ParseRequest):
    """
    Parse deed using legacy parser for comparison.
    
    Uses the original deed parsing logic for:
    - Backward compatibility
    - Performance comparison
    - Validation against AI results
    """
    try:
        # Try to import and use the original deed parser
        try:
            import sys
            import os
            
            # Add the original deed_reader path
            original_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'deed_reader'
            )
            sys.path.insert(0, original_path)
            
            from deed_reader.core.deed_parser import AdvancedDeedParser
            
            # Parse using original logic
            parser = AdvancedDeedParser(enable_filtering=True, filter_mode='hybrid')
            calls = parser.parse_deed_text(request.text)
            
            # Convert to serializable format
            parsed_calls = []
            for call in calls:
                call_dict = {
                    'call_type': call.call_type,
                    'bearing': call.bearing,
                    'distance': call.distance,
                    'units': call.units,
                    'monument': call.monument,
                    'description': call.description,
                    'raw_text': call.raw_text,
                    'confidence': call.confidence
                }
                
                if call.curve_data:
                    call_dict['curve_data'] = call.curve_data
                if call.passing_monuments:
                    call_dict['passing_monuments'] = call.passing_monuments
                    
                parsed_calls.append(call_dict)
            
            # Get summary
            summary = parser.get_call_summary()
            
            return ParseResponse(
                success=True,
                parsed_calls=parsed_calls,
                summary=summary,
                message='Legacy parsing completed successfully'
            )
            
        except ImportError as ie:
            logger.warning(f"Legacy parser not available: {ie}")
            raise HTTPException(
                status_code=503,
                detail={
                    'error': 'Legacy parser not available',
                    'message': 'Original deed parser could not be imported'
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in legacy parsing: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                'error': 'Legacy parsing failed',
                'message': str(e)
            }
        )


@router.post("/compare", response_model=CompareResponse)
async def compare_analysis(request: CompareRequest):
    """
    Compare AI analysis with legacy parsing results.
    
    Provides side-by-side comparison of:
    - AI Claude analysis
    - Legacy parser results
    - Performance metrics
    - Accuracy assessment
    """
    try:
        results = {}
        
        # Try AI analysis
        if ClaudeService.is_available():
            try:
                ai_analysis = ClaudeService.analyze_deed_document(request.text)
                results['ai_analysis'] = ai_analysis
                results['ai_status'] = 'success'
            except Exception as e:
                results['ai_status'] = 'failed'
                results['ai_error'] = str(e)
        else:
            results['ai_status'] = 'unavailable'
        
        # Try legacy parsing
        try:
            import sys
            import os
            
            # Add the original deed_reader path
            original_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'deed_reader'
            )
            sys.path.insert(0, original_path)
            
            from deed_reader.core.deed_parser import AdvancedDeedParser
            
            parser = AdvancedDeedParser(enable_filtering=True, filter_mode='hybrid')
            calls = parser.parse_deed_text(request.text)
            
            # Convert to serializable format
            parsed_calls = []
            for call in calls:
                call_dict = {
                    'call_type': call.call_type,
                    'bearing': call.bearing,
                    'distance': call.distance,
                    'units': call.units,
                    'monument': call.monument,
                    'description': call.description,
                    'raw_text': call.raw_text,
                    'confidence': call.confidence
                }
                parsed_calls.append(call_dict)
            
            results['legacy_analysis'] = {
                'parsed_calls': parsed_calls,
                'summary': parser.get_call_summary()
            }
            results['legacy_status'] = 'success'
            
        except Exception as e:
            results['legacy_status'] = 'failed'
            results['legacy_error'] = str(e)
        
        # Add comparison metadata
        results['comparison_metadata'] = {
            'text_length': len(request.text),
            'both_available': (
                results.get('ai_status') == 'success' and 
                results.get('legacy_status') == 'success'
            )
        }
        
        return CompareResponse(
            success=True,
            comparison=results,
            message='Analysis comparison completed'
        )
        
    except Exception as e:
        logger.error(f"Error in comparison: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                'error': 'Comparison failed',
                'message': str(e)
            }
        ) 