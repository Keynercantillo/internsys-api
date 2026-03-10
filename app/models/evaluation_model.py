from pydantic import BaseModel
from typing import Optional

class Evaluation(BaseModel):
    id: Optional[int] = None
    student_name: str
    score: float
    comments: Optional[str] = None