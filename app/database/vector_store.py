"""
Vector Store using FAISS for efficient similarity search
"""
import faiss
import numpy as np
import json
import pickle
import os

class VectorStore:
    def __init__(self, dimension=2048, index_path='data/embeddings/faiss_index.bin', 
                 metadata_path='data/products.json'):



        """
        Initialize FAISS vector store
        
        Args:
            dimension: Dimension of feature vectors (ResNet50 = 2048)
            index_path: Path to save/load FAISS index
            metadata_path: Path to product metadata JSON
        """
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = metadata_path
        
        # Initialize or load FAISS index
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        else:
            # Create new index (L2 distance)
            self.index = faiss.IndexFlatL2(dimension)
        
        # Load product metadata
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.products = json.load(f)
        else:
            self.products = []
    
    def add_product(self, features, metadata):
        """
        Add product to vector store
        
        Args:
            features: Feature vector (numpy array)
            metadata: Product metadata (dict)
        """
        # Add to FAISS index
        features = np.array([features]).astype('float32')
        self.index.add(features)
        
        # Add metadata
        self.products.append(metadata)
        
        # Save
        self.save()
    
    def search_similar(self, query_features, top_k=10):
        """
        Search for similar products
        
        Args:
            query_features: Query feature vector
            top_k: Number of results to return
        
        Returns:
            List of similar products with similarity scores
        """
        # Convert to proper format
        query_features = np.array([query_features]).astype('float32')
        
        # Search
        distances, indices = self.index.search(query_features, top_k)
        
        # Convert distances to similarity scores (cosine similarity)
        # Since we use L2 normalized features, L2 distance can be converted
        similarities = 1 / (1 + distances[0])
        
        # Prepare results
        results = []
        for idx, (index, similarity) in enumerate(zip(indices[0], similarities)):
            if index < len(self.products):
                product = self.products[index].copy()
                product['similarity_score'] = float(similarity)
                product['rank'] = idx + 1
                results.append(product)
        
        return results
    
    def get_all_products(self):
        """Get all products in database"""
        return self.products
    
    def save(self):
        """Save index and metadata"""
        # Create directory if not exists
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.metadata_path), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, self.index_path)
        
        # Save metadata
        with open(self.metadata_path, 'w') as f:
            json.dump(self.products, f, indent=2)
    
    def load(self):
        """Load index and metadata"""
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                self.products = json.load(f)
