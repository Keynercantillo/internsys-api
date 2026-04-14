from fastapi import APIRouter, HTTPException
from controllers.evaluations_controller import EvaluationsController
from models.evaluation_model import Evaluation

router = APIRouter()

evaluations_controller = EvaluationsController()

@router.post("/create_evaluation")
async def create_evaluation(evaluation: Evaluation):
    rpta = evaluations_controller.create_evaluation(evaluation)
    return rpta

@router.get("/get_evaluation/{evaluation_id}", response_model=Evaluation)
async def get_evaluation(evaluation_id: int):
    rpta = evaluations_controller.get_evaluation(evaluation_id)
    return rpta

@router.get("/get_evaluations/")
async def get_evaluations():
    rpta = evaluations_controller.get_evaluations()
    return rpta

@router.get("/get_evaluations_by_student/{student_id}")
async def get_evaluations_by_student(student_id: int):
    rpta = evaluations_controller.get_evaluations_by_student(student_id)
    return rpta

@router.put("/update_evaluation/{evaluation_id}")
async def update_evaluation(evaluation_id: int, evaluation: Evaluation):
    rpta = evaluations_controller.update_evaluation(evaluation_id, evaluation)
    return rpta

@router.delete("/delete_evaluation/{evaluation_id}")
async def delete_evaluation(evaluation_id: int):
    rpta = evaluations_controller.delete_evaluation(evaluation_id)
    return rpta