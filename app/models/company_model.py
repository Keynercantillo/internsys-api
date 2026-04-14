from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    id: Optional[int] = None
    name: str
    ruc: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    contact_person: Optional[str] = None
    sector: Optional[str] = None
    status: str = "activo"