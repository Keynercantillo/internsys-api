from fastapi import APIRouter, HTTPException
from controllers.internship_assignments_controller import *
from models.internship_assignment_model import InternshipAssignment

router = APIRouter()

nueva_assignment = InternshipAssignmentsController()

@router.post("/create_internship_assignment")
async def create_internship_assignment(assignment: InternshipAssignment):
    rpta = nueva_assignment.create_assignment(assignment)
    return rpta

@router.get("/get_internship_assignment/{assignment_id}", response_model=InternshipAssignment)
async def get_internship_assignment(assignment_id: int):
    rpta = nueva_assignment.get_assignment(assignment_id)
    return rpta

@router.get("/get_internship_assignments/")
async def get_internship_assignments():
    rpta = nueva_assignment.get_assignments()
    return rpta

@router.get("/get_internship_assignments_by_student/{student_id}")
async def get_internship_assignments_by_student(student_id: int):
    rpta = nueva_assignment.get_assignments_by_student(student_id)
    return rpta

@router.get("/get_internship_assignments_by_tutor/{tutor_id}")
async def get_internship_assignments_by_tutor(tutor_id: int):
    rpta = nueva_assignment.get_assignments_by_tutor(tutor_id)
    return rpta

@router.put("/update_internship_assignment/{assignment_id}")
async def update_internship_assignment(assignment_id: int, assignment: InternshipAssignment):
    rpta = nueva_assignment.update_assignment(assignment_id, assignment)
    return rpta

@router.put("/complete_internship_assignment/{assignment_id}")
async def complete_internship_assignment(assignment_id: int, grade: float, observations: str):
    rpta = nueva_assignment.complete_assignment(assignment_id, grade, observations)
    return rpta

@router.delete("/delete_internship_assignment/{assignment_id}")
async def delete_internship_assignment(assignment_id: int):
    rpta = nueva_assignment.delete_assignment(assignment_id)
    return rpta