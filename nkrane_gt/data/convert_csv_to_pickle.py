# nkrane_gt/data/convert_csv_to_pickle.py
"""
Script to convert CSV terminology files to pickle dictionary files.
Usage: python convert_csv_to_pickle.py <csv_file> <language_code>
python3 convert_csv_to_pickle.py nouns_ak.csv ak
"""

import csv
import pickle
import sys
import os

def convert_csv_to_pickle(csv_file_path, language_code):
    """
    Convert a CSV file to a pickle dictionary file.
    
    Args:
        csv_file_path: Path to CSV file
        language_code: Language code (ak, ee, gaa)
    """
    if language_code not in ['ak', 'ee', 'gaa']:
        raise ValueError("Language code must be 'ak', 'ee', or 'gaa'")
    
    # Read CSV and build dictionary
    nouns_dict = {}
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        # Try to detect the delimiter
        sample = csvfile.read(1024)
        csvfile.seek(0)
        
        # Check for common delimiters
        if ',' in sample:
            delimiter = ','
        elif ';' in sample:
            delimiter = ';'
        elif '\t' in sample:
            delimiter = '\t'
        else:
            delimiter = ','  # default
        
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        fieldnames = [f.lower() for f in reader.fieldnames] if reader.fieldnames else []
        
        # Determine which columns to use
        text_col = None
        trans_col = None
        
        # Look for text column
        for col in ['text', 'english', 'source', 'term', 'word']:
            if col in fieldnames:
                text_col = col
                break
        
        # Look for translation column
        for col in ['text_translated', 'translation', 'target', 'translated']:
            if col in fieldnames:
                trans_col = col
                break
        
        # If not found, use first two columns
        if not text_col or not trans_col:
            if len(fieldnames) >= 2:
                text_col = reader.fieldnames[0]
                trans_col = reader.fieldnames[1]
            else:
                print(f"Error: CSV needs at least 2 columns")
                return
        
        # Process rows
        for row in reader:
            english_term = row.get(text_col, '').strip().lower()
            translation = row.get(trans_col, '').strip()
            
            if english_term and translation:
                nouns_dict[english_term] = translation
    
    # Determine output file name
    output_file = os.path.join(os.path.dirname(__file__), f'nouns_{language_code}.pkl')
    
    # Save as pickle
    with open(output_file, 'wb') as pklfile:
        pickle.dump(nouns_dict, pklfile)
    
    print(f"Converted {len(nouns_dict)} terms to {output_file}")
    print(f"Dictionary format: {{'english_term': 'translation'}}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert_csv_to_pickle.py <csv_file> <language_code>")
        print("Language codes: ak (Twi), ee (Ewe), gaa (Ga)")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    lang_code = sys.argv[2]
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found")
        sys.exit(1)
    
    try:
        convert_csv_to_pickle(csv_file, lang_code)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
