from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Application(BaseModel):
    id: Optional[int] = None
    offer_id: int
    student_id: int
    empresa_id: int
    tutor_id: Optional[int] = None
    status: str = "pendiente"
    application_date: date
    comments: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None