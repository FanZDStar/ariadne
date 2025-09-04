#file:ariadne/backend/app/schemas/crisis_warning.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RiskAssessmentResponse(BaseModel):
    """风险评估响应"""
    risk_level: str  # low, medium, high, critical
    score: float     # 0-100的风险评分
    reasons: List[str]  # 风险原因列表
    recommendations: List[str]  # 建议列表
    assessment_date: datetime
    
    class Config:
        from_attributes = True

class CrisisWarningResponse(BaseModel):
    """危机预警响应"""
    warning_id: int
    warning_type: str  # mood_trend, keyword_alert, ai_analysis, behavior_pattern
    risk_level: str    # low, medium, high, critical
    score: float
    title: str
    description: str
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WarningCreateRequest(BaseModel):
    """创建预警请求"""
    warning_type: str
    risk_level: str
    score: float
    title: str
    description: str
    source_data: Optional[str] = None

class WarningResolveRequest(BaseModel):
    """解决预警请求"""
    resolver_notes: Optional[str] = None

class MoodTrendResponse(BaseModel):
    """心情趋势响应"""
    analysis_id: int
    period_days: int
    avg_mood_score: float
    mood_trend: str  # declining, stable, improving
    consecutive_low_days: int
    risk_indicators: List[str]
    recommendations: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class KeywordAlertRequest(BaseModel):
    """关键词预警请求"""
    content: str
    source: str  # diary, chat, etc.

class KeywordAlertResponse(BaseModel):
    """关键词预警响应"""
    detected_keywords: dict  # {category: [keywords]}
    risk_score: float
    risk_level: str
    recommendations: List[str]
