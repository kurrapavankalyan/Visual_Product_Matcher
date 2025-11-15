"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Flask configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Database settings
    FAISS_INDEX_PATH = 'data/embeddings/faiss_index.bin'
    PRODUCTS_JSON_PATH = 'app/database/products.json'
    
    # Model settings
    FEATURE_DIMENSION = 2048
    TOP_K_RESULTS = 10
    MIN_SIMILARITY_THRESHOLD = 0.7