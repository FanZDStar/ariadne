# backend/app/schemas/tree_hole_chat.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TreeHoleChatBase(BaseModel):
    content: str

class TreeHoleChatCreate(TreeHoleChatBase):
    pass

class TreeHoleChat(TreeHoleChatBase):
    chat_id: int
    whisper_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TreeHoleChatParticipant(BaseModel):
    anonymous_nickname: str
    anonymous_avatar: str

    class Config:
        from_attributes = True