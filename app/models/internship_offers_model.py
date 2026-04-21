from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class InternshipOffer(BaseModel):
    id: Optional[int] = None
    company_id: int
    title: str
    description: Optional[str] = None
    required_skills: Optional[str] = None
    available_positions: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "disponible"
    requirements: Optional[str] = None
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None