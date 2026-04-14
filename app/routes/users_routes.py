from fastapi import APIRouter, HTTPException
from controllers.users_controller import UsersController
from models.users_model import User
from pydantic import BaseModel

router = APIRouter()
users_controller = UsersController()

# Modelo para login
class LoginRequest(BaseModel):
    email: str
    password: str

# ============================================
# ENDPOINTS DE USUARIOS
# ============================================

@router.post("/create_user")
async def create_user(user: User):
    rpta = users_controller.create_user(user)
    return rpta

@router.get("/get_user/{user_id}")
async def get_user(user_id: int):
    rpta = users_controller.get_user(user_id)
    return rpta

@router.get("/get_users/")
async def get_users():
    rpta = users_controller.get_users()
    return rpta

@router.get("/get_users_by_role/{role}")
async def get_users_by_role(role: str):
    rpta = users_controller.get_users_by_role(role)
    return rpta

@router.get("/get_user_by_email/{email}")
async def get_user_by_email(email: str):
    rpta = users_controller.get_user_by_email(email)
    return rpta

@router.put("/update_user/{user_id}")
async def update_user(user_id: int, user: User):
    rpta = users_controller.update_user(user_id, user)
    return rpta

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    rpta = users_controller.delete_user(user_id)
    return rpta

@router.post("/login")
async def login(login_data: LoginRequest):
    rpta = users_controller.login(login_data.email, login_data.password)
    return rpta