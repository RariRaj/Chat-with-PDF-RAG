import streamlit as st

from utils.helpers import save_uploaded_file
from utils.pdf_loader import load_pdf
from utils.text_splitter import split_documents
from utils.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
)
from utils.retriever import get_retriever
from utils.rag_pipeline import ask_question

# --------------------------------------------------
# Streamlit Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Enterprise RAG Assistant",
    page_icon="🤖",
    layout="wide",
)


# --------------------------------------------------
# Cache Retriever
# --------------------------------------------------
@st.cache_resource
def get_cached_retriever():
    vector_store = load_vector_store()
    return get_retriever(vector_store)


# --------------------------------------------------
# Session State
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "current_file" not in st.session_state:
    st.session_state.current_file = None


# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("🤖 Enterprise RAG Assistant")

st.caption(
    "Ask intelligent questions about your PDF using Google Gemini, LangChain and FAISS."
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("🤖 Enterprise RAG Assistant")

st.sidebar.markdown("---")

st.sidebar.success("LLM: Gemini 2.5 Flash")
st.sidebar.info("Embeddings: Gemini Embedding")
st.sidebar.info("Vector Database: FAISS")
st.sidebar.info("Framework: LangChain")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("Created by **Rari Raj**")


# --------------------------------------------------
# Upload PDF
# --------------------------------------------------
uploaded_file = st.file_uploader("📄 Upload a PDF", type=["pdf"])

if uploaded_file:

    # Detect new uploaded file
    if uploaded_file.name != st.session_state.current_file:

        st.session_state.current_file = uploaded_file.name
        st.session_state.processed = False

    # Process only once
    if not st.session_state.processed:

        with st.spinner("📄 Processing PDF and creating vector database..."):

            file_path = save_uploaded_file(uploaded_file)

            documents = load_pdf(file_path)

            chunks = split_documents(documents)

            vector_store = create_vector_store(chunks)

            save_vector_store(vector_store)

        st.session_state.processed = True

        st.success("✅ Document Ready!")

        st.info(f"""
📄 **Document:** {uploaded_file.name}

📃 **Pages:** {len(documents)}

🧩 **Chunks:** {len(chunks)}

🟢 **Status:** Ready to Chat
""")


# --------------------------------------------------
# Display Chat History
# --------------------------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------
question = st.chat_input("Ask a question about your document...")

if question:

    # Save user message
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    retriever = get_cached_retriever()

    with st.spinner("🤖 Thinking..."):

        answer, docs = ask_question(retriever, question)

    with st.chat_message("assistant"):

        st.markdown(answer)

        with st.expander("📄 Source References"):

            displayed = set()

            for doc in docs:

                source = doc.metadata.get("source", "Unknown")

                page = doc.metadata.get("page", 0)

                key = (source, page)

                if key in displayed:
                    continue

                displayed.add(key)

                st.markdown(f"""
**📄 File:** `{source}`

**📑 Page:** {page + 1}
""")

                st.caption(doc.page_content[:250] + "...")

    st.session_state.messages.append({"role": "assistant", "content": answer})
