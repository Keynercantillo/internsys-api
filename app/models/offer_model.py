from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class InternshipOffer(BaseModel):
    id: Optional[int] = None
    company_id: int
    title: str
    description: Optional[str] = None
    available_positions: int = 1
    required_skills: Optional[str] = None
    requirements: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "disponible"
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None