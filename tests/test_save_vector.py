from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
)

documents = load_pdf("uploaded_files/resume.pdf")
chunks = split_documents(documents)

vector_store = create_vector_store(chunks)

save_vector_store(vector_store)

loaded_store = load_vector_store()

print(type(loaded_store))
print("Vector Store Loaded Successfully!")
