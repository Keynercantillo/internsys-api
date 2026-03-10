from pydantic import BaseModel
from typing import Optional

class InternshipOffer(BaseModel):
    id: Optional[int] = None
    offer_title: str
    company_name: str
    description: Optional[str] = None