"""
Advanced Deed Parser for Deed Reader Pro
----------------------------------------
AI-powered parsing of metes and bounds descriptions with support for:
- Bearing and distance calls
- Curve descriptions
- Monument references
- Passing monuments
- Adjoining tract descriptions
- Commencement calls
- Multiple units and formats
- Smart text filtering to focus on boundary-relevant content
"""

import re
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class DeedCall:
    """Represents a single call in a deed description."""
    call_type: str  # 'bearing_distance', 'curve', 'tie', 'adjoiner', 'commencement', 'monument'
    bearing: Optional[str] = None
    distance: Optional[float] = None
    units: str = 'feet'
    curve_data: Optional[Dict] = None
    monument: Optional[str] = None
    description: Optional[str] = None
    passing_monuments: Optional[List[str]] = None
    raw_text: str = ""
    confidence: float = 0.0


class AdvancedDeedParser:
    """Advanced AI-powered deed parser with comprehensive pattern recognition."""
    
    # Bearing patterns - supports multiple formats
    BEARING_PATTERNS = [
        # With words: North 45 degrees 30 minutes 15 seconds East
        r'(North|South|N|S)\s+(\d+)\s+degrees?\s+(\d+)\s+minutes?\s+(\d+)\s+seconds?\s+(East|West|E|W)',
        # With words: North 45 degrees 30 minutes East (no seconds)
        r'(North|South|N|S)\s+(\d+)\s+degrees?\s+(\d+)\s+minutes?\s+(East|West|E|W)',
        # Standard surveyor format with symbols: South 28° 50' 45" West
        r'(North|South|N|S)\s+(\d+)[°]\s*(\d+)[\'\s]*(\d+)?[\"\s]*(East|West|E|W)',
        # Standard surveyor format: N45°30'15"E
        r'([NS])\s*(\d+)[°]\s*(\d+)[\']\s*(\d+)["]\s*([EW])',
        # Without seconds: N45°30'E
        r'([NS])\s*(\d+)[°]\s*(\d+)[\']\s*([EW])',
        # Decimal degrees: N45.5°E
        r'([NS])\s*(\d+\.?\d*)[°]\s*([EW])',
        # With colon separator: N45:30:15E
        r'([NS])\s*(\d+):(\d+):(\d+)\s*([EW])',
    ]
    
    # Distance patterns with multiple units
    DISTANCE_PATTERNS = [
        # Combined units first: 5 chains 25 links
        r'(\d+)\s*(chains?|ch)\s+(\d+)\s*(links?|lk)',
        r'(\d+)\s*(poles?|rods?|p)\s+(\d+)\s*(links?|lk)',
        # With "a distance of" phrase
        r'a\s+distance\s+of\s+(\d+\.?\d*)\s*(feet|ft|foot)\b',
        r'a\s+distance\s+of\s+(\d+\.?\d*)\s*(yards?|yd)\b',
        r'a\s+distance\s+of\s+(\d+\.?\d*)\s*(chains?|ch)\b',
        # Standard format: 125.75 feet
        r'(\d+\.?\d*)\s*(feet|ft|foot)\b',
        r'(\d+\.?\d*)\s*(yards?|yd)\b',
        r'(\d+\.?\d*)\s*(chains?|ch)\b',
        r'(\d+\.?\d*)\s*(poles?|rods?|p)\b',
        r'(\d+\.?\d*)\s*(links?|lk)\b',
        r'(\d+\.?\d*)\s*(meters?|m)\b',
        r'(\d+\.?\d*)\s*(vara)\b',
    ]
    
    # Curve patterns
    CURVE_PATTERNS = [
        # Radius and delta: radius=50.0, delta=45°30'
        r'radius\s*=?\s*(\d+\.?\d*),?\s*delta\s*=?\s*([^,;]+)',
        # Chord bearing and distance
        r'chord\s+bearing\s+([^,;]+),?\s*(\d+\.?\d*)\s*(feet|ft)',
        # Arc length
        r'arc\s+length\s*=?\s*(\d+\.?\d*)',
    ]
    
    # Monument patterns
    MONUMENT_PATTERNS = [
        r'\b(iron\s+pin|iron\s+rod|concrete\s+monument|stone|post|stake|nail|pk\s+nail)\b',
        r'\b(found|set|existing|new)\s+(iron\s+pin|iron\s+rod|concrete\s+monument|stone|post)\b',
        r'\b(monument|marker|corner|point)\b',
        r'\b(\d+/\d+"\s+rebar|rebar)\b',
    ]
    
    # Passing monument patterns
    PASSING_PATTERNS = [
        r'passing\s+([^,;]+?)(?:,|\s+to|\s+thence)',
        r'by\s+([^,;]+?)(?:,|\s+to|\s+thence)',
        r'along\s+([^,;]+?)(?:,|\s+to|\s+thence)',
    ]
    
    def __init__(self, enable_filtering: bool = True, filter_mode: str = 'hybrid'):
        self.calls = []
        self.confidence_threshold = 0.5  # Lower threshold for better detection
        self.enable_filtering = enable_filtering
        self.filter_mode = filter_mode
        self.filter_stats = None  # Store filtering statistics
        
        # Check if advanced filtering is available and enabled by configuration
        try:
            from deed_reader.config.settings import ENABLE_ADVANCED_FILTERING
            if ENABLE_ADVANCED_FILTERING and enable_filtering:
                self.use_advanced_filtering = True
            else:
                self.use_advanced_filtering = False
        except ImportError:
            self.use_advanced_filtering = False
        
    def parse_deed_text(self, text: str) -> List[DeedCall]:
        """
        Parse deed text and extract all calls with high confidence.
        Optionally filters text to focus on boundary-relevant content first.
        Returns list of DeedCall objects.
        """
        self.calls = []
        
        # Apply filtering if enabled
        if self.enable_filtering:
            filtered_text, filter_stats = self._filter_deed_text(text)
            self.filter_stats = filter_stats
            text_to_parse = filtered_text
        else:
            text_to_parse = text
            self.filter_stats = {
                'filtering_enabled': False,
                'original_length': len(text),
                'filtered_length': len(text),
                'reduction_percentage': 0.0
            }
        
        # Clean and normalize text
        cleaned_text = self._clean_text(text_to_parse)
        
        # Split into sentences/clauses
        clauses = self._split_into_clauses(cleaned_text)
        
        # Parse each clause
        for clause in clauses:
            call = self._parse_clause(clause)
            if call and call.confidence >= self.confidence_threshold:
                self.calls.append(call)
        
        return self.calls
    
    def _filter_deed_text(self, text: str) -> Tuple[str, Dict]:
        """Filter deed text to extract only boundary-relevant information using advanced filtering."""
        # If advanced filtering is available and enabled, try it first
        if hasattr(self, 'use_advanced_filtering') and self.use_advanced_filtering:
            try:
                from deed_reader.core.advanced_deed_filter import AdvancedDeedFilter, FilterMode
                
                # Map string mode to enum
                mode_mapping = {
                    'rule_based': FilterMode.RULE_BASED,
                    'mistral_ai': FilterMode.MISTRAL_AI,
                    'openai': FilterMode.OPENAI,
                    'hybrid': FilterMode.HYBRID
                }
                
                filter_mode = mode_mapping.get(self.filter_mode, FilterMode.HYBRID)
                filter_obj = AdvancedDeedFilter(filter_mode)
                
                result = filter_obj.filter_deed_text(text)
                return result['filtered_text'], result
                
            except Exception as e:
                print(f"Advanced deed text filtering failed: {e}, falling back to basic filtering")
        
        # Fall back to basic filtering
        try:
            from deed_reader.core.deed_text_filter import DeedTextFilter, FilterMode
            
            mode_mapping = {
                'rule_based': FilterMode.RULE_BASED,
                'mistral_ai': FilterMode.MISTRAL_AI,
                'openai': FilterMode.OPENAI,
                'hybrid': FilterMode.HYBRID
            }
            
            filter_mode = mode_mapping.get(self.filter_mode, FilterMode.HYBRID)
            filter_obj = DeedTextFilter(filter_mode)
            
            result = filter_obj.filter_deed_text(text)
            return result['filtered_text'], result
            
        except Exception as e:
            print(f"Basic deed text filtering failed: {e}")
            return self._fallback_filter(text)
    
    def _fallback_filter(self, text: str) -> Tuple[str, Dict]:
        """Fallback filtering when all AI methods fail."""
        return text, {
            'filtering_enabled': True,
            'filtering_failed': True,
            'error': 'All filtering methods failed',
            'original_length': len(text),
            'filtered_length': len(text),
            'reduction_percentage': 0.0,
            'method_used': 'fallback_no_filtering'
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize deed text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize quotes and special characters
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        # Normalize degree symbols
        text = text.replace('°', '°').replace('º', '°')
        
        return text.strip()
    
    def _split_into_clauses(self, text: str) -> List[str]:
        """Split text into individual clauses for parsing."""
        # Split on common deed delimiters
        delimiters = [';', 'thence', 'then', 'from thence', 'from said']
        
        clauses = [text]
        for delimiter in delimiters:
            new_clauses = []
            for clause in clauses:
                parts = re.split(f'\\b{delimiter}\\b', clause, flags=re.IGNORECASE)
                new_clauses.extend([p.strip() for p in parts if p.strip()])
            clauses = new_clauses
        
        return clauses
    
    def _parse_clause(self, clause: str) -> Optional[DeedCall]:
        """Parse a single clause and extract call information."""
        clause = clause.strip()
        if not clause:
            return None
        
        # Try different call types in order of specificity
        
        # 1. Curve calls
        curve_call = self._parse_curve_call(clause)
        if curve_call:
            return curve_call
        
        # 2. Bearing and distance calls
        bearing_distance_call = self._parse_bearing_distance_call(clause)
        if bearing_distance_call:
            return bearing_distance_call
        
        # 3. Monument calls
        monument_call = self._parse_monument_call(clause)
        if monument_call:
            return monument_call
        
        # 4. Adjoiner calls
        adjoiner_call = self._parse_adjoiner_call(clause)
        if adjoiner_call:
            return adjoiner_call
        
        return None
    
    def _parse_bearing_distance_call(self, clause: str) -> Optional[DeedCall]:
        """Parse bearing and distance from a clause."""
        bearing = self._extract_bearing(clause)
        distance, units = self._extract_distance(clause)
        
        if bearing and distance:
            confidence = 0.9  # High confidence for complete bearing/distance
            
            # Extract passing monuments
            passing_monuments = self._extract_passing_monuments(clause)
            
            # Extract end monument
            monument = self._extract_monument(clause)
            
            return DeedCall(
                call_type='bearing_distance',
                bearing=bearing,
                distance=distance,
                units=units,
                monument=monument,
                passing_monuments=passing_monuments,
                raw_text=clause,
                confidence=confidence
            )
        
        return None
    
    def _parse_curve_call(self, clause: str) -> Optional[DeedCall]:
        """Parse curve information from a clause."""
        # Look for curve keywords
        if not re.search(r'\b(curve|arc|radius|chord|delta)\b', clause, re.IGNORECASE):
            return None
        
        curve_data = {}
        confidence = 0.6
        
        # Extract radius
        radius_match = re.search(r'radius\s*=?\s*(\d+\.?\d*)', clause, re.IGNORECASE)
        if radius_match:
            curve_data['radius'] = float(radius_match.group(1))
            confidence += 0.2
        
        # Extract delta angle
        delta_match = re.search(r'delta\s*=?\s*([^,;]+)', clause, re.IGNORECASE)
        if delta_match:
            curve_data['delta'] = delta_match.group(1).strip()
            confidence += 0.2
        
        # Extract chord bearing and distance
        chord_bearing = self._extract_bearing(clause)
        chord_distance, units = self._extract_distance(clause)
        
        if chord_bearing:
            curve_data['chord_bearing'] = chord_bearing
            confidence += 0.1
        
        if chord_distance:
            curve_data['chord_distance'] = chord_distance
            curve_data['units'] = units
            confidence += 0.1
        
        if curve_data:
            return DeedCall(
                call_type='curve',
                curve_data=curve_data,
                raw_text=clause,
                confidence=confidence
            )
        
        return None
    
    def _parse_monument_call(self, clause: str) -> Optional[DeedCall]:
        """Parse monument description from a clause."""
        monument = self._extract_monument(clause)
        
        if monument:
            # Check if this is a setting or finding monument
            action = None
            if re.search(r'\b(set|setting|placed)\b', clause, re.IGNORECASE):
                action = 'set'
            elif re.search(r'\b(found|existing|located)\b', clause, re.IGNORECASE):
                action = 'found'
            
            return DeedCall(
                call_type='monument',
                monument=monument,
                description=f"{action} {monument}" if action else monument,
                raw_text=clause,
                confidence=0.8
            )
        
        return None
    
    def _parse_adjoiner_call(self, clause: str) -> Optional[DeedCall]:
        """Parse adjoining tract description."""
        # Look for adjoiner keywords
        adjoiner_keywords = [
            r'\bwith\s+lands?\s+of\b',
            r'\balong\s+lands?\s+of\b',
            r'\bbounded\s+by\b',
            r'\badjoining\b',
            r'\babutting\b'
        ]
        
        for pattern in adjoiner_keywords:
            if re.search(pattern, clause, re.IGNORECASE):
                return DeedCall(
                    call_type='adjoiner',
                    description=clause,
                    raw_text=clause,
                    confidence=0.7
                )
        
        return None
    
    def _extract_bearing(self, text: str) -> Optional[str]:
        """Extract bearing from text using multiple patterns."""
        for pattern in self.BEARING_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Return the full match for the bearing
                bearing = match.group(0).strip()
                # Basic validation - bearing should start with N or S
                if bearing.upper().startswith(('N', 'S', 'NORTH', 'SOUTH')):
                    return bearing
        return None
    
    def _extract_distance(self, text: str) -> Tuple[Optional[float], str]:
        """Extract distance and units from text."""
        for pattern in self.DISTANCE_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    # Simple distance and unit
                    distance = float(match.group(1))
                    units = match.group(2).lower()
                    return distance, units
                elif len(match.groups()) == 4:
                    # Combined units (e.g., chains and links)
                    major = float(match.group(1))
                    major_unit = match.group(2).lower()
                    minor = float(match.group(3))
                    minor_unit = match.group(4).lower()
                    
                    # Convert to feet
                    total_feet = self._convert_to_feet(major, major_unit) + self._convert_to_feet(minor, minor_unit)
                    return total_feet, 'feet'
        
        return None, 'feet'
    
    def _extract_monument(self, text: str) -> Optional[str]:
        """Extract monument description from text."""
        for pattern in self.MONUMENT_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def _extract_passing_monuments(self, text: str) -> List[str]:
        """Extract passing monuments from text."""
        monuments = []
        for pattern in self.PASSING_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                monuments.append(match.group(1).strip())
        return monuments
    
    def _convert_to_feet(self, value: float, unit: str) -> float:
        """Convert various units to feet."""
        conversions = {
            'feet': 1.0, 'ft': 1.0, 'foot': 1.0,
            'yards': 3.0, 'yd': 3.0, 'yard': 3.0,
            'chains': 66.0, 'ch': 66.0, 'chain': 66.0,
            'poles': 16.5, 'p': 16.5, 'pole': 16.5, 'rods': 16.5, 'rod': 16.5,
            'links': 0.66, 'lk': 0.66, 'link': 0.66,
            'meters': 3.28084, 'm': 3.28084, 'meter': 3.28084,
            'vara': 2.777778
        }
        
        return value * conversions.get(unit.lower(), 1.0)
    
    def get_call_summary(self) -> Dict:
        """Get summary statistics of parsed calls and filtering performance."""
        summary = {
            'total_calls': len(self.calls),
            'bearing_distance_calls': len([c for c in self.calls if c.call_type == 'bearing_distance']),
            'curve_calls': len([c for c in self.calls if c.call_type == 'curve']),
            'monument_calls': len([c for c in self.calls if c.call_type == 'monument']),
            'adjoiner_calls': len([c for c in self.calls if c.call_type == 'adjoiner']),
            'average_confidence': sum(c.confidence for c in self.calls) / len(self.calls) if self.calls else 0
        }
        
        # Add filtering statistics if available
        if self.filter_stats:
            summary['filtering'] = self.filter_stats
        
        return summary 