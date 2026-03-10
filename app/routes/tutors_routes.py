from fastapi import APIRouter, HTTPException
from controllers.tutors_controller import *
from models.tutor_model import Tutor

router = APIRouter()

nuevo_tutor = TutorsController()

@router.post("/create_tutor")
async def create_tutor(tutor: Tutor):
    rpta = nuevo_tutor.create_tutor(tutor)
    return rpta

@router.get("/get_tutor/{tutor_id}", response_model=Tutor)
async def get_tutor(tutor_id: int):
    rpta = nuevo_tutor.get_tutor(tutor_id)
    return rpta

@router.get("/get_tutors/")
async def get_tutors():
    rpta = nuevo_tutor.get_tutors()
    return rpta

@router.put("/update_tutor/{tutor_id}")
async def update_tutor(tutor_id: int, tutor: Tutor):
    rpta = nuevo_tutor.update_tutor(tutor_id, tutor)
    return rpta

@router.delete("/delete_tutor/{tutor_id}")
async def delete_tutor(tutor_id: int):
    rpta = nuevo_tutor.delete_tutor(tutor_id)
    return rpta