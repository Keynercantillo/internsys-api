from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    id: Optional[int] = None
    user_email: str
    message: str
    is_read: bool = False
    created_at: Optional[datetime] = None