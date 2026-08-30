from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import settings
import os

def build_vectorstore():
    """Documents load, split, aur embed karke persistent Chroma DB banata hai.
    Ye sirf ek baar chalta hai (ya jab documents update hon)."""
    
    loader = DirectoryLoader(
        path="./data/agency_docs/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()

    for doc in documents:
        doc.metadata["source_file"] = os.path.basename(doc.metadata["source"])

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", ", ", " ", ""]
    )
    split_docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=settings.chroma_persists_dir,
        collection_name="pixelo_knowledge_base"
    )
    
    print(f"Vector store built with {len(split_docs)} chunks")
    return vectorstore

def get_vectorstore():
    """Existing persisted vector store ko load karta hai (runtime use ke liye)"""
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

    vectorstore = Chroma(
        persist_directory=settings.chroma_persists_dir,
        embedding_function=embeddings,
        collection_name="pixelo_knowledge_base"
    )
    return vectorstore