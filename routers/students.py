from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload
import models, schemas
from main import DbSession

router = APIRouter()

@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def student_create(student: schemas.StudentCreate, db: DbSession):
    mail_exists = db.query(models.Student).filter(models.Student.mail == student.mail).first()
    if mail_exists:
        raise HTTPException(status_codes=400, detail="Mail already registered.")
    profile_data = student.profile.model_dump()
    db_profile = models.Profile(**profile_data)
    db_student = models.Student(name = student.name, mail = student.mail, profile=db_profile)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/", response_model= List[schemas.Student])
def list_students(db: DbSession):
    return db.query(models.Student).options(joinedload(models.Student.profile)).all()

@router.get("/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, db: DbSession):
    db_student = db.query(models.Student).options(joinedload(models.Student.profile)).filter(models.Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return db_student

