from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Student(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: str
    contraseña: str
    matricula: str
    carrera: str
    semester: int
    promedio: Optional[float] = None
    tutor_academico_id: Optional[int] = None
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None