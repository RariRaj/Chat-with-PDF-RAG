import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# API Configuration
# ===============================
try:
    import streamlit as st

    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ===============================
# Model Configuration
# ===============================
LLM_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/gemini-embedding-001"

# ===============================
# Text Splitter Configuration
# ===============================
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ===============================
# Retriever Configuration
# ===============================
TOP_K = 5
FETCH_K = 20
LAMBDA_MULT = 0.7

# ===============================
# Directories
# ===============================
UPLOAD_FOLDER = "uploaded_files"
VECTOR_DB_FOLDER = "vector_store"
