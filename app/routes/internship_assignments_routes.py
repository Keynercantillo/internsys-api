from fastapi import APIRouter, HTTPException
from controllers.internship_assignments_controller import InternshipAssignmentController
from models.internship_assignments_model import InternshipAssignment

router = APIRouter()

internship_assignment_controller = InternshipAssignmentController()

@router.post("/create_assignment")
async def create_assignment(assignment: InternshipAssignment):
    rpta = internship_assignment_controller.create_assignment(assignment)
    return rpta

@router.get("/get_assignment/{assignment_id}", response_model=InternshipAssignment)
async def get_assignment(assignment_id: int):
    rpta = internship_assignment_controller.get_assignment(assignment_id)
    return rpta

@router.get("/get_assignments/")
async def get_assignments():
    rpta = internship_assignment_controller.get_assignments()
    return rpta

@router.get("/get_assignments_by_student/{student_id}")
async def get_assignments_by_student(student_id: int):
    rpta = internship_assignment_controller.get_assignments_by_student(student_id)
    return rpta

@router.put("/update_assignment/{assignment_id}")
async def update_assignment(assignment_id: int, assignment: InternshipAssignment):
    rpta = internship_assignment_controller.update_assignment(assignment_id, assignment)
    return rpta

@router.delete("/delete_assignment/{assignment_id}")
async def delete_assignment(assignment_id: int):
    rpta = internship_assignment_controller.delete_assignment(assignment_id)
    return rpta