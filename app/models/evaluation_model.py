from pydantic import BaseModel
from typing import Optional
from datetime import date

class Evaluation(BaseModel):
    id: Optional[int] = None
    internship_assignment_id: int
    evaluator_id: int
    evaluation_type: str
    score: float
    comments: Optional[str] = None
    evaluation_date: date
    criteria_json: Optional[str] = None