import os
import pandas as pd
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import json

@dataclass
class Term:
    id: int
    term: str
    translation: str
    domain: str
    language: str

class TerminologyManager:
    def __init__(self, terminologies_dir: str = None):
        """Initialize terminology manager.
        
        Args:
            terminologies_dir: Directory containing terminology CSV files.
                               Defaults to package's terminologies directory.
        """
        if terminologies_dir is None:
            # Default to package directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.terminologies_dir = os.path.join(current_dir, 'terminologies')
        else:
            self.terminologies_dir = terminologies_dir
            
        self.terms_by_domain_lang = defaultdict(dict)
        self.domains_languages = set()
        self._load_terminologies()
    
    def _load_terminologies(self):
        """Load all terminology files from the terminologies directory."""
        if not os.path.exists(self.terminologies_dir):
            raise FileNotFoundError(
                f"Terminologies directory not found: {self.terminologies_dir}"
            )
        
        # Pattern for terminology files: {domain}_terms_{language}.csv
        pattern = re.compile(r'(.+)_terms_(.+)\.csv$')
        
        for filename in os.listdir(self.terminologies_dir):
            match = pattern.match(filename)
            if match:
                domain, language = match.groups()
                self.domains_languages.add((domain, language))
                
                filepath = os.path.join(self.terminologies_dir, filename)
                df = pd.read_csv(filepath)
                
                # Create a dictionary of terms for quick lookup
                terms_dict = {}
                for _, row in df.iterrows():
                    term_id = int(row['id'])
                    term = Term(
                        id=term_id,
                        term=str(row['term']).lower().strip(),
                        translation=str(row['translation']),
                        domain=domain,
                        language=language
                    )
                    terms_dict[term.term] = term
                
                self.terms_by_domain_lang[(domain, language)] = terms_dict
    
    def get_available_domains_languages(self) -> List[Tuple[str, str]]:
        """Get list of available (domain, language) pairs."""
        return sorted(self.domains_languages)
    
    def get_domains(self) -> List[str]:
        """Get list of available domains."""
        return sorted({d for d, _ in self.domains_languages})
    
    def get_languages(self) -> List[str]:
        """Get list of available languages."""
        return sorted({l for _, l in self.domains_languages})
    
    def get_terms_for_domain_lang(self, domain: str, language: str) -> Dict[str, Term]:
        """Get all terms for a specific domain and language."""
        return self.terms_by_domain_lang.get((domain, language), {})
    
    def preprocess_text(self, text: str, domain: str, language: str) -> Tuple[str, Dict[str, Term]]:
        """Replace terms in text with their IDs.
        
        Args:
            text: Input text
            domain: Domain name
            language: Target language
            
        Returns:
            Tuple of (preprocessed_text, id_to_term_mapping)
        """
        terms_dict = self.get_terms_for_domain_lang(domain, language)
        if not terms_dict:
            raise ValueError(f"No terminology found for domain '{domain}' and language '{language}'")
        
        # Sort terms by length (longest first) to handle compound terms
        sorted_terms = sorted(terms_dict.values(), key=lambda x: len(x.term), reverse=True)
        
        preprocessed_text = text
        replacements = {}  # Map of placeholder to term
        
        for term_obj in sorted_terms:
            # Case-insensitive replacement with word boundaries
            pattern = re.compile(r'\b' + re.escape(term_obj.term) + r'\b', re.IGNORECASE)
            
            def replace_with_placeholder(match):
                placeholder = f"<{term_obj.id}>"
                replacements[placeholder] = term_obj
                return placeholder
            
            preprocessed_text = pattern.sub(replace_with_placeholder, preprocessed_text)
        
        return preprocessed_text, replacements
    
    def postprocess_text(self, text: str, replacements: Dict[str, Term]) -> str:
        """Replace IDs in translated text with their translations.
        
        Args:
            text: Translated text with placeholders
            replacements: Mapping from placeholders to Term objects
            
        Returns:
            Postprocessed text with actual translations
        """
        for placeholder, term_obj in replacements.items():
            text = text.replace(placeholder, term_obj.translation)
        return text
    
    def add_terminology(self, domain: str, language: str, terms_data: List[Dict]):
        """Add new terminology programmatically.
        
        Args:
            domain: Domain name
            language: Target language
            terms_data: List of dictionaries with 'term' and 'translation' keys
        """
        key = (domain, language)
        if key not in self.terms_by_domain_lang:
            self.terms_by_domain_lang[key] = {}
            self.domains_languages.add(key)
        
        current_max_id = max(
            [t.id for t in self.terms_by_domain_lang[key].values()] or [0]
        )
        
        for i, term_data in enumerate(terms_data, start=1):
            term_id = current_max_id + i
            term_obj = Term(
                id=term_id,
                term=term_data['term'].lower().strip(),
                translation=term_data['translation'],
                domain=domain,
                language=language
            )
            self.terms_by_domain_lang[key][term_obj.term] = term_obj
