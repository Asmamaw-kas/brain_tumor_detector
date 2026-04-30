import tensorflow as tf
import numpy as np
import os

class BrainTumorModel:
    def __init__(self, model_path):
        """Load the trained model"""
        self.model = tf.keras.models.load_model(model_path)
        self.class_names = ['No Tumor', 'Tumor Detected']
        
    def predict(self, processed_image):
        """
        Make prediction and return results with reasoning
        """
        # Get prediction
        predictions = self.model.predict(processed_image, verbose=0)
        probability = float(predictions[0][0])
        
        # Determine class and confidence
        if probability > 0.5:
            predicted_class = self.class_names[1]  # Tumor Detected
            confidence = probability * 100
        else:
            predicted_class = self.class_names[0]  # No Tumor
            confidence = (1 - probability) * 100
        
        # Generate reasoning based on confidence level
        confidence = round(confidence, 2)
        
        if confidence >= 90:
            confidence_level = "Very High"
            reasoning = f"The model is very confident ({confidence}%) in this prediction. The image shows clear patterns consistent with {predicted_class.lower()}."
        elif confidence >= 70:
            confidence_level = "High"
            reasoning = f"The model shows high confidence ({confidence}%) in this prediction. The image patterns strongly indicate {predicted_class.lower()}."
        elif confidence >= 50:
            confidence_level = "Moderate"
            reasoning = f"The model has moderate confidence ({confidence}%) in this prediction. While patterns suggest {predicted_class.lower()}, clinical correlation is recommended."
        else:
            confidence_level = "Low"
            reasoning = f"The model has low confidence ({confidence}%) in this prediction. The image patterns are unclear, and further investigation is strongly recommended."
        
        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "confidence_level": confidence_level,
            "reasoning": reasoning,
            "raw_probability": probability
        }

# Initialize model
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "brain_tumor_model.h5")
model = BrainTumorModel(MODEL_PATH)