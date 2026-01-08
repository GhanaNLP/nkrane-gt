import os
import pandas as pd
import re
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import json

from .language_codes import convert_lang_code, detect_lang_code_format, is_google_supported

@dataclass
class Term:
    id: int
    term: str
    translation: str
    google_lang_code: str  # Google-compatible language code

class TerminologyManager:
    def __init__(self, csv_path: str = None):
        """Initialize terminology manager with a single CSV file.
        
        Args:
            csv_path: Path to the terminology CSV file. 
                     Defaults to 'terminologies_{lang}.csv' in current directory.
                     If None, looks for terminologies_{lang}.csv in repo root.
        """
        self.csv_path = csv_path
        self.terms = {}  # Dictionary of terms for the language
        self.language = None
        self.google_lang_code = None
        self._load_terminologies()
    
    def _find_terminology_file(self) -> str:
        """Find the terminology CSV file."""
        if self.csv_path and os.path.exists(self.csv_path):
            return self.csv_path
            
        # Look for terminologies_*.csv in current directory
        current_dir = os.getcwd()
        for filename in os.listdir(current_dir):
            if filename.startswith('terminologies_') and filename.endswith('.csv'):
                return os.path.join(current_dir, filename)
        
        # Look in parent directory (in case we're in a subdirectory)
        parent_dir = os.path.dirname(current_dir)
        for filename in os.listdir(parent_dir):
            if filename.startswith('terminologies_') and filename.endswith('.csv'):
                return os.path.join(parent_dir, filename)
        
        raise FileNotFoundError(
            "No terminology CSV file found. Looking for 'terminologies_{lang}.csv' "
            f"in {current_dir} or {parent_dir}"
        )
    
    def _load_terminologies(self):
        """Load terminology from the CSV file."""
        csv_file = self._find_terminology_file()
        
        # Extract language from filename (terminologies_lang.csv)
        basename = os.path.basename(csv_file)
        language = basename.replace('terminologies_', '').replace('.csv', '')
        
        self.language = language
        self.google_lang_code = convert_lang_code(language, to_google=True)
        
        # Check if Google Translate supports this language
        if not is_google_supported(language):
            print(f"Warning: Language '{language}' may not be fully supported by Google Translate")
            print(f"  Using code: '{self.google_lang_code}' for Google Translate")
        
        # Load the CSV file
        df = pd.read_csv(csv_file)
        
        # Create terms dictionary
        self.terms = {}
        for _, row in df.iterrows():
            term_id = int(row['id'])
            term = Term(
                id=term_id,
                term=str(row['term']).lower().strip(),
                translation=str(row['translation']),
                google_lang_code=self.google_lang_code
            )
            self.terms[term.term] = term
    
    def get_google_lang_code(self, language: str = None) -> str:
        """Get Google-compatible language code."""
        if language and language != self.language:
            return convert_lang_code(language, to_google=True)
        return self.google_lang_code
    
    def preprocess_text(self, text: str) -> Tuple[str, Dict[str, Term]]:
        """Replace terms in text with their IDs.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (preprocessed_text, id_to_term_mapping)
        """
        if not self.terms:
            raise ValueError(f"No terminology loaded for language '{self.language}'")
        
        # Sort terms by length (longest first) to handle compound terms
        sorted_terms = sorted(self.terms.values(), key=lambda x: len(x.term), reverse=True)
        
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
