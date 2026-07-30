from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents

# Load the PDF
documents = load_pdf("uploaded_files/resume.pdf")

print(f"Total Pages: {len(documents)}")

# Split into chunks
chunks = split_documents(documents)

print(f"Total Chunks: {len(chunks)}")

print("-" * 80)

print("First Chunk:\n")
print(chunks[0].page_content)

print("-" * 80)

print("Metadata:\n")
print(chunks[0].metadata)
