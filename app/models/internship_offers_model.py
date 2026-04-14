from pydantic import BaseModel
from typing import Optional
from datetime import date

class InternshipOffer(BaseModel):
    id: Optional[int] = None
    company_id: int
    title: str  # ← CORREGIDO: title en lugar de titulo
    description: Optional[str] = None  # ← CORREGIDO: description
    required_skills: Optional[str] = None
    available_positions: int  # ← CORREGIDO: available_positions
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "disponible"  # ← CORREGIDO: status
    requirements: Optional[str] = None