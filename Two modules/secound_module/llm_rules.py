import os
import pandas as pd
from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

RULES_FILE = "final data.xlsx"

if not os.path.exists(RULES_FILE):
    raise FileNotFoundError(f"{RULES_FILE} missing")

df = pd.read_excel(RULES_FILE)
df.columns = df.columns.str.strip()

docs = []
for _, r in df.iterrows():
    text = (
        f"Parameter: {r.get('Parameter','')}\n"
        f"Condition: {r.get('Condition','')}\n"
        f"Range: {r.get('Range','')}\n"
        f"Future Outcome: {r.get('Future Outcome','')}\n"
        f"Doctor Action: {r.get('Doctor Action','')}\n"
        f"Nurse Action: {r.get('Nurse Action','')}"
    )
    docs.append(Document(text=text.strip()))

embed = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = Ollama(model="gemma2:2b")
index = VectorStoreIndex.from_documents(docs, embed_model=embed)
engine = index.as_query_engine(llm=llm)

def get_llm_suggestion(condition_text: str):
    prompt = f"""
Given patient data: {condition_text}

Respond concisely:
1. Summary
2. Future Outcome
3. Basic Actions (nurse-level)
4. Advanced Actions (doctor-level)
"""
    resp = engine.query(prompt)
    text = resp.response
    parts = text.split("2.")
    summary = parts[0].replace("1.", "").strip()
    future = basic = advanced = ""
    try:
        after2 = parts[1]
        future = after2.split("3.")[0].strip()
        after3 = after2.split("3.")[1]
        basic = after3.split("4.")[0].strip()
        advanced = after3.split("4.")[1].strip()
    except Exception:
        pass
    return summary, future, basic, advanced
