from flask import Flask
from maternal_module import maternal_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(maternal_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
