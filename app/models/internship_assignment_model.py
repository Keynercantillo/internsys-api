from pydantic import BaseModel
from typing import Optional

class InternshipAssignment(BaseModel):
    id: Optional[int] = None
    student_name: str
    offer_title: str
    tutor_name: str
    process_status: str = "in_progress"