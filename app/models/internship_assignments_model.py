from pydantic import BaseModel
from typing import Optional
from datetime import date

class InternshipAssignment(BaseModel):
    id: Optional[int] = None
    student_id: int
    internship_offer_id: int
    tutor_id: int
    assignment_date: date
    start_date: date
    end_date: date
    status: str = "activo"
    schedule: Optional[str] = None
    total_hours: int
    completed_hours: int = 0
    # Campos adicionales para mostrar (no se guardan)
    student_nombre: Optional[str] = None
    offer_title: Optional[str] = None
    tutor_nombre: Optional[str] = None