"""
Advanced Deed Text Filter for Deed Reader Pro
--------------------------------------------
Next-generation filtering with multi-pass analysis, contextual understanding,
and enhanced AI prompts for maximum accuracy and efficiency.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
from dataclasses import dataclass

from .deed_text_filter import FilterMode, DeedTextFilter


@dataclass
class DeedSection:
    """Represents a section of deed text with metadata."""
    text: str
    section_type: str  # 'boundary', 'legal', 'recording', 'restrictions', etc.
    confidence: float
    start_pos: int
    end_pos: int
    contains_calls: bool = False
    call_count: int = 0


class AdvancedDeedFilter:
    """
    Advanced deed filtering with multi-pass analysis and contextual understanding.
    """
    
    def __init__(self, mode: FilterMode = FilterMode.HYBRID):
        self.mode = mode
        self.logger = logging.getLogger(__name__)
        
        # Enhanced boundary indicators
        self.boundary_indicators = {
            'strong': [
                'beginning at', 'commencing at', 'starting at', 'point of beginning',
                'thence', 'hence', 'from thence', 'from said point',
                'north', 'south', 'east', 'west', 'bearing',
                'degrees', 'minutes', 'seconds', 'feet', 'chains', 'links',
                'iron pin', 'concrete monument', 'rebar', 'stone', 'post',
                'curve', 'arc', 'radius', 'chord', 'delta'
            ],
            'medium': [
                'corner', 'point', 'monument', 'marker', 'boundary', 'line',
                'property line', 'along', 'following', 'parallel',
                'perpendicular', 'adjoining', 'abutting'
            ],
            'weak': [
                'tract', 'parcel', 'lot', 'piece', 'containing',
                'more or less', 'acres', 'described', 'bounded'
            ]
        }
        
        # Enhanced exclusion indicators
        self.exclusion_indicators = {
            'strong': [
                'grantor', 'grantee', 'convey', 'grant', 'sell', 'purchase',
                'consideration', 'dollars', '$', 'heirs', 'successors',
                'assigns', 'warranty', 'quitclaim', 'witness', 'notary',
                'recorded', 'filing', 'clerk', 'register', 'book', 'page'
            ],
            'medium': [
                'tax', 'assessment', 'valuation', 'easement', 'restriction',
                'covenant', 'condition', 'utility', 'right of way'
            ],
            'weak': [
                'subject to', 'reserving', 'excepting', 'together with'
            ]
        }
        
        # Advanced deed structure patterns
        self.structure_patterns = {
            'metes_bounds_start': [
                r'being\s+more\s+particularly\s+described\s+as\s+follows?\s*:?',
                r'more\s+particularly\s+described\s+as\s+follows?\s*:?',
                r'bounded\s+and\s+described\s+as\s+follows?\s*:?',
                r'metes\s+and\s+bounds\s+description\s*:?',
                r'(?:beginning|commencing|starting)\s+at'
            ],
            'metes_bounds_end': [
                r'to\s+the\s+(?:point\s+of\s+)?beginning',
                r'containing\s+[\d.]+\s+acres?',
                r'more\s+or\s+less',
                r'subject\s+to',
                r'together\s+with'
            ],
            'call_patterns': [
                r'thence\s+[ns]\w*\s+\d+[°]\s*\d+[\']\s*\d*[\"]*\s*[ew]\w*\s+[\d.]+\s+\w+',
                r'[ns]\w*\s+\d+[°]\s*\d+[\']\s*\d*[\"]*\s*[ew]\w*\s+[\d.]+\s+(?:feet|ft|chains?|links?)',
                r'curve.*?radius.*?[\d.]+',
                r'along\s+(?:a\s+)?curve.*?feet',
                r'to\s+(?:an?\s+)?(?:iron\s+pin|concrete\s+monument|rebar|stone)'
            ]
        }
    
    def filter_deed_text(self, text: str) -> Dict[str, any]:
        """
        Advanced multi-pass filtering with contextual analysis.
        
        Returns enhanced filtering results with detailed analysis.
        """
        original_length = len(text)
        
        # Step 1: Structural analysis
        sections = self._analyze_deed_structure(text)
        
        # Step 2: Multi-pass filtering
        if self.mode == FilterMode.RULE_BASED:
            result = self._advanced_rule_based_filter(text, sections)
        elif self.mode == FilterMode.MISTRAL_AI:
            result = self._enhanced_mistral_filter(text, sections)
        elif self.mode == FilterMode.OPENAI:
            result = self._enhanced_openai_filter(text, sections)
        else:  # HYBRID
            result = self._advanced_hybrid_filter(text, sections)
        
        # Step 3: Post-processing and validation
        result = self._post_process_filtered_text(result, sections)
        
        # Step 4: Enhanced statistics
        filtered_length = len(result['filtered_text'])
        reduction_percentage = ((original_length - filtered_length) / original_length * 100) if original_length > 0 else 0
        
        result.update({
            'original_length': original_length,
            'filtered_length': filtered_length,
            'reduction_percentage': reduction_percentage,
            'sections_analyzed': len(sections),
            'boundary_sections_found': len([s for s in sections if s.section_type == 'boundary']),
            'advanced_analysis': True
        })
        
        return result
    
    def _analyze_deed_structure(self, text: str) -> List[DeedSection]:
        """Analyze deed structure and identify different sections."""
        sections = []
        
        # Split into logical sections
        paragraphs = re.split(r'\n\s*\n', text)
        current_pos = 0
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                current_pos += len(paragraph) + 2
                continue
            
            section_type = self._classify_section(paragraph)
            confidence = self._calculate_section_confidence(paragraph, section_type)
            contains_calls, call_count = self._analyze_calls_in_section(paragraph)
            
            section = DeedSection(
                text=paragraph.strip(),
                section_type=section_type,
                confidence=confidence,
                start_pos=current_pos,
                end_pos=current_pos + len(paragraph),
                contains_calls=contains_calls,
                call_count=call_count
            )
            
            sections.append(section)
            current_pos += len(paragraph) + 2
        
        return sections
    
    def _classify_section(self, text: str) -> str:
        """Classify a section of text by type."""
        text_lower = text.lower()
        
        # Check for metes and bounds markers
        for pattern in self.structure_patterns['metes_bounds_start']:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return 'boundary'
        
        # Count indicators
        boundary_score = 0
        exclusion_score = 0
        
        for strength, indicators in self.boundary_indicators.items():
            weight = {'strong': 3, 'medium': 2, 'weak': 1}[strength]
            for indicator in indicators:
                if indicator in text_lower:
                    boundary_score += weight
        
        for strength, indicators in self.exclusion_indicators.items():
            weight = {'strong': 3, 'medium': 2, 'weak': 1}[strength]
            for indicator in indicators:
                if indicator in text_lower:
                    exclusion_score += weight
        
        # Classify based on scores
        if boundary_score > exclusion_score + 5:
            return 'boundary'
        elif exclusion_score > boundary_score + 3:
            if any(term in text_lower for term in ['recorded', 'book', 'page', 'clerk']):
                return 'recording'
            elif any(term in text_lower for term in ['grantor', 'grantee', 'convey']):
                return 'legal'
            elif any(term in text_lower for term in ['tax', 'easement', 'restriction']):
                return 'restrictions'
            else:
                return 'legal'
        elif boundary_score > 3:
            return 'potential_boundary'
        else:
            return 'general'
    
    def _calculate_section_confidence(self, text: str, section_type: str) -> float:
        """Calculate confidence score for section classification."""
        if section_type == 'boundary':
            return self._calculate_boundary_confidence(text)
        elif section_type == 'potential_boundary':
            return self._calculate_boundary_confidence(text) * 0.7
        else:
            return 0.1
    
    def _calculate_boundary_confidence(self, text: str) -> float:
        """Calculate confidence that text contains boundary information."""
        text_lower = text.lower()
        
        # Pattern matching for surveying elements
        patterns = [
            r'\b[ns]\w*\s+\d+[°]\s*\d+[\']\s*\d*[\"]*\s*[ew]\w*',  # Bearings
            r'\b\d+\.?\d*\s+(?:feet|ft|chains?|ch|links?)\b',       # Distances
            r'\b(?:thence|hence|from\s+thence)\b',                   # Direction words
            r'\b(?:iron\s+pin|concrete\s+monument|rebar|stone)\b',   # Monuments
            r'\bcurve.*?radius.*?\d+',                               # Curves
            r'\b(?:beginning|commencing)\s+at\b'                     # Starting points
        ]
        
        pattern_matches = sum(1 for pattern in patterns if re.search(pattern, text_lower))
        max_patterns = len(patterns)
        
        # Word-based scoring
        total_words = len(text_lower.split())
        boundary_words = sum(1 for word in self.boundary_indicators['strong'] if word in text_lower)
        
        # Combine scores
        pattern_score = pattern_matches / max_patterns
        word_score = min(1.0, boundary_words / max(1, total_words / 10))
        
        return min(1.0, (pattern_score * 0.7) + (word_score * 0.3))
    
    def _analyze_calls_in_section(self, text: str) -> Tuple[bool, int]:
        """Analyze if section contains surveying calls."""
        call_count = 0
        
        for pattern in self.structure_patterns['call_patterns']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            call_count += len(matches)
        
        return call_count > 0, call_count
    
    def _enhanced_mistral_filter(self, text: str, sections: List[DeedSection]) -> Dict[str, any]:
        """Enhanced Mistral AI filtering with improved prompts."""
        try:
            from deed_reader.data.ocr.mistral_ocr import MistralOCR
            
            mistral = MistralOCR()
            
            # Enhanced prompt with more specific instructions
            enhanced_prompt = f"""
You are an expert land surveyor and legal document analyst. Extract ONLY the metes and bounds boundary description from this deed text.

CRITICAL INSTRUCTIONS:
1. INCLUDE ONLY these elements that define the property boundary:
   - Complete bearing/distance calls (e.g., "North 45° 30' 15" East 125.75 feet")
   - All curve descriptions with radius, delta, chord bearing, and arc length
   - Monument descriptions at corners (iron pins, concrete monuments, stones, etc.)
   - Starting point descriptions ("Beginning at...")
   - Directional progression words ("THENCE", "from thence", "hence")
   - Point-to-point connections that trace the boundary
   - Closing statements ("to the point of beginning")

2. EXCLUDE COMPLETELY:
   - ALL legal language (grantor, grantee, convey, grant, warrant, etc.)
   - Recording information (book, page, volume, clerk, register, etc.)
   - Financial information (consideration, dollars, payment terms)
   - Ownership history and transfers
   - Rights, restrictions, easements, covenants
   - Tax information and assessments
   - Witness clauses and notary information
   - General property descriptions without specific measurements

3. FORMATTING REQUIREMENTS:
   - Preserve exact bearing formats with degrees, minutes, seconds
   - Keep all distance measurements with units
   - Maintain monument descriptions exactly as written
   - Preserve directional progression (THENCE statements)
   - Keep logical flow of boundary traversal

4. QUALITY CONTROL:
   - Only include text that a surveyor would use to plot the boundary
   - Ensure all bearing/distance pairs are complete
   - Verify curve information includes necessary parameters
   - Confirm monument references are specific and useful

Text to analyze:
{text[:4000]}

Return ONLY the metes and bounds boundary description:
"""
            
            filtered_text = mistral.extract_boundary_description(enhanced_prompt)
            
            # Validate and enhance the result
            validated_text = self._validate_mistral_output(filtered_text, sections)
            
            return {
                'filtered_text': validated_text,
                'confidence': 0.95,  # Higher confidence with enhanced prompting
                'sections_found': [{'type': 'ai_enhanced_extraction', 'method': 'mistral_v2'}],
                'method_used': 'mistral_ai_enhanced'
            }
            
        except Exception as e:
            self.logger.warning(f"Enhanced Mistral AI filtering failed: {e}, falling back to advanced rule-based")
            return self._advanced_rule_based_filter(text, sections)
    
    def _validate_mistral_output(self, ai_text: str, sections: List[DeedSection]) -> str:
        """Validate and enhance AI output using structural analysis."""
        if not ai_text or len(ai_text.strip()) < 50:
            # AI output too short, use best boundary sections
            boundary_sections = [s for s in sections if s.section_type == 'boundary']
            if boundary_sections:
                return '\n\n'.join(s.text for s in boundary_sections)
        
        # Check if AI output contains key elements
        ai_lower = ai_text.lower()
        required_elements = ['beginning', 'thence', 'feet']
        
        if not any(element in ai_lower for element in required_elements):
            # AI output missing key elements, supplement with rule-based
            boundary_sections = [s for s in sections if s.section_type in ['boundary', 'potential_boundary']]
            if boundary_sections:
                combined_text = ai_text + '\n\n' + '\n\n'.join(s.text for s in boundary_sections)
                return self._remove_duplicates(combined_text)
        
        return ai_text
    
    def _advanced_rule_based_filter(self, text: str, sections: List[DeedSection]) -> Dict[str, any]:
        """Advanced rule-based filtering with structural analysis."""
        filtered_sections = []
        sections_found = []
        
        # Prioritize boundary sections
        for section in sections:
            if section.section_type == 'boundary' and section.confidence > 0.7:
                filtered_sections.append(section.text)
                sections_found.append({
                    'type': 'high_confidence_boundary',
                    'confidence': section.confidence,
                    'call_count': section.call_count
                })
            elif section.section_type == 'potential_boundary' and section.confidence > 0.5:
                filtered_sections.append(section.text)
                sections_found.append({
                    'type': 'potential_boundary',
                    'confidence': section.confidence,
                    'call_count': section.call_count
                })
        
        # If no high-confidence sections, be more inclusive
        if not filtered_sections:
            for section in sections:
                if section.contains_calls or section.confidence > 0.3:
                    filtered_sections.append(section.text)
                    sections_found.append({
                        'type': 'fallback_section',
                        'confidence': section.confidence
                    })
        
        confidence = min(0.9, max(0.3, sum(s.confidence for s in sections if s.section_type in ['boundary', 'potential_boundary']) / max(1, len(sections))))
        
        return {
            'filtered_text': '\n\n'.join(filtered_sections),
            'confidence': confidence,
            'sections_found': sections_found,
            'method_used': 'advanced_rule_based'
        }
    
    def _advanced_hybrid_filter(self, text: str, sections: List[DeedSection]) -> Dict[str, any]:
        """Advanced hybrid filtering combining multiple approaches."""
        # Start with rule-based analysis
        rule_result = self._advanced_rule_based_filter(text, sections)
        
        # If we have good content, enhance with AI
        if rule_result['confidence'] > 0.6 and len(rule_result['filtered_text']) > 100:
            try:
                # Use AI to refine the pre-filtered content
                ai_result = self._enhanced_mistral_filter(rule_result['filtered_text'], sections)
                
                # Combine the best of both
                return {
                    'filtered_text': ai_result['filtered_text'],
                    'confidence': min(0.98, (rule_result['confidence'] + ai_result['confidence']) / 2),
                    'sections_found': rule_result['sections_found'] + ai_result['sections_found'],
                    'method_used': 'advanced_hybrid'
                }
                
            except Exception as e:
                self.logger.warning(f"AI enhancement failed: {e}, using advanced rule-based result")
                rule_result['method_used'] = 'advanced_hybrid_rule_only'
                return rule_result
        
        # Try pure AI if rule-based didn't find much
        try:
            return self._enhanced_mistral_filter(text, sections)
        except Exception:
            return rule_result
    
    def _post_process_filtered_text(self, result: Dict, sections: List[DeedSection]) -> Dict:
        """Post-process filtered text for quality and consistency."""
        text = result['filtered_text']
        
        # Remove duplicate content
        text = self._remove_duplicates(text)
        
        # Clean up formatting
        text = self._clean_formatting(text)
        
        # Validate completeness
        text = self._ensure_completeness(text, sections)
        
        result['filtered_text'] = text
        return result
    
    def _remove_duplicates(self, text: str) -> str:
        """Remove duplicate sentences and phrases."""
        sentences = re.split(r'[.;]', text)
        unique_sentences = []
        seen = set()
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence.lower() not in seen:
                unique_sentences.append(sentence)
                seen.add(sentence.lower())
        
        return '. '.join(unique_sentences).strip()
    
    def _clean_formatting(self, text: str) -> str:
        """Clean up text formatting and spacing."""
        # Fix spacing around degree symbols
        text = re.sub(r'\s*°\s*', '° ', text)
        
        # Fix spacing around quote marks
        text = re.sub(r'\s*\'\s*', '\' ', text)
        text = re.sub(r'\s*\"\s*', '\" ', text)
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Ensure proper capitalization for direction words
        text = re.sub(r'\bthence\b', 'THENCE', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbeginning\b', 'BEGINNING', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _ensure_completeness(self, text: str, sections: List[DeedSection]) -> str:
        """Ensure the filtered text contains complete boundary information."""
        text_lower = text.lower()
        
        # Check for essential elements
        has_beginning = 'beginning' in text_lower
        has_thence = 'thence' in text_lower
        has_distances = bool(re.search(r'\d+\.?\d*\s+(?:feet|ft|chains?)', text_lower))
        has_bearings = bool(re.search(r'[ns]\w*\s+\d+[°]', text_lower))
        
        # If missing critical elements, try to add them from high-confidence sections
        if not (has_beginning and has_thence and has_distances and has_bearings):
            for section in sections:
                if section.section_type == 'boundary' and section.confidence > 0.8:
                    if section.text.lower() not in text_lower:
                        text += '\n\n' + section.text
                        break
        
        return text
    
    def _enhanced_openai_filter(self, text: str, sections: List[DeedSection]) -> Dict[str, any]:
        """Enhanced OpenAI filtering (placeholder for future implementation)."""
        # For now, fall back to rule-based
        return self._advanced_rule_based_filter(text, sections)


# Enhanced convenience function
def filter_deed_advanced(text: str, mode: FilterMode = FilterMode.HYBRID) -> Dict[str, any]:
    """
    Advanced deed filtering with comprehensive analysis.
    
    Args:
        text: Raw deed text
        mode: Filtering mode to use
        
    Returns:
        Comprehensive filtering results with detailed analysis
    """
    filter_obj = AdvancedDeedFilter(mode)
    return filter_obj.filter_deed_text(text) 