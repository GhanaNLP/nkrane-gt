# nkrane_gt/language_codes.py
"""
Language code conversion utilities.
"""

LANGUAGE_CODE_MAPPING = {
    # ISO 639-3 to Google Translate (ISO 639-1)
    'eng': 'en',
    'spa': 'es',
    'fra': 'fr',
    'tha': 'th',  # Thai
    
    # Ghanaian languages
    'twi': 'ak',  # Akan/Twi (using 'ak' for Google)
    'aka': 'ak',  # Akan
    'gaa': 'gaa',  # Ga
    'ewe': 'ee',  # Ewe
    
    # Other African languages
    'hau': 'ha',  # Hausa
    'ibo': 'ig',  # Igbo
    'yor': 'yo',  # Yoruba
    'zul': 'zu',  # Zulu
    'swa': 'sw',  # Swahili
    'amh': 'am',  # Amharic
}

def convert_lang_code(lang_code: str, to_google: bool = True) -> str:
    """
    Convert between ISO 639-3 (3-letter) and Google Translate (2-letter) codes.
    
    Args:
        lang_code: Language code to convert
        to_google: If True, convert to Google format; if False, convert from Google format
        
    Returns:
        Converted language code
    """
    lang_code = lang_code.lower()
    
    if to_google:
        # Convert 3-letter to 2-letter
        if len(lang_code) == 2:
            return lang_code  # Already in Google format
        return LANGUAGE_CODE_MAPPING.get(lang_code, lang_code[:2] if len(lang_code) >= 2 else lang_code)
    else:
        # Convert 2-letter to 3-letter (reverse lookup)
        if len(lang_code) == 3:
            return lang_code  # Already in ISO 639-3 format
        
        # Reverse lookup
        for iso3, google in LANGUAGE_CODE_MAPPING.items():
            if google == lang_code:
                return iso3
        return lang_code + 'x'  # Default if not found

def is_google_supported(lang_code: str) -> bool:
    """
    Check if a language is likely supported by Google Translate.
    
    Args:
        lang_code: Language code to check
        
    Returns:
        True if likely supported, False otherwise
    """
    google_code = convert_lang_code(lang_code, to_google=True)
    
    # Common Google Translate supported languages including our target languages
    supported_codes = {
        'en', 'es', 'fr', 'de', 'zh', 'ja', 'ko', 'ru', 'ar', 'hi',
        'pt', 'it', 'nl', 'pl', 'sv', 'da', 'fi', 'el', 'cs', 'ro',
        'hu', 'sk', 'bg', 'sl', 'lt', 'lv', 'et', 'mt', 'th',
        
        # African languages
        'ak',  # Twi/Akan
        'gaa',  # Ga
        'ee',  # Ewe
        'ha', 'ig', 'yo', 'zu', 'sw', 'am'
    }
    
    return google_code in supported_codes
