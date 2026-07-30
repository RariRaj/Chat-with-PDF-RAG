import os
import streamlit as st

from utils.file_hash import get_file_hash
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
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "document_hash" not in st.session_state:
    st.session_state.document_hash = None


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

uploaded_file = st.file_uploader(
    "📄 Upload a PDF",
    type=["pdf"],
)

if uploaded_file:

    document_hash = get_file_hash(uploaded_file)

    vector_folder = os.path.join(
        "vector_store",
        document_hash,
    )

    if st.session_state.document_hash != document_hash:

        st.session_state.document_hash = document_hash

        # -----------------------------
        # Load Existing Vector Store
        # -----------------------------

        if os.path.exists(vector_folder):

            with st.spinner("📂 Loading existing vector database..."):

                vector_store = load_vector_store(document_hash)

            st.success("✅ Existing vector database loaded.")

        # -----------------------------
        # Create New Vector Store
        # -----------------------------

        else:

            with st.spinner("📄 Creating vector database..."):

                file_path = save_uploaded_file(uploaded_file)

                documents = load_pdf(file_path)

                chunks = split_documents(documents)

                vector_store = create_vector_store(chunks)

                save_vector_store(
                    vector_store,
                    document_hash,
                )

            st.success("✅ Document indexed successfully!")

            st.info(f"""
📄 **Document:** {uploaded_file.name}

📃 **Pages:** {len(documents)}

🧩 **Chunks:** {len(chunks)}

🟢 **Status:** Ready to Chat
""")

        st.session_state.retriever = get_retriever(vector_store)


# --------------------------------------------------
# Display Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# Chat
# --------------------------------------------------

question = st.chat_input("Ask a question about your document...")

if question:

    if st.session_state.retriever is None:

        st.warning("Please upload a PDF first.")

        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.spinner("🤖 Thinking..."):

        answer, docs = ask_question(
            st.session_state.retriever,
            question,
        )

    with st.chat_message("assistant"):

        st.markdown(answer)

        with st.expander("📄 Source References"):

            displayed = set()

            for doc in docs:

                source = doc.metadata.get(
                    "source",
                    "Unknown",
                )

                page = doc.metadata.get(
                    "page",
                    0,
                )

                key = (source, page)

                if key in displayed:
                    continue

                displayed.add(key)

                st.markdown(f"""
**📄 File:** `{source}`

**📑 Page:** {page + 1}
""")

                st.caption(doc.page_content[:250] + "...")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )
