from langchain_core.prompts import ChatPromptTemplate

from utils.llm import get_llm


def ask_question(retriever, question):
    """
    Retrieve relevant context and generate an answer using Gemini.
    """

    # Retrieve relevant chunks
    docs = retriever.invoke(question)

    # Combine retrieved chunks
    context = "\n\n".join([doc.page_content for doc in docs])

    # Prompt template
    prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that answers questions only from the provided context.

Context:
{context}

Question:
{question}

Instructions:
- Answer only using the provided context.
- If the answer is not available, say:
  "I couldn't find that information in the uploaded document."
- Keep your answer concise and professional.
""")

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({"context": context, "question": question})

    return response.content
