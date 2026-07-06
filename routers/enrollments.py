from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import joinedload
from datetime import datetime
import models, schemas
from main import DbSession

router = APIRouter()

@router.post("/enrollments/", response_model=schemas.Enrollment)
def enrollments_create(enrollment:schemas.EnrollmentCreate, db: DbSession):
    student_exists = db.query(models.Student).filter(models.Student.id == enrollment.student_id).first()
    if not student_exists:
        raise HTTPException(status_code=400, detail="Student not found.")
    subject_exists = db.query(models.Subject).filter(models.Student.id == enrollment.subject_id).first()
    if not subject_exists:
        raise HTTPException(status_code=400, detail="Subject not found.")
    enrollment_exists = db.query(models.Enrollment).filter(models.Enrollment.subject_id == enrollment.subject_id).first()
    if enrollment_exists:
        raise HTTPException(status_code=400, detail="Enrollment already has a Student.")
    
    enrollment_data = enrollment.model_dump()

    if enrollment_data.get("enrollment_date") is None:
        enrollment_data["entollmente_date"] = datetime.now()

    db_enrollment = models.Enrollment(**enrollment_data)
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

@router.get("/enrollments/", response_model=List[schemas.Enrollment])
def list_enrollment(db: DbSession):
    enrollments = db.query(models.Enrollment).all()
    return enrollments