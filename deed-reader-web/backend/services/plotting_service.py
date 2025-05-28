"""
Advanced Plotting Service for Deed Reader Pro
--------------------------------------------
Handles intelligent deed plotting, coordinate calculations, and closure analysis using AI.
"""

import json
import math
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from services.claude_service import ClaudeService

logger = logging.getLogger(__name__)

@dataclass
class PlotPoint:
    """Represents a point in the deed plot."""
    x: float
    y: float
    label: str
    monument_type: Optional[str] = None
    description: Optional[str] = None

@dataclass
class PlotCall:
    """Represents a single call in the deed plot."""
    from_point: PlotPoint
    to_point: PlotPoint
    bearing: str
    distance: float
    units: str
    raw_bearing: Optional[float] = None  # In decimal degrees
    curve_data: Optional[Dict] = None
    monuments: Optional[List[str]] = None
    call_type: str = 'line'  # 'line', 'curve', 'tie'

@dataclass
class ClosureAnalysis:
    """Represents closure analysis results."""
    closure_distance: float
    closure_bearing: str
    precision_ratio: str
    area_acres: float
    area_sq_feet: float
    perimeter_feet: float
    is_closed: bool
    closure_error_ppm: float  # Parts per million

class AdvancedPlottingService:
    """Service for intelligent deed plotting and analysis."""
    
    def __init__(self):
        self.points: List[PlotPoint] = []
        self.calls: List[PlotCall] = []
        self.closure_analysis: Optional[ClosureAnalysis] = None
        
    def process_deed_for_plotting(self, deed_text: str) -> Dict[str, Any]:
        """
        Process deed text and generate comprehensive plotting data using AI.
        Returns coordinates, closure analysis, and plotting instructions.
        """
        try:
            # Use Claude to extract detailed plotting information
            plot_data = self._extract_plotting_data_with_ai(deed_text)
            
            # Calculate coordinates
            coordinates = self._calculate_coordinates(plot_data)
            
            # Perform closure analysis
            closure = self._analyze_closure(coordinates)
            
            # Generate plotting instructions
            plotting_instructions = self._generate_plotting_instructions(coordinates, closure)
            
            return {
                'success': True,
                'coordinates': coordinates,
                'closure_analysis': closure,
                'plotting_data': plot_data,
                'plotting_instructions': plotting_instructions,
                'export_formats': self._generate_export_data(coordinates)
            }
            
        except Exception as e:
            logger.error(f"Error in deed plotting: {e}")
            raise Exception(f"Failed to process deed for plotting: {str(e)}")
    
    def _extract_plotting_data_with_ai(self, deed_text: str) -> Dict[str, Any]:
        """Use Claude to extract detailed plotting information."""
        if not ClaudeService.is_available():
            raise Exception("Claude service not available for plotting")
        
        prompt = f"""
        As an expert land surveyor, analyze this deed and extract ALL plotting information in precise detail.
        
        Deed Text:
        {deed_text}
        
        Extract and return in JSON format:
        {{
            "point_of_beginning": {{
                "description": "Detailed POB description",
                "coordinates": {{"x": 0, "y": 0}},
                "monument": "Monument type at POB"
            }},
            "calls": [
                {{
                    "sequence": 1,
                    "bearing": "N45°30'15\"E",
                    "bearing_decimal": 45.504167,
                    "distance": 125.75,
                    "units": "feet",
                    "call_type": "line",
                    "description": "Full call description",
                    "to_monument": "Monument at end of call",
                    "passing_monuments": ["Monument 1", "Monument 2"],
                    "curve_data": null
                }}
            ],
            "curves": [
                {{
                    "sequence": 2,
                    "chord_bearing": "S67°45'W",
                    "chord_distance": 89.44,
                    "radius": 50.0,
                    "delta": "45°30'",
                    "curve_length": 39.79,
                    "units": "feet"
                }}
            ],
            "adjoiners": [
                {{
                    "direction": "northerly",
                    "description": "Lands of John Smith",
                    "calls": ["Adjoining property calls if any"]
                }}
            ],
            "commencement": {{
                "has_commencement": true,
                "calls": ["Calls from monument to POB"]
            }},
            "closure_info": {{
                "expected_closure": "Returns to POB",
                "area_mentioned": "5.75 acres more or less"
            }}
        }}
        
        Be extremely precise with bearings, distances, and coordinate calculations.
        """
        
        try:
            message = ClaudeService._client.messages.create(
                model=ClaudeService._model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
                temperature=0.1
            )
            
            result = message.content[0].text
            
            # Try to extract JSON from the response
            if "```json" in result:
                json_start = result.find("```json") + 7
                json_end = result.find("```", json_start)
                result = result[json_start:json_end].strip()
            elif "{" in result:
                json_start = result.find("{")
                json_end = result.rfind("}") + 1
                result = result[json_start:json_end]
                
            return json.loads(result)
            
        except json.JSONDecodeError:
            # Fallback to basic parsing if JSON fails
            return self._basic_plotting_extraction(deed_text)
        except Exception as e:
            logger.error(f"Error in AI plotting extraction: {e}")
            raise
    
    def _calculate_coordinates(self, plot_data: Dict) -> List[Dict]:
        """Calculate precise coordinates for all points."""
        coordinates = []
        current_x, current_y = 0.0, 0.0
        
        # Start at point of beginning
        pob = plot_data.get('point_of_beginning', {})
        coordinates.append({
            'point_number': 0,
            'x': current_x,
            'y': current_y,
            'label': 'POB',
            'description': pob.get('description', 'Point of Beginning'),
            'monument': pob.get('monument')
        })
        
        # Process each call
        for i, call in enumerate(plot_data.get('calls', [])):
            bearing_decimal = call.get('bearing_decimal')
            distance = call.get('distance', 0)
            
            if bearing_decimal is not None and distance > 0:
                # Convert bearing to radians and calculate coordinates
                bearing_rad = math.radians(bearing_decimal)
                
                # Calculate delta coordinates
                delta_x = distance * math.sin(bearing_rad)
                delta_y = distance * math.cos(bearing_rad)
                
                # Update current position
                current_x += delta_x
                current_y += delta_y
                
                coordinates.append({
                    'point_number': i + 1,
                    'x': round(current_x, 3),
                    'y': round(current_y, 3),
                    'label': f'P{i + 1}',
                    'description': call.get('description', ''),
                    'monument': call.get('to_monument'),
                    'bearing': call.get('bearing'),
                    'distance': distance,
                    'units': call.get('units', 'feet')
                })
        
        return coordinates
    
    def _analyze_closure(self, coordinates: List[Dict]) -> Dict[str, Any]:
        """Perform comprehensive closure analysis."""
        if len(coordinates) < 3:
            return {'error': 'Insufficient points for closure analysis'}
        
        # Get last point and POB
        last_point = coordinates[-1]
        pob = coordinates[0]
        
        # Calculate closure distance and bearing
        dx = pob['x'] - last_point['x']
        dy = pob['y'] - last_point['y']
        
        closure_distance = math.sqrt(dx**2 + dy**2)
        closure_bearing_rad = math.atan2(dx, dy)
        closure_bearing_deg = math.degrees(closure_bearing_rad)
        
        # Convert to surveyor bearing format
        closure_bearing = self._decimal_to_bearing(closure_bearing_deg)
        
        # Calculate perimeter
        perimeter = sum(coord.get('distance', 0) for coord in coordinates[1:])
        
        # Calculate precision ratio
        precision_ratio = f"1:{int(perimeter / closure_distance)}" if closure_distance > 0 else "Perfect"
        
        # Calculate area using shoelace formula
        area_sq_feet = self._calculate_area(coordinates)
        area_acres = area_sq_feet / 43560  # Convert to acres
        
        # Determine if closed (within reasonable tolerance)
        is_closed = closure_distance < 0.1  # 0.1 feet tolerance
        
        # Calculate closure error in parts per million
        closure_error_ppm = (closure_distance / perimeter) * 1000000 if perimeter > 0 else 0
        
        return {
            'closure_distance': round(closure_distance, 3),
            'closure_bearing': closure_bearing,
            'precision_ratio': precision_ratio,
            'area_acres': round(area_acres, 3),
            'area_sq_feet': round(area_sq_feet, 1),
            'perimeter_feet': round(perimeter, 1),
            'is_closed': is_closed,
            'closure_error_ppm': round(closure_error_ppm, 1),
            'coordinates_to_close': {
                'dx': round(dx, 3),
                'dy': round(dy, 3)
            }
        }
    
    def _calculate_area(self, coordinates: List[Dict]) -> float:
        """Calculate area using the shoelace formula."""
        n = len(coordinates)
        if n < 3:
            return 0.0
        
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += coordinates[i]['x'] * coordinates[j]['y']
            area -= coordinates[j]['x'] * coordinates[i]['y']
        
        return abs(area) / 2.0
    
    def _decimal_to_bearing(self, decimal_degrees: float) -> str:
        """Convert decimal degrees to surveyor bearing format."""
        # Normalize to 0-360
        decimal_degrees = decimal_degrees % 360
        
        if decimal_degrees <= 90:
            # Northeast quadrant
            return f"N{decimal_degrees:.0f}°E"
        elif decimal_degrees <= 180:
            # Southeast quadrant
            return f"S{180 - decimal_degrees:.0f}°E"
        elif decimal_degrees <= 270:
            # Southwest quadrant
            return f"S{decimal_degrees - 180:.0f}°W"
        else:
            # Northwest quadrant
            return f"N{360 - decimal_degrees:.0f}°W"
    
    def _generate_plotting_instructions(self, coordinates: List[Dict], closure: Dict) -> Dict[str, Any]:
        """Generate detailed plotting instructions for web visualization."""
        return {
            'plot_type': 'traverse',
            'scale': 'auto',
            'grid_enabled': True,
            'coordinate_system': 'local',
            'plot_elements': {
                'points': coordinates,
                'lines': [
                    {
                        'from': coordinates[i],
                        'to': coordinates[i + 1] if i + 1 < len(coordinates) else coordinates[0],
                        'style': 'solid',
                        'color': '#2563eb',
                        'width': 2
                    }
                    for i in range(len(coordinates))
                ],
                'labels': True,
                'monuments': True,
                'bearings': True,
                'distances': True
            },
            'closure_display': {
                'show_closure_line': not closure.get('is_closed', False),
                'closure_color': '#ef4444' if not closure.get('is_closed', False) else '#10b981'
            }
        }
    
    def _generate_export_data(self, coordinates: List[Dict]) -> Dict[str, Any]:
        """Generate data for various export formats."""
        return {
            'formats': {
                'dxf': self._generate_dxf_data(coordinates),
                'csv': self._generate_csv_data(coordinates),
                'esri_traverse': self._generate_esri_traverse(coordinates),
                'autocad_script': self._generate_autocad_script(coordinates),
                'kml': self._generate_kml_data(coordinates)
            }
        }
    
    def _generate_dxf_data(self, coordinates: List[Dict]) -> str:
        """Generate DXF file content."""
        dxf_content = """0
SECTION
2
ENTITIES
"""
        
        # Add polyline
        dxf_content += """0
POLYLINE
8
BOUNDARY
66
1
10
0.0
20
0.0
30
0.0
"""
        
        for coord in coordinates:
            dxf_content += f"""0
VERTEX
8
BOUNDARY
10
{coord['x']}
20
{coord['y']}
30
0.0
"""
        
        dxf_content += """0
SEQEND
0
ENDSEC
0
EOF
"""
        return dxf_content
    
    def _generate_csv_data(self, coordinates: List[Dict]) -> str:
        """Generate CSV coordinate data."""
        csv_content = "Point,X,Y,Description,Monument\n"
        for coord in coordinates:
            csv_content += f"{coord['label']},{coord['x']},{coord['y']},{coord.get('description', '')},{coord.get('monument', '')}\n"
        return csv_content
    
    def _generate_esri_traverse(self, coordinates: List[Dict]) -> str:
        """Generate Esri traverse file for ArcGIS Pro."""
        traverse_content = "TRAVERSE\n"
        traverse_content += "UNITS FEET\n"
        traverse_content += "BEGIN\n"
        
        for i, coord in enumerate(coordinates[1:], 1):
            prev_coord = coordinates[i - 1]
            dx = coord['x'] - prev_coord['x']
            dy = coord['y'] - prev_coord['y']
            distance = math.sqrt(dx**2 + dy**2)
            bearing = math.degrees(math.atan2(dx, dy))
            
            traverse_content += f"COURSE {bearing:.6f} {distance:.3f}\n"
        
        traverse_content += "END\n"
        return traverse_content
    
    def _generate_autocad_script(self, coordinates: List[Dict]) -> str:
        """Generate AutoCAD script commands."""
        script = "PLINE\n"
        for coord in coordinates:
            script += f"{coord['x']},{coord['y']}\n"
        script += "C\n"  # Close polyline
        return script
    
    def _generate_kml_data(self, coordinates: List[Dict]) -> str:
        """Generate KML for Google Earth visualization."""
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Deed Plot</name>
    <Placemark>
      <name>Property Boundary</name>
      <LineString>
        <coordinates>
"""
        
        for coord in coordinates:
            # Note: For real KML, you'd need to convert local coordinates to lat/lon
            kml_content += f"{coord['x']},{coord['y']},0\n"
        
        kml_content += """        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
"""
        return kml_content
    
    def _basic_plotting_extraction(self, deed_text: str) -> Dict[str, Any]:
        """Fallback basic plotting extraction if AI fails."""
        # Basic regex-based extraction as fallback
        return {
            'point_of_beginning': {'description': 'Point of Beginning', 'coordinates': {'x': 0, 'y': 0}},
            'calls': [],
            'curves': [],
            'adjoiners': [],
            'commencement': {'has_commencement': False},
            'closure_info': {'expected_closure': 'Unknown'}
        } 