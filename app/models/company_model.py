from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None