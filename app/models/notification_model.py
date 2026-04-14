from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    id: Optional[int] = None
    user_id: int
    title: str
    message: str
    type: str
    read: bool = False
    created_at: Optional[datetime] = None
    link_url: Optional[str] = None