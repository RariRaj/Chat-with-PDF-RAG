import os

from langchain_community.vectorstores import FAISS
from utils.embeddings import get_embeddings


def create_vector_store(chunks):
    embeddings = get_embeddings()

    return FAISS.from_documents(
        chunks,
        embeddings,
    )


def save_vector_store(vector_store, document_hash):
    folder = os.path.join("vector_store", document_hash)

    os.makedirs(folder, exist_ok=True)

    vector_store.save_local(folder)


def load_vector_store(document_hash):
    folder = os.path.join("vector_store", document_hash)

    embeddings = get_embeddings()

    return FAISS.load_local(
        folder,
        embeddings,
        allow_dangerous_deserialization=True,
    )
