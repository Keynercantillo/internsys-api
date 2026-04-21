from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Agreement(BaseModel):
    id: Optional[int] = None
    student_id: int
    tutor_id: int
    company_id: int
    start_date: date
    end_date: date
    status: str = "activo"
    signed_date: Optional[date] = None
    file_url: Optional[str] = None
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None