from pydantic import BaseModel
from typing import Optional

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