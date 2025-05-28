"""
Deed Text Filter for Deed Reader Pro
-----------------------------------
AI-powered filtering to extract only boundary-relevant information from deed documents.
Removes irrelevant content like legal descriptions, ownership history, tax info, etc.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum


class FilterMode(Enum):
    """Filtering modes available."""
    RULE_BASED = "rule_based"
    MISTRAL_AI = "mistral_ai"
    OPENAI = "openai"
    HYBRID = "hybrid"


class DeedTextFilter:
    """Intelligent deed text filter that extracts only boundary-relevant information."""
    
    def __init__(self, mode: FilterMode = FilterMode.HYBRID):
        self.mode = mode
        self.logger = logging.getLogger(__name__)
        
        # Keywords that indicate boundary-relevant sections
        self.boundary_keywords = [
            # Direction and measurement terms
            'north', 'south', 'east', 'west', 'bearing', 'degrees', 'minutes', 'seconds',
            'feet', 'chains', 'links', 'poles', 'rods', 'yards', 'meters', 'vara',
            
            # Surveying terms
            'thence', 'beginning', 'commence', 'corner', 'point', 'monument', 'marker',
            'iron', 'pin', 'rod', 'stake', 'stone', 'concrete', 'post', 'nail',
            'found', 'set', 'existing', 'placed', 'located',
            
            # Geometric terms
            'curve', 'arc', 'radius', 'chord', 'delta', 'tangent', 'angle',
            'line', 'boundary', 'perimeter', 'property line',
            
            # Metes and bounds phrases
            'metes and bounds', 'more particularly described', 'being more particularly',
            'bounded and described', 'tract of land', 'parcel of land',
            'piece of land', 'lot of land', 'containing',
            
            # Adjoining references
            'adjoining', 'abutting', 'along', 'with lands of', 'bounded by',
            'adjacent to', 'contiguous'
        ]
        
        # Keywords that indicate irrelevant sections
        self.irrelevant_keywords = [
            # Legal/ownership terms
            'grantor', 'grantee', 'convey', 'grant', 'bargain', 'sell', 'deed',
            'warranty', 'quitclaim', 'consideration', 'dollars', '$',
            'heirs', 'successors', 'assigns', 'title', 'ownership',
            
            # Recording information
            'recorded', 'filing', 'clerk', 'register', 'book', 'page',
            'document', 'instrument', 'volume', 'plat', 'subdivision',
            
            # Legal descriptions
            'whereas', 'know all men', 'witnesseth', 'habendum',
            'tenendum', 'reversion', 'remainder', 'estate',
            
            # Restrictions and easements (unless they affect boundary)
            'easement', 'right of way', 'utility', 'restriction',
            'covenant', 'condition', 'mineral rights', 'water rights',
            
            # Tax and valuation
            'tax', 'assessment', 'valuation', 'appraised', 'market value'
        ]
        
        # Section markers that often contain boundary descriptions
        self.boundary_section_markers = [
            r'being\s+more\s+particularly\s+described',
            r'more\s+particularly\s+described\s+as\s+follows',
            r'bounded\s+and\s+described\s+as\s+follows',
            r'metes\s+and\s+bounds\s+description',
            r'tract\s+of\s+land.*described\s+as\s+follows',
            r'beginning\s+at',
            r'commencing\s+at',
            r'starting\s+at'
        ]
    
    def filter_deed_text(self, text: str) -> Dict[str, any]:
        """
        Filter deed text to extract only boundary-relevant information.
        
        Returns:
            dict: {
                'filtered_text': str,
                'confidence': float,
                'sections_found': list,
                'method_used': str,
                'original_length': int,
                'filtered_length': int,
                'reduction_percentage': float
            }
        """
        original_length = len(text)
        
        if self.mode == FilterMode.RULE_BASED:
            result = self._rule_based_filter(text)
        elif self.mode == FilterMode.MISTRAL_AI:
            result = self._mistral_ai_filter(text)
        elif self.mode == FilterMode.OPENAI:
            result = self._openai_filter(text)
        else:  # HYBRID
            result = self._hybrid_filter(text)
        
        # Calculate statistics
        filtered_length = len(result['filtered_text'])
        reduction_percentage = ((original_length - filtered_length) / original_length * 100) if original_length > 0 else 0
        
        result.update({
            'original_length': original_length,
            'filtered_length': filtered_length,
            'reduction_percentage': reduction_percentage
        })
        
        return result
    
    def _rule_based_filter(self, text: str) -> Dict[str, any]:
        """Extract boundary-relevant sections using rule-based pattern matching."""
        sections_found = []
        filtered_paragraphs = []
        
        # Split text into paragraphs
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        
        for i, paragraph in enumerate(paragraphs):
            score = self._calculate_boundary_relevance_score(paragraph)
            
            # Include paragraphs with high boundary relevance
            if score > 0.3:  # Threshold for relevance
                filtered_paragraphs.append(paragraph)
                sections_found.append({
                    'paragraph_index': i,
                    'score': score,
                    'preview': paragraph[:100] + "..." if len(paragraph) > 100 else paragraph
                })
        
        # Also look for explicit boundary description sections
        boundary_sections = self._extract_boundary_sections(text)
        for section in boundary_sections:
            if section not in filtered_paragraphs:
                filtered_paragraphs.append(section)
                sections_found.append({
                    'type': 'explicit_boundary_section',
                    'preview': section[:100] + "..." if len(section) > 100 else section
                })
        
        return {
            'filtered_text': '\n\n'.join(filtered_paragraphs),
            'confidence': min(0.8, len(sections_found) * 0.2),  # Higher confidence with more sections
            'sections_found': sections_found,
            'method_used': 'rule_based'
        }
    
    def _calculate_boundary_relevance_score(self, text: str) -> float:
        """Calculate how relevant a text section is to boundary description."""
        text_lower = text.lower()
        
        # Count boundary-relevant keywords
        boundary_count = sum(1 for keyword in self.boundary_keywords if keyword in text_lower)
        
        # Count irrelevant keywords (negative score)
        irrelevant_count = sum(1 for keyword in self.irrelevant_keywords if keyword in text_lower)
        
        # Look for surveying patterns
        surveying_patterns = [
            r'\b[ns]\s*\d+[°]\s*\d+[\']\s*\d*[\"]*\s*[ew]\b',  # Bearing format
            r'\b\d+\.?\d*\s*(feet|ft|chains?|ch|links?)\b',     # Distance format
            r'\bthence\b',                                       # Direction words
            r'\bbeginning\s+at\b',                              # Starting points
            r'\bcorner\s+of\b'                                  # Corner references
        ]
        
        pattern_count = sum(1 for pattern in surveying_patterns 
                          if re.search(pattern, text_lower))
        
        # Calculate weighted score
        total_words = len(text_lower.split())
        if total_words == 0:
            return 0.0
        
        # Boundary keywords: +1 point each
        # Surveying patterns: +3 points each  
        # Irrelevant keywords: -1 point each
        raw_score = boundary_count + (pattern_count * 3) - irrelevant_count
        
        # Normalize by text length and cap at 1.0
        normalized_score = min(1.0, max(0.0, raw_score / total_words * 10))
        
        return normalized_score
    
    def _extract_boundary_sections(self, text: str) -> List[str]:
        """Extract sections that explicitly contain boundary descriptions."""
        sections = []
        
        for pattern in self.boundary_section_markers:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            
            for match in matches:
                # Extract text from match to end of paragraph or next section
                start_pos = match.start()
                
                # Find the end of this section (next paragraph break or end of text)
                remaining_text = text[start_pos:]
                
                # Look for natural break points
                section_end = len(remaining_text)
                for end_pattern in [r'\n\s*\n', r'\.[\s]*[A-Z]', r'WITNESS', r'IN WITNESS']:
                    end_match = re.search(end_pattern, remaining_text)
                    if end_match and end_match.start() < section_end:
                        section_end = end_match.start()
                
                section = remaining_text[:section_end].strip()
                if len(section) > 50:  # Only include substantial sections
                    sections.append(section)
        
        return sections
    
    def _mistral_ai_filter(self, text: str) -> Dict[str, any]:
        """Use Mistral AI to extract boundary-relevant information."""
        try:
            # Check if Mistral AI is available
            from deed_reader.data.ocr.mistral_ocr import MistralOCR
            
            mistral = MistralOCR()
            
            # Create a focused prompt for boundary extraction
            prompt = self._create_boundary_extraction_prompt(text)
            
            # Use Mistral to analyze and filter the text
            filtered_text = mistral.extract_boundary_description(prompt)
            
            return {
                'filtered_text': filtered_text,
                'confidence': 0.9,  # High confidence in AI analysis
                'sections_found': [{'type': 'ai_extracted', 'method': 'mistral'}],
                'method_used': 'mistral_ai'
            }
            
        except Exception as e:
            self.logger.warning(f"Mistral AI filtering failed: {e}, falling back to rule-based")
            return self._rule_based_filter(text)
    
    def _openai_filter(self, text: str) -> Dict[str, any]:
        """Use OpenAI to extract boundary-relevant information."""
        try:
            import openai
            
            # Check if OpenAI is configured
            api_key = self._get_openai_api_key()
            if not api_key:
                raise ValueError("OpenAI API key not found")
            
            client = openai.OpenAI(api_key=api_key)
            
            prompt = f"""
            You are a professional land surveyor and deed analyst. Extract ONLY the metes and bounds description from this deed document. 

            Focus on:
            - Bearing and distance calls (e.g., "North 45° 30' East 125.75 feet")
            - Curve descriptions with radius, delta, chord information
            - Monument references (iron pins, stones, corners, etc.)
            - Starting points and corners
            - Boundary descriptions that describe the property perimeter

            Exclude:
            - Legal ownership language
            - Grantor/grantee information  
            - Recording details
            - Tax or valuation information
            - Rights and restrictions (unless they affect the boundary)
            - Historical ownership information

            Return only the text that describes the physical boundary of the property.

            Deed text:
            {text[:4000]}  # Limit text to avoid token limits
            """
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1  # Low temperature for consistent extraction
            )
            
            filtered_text = response.choices[0].message.content.strip()
            
            return {
                'filtered_text': filtered_text,
                'confidence': 0.95,  # Very high confidence in OpenAI analysis
                'sections_found': [{'type': 'ai_extracted', 'method': 'openai'}],
                'method_used': 'openai'
            }
            
        except Exception as e:
            self.logger.warning(f"OpenAI filtering failed: {e}, falling back to rule-based")
            return self._rule_based_filter(text)
    
    def _hybrid_filter(self, text: str) -> Dict[str, any]:
        """Use combined rule-based and AI filtering for best results."""
        # Start with rule-based filtering
        rule_result = self._rule_based_filter(text)
        
        # If rule-based found good content, enhance with AI
        if rule_result['confidence'] > 0.5 and len(rule_result['filtered_text']) > 100:
            try:
                # Try Mistral AI first (since it's already integrated)
                if self._is_mistral_available():
                    ai_result = self._mistral_ai_filter(rule_result['filtered_text'])
                else:
                    ai_result = self._openai_filter(rule_result['filtered_text'])
                
                # Combine results
                return {
                    'filtered_text': ai_result['filtered_text'],
                    'confidence': min(0.95, (rule_result['confidence'] + ai_result['confidence']) / 2),
                    'sections_found': rule_result['sections_found'] + ai_result['sections_found'],
                    'method_used': 'hybrid_rule_and_ai'
                }
                
            except Exception as e:
                self.logger.warning(f"AI enhancement failed: {e}, using rule-based result")
                rule_result['method_used'] = 'hybrid_rule_only'
                return rule_result
        
        # If rule-based didn't find much, try pure AI
        try:
            if self._is_mistral_available():
                return self._mistral_ai_filter(text)
            else:
                return self._openai_filter(text)
        except Exception:
            return rule_result
    
    def _create_boundary_extraction_prompt(self, text: str) -> str:
        """Create a focused prompt for AI boundary extraction."""
        return f"""
        Extract only the metes and bounds property boundary description from this deed text.

        Include ONLY:
        - Bearing and distance measurements
        - Curve descriptions (radius, delta, chord)
        - Monument references and corner descriptions
        - Starting and ending points
        - Directional calls (North, South, East, West with angles)

        Exclude everything else including legal language, ownership details, recording information.

        Text: {text[:3000]}
        """
    
    def _is_mistral_available(self) -> bool:
        """Check if Mistral AI is available and configured."""
        try:
            from deed_reader.data.ocr.mistral_ocr import MistralOCR
            return True
        except ImportError:
            return False
    
    def _get_openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment or config."""
        import os
        return os.getenv('OPENAI_API_KEY')


# Convenience function for easy integration
def filter_deed_for_boundary(text: str, mode: FilterMode = FilterMode.HYBRID) -> str:
    """
    Quick function to filter deed text for boundary information.
    
    Args:
        text: Raw deed text
        mode: Filtering mode to use
        
    Returns:
        Filtered text containing only boundary-relevant information
    """
    filter_obj = DeedTextFilter(mode)
    result = filter_obj.filter_deed_text(text)
    return result['filtered_text'] 