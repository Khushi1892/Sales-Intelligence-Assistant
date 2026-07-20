from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import os

def load_documents():
    print("Loading documents...")
    files = [
        "docs/sales_policy.txt",
        "docs/pricing.txt",
        "docs/employee_handbook.txt"
    ]
    documents = []
    for file in files:
        loader = TextLoader(file, encoding="utf-8")
        documents.extend(loader.load())
    print(f"Loaded {len(documents)} documents.")
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50

    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")
    return chunks


def create_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings


def create_vectorstore(chunks, embeddings):
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db"
    )
    print("Vector database created successfully.")
    return vectorstore


def setup_rag():
    documents = load_documents()
    chunks = split_documents(documents)
    embeddings = create_embeddings()
    vectorstore = create_vectorstore(chunks,embeddings)
    print("RAG setup completed!")
    return vectorstore


if __name__ == "__main__":
    setup_rag()