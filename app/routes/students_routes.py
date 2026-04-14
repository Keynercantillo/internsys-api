from fastapi import APIRouter, HTTPException
from controllers.students_controller import StudentsController
from models.students_model import Student  # ✅ CORREGIDO: students_model (plural)

router = APIRouter()

students_controller = StudentsController()

@router.post("/create_student")
async def create_student(student: Student):
    rpta = students_controller.create_student(student)
    return rpta

@router.get("/get_student/{student_id}", response_model=Student)
async def get_student(student_id: int):
    rpta = students_controller.get_student(student_id)
    return rpta

@router.get("/get_students/")
async def get_students():
    rpta = students_controller.get_students()
    return rpta

@router.get("/get_students_by_career/{carrera}")
async def get_students_by_career(carrera: str):
    rpta = students_controller.get_students_by_career(carrera)
    return rpta

@router.put("/update_student/{student_id}")
async def update_student(student_id: int, student: Student):
    rpta = students_controller.update_student(student_id, student)
    return rpta

@router.delete("/delete_student/{student_id}")
async def delete_student(student_id: int):
    rpta = students_controller.delete_student(student_id)
    return rpta