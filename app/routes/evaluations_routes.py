from fastapi import APIRouter, HTTPException
from controllers.evaluations_controller import *
from models.evaluation_model import Evaluation

router = APIRouter()

nueva_evaluation = EvaluationsController()

@router.post("/create_evaluation")
async def create_evaluation(evaluation: Evaluation):
    rpta = nueva_evaluation.create_evaluation(evaluation)
    return rpta

@router.get("/get_evaluation/{evaluation_id}", response_model=Evaluation)
async def get_evaluation(evaluation_id: int):
    rpta = nueva_evaluation.get_evaluation(evaluation_id)
    return rpta

@router.get("/get_evaluations/")
async def get_evaluations():
    rpta = nueva_evaluation.get_evaluations()
    return rpta

@router.get("/get_evaluation_by_assignment/{assignment_id}")
async def get_evaluation_by_assignment(assignment_id: int):
    rpta = nueva_evaluation.get_evaluation_by_assignment(assignment_id)
    return rpta

@router.get("/get_evaluations_by_student/{student_id}")
async def get_evaluations_by_student(student_id: int):
    rpta = nueva_evaluation.get_evaluations_by_student(student_id)
    return rpta

@router.put("/update_evaluation/{evaluation_id}")
async def update_evaluation(evaluation_id: int, evaluation: Evaluation):
    rpta = nueva_evaluation.update_evaluation(evaluation_id, evaluation)
    return rpta

@router.delete("/delete_evaluation/{evaluation_id}")
async def delete_evaluation(evaluation_id: int):
    rpta = nueva_evaluation.delete_evaluation(evaluation_id)
    return rpta