import logging
import re
from typing import Dict, List
import spacy
from spacy.matcher import Matcher

class NLPProcessor:
    """Handles NLP processing for clause extraction and analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            # Load English language model
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            self.logger.warning("spaCy English model not found. Using basic processing.")
            self.nlp = None
        
        # Initialize matcher for common contract patterns
        if self.nlp:
            self.matcher = Matcher(self.nlp.vocab)
            self._setup_patterns()
    
    def _setup_patterns(self):
        """Setup common contract clause patterns"""
        
        # Payment terms patterns
        payment_patterns = [
            [{"LOWER": {"IN": ["payment", "pay"]}}, {"LOWER": {"IN": ["shall", "will", "must"]}}, {"IS_ALPHA": True, "OP": "*"}],
            [{"LOWER": "freight"}, {"IS_ALPHA": True, "OP": "*"}, {"LOWER": {"IN": ["payable", "due", "payment"]}}],
            [{"LOWER": {"IN": ["demurrage", "despatch"]}}, {"IS_ALPHA": True, "OP": "*"}]
        ]
        
        # Laytime patterns
        laytime_patterns = [
            [{"LOWER": "laytime"}, {"IS_ALPHA": True, "OP": "*"}],
            [{"LOWER": {"IN": ["loading", "discharging"]}}, {"LOWER": "time"}, {"IS_ALPHA": True, "OP": "*"}],
            [{"LIKE_NUM": True}, {"LOWER": {"IN": ["hours", "days"]}}, {"LOWER": {"IN": ["loading", "discharging", "laytime"]}}]
        ]
        
        # Cargo patterns
        cargo_patterns = [
            [{"LOWER": "cargo"}, {"IS_ALPHA": True, "OP": "*"}],
            [{"LOWER": {"IN": ["quantity", "tonnage"]}}, {"IS_ALPHA": True, "OP": "*"}],
            [{"LIKE_NUM": True}, {"LOWER": {"IN": ["mt", "tons", "tonnes", "metric"]}}]
        ]
        
        # Add patterns to matcher
        self.matcher.add("PAYMENT_TERMS", payment_patterns)
        self.matcher.add("LAYTIME", laytime_patterns)
        self.matcher.add("CARGO", cargo_patterns)
    
    def extract_clauses(self, document_contents: Dict[str, str]) -> Dict[str, List[str]]:
        """Extract and categorize clauses from document contents"""
        
        extracted_clauses = {
            'payment_terms': [],
            'laytime_clauses': [],
            'cargo_specifications': [],
            'port_clauses': [],
            'general_terms': [],
            'key_entities': []
        }
        
        try:
            # Process each document
            for doc_type, content in document_contents.items():
                if not content:
                    continue
                
                self.logger.info(f"Processing {doc_type} for clause extraction")
                
                # Extract clauses using different methods
                if self.nlp:
                    # Use spaCy for advanced processing
                    doc = self.nlp(content)
                    
                    # Extract named entities
                    entities = self._extract_entities(doc)
                    extracted_clauses['key_entities'].extend(entities)
                    
                    # Use pattern matching
                    pattern_matches = self._extract_pattern_matches(doc)
                    for category, matches in pattern_matches.items():
                        extracted_clauses[category].extend(matches)
                    
                    # Extract sentences containing key terms
                    key_sentences = self._extract_key_sentences(doc)
                    for category, sentences in key_sentences.items():
                        extracted_clauses[category].extend(sentences)
                
                # Fallback to regex-based extraction
                regex_clauses = self._extract_with_regex(content)
                for category, clauses in regex_clauses.items():
                    extracted_clauses[category].extend(clauses)
            
            # Remove duplicates and clean up
            for category in extracted_clauses:
                extracted_clauses[category] = list(set(extracted_clauses[category]))
                extracted_clauses[category] = [clause.strip() for clause in extracted_clauses[category] if clause.strip()]
            
            self.logger.info(f"Extracted clauses: {sum(len(clauses) for clauses in extracted_clauses.values())} total")
            
        except Exception as e:
            self.logger.error(f"Error in clause extraction: {str(e)}")
        
        return extracted_clauses
    
    def _extract_entities(self, doc) -> List[str]:
        """Extract named entities from document"""
        entities = []
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'GPE', 'MONEY', 'DATE', 'QUANTITY']:
                entities.append(f"{ent.text} ({ent.label_})")
        return entities
    
    def _extract_pattern_matches(self, doc) -> Dict[str, List[str]]:
        """Extract clauses using pattern matching"""
        matches = {
            'payment_terms': [],
            'laytime_clauses': [],
            'cargo_specifications': []
        }
        
        # Get pattern matches
        pattern_matches = self.matcher(doc)
        
        for match_id, start, end in pattern_matches:
            label = self.nlp.vocab.strings[match_id]
            matched_text = doc[start:end].text
            
            if label == "PAYMENT_TERMS":
                matches['payment_terms'].append(matched_text)
            elif label == "LAYTIME":
                matches['laytime_clauses'].append(matched_text)
            elif label == "CARGO":
                matches['cargo_specifications'].append(matched_text)
        
        return matches
    
    def _extract_key_sentences(self, doc) -> Dict[str, List[str]]:
        """Extract sentences containing key contract terms"""
        key_terms = {
            'payment_terms': ['payment', 'freight', 'demurrage', 'despatch', 'commission'],
            'laytime_clauses': ['laytime', 'loading', 'discharging', 'notice', 'commencement'],
            'port_clauses': ['port', 'berth', 'anchorage', 'terminal', 'wharf'],
            'general_terms': ['force majeure', 'arbitration', 'governing law', 'cancellation']
        }
        
        extracted = {category: [] for category in key_terms}
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            sent_lower = sent_text.lower()
            
            for category, terms in key_terms.items():
                if any(term in sent_lower for term in terms):
                    if len(sent_text) > 20:  # Filter out very short sentences
                        extracted[category].append(sent_text)
        
        return extracted
    
    def _extract_with_regex(self, content: str) -> Dict[str, List[str]]:
        """Extract clauses using regex patterns as fallback"""
        extracted = {
            'payment_terms': [],
            'laytime_clauses': [],
            'cargo_specifications': [],
            'port_clauses': [],
            'general_terms': []
        }
        
        # Payment terms patterns
        payment_patterns = [
            r'freight\s+.*?payable.*?[.;]',
            r'demurrage\s+.*?[.;]',
            r'payment\s+.*?[.;]'
        ]
        
        # Laytime patterns
        laytime_patterns = [
            r'laytime\s+.*?[.;]',
            r'loading\s+time\s+.*?[.;]',
            r'discharging\s+time\s+.*?[.;]'
        ]
        
        # Cargo patterns
        cargo_patterns = [
            r'\d+\s*(?:mt|tons?|tonnes?)\s+.*?[.;]',
            r'cargo\s+.*?[.;]',
            r'quantity\s+.*?[.;]'
        ]
        
        # Port patterns
        port_patterns = [
            r'port\s+of\s+.*?[.;]',
            r'berth\s+.*?[.;]',
            r'terminal\s+.*?[.;]'
        ]
        
        # General terms patterns
        general_patterns = [
            r'force\s+majeure\s+.*?[.;]',
            r'arbitration\s+.*?[.;]',
            r'governing\s+law\s+.*?[.;]'
        ]
        
        # Apply patterns
        pattern_groups = [
            (payment_patterns, 'payment_terms'),
            (laytime_patterns, 'laytime_clauses'),
            (cargo_patterns, 'cargo_specifications'),
            (port_patterns, 'port_clauses'),
            (general_patterns, 'general_terms')
        ]
        
        for patterns, category in pattern_groups:
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                extracted[category].extend([match.strip() for match in matches])
        
        return extracted
    
    def analyze_contract_completeness(self, extracted_clauses: Dict[str, List[str]]) -> Dict[str, str]:
        """Analyze completeness of contract based on extracted clauses"""
        analysis = {}
        
        # Check for essential elements
        essential_elements = {
            'payment_terms': 'Payment and freight terms',
            'cargo_specifications': 'Cargo specifications',
            'port_clauses': 'Port and loading/discharging terms',
            'laytime_clauses': 'Laytime provisions'
        }
        
        for element, description in essential_elements.items():
            if extracted_clauses.get(element):
                analysis[element] = f"✓ {description} found"
            else:
                analysis[element] = f"⚠ {description} missing or unclear"
        
        return analysis
