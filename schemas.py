from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class Profile(BaseModel):
    id: int
    age: int
    address: str
    student_id: int

    class Config:
        from_attributes = True

class ProfileCreate(BaseModel):
    age: int
    address: str

class Student(BaseModel):
    id: int
    name: str
    profile: Optional[Profile] = None

    class Config:
        from_attributes = True

class StudentCreate(BaseModel):
    name: str
    mail: str
    profile: ProfileCreate

class Teacher(BaseModel):
    id:int
    name: str
    class Config:
        from_attributes = True

class TeacherCreate(BaseModel):
    name: str

class Subject(BaseModel):
    id: int
    name: str
    description: str
    teacher_id: int
    
    class Config:
        from_attributes = True

class SubjectCreate(BaseModel):
    name: str
    description: str
    teacher_id: Optional[int] = None

class Enrollment(BaseModel):
    id: int
    enrollment_date: datetime
    subject_id: int
    student_id: int
    
    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    subject_id: int
    student_id: int
    enrollment_date: Optional[datetime] = None


