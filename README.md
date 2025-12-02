# 🩺 MatriCare AI — Intelligent Maternal Health Monitoring System

[🔗 Project Website](https://zaidsutar2151.github.io/MatriCare/)

---

MatriCare AI is a complete **AI-driven maternal monitoring system** designed to assist doctors and nurses in predicting pregnancy-related complications using Machine Learning (ML) and LLM-based clinical reasoning.

This repository contains everything required to understand, run, and evaluate the project—including code, documentation, datasets, models, diagrams, and demonstrations.

---

## 🌟 Project Overview

Maternal complications often go undetected due to lack of continuous monitoring, delayed diagnosis, and limited decision-support systems—especially in low-resource hospitals.

MatriCare AI solves this by combining:

### 🔹 1. Continuous Risk Prediction Model (8 Parameters)
- Automatically tracks 8 vital maternal parameters using sensors/hospital devices.
- Predicts real-time maternal state:
  - **Stable** | **Moderate** | **Critical**
- **Accuracy:** 91.5%

### 🔹 2. LLM-Based Suggestion Model (19 Parameters)
- Uses 19 detailed inputs like hydration, pain score, mood, lochia etc.
- Provides:
  - Future complication warnings
  - Nurse-level Immediate Actions
  - Doctor-level Advanced Actions
- **Accuracy:** 95%
- Powered by **Gemma-2:2B** via Ollama and LlamaIndex vector search.

---

## 📁 Repository Structure

```text
MatriCare/
│
├── Documentation/
│   ├── Project Report
│   ├── PPT Slides
│   ├── Abstract & Certificates
│   └── Letters (Guide/Completion)
│
├── Models Training/
│   ├── 8-Parameter ML Model (Training + Testing)
│   ├── 19-Parameter ML Model (Training + Testing)
│   └── LLM Integration using LlamaIndex
│
├── One Module/
│   └── Single Flask App (Combined ML + LLM)
│
├── Two Modules/
│   ├── first_module/ (8-parameter Continuous ML model)
│   └── second_module/ (19-parameter LLM Suggester)
│
├── wifi data sharing/
│   ├── Sender Script
│   └── Receiver Script
│
├── Maternal_8_Parameters_Explanation.docx
├── MetricCare_19_Parameter_Explanations.docx
└── Maternal_Monitoring_48H.xlsx
```

---

## 🚀 How to Run the Project

### Prerequisites

Ensure you have installed:
- Python 3.10+
- Flask
- Scikit-learn
- Pandas / NumPy
- Ollama
- Gemma2:2B model
- LlamaIndex

### 🔹 Step 1 — Start the LLM Backend

```bash
ollama run gemma2:2b
```
Keep this terminal running.

### 🔹 Option A — Run One-Module Version (Single App)
```bash
cd One Module
python app.py
```
This version runs both ML + LLM inside one Flask server.

### 🔹 Option B — Run Two-Module Version (Both Apps Separately)
**First module (Continuous Risk Model)**
```bash
cd Two modules/first_module
python app.py
```
**Second module (LLM Suggestion System)**
```bash
cd Two modules/second_module
python app.py
```
Both servers must be running simultaneously.

---

## 📡 WiFi Data Sharing (Optional Module)

To stream patient data between two devices on the same network:

**Sender**
```bash
python sender.py
```
**Receiver**
```bash
python receiver.py
```
This can be used for sending vital signs from bedside device → nurse station.

---

## 📊 Model Performance

### 8-Parameter Continuous Model
- **Accuracy:** 0.915
- **Classification:** Stable / Moderate / Critical
- **Purpose:** Real-time automated risk monitoring

### 19-Parameter Detailed Model
- **Accuracy:** 0.95
- **Purpose:** Medical suggestions + future complication prediction

Training plots & confusion matrices present in Models Training folder.

---

## 🧠 Technologies Used

| Layer           | Tech                                  |
|-----------------|---------------------------------------|
| Backend         | Flask (Python)                        |
| ML Models       | Scikit-Learn                          |
| LLM             | Gemma2:2B (via Ollama)                |
| Knowledge Retrieval | LlamaIndex (Vector Search)         |
| Data Transfer   | Socket-based WiFi Sharing             |
| Frontend        | HTML, CSS, JavaScript                 |
| Documentation   | Word, PPT, PDF                        |

---

## 🏥 Key Features

- Real-time automated maternal monitoring
- Dual-model AI system
- Nurse-friendly and doctor-friendly suggestions
- Low-cost technology suitable for rural hospitals
- Easy deployment on any Windows/Linux system
- Expandable rule-base + vector searchable knowledge system

---

## 🧪 Testing

- Functional testing completed for both ML modules
- End-to-end testing for Flask-based UIs
- Data flow testing for WiFi data sharing
- Manual + automated validation of LLM outputs

---

## 📌 Use Case Example

A nurse enters maternal vitals into the system →
Continuous ML model predicts Moderate Risk →
Nurse enters detailed 19 parameters →
LLM gives:
- Possible upcoming complications
- Immediate steps
- Doctor-level recommendations

This supports faster, accurate clinical decisions.

---

## 📄 Documentation

Complete documentation is available inside:

`/Documentation`

Including:
- Full Project Report (40+ pages)
- PPT Presentations
- Parameter definitions
- Certificates & Letters

---

## 🤝 Contributors

**Md Zaid Sutar**  
Developer • Machine Learning Engineer • Researcher

⭐ If you found this project useful, give it a star on GitHub!

Your support encourages further development.
