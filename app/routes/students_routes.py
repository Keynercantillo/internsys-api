from fastapi import APIRouter, HTTPException
from controllers.students_controller import *
from models.student_model import Student

router = APIRouter()

nuevo_student = StudentsController()

@router.post("/create_student")
async def create_student(student: Student):
    rpta = nuevo_student.create_student(student)
    return rpta

@router.get("/get_student/{student_id}", response_model=Student)
async def get_student(student_id: int):
    rpta = nuevo_student.get_student(student_id)
    return rpta

@router.get("/get_students/")
async def get_students():
    rpta = nuevo_student.get_students()
    return rpta

@router.put("/update_student/{student_id}")
async def update_student(student_id: int, student: Student):
    rpta = nuevo_student.update_student(student_id, student)
    return rpta

@router.delete("/delete_student/{student_id}")
async def delete_student(student_id: int):
    rpta = nuevo_student.delete_student(student_id)
    return rpta