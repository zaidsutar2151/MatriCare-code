from flask import Flask, render_template, jsonify
import joblib
import numpy as np
import socket
import threading
import json
import time
import os
from maternal_module import maternal_bp

app = Flask(__name__)
app.register_blueprint(maternal_bp, url_prefix='/maternal')

# ====== Model & Config ======
rf_model = joblib.load("8 para model.pkl")
feature_names = ["SysBP", "DiaBP", "HR", "Temp", "SpO2", "RR", "FHR", "Toco"]

latest_data = {name: 0 for name in feature_names}
last_update_time = 0

status_map = {
    0: ("Stable", "#28a745"),
    1: ("Moderate", "#ffc107"),
    2: ("Critical", "#dc3545")
}

HOST = "0.0.0.0"
PORT = 5000

# ===== SOCKET LISTENER THREAD =====
def socket_listener():
    global latest_data, last_update_time
    try:
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ✅ Prevent "address in use"
        server_sock.bind((HOST, PORT))
        server_sock.listen(1)

        print("📡 Waiting for connection...")
        print("💻 Receiver IP:", socket.gethostbyname(socket.gethostname()))
        print(f"➡️ Listening on port {PORT}")

        client_sock, addr = server_sock.accept()
        print(f"✅ Connected from {addr}")

        buffer = ""
        while True:
            chunk = client_sock.recv(1024)
            if not chunk:
                break
            buffer += chunk.decode()

            # Split by newline
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                print("📥 Received:", line)
                try:
                    parsed = json.loads(line)
                    if all(k in parsed for k in feature_names):
                        latest_data = parsed
                        last_update_time = time.time()
                except Exception as e:
                    print("❌ JSON parse error:", e)

    except Exception as e:
        print("🛑 Socket error:", e)
    finally:
        try:
            client_sock.close()
        except:
            pass
        try:
            server_sock.close()
        except:
            pass
        print("🔌 Socket closed.")

# ===== FLASK ROUTES =====
@app.route('/')
def dashboard():
    return render_template('dashboard.html', feature_names=feature_names)

@app.route('/predict')
def predict():
    global latest_data

    features = [latest_data.get(f, 0) for f in feature_names]
    input_data = np.array([features])

    if any(v != 0 for v in features):
        prediction_raw = rf_model.predict(input_data)[0]
        label, color = status_map.get(prediction_raw, ("Unknown", "#6c757d"))
    else:
        label, color = ("Waiting for data...", "#6c757d")

    return jsonify({
        "features": latest_data,
        "prediction": label,
        "color": color,
        "last_update": last_update_time
    })

# ===== START SERVER SAFELY =====
if __name__ == '__main__':
    # Avoid re-launching multiple threads on Flask reload
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=socket_listener, daemon=True).start()
    print("🚀 Flask dashboard running on port 8000...")
    app.run(host='0.0.0.0', port=8001, debug=True)
