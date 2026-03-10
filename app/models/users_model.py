from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: Optional[int] = None
    email: str
    password_hash: str
    role: str
    created_at: Optional[datetime] = None