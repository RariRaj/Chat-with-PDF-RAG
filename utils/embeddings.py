from dotenv import load_dotenv
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()


def get_embeddings():
    """
    Initialize and return Google's embedding model.
    """

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    return embeddings
