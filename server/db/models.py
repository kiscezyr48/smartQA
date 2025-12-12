from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from db.database import Base


# 평가 모델
class Evaluate(Base):
    __tablename__ = "evaluate"

    id          = Column(Integer, primary_key=True, index=True)
    stock_no    = Column(String(255), nullable=False)   # 증권번호
    counts      = Column(Integer, default=1)            # 재평가횟수
    messages    = Column(Text, nullable=False)          # JSON 문자열로 저장
    docs        = Column(Text, nullable=True)           # JSON 문자열로 저장
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
