from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# DTO 클래스 정의
class EvaluateBase(BaseModel):
    stock_no    : str   # 증권번호
    counts      : int   # 재평가 횟수
    messages    : str   # JSON 문자열
    docs        : Optional[str] = None  # JSON 문자열


class EvaluateCreate(EvaluateBase):
    pass


class EvaluateSchema(EvaluateBase):
    id          : int
    created_at  : datetime

    class Config:
        from_attributes = True
