import os
from langchain_community.vectorstores import FAISS

from utils.embeddings import get_embeddings
from config import VECTOR_DB_FOLDER


def create_vector_store(chunks):
    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)

    return vector_store


def save_vector_store(vector_store):
    os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)

    vector_store.save_local(VECTOR_DB_FOLDER)


def load_vector_store():
    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        VECTOR_DB_FOLDER, embeddings, allow_dangerous_deserialization=True
    )

    return vector_store
