"""
Visual Product Matcher - Main Flask Application
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import sys

# Add app directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models.feature_extractor import FeatureExtractor
from database.vector_store import VectorStore
from utils.image_processor import preprocess_image
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize models
feature_extractor = FeatureExtractor()
vector_store = VectorStore()

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """Handle image upload and return similar products"""
    try:
        # Check if file is present
        if 'file' not in request.files and 'image_url' not in request.form:
            return jsonify({'error': 'No image provided'}), 400
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_path = filepath
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        
        # Handle URL input
        elif 'image_url' in request.form:
            image_url = request.form['image_url']
            # For now, just use the URL directly in frontend
            image_path = image_url
        
        # Extract features
        image_tensor = preprocess_image(image_path)
        features = feature_extractor.extract_features(image_tensor)
        
        # Find similar products
        similar_products = vector_store.search_similar(features, top_k=10)
        
        # Get similarity threshold from request
        min_similarity = float(request.form.get('min_similarity', 0.7))
        
        # Filter by similarity score
        filtered_products = [
            p for p in similar_products 
            if p['similarity_score'] >= min_similarity
        ]
        
        return jsonify({
            'success': True,
            'uploaded_image': filename if 'file' in request.files else image_url,
            'results': filtered_products,
            'count': len(filtered_products)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products in database"""
    try:
        products = vector_store.get_all_products()
        return jsonify({'products': products})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
