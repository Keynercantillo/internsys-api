from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    id: Optional[int] = None
    student_name: str
    student_id_code: str
    major: str