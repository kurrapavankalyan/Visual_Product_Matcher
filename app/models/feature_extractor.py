"""
Feature Extractor using ResNet50 pre-trained model
"""
import torch
import torch.nn as nn
import numpy as np
from torchvision import models
from torchvision.models import ResNet50_Weights

class FeatureExtractor:
    def __init__(self):
        """Initialize ResNet50 model without final classification layer"""
        # Load pre-trained ResNet50
        self.model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        
        # Remove the final fully connected layer
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        
        # Set to evaluation mode
        self.model.eval()
        
        # Use GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
    
    def extract_features(self, image_tensor):
        """
        Extract feature vector from image tensor
        
        Args:
            image_tensor: Preprocessed image tensor (1, 3, 224, 224)
        
        Returns:
            Feature vector as numpy array (2048,)
        """
        with torch.no_grad():
            image_tensor = image_tensor.to(self.device)
            features = self.model(image_tensor)
            
            # Flatten the features
            features = features.squeeze().cpu().numpy()
            
            # Normalize features (L2 normalization)
            norm = np.linalg.norm(features)
            features = features / (norm + 1e-8)
            
        return features
    
    def batch_extract_features(self, image_tensors):
        """
        Extract features from batch of images
        
        Args:
            image_tensors: Batch of preprocessed image tensors
        
        Returns:
            Array of feature vectors
        """
        with torch.no_grad():
            image_tensors = image_tensors.to(self.device)
            features = self.model(image_tensors)
            
            # Flatten and normalize
            features = features.squeeze().cpu().numpy()
            
            if len(features.shape) == 1:
                features = features.reshape(1, -1)
            
            # L2 normalization
            norms = np.linalg.norm(features, axis=1, keepdims=True)
            features = features / (norms + 1e-8)
            
        return features
