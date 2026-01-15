import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def ingest_docs():
    loader = DirectoryLoader("rag/docs", glob="*.md")
    docs = loader.load()
    if len(docs) == 0:
        raise ValueError("❌ No .md files found in rag/docs")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs("rag/faiss_index", exist_ok=True)
    vectorstore.save_local("rag/faiss_index")

    print("✅ FAISS index created at rag/faiss_index")

if __name__ == "__main__":
    ingest_docs()
