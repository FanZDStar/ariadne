"""
心灵预警检测API
提供统一的危机检测接口，供前端调用
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, List

from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.crisis_detector_component import get_crisis_detector, CrisisDetectionResult

router = APIRouter(prefix="/crisis-detection", tags=["心灵预警"])


class CrisisDetectionRequest(BaseModel):
    """危机检测请求"""
    content: str = Field(..., description="待检测内容")
    scene: str = Field(default="tree-hole", description="场景类型：tree-hole, diary, chat等")
    enable_ai: bool = Field(default=True, description="是否启用AI分析")


class CrisisDetectionResponse(BaseModel):
    """危机检测响应"""
    has_risk: bool = Field(description="是否存在风险")
    risk_level: str = Field(description="风险等级：low, medium, high, critical")
    risk_score: float = Field(description="风险分数 0-100")
    ai_brief_analysis: Optional[str] = Field(description="AI简短分析（约30字）")
    should_show_bubble: bool = Field(description="是否显示看板娘气泡")
    bubble_message: Optional[str] = Field(description="气泡消息内容")
    detected_keywords: List[str] = Field(default=[], description="检测到的关键词")
    recommendations: List[str] = Field(default=[], description="建议")


@router.post("/analyze", response_model=CrisisDetectionResponse)
async def analyze_content(
    request: CrisisDetectionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    分析内容的心理风险
    
    用于悄悄话、日记、聊天等内容发布前的实时检测
    """
    detector = get_crisis_detector(db)
    
    result = await detector.detect_content_risk(
        content=request.content,
        scene=request.scene,
        user_id=current_user.user_id,
        enable_ai=request.enable_ai
    )
    
    return CrisisDetectionResponse(
        has_risk=result.has_risk,
        risk_level=result.risk_level,
        risk_score=result.risk_score,
        ai_brief_analysis=result.ai_brief_analysis,
        should_show_bubble=result.should_show_bubble,
        bubble_message=result.bubble_message,
        detected_keywords=result.detected_keywords,
        recommendations=result.recommendations
    )


@router.post("/quick-check")
async def quick_keyword_check(
    request: CrisisDetectionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    快速关键词检测（不使用AI，适合实时检测）
    
    前端可以在用户输入时实时调用此接口，性能更好
    """
    from app.services.crisis_warning_service import CrisisWarningService
    
    service = CrisisWarningService(None)  # 不需要db的快速检测
    keyword_result = service._enhanced_keyword_detection(request.content)
    
    has_risk = len(keyword_result['keywords']) > 0 or len(keyword_result['fuzzy_matches']) > 0
    
    return {
        "has_risk": has_risk,
        "detected_keywords": keyword_result['keywords'],
        "fuzzy_matches": keyword_result['fuzzy_matches'],
        "categories": keyword_result['categories'],
        "score": keyword_result['score']
    }
