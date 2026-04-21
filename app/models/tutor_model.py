from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Tutor(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: str
    contraseña: str
    tipo: str  # empresarial, academico
    especialidad: Optional[str] = None
    telefono: str
    email: str
    empresa_id: Optional[int] = None
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None