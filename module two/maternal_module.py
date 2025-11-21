from flask import Blueprint, render_template, request, jsonify
import joblib, numpy as np
from llm_rules import get_llm_suggestion

maternal_bp = Blueprint("maternal", __name__)

MODEL_FILE = "health_model.pkl"
health_model = joblib.load(MODEL_FILE)

FEATURES = [
    "Blood Pressure (Sys)", "Blood Pressure (Dia)", "Pulse (HR)", "Temperature",
    "Cervical Dilation (cm)", "Uterine Contractions (/10min)", "Fetal Heart Rate (FHR)",
    "Station/Descent of Head", "Amniotic Fluid", "SpO₂", "Lochia", "Uterus Tone",
    "Urine Output (ml/hr)", "Hydration (ml/day)", "Pain Level (0-10)",
    "Breast Engorgement (0-10)", "Fatigue Level (0-10)", "Mood (0=happy,10=depressed)",
    "Bowel/Urinary Issues (0-10)"
]

@maternal_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html", feature_names=FEATURES)

@maternal_bp.route("/predict", methods=["POST"])
def predict():
    values = []
    for k in FEATURES:
        try:
            values.append(float(request.form.get(k, 0)))
        except:
            values.append(0.0)
    X = np.array([values])
    pred_raw = health_model.predict(X)[0]
    pred_label = {0: "Stable", 1: "Moderate", 2: "Critical"}.get(pred_raw, "Unknown")

    cond_text = ", ".join([f"{n}:{v}" for n, v in zip(FEATURES, values)])
    summary, future, basic, advanced = get_llm_suggestion(cond_text)

    return jsonify({
        "prediction": pred_label,
        "summary": summary,
        "future": future,
        "basic": basic,
        "advanced": advanced
    })
