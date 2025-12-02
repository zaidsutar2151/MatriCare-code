import streamlit as st
import pandas as pd
from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

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

# UI
st.title("Maternal Monitoring Assistant 👩‍⚕️")
condition = st.text_input("Enter patient condition:")

if st.button("Get Suggestions"):
    prompt = f"""
    Given the condition: {condition}, provide:
    1. Basic action (for nurses).
    2. Advanced action (for doctors).
    """
    response = query_engine.query(prompt)
    st.markdown("### Nurse Suggestion:")
    st.write(response.response.split("2.")[0].replace("1.", "").strip())
    st.markdown("### Doctor Suggestion:")
    if "2." in response.response:
        st.write(response.response.split("2.")[1].strip())
    else:
        st.write("Not clearly separated, here’s the full response:")
        st.write(response.response)
