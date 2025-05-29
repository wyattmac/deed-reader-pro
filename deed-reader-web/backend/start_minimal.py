#!/usr/bin/env python3
"""
Minimal Flask app to test without all dependencies
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import PyPDF2

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Minimal backend running',
        'claude': 'not initialized'
    })

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Try to extract text
        text = ""
        if filename.lower().endswith('.pdf'):
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        
        if not text.strip():
            text = "This appears to be a scanned PDF. OCR functionality would extract the text here."
        
        return jsonify({
            'success': True,
            'filename': filename,
            'file_type': 'pdf',
            'text_length': len(text),
            'extracted_text': text,
            'upload_id': filename.replace('.', '_'),
            'message': 'Document uploaded (minimal processing)'
        })
        
    except Exception as e:
        return jsonify({'error': 'Upload failed', 'message': str(e)}), 500

if __name__ == '__main__':
    print("Starting minimal Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)