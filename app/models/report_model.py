from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Report(BaseModel):
    id: Optional[int] = None
    generated_by: int
    report_type: str
    title: str
    content_json: Optional[str] = None
    generated_date: date
    file_url: Optional[str] = None
    filters_used: Optional[str] = None
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None