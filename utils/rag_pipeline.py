from langchain_core.prompts import ChatPromptTemplate

from utils.llm import get_llm


def ask_question(retriever, question):
    """
    Retrieve relevant context and generate an answer using Gemini.
    """

    # Retrieve relevant chunks
    docs = retriever.invoke(question)

    # Combine retrieved chunks
    context = ""

    for i, doc in enumerate(docs, start=1):
        context += f"""
      Document {i}
      Page: {doc.metadata.get('page', 'Unknown')}

      {doc.page_content}

      -----------------------------------
      """

    # Prompt template
    prompt = ChatPromptTemplate.from_template("""
    You are an Enterprise AI Document Assistant.

    Use ONLY the information provided in the retrieved context.

    Context:
    {context}

    Question:
    {question}

    Instructions:
    - Answer only from the provided context.
    - Do not make assumptions or invent information.
    - If multiple items exist (projects, skills, certifications, experience), include ALL relevant items found in the retrieved context.
    - Present the answer using bullet points whenever appropriate.
    - If the answer cannot be found, reply exactly:
    "I couldn't find that information in the uploaded document."
    """)

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke({"context": context, "question": question})

    return response.content, docs
