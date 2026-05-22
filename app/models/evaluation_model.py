from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Evaluation(BaseModel):
    id: Optional[int] = None
    internship_assignment_id: int
    evaluator_id: int  # ID del tutor que evalúa
    evaluation_type: Optional[str] = "desempeño"
    score: Optional[float] = None
    comments: Optional[str] = None
    evaluation_date: date
    criteria_json: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None