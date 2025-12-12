# LangGraph 상태 정의 - RAG 관련 필드 추가
from typing import Dict, List, TypedDict


class AgentType:
    SQAA = "SQAA_AGENT" # SmartQA Assistant

    @classmethod
    def to_korean(cls, role: str) -> str:
        if role == cls.SQAA:
            return "SQAA"
        else:
            return role


class EvaluateState(TypedDict):
    stock_no        : str           # 증권번호
    messages        : List[Dict]    # 메시지내용
    current_count   : int           # 현재 재평가 횟수
    prev_node       : str
    max_counts      : int           # 최대 재평가 횟수
    docs            : Dict[str, List] # RAG 검색 결과
    contexts        : Dict[str, str]  # RAG 검색 컨텍스트
