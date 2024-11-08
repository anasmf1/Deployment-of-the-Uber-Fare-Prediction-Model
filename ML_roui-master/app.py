from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import logging


app = Flask(__name__)
app.debug = True
# Load the scaler and model
# Load the model and scaler
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/prediction')
def predict_page():
    return render_template('prediction.html')
# Route pour effectuer la prédiction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve data from JSON request
        data = request.json
        features = [
            int(data.get('passenger_count', 0)),
            int(data.get('year', 0)),
            int(data.get('month', 0)),
            int(data.get('day', 0)),
            int(data.get('hour', 0)),
            float(data.get('distance', 0.0))
        ]

        # Convert features to a DataFrame
        features_df = pd.DataFrame([features], columns=['passenger_count', 'year', 'month', 'day', 'hour', 'distance'])

        # Standardize the data
        features_scaled = scaler.transform(features_df)

        # Make prediction
        prediction = model.predict(features_scaled)
        fare = round(prediction[0], 2)

        # Log prediction if in debug mode
        if app.debug:
            logging.debug(f"Predicted fare: {fare}")

        # Return prediction as JSON response
        return jsonify({'prediction': fare})

    except Exception as e:
        # Log the error if in debug mode
        if app.debug:
            logging.error(f"Error during prediction: {e}")

        # Return a JSON response with an error message
        return jsonify({'error': str(e)}), 500

@app.route('/status')
def status_page():
    return render_template('status.html')
@app.route('/status', methods=['POST'])  # Changer GET à POST
def tester():
    return jsonify({'status': ' All systems are operational. '})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)