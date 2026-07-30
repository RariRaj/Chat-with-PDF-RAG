from dotenv import load_dotenv
import os
from config import EMBEDDING_MODEL, GOOGLE_API_KEY

from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()


def get_embeddings():
    """
    Initialize and return Google's embedding model.
    """

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL, google_api_key=GOOGLE_API_KEY
    )

    return embeddings
