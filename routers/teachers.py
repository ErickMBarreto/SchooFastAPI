from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload
import models, schemas
from main import DbSession

router = APIRouter()

@router.post("/teachers/", response_model=schemas.Teacher)
def teacher_create(teacher: schemas.TeacherCreate, db: DbSession):
    db_teacher = models.Teacher(**teacher.model_dump())
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/teachers/", response_model=List[schemas.Teacher])
def list_teachers(db: DbSession):
    teachers = db.query(models.Teacher).options(joinedload(models.Teacher.subjects)).all()
    return teachers