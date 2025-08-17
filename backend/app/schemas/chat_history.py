from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatMessageBase(BaseModel):
    role: str = Field(..., description="消息角色: user 或 assistant")
    content: str = Field(..., description="消息内容")

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessage(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatSessionBase(BaseModel):
    scene: str = Field(..., description="对话场景: self-dialog, love-experiment, love-yourself")
    title: str = Field(..., description="对话标题")

class ChatSessionCreate(ChatSessionBase):
    messages: List[ChatMessageCreate] = Field(..., description="对话消息列表")

class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None

class ChatSession(ChatSessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessage] = []
    
    class Config:
        from_attributes = True

class SaveChatRequest(BaseModel):
    scene: str = Field(..., description="对话场景")
    messages: List[ChatMessageCreate] = Field(..., description="要保存的消息列表")
    title: Optional[str] = Field(None, description="对话标题，如果不提供则自动生成")
    session_id: Optional[int] = Field(None, description="现有会话ID，如果提供则更新现有会话")

class ChatHistoryResponse(BaseModel):
    sessions: List[ChatSession]
    total: int
