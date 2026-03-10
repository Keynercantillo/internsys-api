from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Report(BaseModel):
    id: Optional[int] = None
    student_name: str
    file_url: str
    submission_date: Optional[datetime] = None