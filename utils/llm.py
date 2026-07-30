import os
from dotenv import load_dotenv
from config import LLM_MODEL, GOOGLE_API_KEY

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():
    """
    Initialize and return the Gemini LLM.
    """

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.2
    )

    return llm
