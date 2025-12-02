import joblib
import pandas as pd

# Load trained model
model = joblib.load("health_model.pkl")  # replace with your saved file name

# Example input row (from your dataset)
input_data = {
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
# Convert to DataFrame (same format as training)
df_input = pd.DataFrame([input_data])

# Predict
prediction = model.predict(df_input)
print("Predicted Outcome:", prediction)
