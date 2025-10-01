from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class MessageSchema(BaseModel):
    """对话消息模式"""
    role: str = Field(..., description="角色: user 或 assistant")
    content: str = Field(..., description="消息内容")
    timestamp: Optional[datetime] = Field(None, description="消息时间戳")

class InterpersonalPracticeSessionBase(BaseModel):
    """人际沟通练习会话基础模式"""
    session_title: str = Field(..., description="会话标题")
    practice_scenario: str = Field(..., description="练习场景类型")
    practice_scenario_name: str = Field(..., description="练习场景名称")
    scenario_description: Optional[str] = Field(None, description="场景描述")
    practice_type: str = Field(default="ai_dialog", description="练习类型")
    difficulty_level: Optional[str] = Field(None, description="难度等级")

class InterpersonalPracticeSessionCreate(InterpersonalPracticeSessionBase):
    """创建人际沟通练习会话模式"""
    messages: List[Dict[str, Any]] = Field(default=[], description="对话消息数组")
    practice_duration: Optional[int] = Field(default=0, description="练习时长(秒)")
    practice_quality_score: Optional[float] = Field(None, description="练习质量评分")
    ai_feedback: Optional[str] = Field(None, description="AI反馈")
    strengths: Optional[List[str]] = Field(default=[], description="优势点")
    improvements: Optional[List[str]] = Field(default=[], description="改进建议")
    skills_practiced: Optional[List[str]] = Field(default=[], description="练习的技能")
    completion_status: str = Field(default="completed", description="完成状态")

class InterpersonalPracticeSessionUpdate(BaseModel):
    """更新人际沟通练习会话模式"""
    session_title: Optional[str] = Field(None, description="会话标题")
    practice_quality_score: Optional[float] = Field(None, description="练习质量评分")
    ai_feedback: Optional[str] = Field(None, description="AI反馈")
    strengths: Optional[List[str]] = Field(None, description="优势点")
    improvements: Optional[List[str]] = Field(None, description="改进建议")
    skills_practiced: Optional[List[str]] = Field(None, description="练习的技能")
    is_favorite: Optional[bool] = Field(None, description="是否收藏")
    user_rating: Optional[int] = Field(None, description="用户评分")
    user_notes: Optional[str] = Field(None, description="用户笔记")

class InterpersonalPracticeSessionResponse(InterpersonalPracticeSessionBase):
    """人际沟通练习会话响应模式"""
    id: int = Field(..., description="会话ID")
    user_id: int = Field(..., description="用户ID")
    messages: List[Dict[str, Any]] = Field(default=[], description="对话消息数组")
    total_messages: int = Field(default=0, description="消息总数")
    practice_duration: int = Field(default=0, description="练习时长(秒)")
    start_time: datetime = Field(..., description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    practice_quality_score: Optional[float] = Field(None, description="练习质量评分")
    ai_feedback: Optional[str] = Field(None, description="AI反馈")
    strengths: Optional[List[str]] = Field(default=[], description="优势点")
    improvements: Optional[List[str]] = Field(default=[], description="改进建议")
    skills_practiced: Optional[List[str]] = Field(default=[], description="练习的技能")
    skill_improvements: Optional[List[Dict[str, Any]]] = Field(default=[], description="技能改进记录")
    completion_status: str = Field(default="completed", description="完成状态")
    is_favorite: bool = Field(default=False, description="是否收藏")
    user_rating: Optional[int] = Field(None, description="用户评分")
    user_notes: Optional[str] = Field(None, description="用户笔记")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

class InterpersonalPracticeSessionList(BaseModel):
    """人际沟通练习会话列表响应模式"""
    sessions: List[InterpersonalPracticeSessionResponse] = Field(..., description="会话列表")
    total: int = Field(..., description="总数")
    skip: int = Field(..., description="跳过数量")
    limit: int = Field(..., description="限制数量")

class PracticeStatistics(BaseModel):
    """练习统计模式"""
    total_sessions: int = Field(..., description="总练习次数")
    total_duration: int = Field(..., description="总练习时长")
    average_score: float = Field(..., description="平均得分")
    favorite_sessions: int = Field(..., description="收藏的会话数")
    practice_scenarios: Dict[str, int] = Field(..., description="场景分布")
    recent_activity: List[Dict[str, Any]] = Field(..., description="最近活动")

class SessionAnalysis(BaseModel):
    """会话分析模式"""
    session_id: int = Field(..., description="会话ID")
    session_title: str = Field(..., description="会话标题")
    total_messages: int = Field(..., description="消息总数")
    practice_duration: int = Field(..., description="练习时长")
    quality_score: Optional[float] = Field(None, description="质量评分")
    strengths: Optional[List[str]] = Field(None, description="优势点")
    improvements: Optional[List[str]] = Field(None, description="改进建议")
    skills_practiced: Optional[List[str]] = Field(None, description="练习的技能")
    ai_feedback: Optional[str] = Field(None, description="AI反馈")
    message_analysis: Dict[str, Any] = Field(..., description="消息分析")