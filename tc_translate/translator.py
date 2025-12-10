from googletrans import Translator as GoogleTranslator
from .terminology_manager import TerminologyManager
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TCTranslator:
    def __init__(self, domain: str, target_lang: str, 
                 src_lang: str = 'en', terminologies_dir: str = None):
        """
        Initialize Terminology-Controlled Translator.
        
        Args:
            domain: Domain name (e.g., 'agric', 'science')
            target_lang: Target language code (e.g., 'twi')
            src_lang: Source language code (default: 'en')
            terminologies_dir: Custom directory for terminology files
        """
        self.domain = domain
        self.target_lang = target_lang
        self.src_lang = src_lang
        
        # Initialize terminology manager
        self.terminology_manager = TerminologyManager(terminologies_dir)
        
        # Initialize Google Translate
        self.google_translator = GoogleTranslator()
        
        # Verify domain and language are available
        available = self.terminology_manager.get_available_domains_languages()
        if (domain, target_lang) not in available:
            raise ValueError(
                f"Domain '{domain}' with language '{target_lang}' not found. "
                f"Available: {available}"
            )
    
    def translate(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Translate text with terminology control.
        
        Args:
            text: Text to translate
            **kwargs: Additional arguments for Google Translate
            
        Returns:
            Dictionary with translation results
        """
        # Step 1: Preprocess - replace terms with IDs
        preprocessed_text, replacements = self.terminology_manager.preprocess_text(
            text, self.domain, self.target_lang
        )
        
        logger.info(f"Preprocessed text: {preprocessed_text}")
        logger.info(f"Replacements: {list(replacements.keys())}")
        
        # Step 2: Translate with Google Translate
        try:
            google_result = self.google_translator.translate(
                preprocessed_text,
                src=self.src_lang,
                dest=self.target_lang,
                **kwargs
            )
            
            translated_with_placeholders = google_result.text
            
            # Step 3: Postprocess - replace IDs with translations
            final_text = self.terminology_manager.postprocess_text(
                translated_with_placeholders,
                replacements
            )
            
            return {
                'text': final_text,
                'src': self.src_lang,
                'dest': self.target_lang,
                'domain': self.domain,
                'original': text,
                'preprocessed': preprocessed_text,
                'google_translation': google_result.text,
                'replacements_count': len(replacements)
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise
    
    def batch_translate(self, texts: list, **kwargs) -> list:
        """Translate multiple texts."""
        return [self.translate(text, **kwargs) for text in texts]

# Google Translate-like API wrapper
class Translator:
    """Google Translate-like API with terminology control."""
    
    def __init__(self, terminologies_dir: str = None):
        self.terminology_manager = TerminologyManager(terminologies_dir)
        self.google_translator = GoogleTranslator()
    
    def translate(self, text: str, src: str = 'en', dest: str = 'twi', 
                  domain: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """
        Translate text with optional terminology control.
        
        Args:
            text: Text to translate
            src: Source language
            dest: Destination language
            domain: Domain for terminology control (optional)
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with translation results
        """
        if domain:
            # Use terminology-controlled translation
            tc_translator = TCTranslator(
                domain=domain,
                target_lang=dest,
                src_lang=src,
                terminologies_dir=self.terminology_manager.terminologies_dir
            )
            return tc_translator.translate(text, **kwargs)
        else:
            # Use regular Google Translate
            result = self.google_translator.translate(text, src=src, dest=dest, **kwargs)
            return {
                'text': result.text,
                'src': src,
                'dest': dest,
                'original': text
            }
    
    def detect(self, text: str):
        """Detect language of text."""
        return self.google_translator.detect(text)
