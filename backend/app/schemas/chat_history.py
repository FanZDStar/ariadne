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

class StarRewardInfo(BaseModel):
    """星点奖励信息"""
    earned_points: int = Field(0, description="获得的星点数量")
    is_rewarded: bool = Field(False, description="是否有奖励")
    action_type: Optional[str] = Field(None, description="奖励类型")
    description: Optional[str] = Field(None, description="奖励描述")
    show_toast: bool = Field(False, description="是否显示奖励提示")

class AffectionRewardInfo(BaseModel):
    """好感度奖励信息"""
    earned_affection: int = Field(0, description="获得的好感度数量")
    is_rewarded: bool = Field(False, description="是否有奖励")
    action_type: Optional[str] = Field(None, description="奖励类型")
    description: Optional[str] = Field(None, description="奖励描述")
    level_up: bool = Field(False, description="是否升级")
    new_level: Optional[int] = Field(None, description="新等级")
    show_toast: bool = Field(False, description="是否显示奖励提示")

class ChatSessionWithRewardResponse(ChatSession):
    """包含星点奖励和好感度奖励信息的聊天会话响应"""
    star_reward: StarRewardInfo = Field(default_factory=StarRewardInfo, description="星点奖励信息")
    affection_reward: AffectionRewardInfo = Field(default_factory=AffectionRewardInfo, description="好感度奖励信息")

class ChatSessionWithStarResponse(ChatSession):
    """包含星点奖励信息的聊天会话响应（保持向后兼容）"""
    star_reward: StarRewardInfo = Field(default_factory=StarRewardInfo, description="星点奖励信息")
