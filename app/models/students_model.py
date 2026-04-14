from pydantic import BaseModel
from typing import Optional

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