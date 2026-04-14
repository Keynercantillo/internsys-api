from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from controllers.users_controller import UsersController
from models.users_model import User

router = APIRouter()
users_controller = UsersController()

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: str
    contraseña: str
    email: str
    rol: str = "estudiante"

@router.post("/auth/login")
async def login(login_data: LoginRequest):
    rpta = users_controller.login(login_data.email, login_data.password)
    return rpta

@router.post("/auth/register")
async def register(register_data: RegisterRequest):
    user = User(
        nombre=register_data.nombre,
        apellido=register_data.apellido,
        cedula=register_data.cedula,
        edad=register_data.edad,
        usuario=register_data.usuario,
        contraseña=register_data.contraseña,
        rol=register_data.rol,
        email=register_data.email
    )
    rpta = users_controller.create_user(user)
    return rpta

@router.post("/auth/logout")
async def logout():
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/auth/verify")
async def verify_token():
    return {"valid": True}