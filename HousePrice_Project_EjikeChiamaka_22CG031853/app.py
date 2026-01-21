import os
import flask
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Get port from environment variable (for deployment)
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("FLASK_ENV", "production") == "development"

# Load model, scaler, and feature list
MODEL_PATH = os.path.join('model', 'house_price_model.pkl')
SCALER_PATH = os.path.join('model', 'scaler.pkl')
FEATURES_PATH = os.path.join('model', 'selected_features.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    selected_features = joblib.load(FEATURES_PATH)
    model_loaded = True
except Exception as e:
    print(f"Error loading model artifacts: {str(e)}")
    model_loaded = False
    model = None
    scaler = None
    selected_features = None


@app.route('/')
def home():
    """Render the home page with prediction form"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for deployment monitoring"""
    return jsonify({
        'status': 'OK',
        'model_loaded': model_loaded,
        'features': selected_features if selected_features else []
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict house price from user input.
    
    CRITICAL: Using correct inference logic:
    - predict() returns the predicted value directly (for regression)
    - We do NOT use argmax or max on a single value
    """
    try:
        if not model_loaded:
            return jsonify({
                'error': 'Model not loaded. Please ensure model artifacts are present.',
                'success': False
            }), 500

        # Get JSON data from request
        data = request.get_json()

        # Validate input has all required features
        missing_features = [f for f in selected_features if f not in data]
        if missing_features:
            return jsonify({
                'error': f'Missing features: {", ".join(missing_features)}',
                'success': False
            }), 400

        # Extract features in the correct order
        input_values = [float(data[feature]) for feature in selected_features]

        # Create DataFrame to maintain feature names and order
        input_df = pd.DataFrame([input_values], columns=selected_features)

        # Scale the input using the saved scaler
        input_scaled = scaler.transform(input_df)

        # CORRECT inference logic for regression:
        # predict() returns the predicted value directly
        predicted_price = float(model.predict(input_scaled)[0])

        # For regression, we can provide prediction intervals or confidence
        # Get predictions from trees to calculate std deviation
        predictions_individual = np.array([
            tree.predict(input_scaled)[0] for tree in model.estimators_
        ])
        confidence = float(np.std(predictions_individual))

        return jsonify({
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'confidence_std': round(confidence, 2),
            'features_used': selected_features,
            'input_values': {selected_features[i]: input_values[i] for i in range(len(selected_features))}
        }), 200

    except ValueError as e:
        return jsonify({
            'error': f'Invalid input values: {str(e)}',
            'success': False
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}',
            'success': False
        }), 500


@app.route('/features', methods=['GET'])
def get_features():
    """Get the list of features used by the model"""
    if model_loaded:
        return jsonify({
            'success': True,
            'features': selected_features
        }), 200
    else:
        return jsonify({
            'success': False,
            'error': 'Model not loaded'
        }), 500


if __name__ == '__main__':
    # Use environment variables for production-safe deployment
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )
