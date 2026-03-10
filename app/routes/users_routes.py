# routes/users_routes.py
from fastapi import APIRouter, HTTPException
from controllers.users_controller import *
from models.users_model import User

router = APIRouter()

nuevo_user = UsersController()

@router.post("/create_user")
async def create_user(user: User):
    rpta = nuevo_user.create_user(user)
    return rpta

@router.get("/get_user/{user_id}", response_model=User)
async def get_user(user_id: int):
    rpta = nuevo_user.get_user(user_id)
    return rpta

@router.get("/get_users/")
async def get_users():
    rpta = nuevo_user.get_users()
    return rpta

@router.get("/get_users_by_role/{role}")
async def get_users_by_role(role: str):
    rpta = nuevo_user.get_users_by_role(role)
    return rpta

@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: User):
    rpta = nuevo_user.update_user(user_id, user)
    return rpta

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    rpta = nuevo_user.delete_user(user_id)
    return rpta