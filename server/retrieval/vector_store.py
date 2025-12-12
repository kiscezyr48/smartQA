import streamlit as st
from langchain_community.vectorstores import FAISS
from typing import Any, Dict, Optional, List
from retrieval.search_service import get_search_content, improve_search_query
from utils.config import get_embeddings


def get_stock_no_vector_store(
    stock_no: str, role: str, language: str = "ko"
) -> Optional[FAISS]:

    # 검색어 개선
    improved_queries = improve_search_query(stock_no, role)
    # 개선된 검색어로 검색 콘텐츠 가져오기
    documents = get_search_content(improved_queries, language)
    if not documents:
        return None
    try:
        return FAISS.from_documents(documents, get_embeddings())
    except Exception as e:
        st.error(f"Vector DB 생성 중 오류 발생: {str(e)}")
        return None


def search_stock_no(stock_no: str, role: str, query: str, k: int = 5) -> List[Dict[str, Any]]:
    # 문서를 검색해서 벡터 스토어 생성
    vector_store = get_stock_no_vector_store(stock_no, role)
    if not vector_store:
        return []
    try:
        # 벡터 스토어에서 Similarity Search 수행
        return vector_store.similarity_search(query, k=k)
    except Exception as e:
        st.error(f"검색 중 오류 발생: {str(e)}")
        return []
