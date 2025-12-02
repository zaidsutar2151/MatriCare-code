from flask import Flask, render_template, request
import pandas as pd
from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

app = Flask(__name__)

# Load Excel
df = pd.read_excel("maternal_monitoring_actions.xlsx")

# Convert rows into knowledge chunks
documents = []
for _, row in df.iterrows():
    text = f"""
    Parameter: {row['Parameter']}
    
    Yellow Range: {row['Yellow Range']}
    Nurse Action (Yellow): {row['Nurse Action (Yellow)']}
    Doctor Action (Yellow): {row['Doctor Action (Yellow)']}
    
    Red Range: {row['Red Range']}
    Nurse Action (Red): {row['Nurse Action (Red)']}
    Doctor Action (Red): {row['Doctor Action (Red)']}
    """
    documents.append(Document(text=text.strip()))

# Embeddings + LLM
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Ollama(model="gemma2:2b")
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
query_engine = index.as_query_engine(llm=llm)

@app.route("/", methods=["GET", "POST"])
def home():
    nurse_suggestion = ""
    doctor_suggestion = ""

    if request.method == "POST":
        condition = request.form["condition"]
        prompt = f"""
        Given the condition: {condition}, provide:
        1. Basic action (for nurses).
        2. Advanced action (for doctors).
        """
        response = query_engine.query(prompt)

        # Try to split output
        if "2." in response.response:
            nurse_suggestion = response.response.split("2.")[0].replace("1.", "").strip()
            doctor_suggestion = response.response.split("2.")[1].strip()
        else:
            nurse_suggestion = response.response
            doctor_suggestion = "Not clearly separated."

    return render_template("index.html", 
                           nurse=nurse_suggestion, 
                           doctor=doctor_suggestion)

if __name__ == "__main__":
    app.run(debug=True)
