from fastapi import APIRouter, HTTPException, Depends
from controllers.evaluations_controller import EvaluationsController
from models.evaluation_model import Evaluation

router = APIRouter()
evaluations_controller = EvaluationsController()

@router.post("/create_evaluation")
async def create_evaluation(evaluation: Evaluation):
    """Crear una evaluación (solo tutor asignado)"""
    rpta = evaluations_controller.create_evaluation(evaluation)
    return rpta

@router.get("/get_evaluations_by_tutor/{tutor_id}")
async def get_evaluations_by_tutor(tutor_id: int):
    """Obtener evaluaciones hechas por un tutor"""
    rpta = evaluations_controller.get_evaluations_by_tutor(tutor_id)
    return rpta

@router.get("/get_evaluations_by_student_and_tutor/{student_id}/{tutor_id}")
async def get_evaluations_by_student_and_tutor(student_id: int, tutor_id: int):
    """Obtener evaluaciones de un estudiante por un tutor"""
    rpta = evaluations_controller.get_evaluations_by_student_and_tutor(student_id, tutor_id)
    return rpta

@router.put("/update_evaluation/{evaluation_id}/{tutor_id}")
async def update_evaluation(evaluation_id: int, tutor_id: int, evaluation: Evaluation):
    """Actualizar evaluación (solo el tutor que la creó)"""
    rpta = evaluations_controller.update_evaluation(evaluation_id, evaluation, tutor_id)
    return rpta

@router.delete("/delete_evaluation/{evaluation_id}/{tutor_id}")
async def delete_evaluation(evaluation_id: int, tutor_id: int):
    """Eliminar evaluación (solo el tutor que la creó)"""
    rpta = evaluations_controller.delete_evaluation(evaluation_id, tutor_id)
    return rpta