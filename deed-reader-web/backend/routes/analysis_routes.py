"""
Analysis Routes for Deed Reader Pro
----------------------------------
Handles AI-powered document analysis using Claude.
"""

import logging
from flask import Blueprint, request, jsonify
from services.claude_service import ClaudeService

logger = logging.getLogger(__name__)

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_deed():
    """Perform comprehensive AI analysis of deed document."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if not text or len(text.strip()) < 10:
            return jsonify({'error': 'Text too short for analysis'}), 400
        
        # Check if Claude is available
        if not ClaudeService.is_available():
            return jsonify({
                'error': 'AI analysis not available',
                'message': 'Claude service is not configured'
            }), 503
        
        # Perform AI analysis
        analysis_result = ClaudeService.analyze_deed_document(text)
        
        # Add metadata
        analysis_result['analysis_metadata'] = {
            'text_length': len(text),
            'token_count': len(text.split()),  # Simple token count
            'analysis_timestamp': None,  # Could add timestamp
            'model_used': ClaudeService._model
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'message': 'Deed analysis completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in deed analysis: {e}")
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500

@analysis_bp.route('/summary', methods=['POST'])
def generate_summary():
    """Generate a concise summary of the deed document."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if not text or len(text.strip()) < 10:
            return jsonify({'error': 'Text too short for summary'}), 400
        
        # Check if Claude is available
        if not ClaudeService.is_available():
            return jsonify({
                'error': 'AI summary not available',
                'message': 'Claude service is not configured'
            }), 503
        
        # Generate summary
        summary = ClaudeService.generate_summary(text)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'metadata': {
                'text_length': len(text),
                'summary_length': len(summary),
                'model_used': ClaudeService._model
            },
            'message': 'Summary generated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return jsonify({
            'error': 'Summary generation failed',
            'message': str(e)
        }), 500

@analysis_bp.route('/coordinates', methods=['POST'])
def extract_coordinates():
    """Extract coordinate information from deed text."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        if not text or len(text.strip()) < 10:
            return jsonify({'error': 'Text too short for coordinate extraction'}), 400
        
        # Check if Claude is available
        if not ClaudeService.is_available():
            return jsonify({
                'error': 'AI coordinate extraction not available',
                'message': 'Claude service is not configured'
            }), 503
        
        # Extract coordinates
        coordinates = ClaudeService.extract_coordinates(text)
        
        return jsonify({
            'success': True,
            'coordinates': coordinates,
            'metadata': {
                'text_length': len(text),
                'model_used': ClaudeService._model
            },
            'message': 'Coordinate extraction completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error extracting coordinates: {e}")
        return jsonify({
            'error': 'Coordinate extraction failed',
            'message': str(e)
        }), 500

@analysis_bp.route('/validate', methods=['POST'])
def validate_analysis():
    """Validate extracted deed data using AI."""
    try:
        data = request.get_json()
        
        if not data or 'extracted_data' not in data:
            return jsonify({'error': 'No extracted data provided'}), 400
        
        extracted_data = data['extracted_data']
        
        # Check if Claude is available
        if not ClaudeService.is_available():
            return jsonify({
                'error': 'AI validation not available',
                'message': 'Claude service is not configured'
            }), 503
        
        # Validate data
        validation_result = ClaudeService.validate_deed_data(extracted_data)
        
        return jsonify({
            'success': True,
            'validation': validation_result,
            'message': 'Data validation completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error validating data: {e}")
        return jsonify({
            'error': 'Data validation failed',
            'message': str(e)
        }), 500

@analysis_bp.route('/parse', methods=['POST'])
def parse_deed_legacy():
    """Parse deed using legacy parser for comparison."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        
        # Try to import and use the original deed parser
        try:
            import sys
            import os
            
            # Add the original deed_reader path
            original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'deed_reader')
            sys.path.insert(0, original_path)
            
            from deed_reader.core.deed_parser import AdvancedDeedParser
            
            # Parse using original logic
            parser = AdvancedDeedParser(enable_filtering=True, filter_mode='hybrid')
            calls = parser.parse_deed_text(text)
            
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
            
            return jsonify({
                'success': True,
                'parsed_calls': parsed_calls,
                'summary': summary,
                'message': 'Legacy parsing completed successfully'
            })
            
        except ImportError as ie:
            logger.warning(f"Legacy parser not available: {ie}")
            return jsonify({
                'error': 'Legacy parser not available',
                'message': 'Original deed parser could not be imported'
            }), 503
            
    except Exception as e:
        logger.error(f"Error in legacy parsing: {e}")
        return jsonify({
            'error': 'Legacy parsing failed',
            'message': str(e)
        }), 500

@analysis_bp.route('/compare', methods=['POST'])
def compare_analysis():
    """Compare AI analysis with legacy parsing results."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        results = {}
        
        # Try AI analysis
        if ClaudeService.is_available():
            try:
                ai_analysis = ClaudeService.analyze_deed_document(text)
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
            original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'deed_reader')
            sys.path.insert(0, original_path)
            
            from deed_reader.core.deed_parser import AdvancedDeedParser
            
            parser = AdvancedDeedParser(enable_filtering=True, filter_mode='hybrid')
            calls = parser.parse_deed_text(text)
            
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
            'text_length': len(text),
            'both_available': results.get('ai_status') == 'success' and results.get('legacy_status') == 'success'
        }
        
        return jsonify({
            'success': True,
            'comparison': results,
            'message': 'Analysis comparison completed'
        })
        
    except Exception as e:
        logger.error(f"Error in comparison: {e}")
        return jsonify({
            'error': 'Comparison failed',
            'message': str(e)
        }), 500 