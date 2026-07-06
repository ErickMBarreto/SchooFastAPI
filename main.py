from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from typing import Annotated
from routers import students, subjects, enrollments, teachers


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]

app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])
app.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])

@app.get("/")
def root():
    return{"message": "API status: 200"}