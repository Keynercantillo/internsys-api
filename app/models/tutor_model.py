from pydantic import BaseModel
from typing import Optional

class Tutor(BaseModel):
    id: Optional[int] = None
    tutor_name: str
    department_faculty: str