"""
Image preprocessing utilities
"""
from PIL import Image
import torch
from torchvision import transforms
import requests
from io import BytesIO

def preprocess_image(image_path):
    """
    Preprocess image for ResNet50 model
    
    Args:
        image_path: Path to image file or PIL Image object
    
    Returns:
        Preprocessed image tensor (1, 3, 224, 224)
    """
    # Define preprocessing transforms
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    # Load image
    if isinstance(image_path, str):
        image = Image.open(image_path).convert('RGB')
    else:
        image = image_path.convert('RGB')
    
    # Apply transforms
    image_tensor = transform(image)
    
    # Add batch dimension
    image_tensor = image_tensor.unsqueeze(0)
    
    return image_tensor

def load_image_from_url(url):
    """
    Load image from URL
    
    Args:
        url: Image URL
    
    Returns:
        PIL Image object
    """
    response = requests.get(url, timeout=10)
    image = Image.open(BytesIO(response.content))
    return image

def validate_image(image_path):
    """
    Validate if file is a valid image
    
    Args:
        image_path: Path to image file
    
    Returns:
        True if valid, False otherwise
    """
    try:
        img = Image.open(image_path)
        img.verify()
        return True
    except:
        return False