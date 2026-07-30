from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.vector_store import create_vector_store
from utils.retriever import get_retriever
from utils.rag_pipeline import ask_question

# Load PDF
documents = load_pdf("uploaded_files/resume.pdf")

# Split
chunks = split_documents(documents)

# Create vector store
vector_store = create_vector_store(chunks)

# Retriever
retriever = get_retriever(vector_store)

# Ask question
question = input("Ask a question: ")

answer = ask_question(retriever, question)

print("\nAnswer:\n")
print(answer)
