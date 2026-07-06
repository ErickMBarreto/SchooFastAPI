from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload
import models, schemas
from main import DbSession

router = APIRouter()

@router.post("/subjects/", response_model=schemas.Subject)
def subject_create(subject: schemas.SubjectCreate, db: DbSession):
    if subject.teacher_id is not None:
        teacher_exists = db.query(models.Teacher). filter(models.Teacher.id == subject.teacher_id).first()
        if not teacher_exists:
            raise HTTPException(status_code=400, detail="Teacher not found.")
        
    db_subject = models.Subject(**subject.model_dump())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/subjects/", response_model= List[schemas.Subject])
def list_subject(db: DbSession):
    subjects = db.query(models.Subject).options(joinedload(models.Subject.teacher)).all()
    return subjects