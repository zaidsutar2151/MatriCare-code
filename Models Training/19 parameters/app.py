from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# --- Sample preset datasets ---
PRESET_DATA = {
    "stable": {
        "Blood Pressure (Sys)": 115,
        "Blood Pressure (Dia)": 75,
        "Pulse (HR)": 85,
        "Temperature": 36.8,
        "Cervical Dilation (cm)": 5,
        "Uterine Contractions (/10min)": 4,
        "Fetal Heart Rate (FHR)": 140,
        "Station/Descent of Head": 2,
        "Amniotic Fluid": 12,
        "SpO2": 98,
        "Lochia": 1,
        "Uterus Tone": 2,
        "Urine Output (ml/hr)": 60,
        "Hydration (ml/day)": 2500,
        "Pain Level (0-10)": 2,
        "Breast Engorgement (0-10)": 3,
        "Fatigue Level (0-10)": 2,
        "Mood (0=happy,10=depressed)": 2,
        "Bowel/Urinary Issues (0-10)": 1
    },
    "moderate": {
        "Blood Pressure (Sys)": 135,
        "Blood Pressure (Dia)": 88,
        "Pulse (HR)": 105,
        "Temperature": 37.8,
        "Cervical Dilation (cm)": 6,
        "Uterine Contractions (/10min)": 5,
        "Fetal Heart Rate (FHR)": 165,
        "Station/Descent of Head": 0,
        "Amniotic Fluid": 8,
        "SpO2": 92,
        "Lochia": 2,
        "Uterus Tone": 1,
        "Urine Output (ml/hr)": 25,
        "Hydration (ml/day)": 1800,
        "Pain Level (0-10)": 6,
        "Breast Engorgement (0-10)": 5,
        "Fatigue Level (0-10)": 6,
        "Mood (0=happy,10=depressed)": 5,
        "Bowel/Urinary Issues (0-10)": 3
    },
    "critical": {
        "Blood Pressure (Sys)": 170,
        "Blood Pressure (Dia)": 110,
        "Pulse (HR)": 130,
        "Temperature": 39.5,
        "Cervical Dilation (cm)": 1,
        "Uterine Contractions (/10min)": 0,
        "Fetal Heart Rate (FHR)": 90,
        "Station/Descent of Head": 3,
        "Amniotic Fluid": 5,
        "SpO2": 85,
        "Lochia": 1000,
        "Uterus Tone": 0,
        "Urine Output (ml/hr)": 10,
        "Hydration (ml/day)": 1200,
        "Pain Level (0-10)": 9,
        "Breast Engorgement (0-10)": 8,
        "Fatigue Level (0-10)": 10,
        "Mood (0=happy,10=depressed)": 9,
        "Bowel/Urinary Issues (0-10)": 7
    }
}

# Load model
with open("health_model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        # Collect all inputs
        sample_input = { 
            "Blood Pressure (Sys)": float(request.form['bp_sys']),
            "Blood Pressure (Dia)": float(request.form['bp_dia']),
            "Pulse (HR)": float(request.form['pulse']),
            "Temperature": float(request.form['temperature']),
            "Cervical Dilation (cm)": float(request.form['cervical_dilation']),
            "Uterine Contractions (/10min)": float(request.form['contractions']),
            "Fetal Heart Rate (FHR)": float(request.form['fhr']),
            "Station/Descent of Head": float(request.form['station']),
            "Amniotic Fluid": float(request.form['amniotic_fluid']),
            "SpO2": float(request.form['spo2']),
            "Lochia": float(request.form['lochia']),
            "Uterus Tone": float(request.form['uterus_tone']),
            "Urine Output (ml/hr)": float(request.form['urine_output']),
            "Hydration (ml/day)": float(request.form['hydration']),
            "Pain Level (0-10)": float(request.form['pain']),
            "Breast Engorgement (0-10)": float(request.form['engorgement']),
            "Fatigue Level (0-10)": float(request.form['fatigue']),
            "Mood (0=happy,10=depressed)": float(request.form['mood']),
            "Bowel/Urinary Issues (0-10)": float(request.form['bowel'])
        }
        
        df_input = pd.DataFrame([sample_input])
        pred_num = model.predict(df_input)[0]
        label_map = {0: "Stable", 1: "Moderate", 2: "Critical"}
        prediction = label_map.get(pred_num, "Unknown")
    
    return render_template('index.html', prediction=prediction)

@app.route('/get_preset/<preset_id>')
def get_preset(preset_id):
    return jsonify(PRESET_DATA.get(preset_id, {}))

if __name__ == '__main__':
    app.run(debug=True)
