from fastapi import APIRouter, HTTPException
from controllers.tutors_controller import TutorsController
from models.tutor_model import Tutor

router = APIRouter()

tutors_controller = TutorsController()

@router.post("/create_tutor")
async def create_tutor(tutor: Tutor):
    rpta = tutors_controller.create_tutor(tutor)
    return rpta

@router.get("/get_tutor/{tutor_id}", response_model=Tutor)
async def get_tutor(tutor_id: int):
    rpta = tutors_controller.get_tutor(tutor_id)
    return rpta

@router.get("/get_tutors/")
async def get_tutors():
    rpta = tutors_controller.get_tutors()
    return rpta

@router.get("/get_tutors_by_type/{tipo}")
async def get_tutors_by_type(tipo: str):
    rpta = tutors_controller.get_tutors_by_type(tipo)
    return rpta

@router.put("/update_tutor/{tutor_id}")
async def update_tutor(tutor_id: int, tutor: Tutor):
    rpta = tutors_controller.update_tutor(tutor_id, tutor)
    return rpta

@router.delete("/delete_tutor/{tutor_id}")
async def delete_tutor(tutor_id: int):
    rpta = tutors_controller.delete_tutor(tutor_id)
    return rpta