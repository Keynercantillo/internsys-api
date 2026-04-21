from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class Profile(BaseModel):
    id: Optional[int] = None
    user_id: int
    bio: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[date] = None
    profile_picture_url: Optional[str] = None
    social_links: Optional[str] = None
    # Campos de auditoría
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None