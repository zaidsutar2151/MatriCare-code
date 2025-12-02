from flask import Flask, render_template, jsonify
import joblib
import numpy as np
import random

app = Flask(__name__)

# Load model
rf_model = joblib.load("8 para model.pkl")

# Parameter list
feature_names = ["SysBP", "DiaBP", "HR", "Temp", "SpO2", "RR", "FHR", "Toco"]

# Realistic physiological parameter ranges
param_ranges = {
    "SysBP": (80, 160),
    "DiaBP": (50, 100),
    "HR": (50, 140),
    "Temp": (36, 40),
    "SpO2": (85, 100),
    "RR": (10, 35),
    "FHR": (90, 180),
    "Toco": (10, 80)
}

# Map model numeric output to descriptive label and color
status_map = {
    0: ("Stable", "#28a745"),
    1: ("Moderate", "#ffc107"),
    2: ("Critical", "#dc3545")
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', feature_names=feature_names)

@app.route('/predict')
def predict():
    # Random sample generation
    features = [round(random.uniform(*param_ranges[f]), 2) for f in feature_names]
    input_data = np.array([features])

    # Predict
    prediction_raw = rf_model.predict(input_data)[0]
    label, color = status_map.get(prediction_raw, ("Unknown", "#6c757d"))

    return jsonify({
        "features": dict(zip(feature_names, features)),
        "prediction": label,
        "color": color
    })

if __name__ == '__main__':
    app.run(debug=True)
