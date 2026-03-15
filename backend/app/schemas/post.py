from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostCreate(BaseModel):
    title: str
    text: str


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    text: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
