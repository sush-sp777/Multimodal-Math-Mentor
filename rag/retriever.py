import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import streamlit as st

# Absolute path to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to FAISS index
INDEX_PATH = os.path.join(BASE_DIR, "rag", "faiss_index")

@st.cache_resource(show_spinner="Loading embedding model...")
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
@st.cache_resource(show_spinner="Loading FAISS index...")
def load_vectorstore():
    embeddings = load_embeddings()
    return FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

def retrieve_context(query: str, k: int = 3):
    """
    Retrieve relevant context from FAISS vector store.
    """
    if not os.path.exists(INDEX_PATH):
        print("❌ FAISS index not found at:", INDEX_PATH)
        return []

    
    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(query, k=k)

    print(f"🔍 RAG retrieved {len(docs)} documents")

    return docs
