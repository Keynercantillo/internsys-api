from pydantic import BaseModel
from typing import Optional
from datetime import date

class Report(BaseModel):
    id: Optional[int] = None
    generated_by: int
    report_type: str
    title: str
    content_json: Optional[str] = None
    generated_date: date
    file_url: Optional[str] = None
    filters_used: Optional[str] = None