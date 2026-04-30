import numpy as np
from PIL import Image
import io
import cv2

def preprocess_image(image_bytes, target_size=(128, 128)):
    """
    Preprocess the uploaded image for model prediction
    """
    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB (model expects 3 channels)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize to target size using high-quality resampling
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Normalize to [0, 1]
    img_array = img_array / 255.0
    
    # Add batch dimension (batch_size, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array