from flask import Flask, request, jsonify, render_template
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Use relative path for model
MODEL_PATH = os.path.join('model', 'concrete_strength_model_kfold.h5')

# Load the trained model with explicit error handling
try:
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Attempting to load model from: {MODEL_PATH}")
    
    if not os.path.exists(MODEL_PATH):
        logger.error(f"Model file not found at: {MODEL_PATH}")
        model = None
    else:
        # Load model with custom objects
        custom_objects = {
            'MeanSquaredError': MeanSquaredError,
            'MeanAbsoluteError': MeanAbsoluteError
        }
        model = load_model(MODEL_PATH, custom_objects=custom_objects)
        logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    model = None

# Initialize feature names
feature_names = [
    "Cement", "BlastFurnaceSlag", "FlyAsh", "Water", "Superplasticizer",
    "CoarseAggregate", "FineAggregate", "Age"
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        logger.error("Model not loaded - cannot make prediction")
        return jsonify({
            'error': 'Model not loaded. Please check if model file exists in the model directory.',
            'status': 'error'
        }), 503

    try:
        # Get values from the form with type checking
        features = []
        for feature in feature_names:
            try:
                value = float(request.form.get(feature, 0))
                if value < 0:
                    raise ValueError(f"Negative value not allowed for {feature}")
                features.append(value)
            except ValueError as e:
                logger.error(f"Invalid input: {str(e)}")
                return jsonify({
                    'error': f"Invalid value for {feature}: {str(e)}",
                    'status': 'error'
                })
        
        # Convert to numpy array and reshape
        features_array = np.array(features).reshape(1, -1)
        
        # Create a scaler instance with predefined parameters
        scaler = StandardScaler()
        scaler.mean_ = np.array([300, 100, 50, 175, 5, 1000, 800, 28])
        scaler.scale_ = np.array([100, 50, 25, 25, 2, 200, 150, 14])
        
        # Transform the features
        features_scaled = scaler.transform(features_array)
        
        # Make prediction
        logger.debug(f"Making prediction with features: {features}")
        prediction = model.predict(features_scaled, verbose=0)
        logger.debug(f"Prediction result: {prediction}")
        
        return jsonify({
            'prediction': float(prediction[0][0]),
            'status': 'success'
        })

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': f'Error making prediction: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    # Log startup information
    logger.info(f"Starting server...")
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Model loaded: {model is not None}")
    
    app.run(debug=True)