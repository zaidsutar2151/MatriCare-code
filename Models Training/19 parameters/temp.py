# Multiple test cases for manual evaluation

input_stable = {
    "Blood Pressure (Sys)": 115,   # within 110–130
    "Blood Pressure (Dia)": 75,    # within 70–85
    "Pulse (HR)": 85,              # within 60–100
    "Temperature": 36.8,           # normal 36.5–37.5
    "Cervical Dilation (cm)": 5,
    "Uterine Contractions (/10min)": 4,
    "Fetal Heart Rate (FHR)": 140, # normal 110–160
    "Station/Descent of Head": 2,
    "Amniotic Fluid": 12,
    "SpO2": 98,                    # >95 good
    "Lochia": 1,
    "Uterus Tone": 2,
    "Urine Output (ml/hr)": 60,    # >30 normal
    "Hydration (ml/day)": 2500,
    "Pain Level (0-10)": 2,
    "Breast Engorgement (0-10)": 3,
    "Fatigue Level (0-10)": 2,
    "Mood (0=happy,10=depressed)": 2,
    "Bowel/Urinary Issues (0-10)": 1
}

input_critical = {
    "Blood Pressure (Sys)": 170,   # very high
    "Blood Pressure (Dia)": 110,   # very high
    "Pulse (HR)": 130,             # tachycardia
    "Temperature": 39.5,           # fever
    "Cervical Dilation (cm)": 1,   # no progress
    "Uterine Contractions (/10min)": 0, # absent
    "Fetal Heart Rate (FHR)": 90,  # fetal distress (<110)
    "Station/Descent of Head": -3,
    "Amniotic Fluid": 5,           # low
    "SpO2": 85,                    # hypoxia
    "Lochia": 4,                   # heavy
    "Uterus Tone": 0,              # atonic
    "Urine Output (ml/hr)": 10,    # very low
    "Hydration (ml/day)": 1200,
    "Pain Level (0-10)": 9,
    "Breast Engorgement (0-10)": 8,
    "Fatigue Level (0-10)": 10,
    "Mood (0=happy,10=depressed)": 9,
    "Bowel/Urinary Issues (0-10)": 7
}

input_moderate = {
    "Blood Pressure (Sys)": 135,   # slightly high
    "Blood Pressure (Dia)": 88,    # borderline high
    "Pulse (HR)": 105,             # mild tachycardia
    "Temperature": 37.8,           # low-grade fever
    "Cervical Dilation (cm)": 6,   # progressing
    "Uterine Contractions (/10min)": 5,
    "Fetal Heart Rate (FHR)": 165, # borderline high
    "Station/Descent of Head": 0,
    "Amniotic Fluid": 8,
    "SpO2": 92,                    # borderline hypoxia
    "Lochia": 2,
    "Uterus Tone": 1,
    "Urine Output (ml/hr)": 25,    # low
    "Hydration (ml/day)": 1800,
    "Pain Level (0-10)": 6,
    "Breast Engorgement (0-10)": 5,
    "Fatigue Level (0-10)": 6,
    "Mood (0=happy,10=depressed)": 5,
    "Bowel/Urinary Issues (0-10)": 3
}


# Collect them for evaluation
test_cases = [input_stable, input_critical, input_moderate]

# Convert to DataFrame for prediction
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("maternal_health_model.pkl")

for i, case in enumerate(test_cases, 1):
    df = pd.DataFrame([case])
    prediction = model.predict(df)[0]
    print(f"Case {i} Prediction: {prediction}")
