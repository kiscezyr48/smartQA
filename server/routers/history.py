from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db
from server.db.models import Evaluate as EvaluateModel
from server.db.schemas import EvaluateSchema, EvaluateCreate

router = APIRouter(prefix="/api/v1", tags=["evaluates"])


# 평가 목록 조회
@router.get("/evaluates/", response_model=List[EvaluateSchema])
def read_evaluates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    evaluates = db.query(EvaluateModel).offset(skip).limit(limit).all()
    return evaluates


# 평가 생성
@router.post("/evaluates/", response_model=EvaluateSchema)
def create_evaluate(evaluate: EvaluateCreate, db: Session = Depends(get_db)):
    db_evaluate = EvaluateModel(**evaluate.model_dump())
    db.add(db_evaluate)
    db.commit()
    db.refresh(db_evaluate)
    return db_evaluate


# 평가 조회
@router.get("/evaluates/{evaluate_id}", response_model=EvaluateSchema)
def read_evaluate(evaluate_id: int, db: Session = Depends(get_db)):
    db_evaluate = db.query(EvaluateModel).filter(EvaluateModel.id == evaluate_id).first()
    if db_evaluate is None:
        raise HTTPException(status_code=404, detail="Evaluate not found")
    return db_evaluate


# 평가 삭제
@router.delete("/evaluates/{evaluate_id}")
def delete_evaluate(evaluate_id: int, db: Session = Depends(get_db)):
    db_evaluate = db.query(EvaluateModel).filter(EvaluateModel.id == evaluate_id).first()
    if db_evaluate is None:
        raise HTTPException(status_code=404, detail="Evaluate not found")

    db.delete(db_evaluate)
    db.commit()
    return {"detail": "Evaluate successfully deleted"}
