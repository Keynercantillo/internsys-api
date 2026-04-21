from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: str
    contraseña: str
    rol: str
    email: str
    is_active: bool = True
    last_login: Optional[datetime] = None
    empresa_id: Optional[int] = None
    # Campos adicionales para tutores
    telefono: Optional[str] = None
    tipo: Optional[str] = None
    especialidad: Optional[str] = None
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None