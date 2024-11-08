import joblib
import pandas as pd

# Load the saved model and scaler
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# Define a sample input for testing
sample_data = {
    'passenger_count': 2,
    'year': 2023,
    'month': 11,
    'day': 8,
    'hour': 15,
    'distance': 5.7
}

# Convert sample input into a DataFrame for compatibility
features = [
    sample_data['passenger_count'],
    sample_data['year'],
    sample_data['month'],
    sample_data['day'],
    sample_data['hour'],
    sample_data['distance']
]
features_df = pd.DataFrame([features], columns=['passenger_count', 'year', 'month', 'day', 'hour', 'distance'])

# Scale the features using the loaded scaler
features_scaled = scaler.transform(features_df)

# Make a prediction
prediction = model.predict(features_scaled)
fare = round(prediction[0], 2)

print(f"Predicted Fare: {fare}")
