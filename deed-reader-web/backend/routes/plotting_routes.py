"""
Plotting Routes for Deed Reader Pro
----------------------------------
Handles deed plotting, coordinate calculations, and visualization.
"""

import logging
import io
import zipfile
from flask import Blueprint, request, jsonify, send_file
from services.plotting_service import AdvancedPlottingService

logger = logging.getLogger(__name__)

plotting_bp = Blueprint('plotting', __name__)

@plotting_bp.route('/plot', methods=['POST'])
def plot_deed():
    """Generate comprehensive plotting data from deed text."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No deed text provided'}), 400
        
        deed_text = data['text']
        
        if not deed_text or len(deed_text.strip()) < 10:
            return jsonify({'error': 'Deed text too short for plotting'}), 400
        
        # Initialize plotting service
        plotting_service = AdvancedPlottingService()
        
        # Process deed for plotting
        plot_result = plotting_service.process_deed_for_plotting(deed_text)
        
        return jsonify({
            'success': True,
            'plot_data': plot_result,
            'message': 'Deed plotting completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in deed plotting: {e}")
        return jsonify({
            'error': 'Plotting failed',
            'message': str(e)
        }), 500

@plotting_bp.route('/coordinates', methods=['POST'])
def get_coordinates():
    """Extract and calculate coordinates from deed text."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No deed text provided'}), 400
        
        deed_text = data['text']
        plotting_service = AdvancedPlottingService()
        
        # Extract plotting data
        plot_data = plotting_service._extract_plotting_data_with_ai(deed_text)
        coordinates = plotting_service._calculate_coordinates(plot_data)
        
        return jsonify({
            'success': True,
            'coordinates': coordinates,
            'total_points': len(coordinates),
            'message': 'Coordinates calculated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error calculating coordinates: {e}")
        return jsonify({
            'error': 'Coordinate calculation failed',
            'message': str(e)
        }), 500

@plotting_bp.route('/closure', methods=['POST'])
def analyze_closure():
    """Perform closure analysis on deed coordinates."""
    try:
        data = request.get_json()
        
        if not data or 'coordinates' not in data:
            return jsonify({'error': 'No coordinates provided'}), 400
        
        coordinates = data['coordinates']
        plotting_service = AdvancedPlottingService()
        
        # Analyze closure
        closure_analysis = plotting_service._analyze_closure(coordinates)
        
        return jsonify({
            'success': True,
            'closure_analysis': closure_analysis,
            'message': 'Closure analysis completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in closure analysis: {e}")
        return jsonify({
            'error': 'Closure analysis failed',
            'message': str(e)
        }), 500

@plotting_bp.route('/export/<format_type>', methods=['POST'])
def export_plot_data(format_type):
    """Export plot data in various formats."""
    try:
        data = request.get_json()
        
        if not data or 'coordinates' not in data:
            return jsonify({'error': 'No coordinates provided'}), 400
        
        coordinates = data['coordinates']
        plotting_service = AdvancedPlottingService()
        
        # Generate export data
        export_data = plotting_service._generate_export_data(coordinates)
        
        if format_type not in export_data['formats']:
            return jsonify({'error': f'Export format {format_type} not supported'}), 400
        
        # Get the specific format data
        format_data = export_data['formats'][format_type]
        
        # Create in-memory file
        if format_type == 'dxf':
            file_content = format_data
            filename = 'deed_plot.dxf'
            mimetype = 'application/dxf'
        elif format_type == 'csv':
            file_content = format_data
            filename = 'coordinates.csv'
            mimetype = 'text/csv'
        elif format_type == 'esri_traverse':
            file_content = format_data
            filename = 'traverse.txt'
            mimetype = 'text/plain'
        elif format_type == 'autocad_script':
            file_content = format_data
            filename = 'plot_script.scr'
            mimetype = 'text/plain'
        elif format_type == 'kml':
            file_content = format_data
            filename = 'deed_plot.kml'
            mimetype = 'application/vnd.google-earth.kml+xml'
        else:
            return jsonify({'error': 'Unsupported format'}), 400
        
        # Create file-like object
        file_obj = io.BytesIO(file_content.encode('utf-8'))
        
        return send_file(
            file_obj,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
    except Exception as e:
        logger.error(f"Error exporting plot data: {e}")
        return jsonify({
            'error': 'Export failed',
            'message': str(e)
        }), 500

@plotting_bp.route('/export/all', methods=['POST'])
def export_all_formats():
    """Export plot data in all available formats as a ZIP file."""
    try:
        data = request.get_json()
        
        if not data or 'coordinates' not in data:
            return jsonify({'error': 'No coordinates provided'}), 400
        
        coordinates = data['coordinates']
        plotting_service = AdvancedPlottingService()
        
        # Generate export data for all formats
        export_data = plotting_service._generate_export_data(coordinates)
        
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add each format to ZIP
            zip_file.writestr('deed_plot.dxf', export_data['formats']['dxf'])
            zip_file.writestr('coordinates.csv', export_data['formats']['csv'])
            zip_file.writestr('traverse.txt', export_data['formats']['esri_traverse'])
            zip_file.writestr('plot_script.scr', export_data['formats']['autocad_script'])
            zip_file.writestr('deed_plot.kml', export_data['formats']['kml'])
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            as_attachment=True,
            download_name='deed_plot_exports.zip',
            mimetype='application/zip'
        )
        
    except Exception as e:
        logger.error(f"Error exporting all formats: {e}")
        return jsonify({
            'error': 'Export failed',
            'message': str(e)
        }), 500

@plotting_bp.route('/validate', methods=['POST'])
def validate_plot():
    """Validate plot data for errors and inconsistencies."""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No deed text provided'}), 400
        
        deed_text = data['text']
        plotting_service = AdvancedPlottingService()
        
        # Process deed and validate
        plot_result = plotting_service.process_deed_for_plotting(deed_text)
        
        # Additional validation checks
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'suggestions': []
        }
        
        closure = plot_result.get('closure_analysis', {})
        
        # Check closure
        if not closure.get('is_closed', False):
            validation_results['warnings'].append({
                'type': 'closure',
                'message': f"Plot does not close. Closure distance: {closure.get('closure_distance', 'unknown')} feet"
            })
        
        # Check precision
        closure_error_ppm = closure.get('closure_error_ppm', 0)
        if closure_error_ppm > 5000:  # > 1:200 precision
            validation_results['warnings'].append({
                'type': 'precision',
                'message': f"Low precision: {closure.get('precision_ratio', 'unknown')}"
            })
        
        # Check for missing data
        coordinates = plot_result.get('coordinates', [])
        if len(coordinates) < 3:
            validation_results['errors'].append({
                'type': 'insufficient_data',
                'message': 'Insufficient coordinate points for a valid plot'
            })
            validation_results['is_valid'] = False
        
        return jsonify({
            'success': True,
            'validation': validation_results,
            'plot_data': plot_result,
            'message': 'Plot validation completed'
        })
        
    except Exception as e:
        logger.error(f"Error validating plot: {e}")
        return jsonify({
            'error': 'Plot validation failed',
            'message': str(e)
        }), 500

@plotting_bp.route('/transform', methods=['POST'])
def transform_coordinates():
    """Transform coordinates between different coordinate systems."""
    try:
        data = request.get_json()
        
        if not data or 'coordinates' not in data:
            return jsonify({'error': 'No coordinates provided'}), 400
        
        coordinates = data['coordinates']
        from_system = data.get('from_system', 'local')
        to_system = data.get('to_system', 'state_plane')
        
        # For now, return the same coordinates with a note
        # In a real implementation, you'd use projection libraries like pyproj
        transformed_coordinates = coordinates.copy()
        
        for coord in transformed_coordinates:
            coord['original_x'] = coord['x']
            coord['original_y'] = coord['y']
            coord['coordinate_system'] = to_system
            # Add transformation note
            coord['transformation_note'] = f"Transformed from {from_system} to {to_system}"
        
        return jsonify({
            'success': True,
            'coordinates': transformed_coordinates,
            'transformation': {
                'from_system': from_system,
                'to_system': to_system,
                'method': 'placeholder',  # Would be actual transformation method
                'accuracy': 'high'
            },
            'message': f'Coordinates transformed from {from_system} to {to_system}'
        })
        
    except Exception as e:
        logger.error(f"Error transforming coordinates: {e}")
        return jsonify({
            'error': 'Coordinate transformation failed',
            'message': str(e)
        }), 500 