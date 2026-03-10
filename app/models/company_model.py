from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    id: Optional[int] = None
    company_name: str
    user_email: str
    tax_id_number: str