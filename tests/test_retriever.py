from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.vector_store import create_vector_store
from utils.retriever import get_retriever

# Load PDF
documents = load_pdf("uploaded_files/resume.pdf")

# Split into chunks
chunks = split_documents(documents)

# Create FAISS vector store
vector_store = create_vector_store(chunks)

# Create retriever
retriever = get_retriever(vector_store)

# Ask a question
query = "What are this person's technical skills?"

results = retriever.invoke(query)

print(f"Retrieved {len(results)} chunks.\n")

for i, doc in enumerate(results, start=1):
    print("=" * 80)
    print(f"Chunk {i}")
    print("=" * 80)
    print(doc.page_content)
    print("\nMetadata:")
    print(doc.metadata)
    print()
