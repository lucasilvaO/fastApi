from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    email: str


db: List[Student] = [Student(id=1, name="Lucas", email="lucas@gmail.com")]
next_id = 2

app = FastAPI()


class StudentCreate(BaseModel):
    name: str
    email: str


@app.get("/students", response_model=List[Student], tags=["Students"])
def list_students():
    return db


@app.get("/students/{student_id}", response_model=Student, tags=["Students"])
def get_student(student_id: int):
    for student in db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


@app.post("/students", response_model=Student, status_code=201, tags=["Students"])
def create_student(student: StudentCreate):
    global next_id

    for existing_student in db:
        if existing_student.email == student.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    new_student = Student(id=next_id, name=student.name, email=student.email)
    db.append(new_student)
    next_id += 1
    return new_student
