"""
Flask Backend for Image Captioning Application
Handles image uploads and caption generation
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from PIL import Image
import io
import os
import logging
from model_loader import generate_caption, generate_detailed_caption

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Handle image upload and generate caption
    
    Expected: multipart/form-data with 'image' file
    Returns: JSON with caption or error message
    """
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Read and validate image
        try:
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
                
        except Exception as e:
            logger.error(f"Error reading image: {str(e)}")
            return jsonify({'error': 'Invalid or corrupted image file'}), 400
        
        # Get caption type from request (default or detailed)
        caption_type = request.form.get('type', 'default')
        
        # Generate caption
        try:
            if caption_type == 'detailed':
                caption = generate_detailed_caption(image)
            else:
                caption = generate_caption(image)
                
            logger.info(f"Successfully generated caption for {file.filename}")
            
            return jsonify({
                'success': True,
                'caption': caption,
                'filename': file.filename
            }), 200
            
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            return jsonify({'error': 'Failed to generate caption. Please try again.'}), 500
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Image Captioning API'}), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    logger.info("Starting Image Captioning Server...")
    logger.info("Server will be available at http://localhost:5000")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
