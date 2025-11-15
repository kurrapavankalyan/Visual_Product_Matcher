"""
Script to generate embeddings for product catalog
"""
import os
import sys
from tqdm import tqdm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.feature_extractor import FeatureExtractor
from app.database.vector_store import VectorStore
from app.utils.image_processor import preprocess_image

def generate_embeddings(images_dir='data/product_images'):
    """Generate embeddings for all product images"""
    print("Initializing feature extractor...")
    extractor = FeatureExtractor()
    
    print("Initializing vector store...")
    vector_store = VectorStore()
    
    print(f"Loading products from {images_dir}...")
    
    # Check if directory exists
    if not os.path.exists(images_dir):
        print(f"Directory {images_dir} does not exist. Creating...")
        os.makedirs(images_dir, exist_ok=True)
        print("Please add product images to this directory and run again.")
        return
    
    # Get all image files
    image_files = [
        f for f in os.listdir(images_dir) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
    ]
    
    if len(image_files) == 0:
        print("No images found in directory. Please add images first.")
        return
    
    print(f"Found {len(image_files)} images")
    
    # Process each image
    for idx, image_file in enumerate(tqdm(image_files, desc="Processing images")):
        try:
            image_path = os.path.join(images_dir, image_file)
            
            # Preprocess image
            image_tensor = preprocess_image(image_path)
            
            # Extract features
            features = extractor.extract_features(image_tensor)
            
            # Create metadata
            metadata = {
                'id': idx,
                'name': os.path.splitext(image_file)[0],
                'category': 'general',
                'image_path': f'{images_dir}/{image_file}',
                'price': 0.0,
                'description': f'Product {idx+1}'
            }
            
            # Add to vector store
            vector_store.add_product(features, metadata)
            
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
    
    print("\n✅ Embeddings generated successfully!")
    print(f"Total products in database: {len(vector_store.get_all_products())}")

if __name__ == '__main__':
    generate_embeddings()