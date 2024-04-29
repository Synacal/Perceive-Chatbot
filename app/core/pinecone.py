from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

def get_pinecone_client():
    print(os.getenv("PINECONE_API_KEY"))
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME")
    index = pc.Index(index_name)
    return index