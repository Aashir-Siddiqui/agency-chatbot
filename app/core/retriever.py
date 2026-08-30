from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from app.core.vectorstore import get_vectorstore

def build_retriever():
    """Broad retrieval + re-ranking combine karta hai — production-grade accuracy"""
    vectorstore = get_vectorstore()

    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 8})
    
    cross_encoder = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
    reranker = CrossEncoderReranker(model=cross_encoder, top_n=3)

    compression_retiever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=base_retriever
    )
    
    return compression_retiever