from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.vector_store import create_vector_store

# Load PDF
documents = load_pdf("uploaded_files/resume.pdf")

# Split into chunks
chunks = split_documents(documents)

# Create vector store
vector_store = create_vector_store(chunks)

print("Vector Store Created Successfully!")

print(type(vector_store))
