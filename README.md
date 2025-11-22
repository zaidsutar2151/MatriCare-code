MatriCare AI — Intelligent Maternal Health Monitoring System

MatriCare AI is an advanced maternal healthcare support system that integrates machine learning, real-time monitoring, and LLM-based clinical reasoning to predict pregnancy-related complications and assist healthcare workers during labor and postpartum care.

This system bridges the gap in continuous maternal monitoring, especially in low-resource settings, by providing automated risk prediction and intelligent medical suggestions based on physiological data.

🚀 Features
🔹 1. Continuous Maternal Monitoring (Automated Module)

Tracks 8 real-time physiological parameters

Processes incoming sensor data instantly

Uses a trained Random Forest model for live prediction

Categorizes patients into:

Stable

Moderate

Critical

🔹 2. LLM-Based Clinical Decision Support (Advanced Module)

Accepts 19 maternal health parameters manually

Matches medical rules from dataset (final data.xlsx)

Uses vector embeddings + LLM (via LlamaIndex) to:

Predict future complications

Suggest Basic Actions (Nurse-level)

Suggest Advanced Actions (Doctor-level)

Provides contextual and medically aligned explanations

🔹 3. Clean UI with Two Modules

Module 1: Continuous Monitoring Dashboard

Module 2: Manual Input + LLM Analysis

Modern UI with preloader animation and color-coded predictions

📊 Technologies Used
Machine Learning
Random Forest Classifier
XGBoost (optional experimentation)
Scikit-Learn preprocessing
LLM & AI
LlamaIndex
HuggingFace Embeddings
Ollama local LLM (Gemma 2B or similar)
Semantic Vector Retrieval

Backend
Python
Flask

Frontend
HTML
CSS
JavaScript

🧠 How It Works

1️⃣ Continuous Monitoring Module

Receives live sensor data via a socket listener
Processes 8 parameters
Predicts maternal state using ML model
Updates dashboard instantly

2️⃣ LLM Rule-Based Suggestion Module

Accepts 19 parameters
Matches conditions with medical rules from dataset
Embeds dataset into a vector store

LLM generates:

Summary
Future Complication
Basic Action (Nurse-level)
Advanced Action (Doctor-level)


🏥 Use Cases
Labor room monitoring
Postpartum complication prediction
Nursing decision support
Rural/low-resource clinical settings
Real-time emergency alerts

🔧 Installation

cd MatriCare-AI

2. Install dependencies
pip install -r requirements.txt

3. Run Ollama (LLM Backend)
Make sure you have Ollama installed:
ollama run gemma2:2b

4. Start Flask App
python app.py

🧪 Testing

Use sample buttons provided in the UI
Upload or stream continuous data for dashboard testing
Try multiple parameter combinations

🛣️ Future Enhancements

Mobile App Integration
Larger models for deeper reasoning
Integration with IoT medical belts
Patient risk timeline charts
Voice-based interaction
