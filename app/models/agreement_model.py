from pydantic import BaseModel
from typing import Optional
from datetime import date

class Agreement(BaseModel):
    id: Optional[int] = None
    company_name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "active"