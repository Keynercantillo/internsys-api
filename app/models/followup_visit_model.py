from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FollowupVisit(BaseModel):
    id: Optional[int] = None
    student_name: str
    visit_date: Optional[datetime] = None
    observations: Optional[str] = None