from pydantic import BaseModel
from typing import Optional
from datetime import date

class FollowupVisit(BaseModel):
    id: Optional[int] = None
    internship_assignment_id: int
    visit_date: date
    tutor_feedback: Optional[str] = None
    student_feedback: Optional[str] = None
    supervisor_name: Optional[str] = None
    observations: Optional[str] = None
    status: str = "pendiente"
    next_visit_date: Optional[date] = None