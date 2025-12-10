#!/usr/bin/env python3
"""
API server example for TC Translator
"""

from flask import Flask, request, jsonify
from tc_translate import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate():
    """Translation endpoint with terminology control."""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
    
    text = data['text']
    src = data.get('src', 'en')
    dest = data.get('dest', 'twi')
    domain = data.get('domain')
    
    try:
        result = translator.translate(text, src=src, dest=dest, domain=domain)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/domains', methods=['GET'])
def list_domains():
    """List available domains and languages."""
    from tc_translate.utils import list_available_options
    options = list_available_options()
    return jsonify(options)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
