#file:ariadne/backend/app/api/routes/crisis_warning.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import logging

from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.crisis_warning import CrisisWarning, RiskLevel, WarningType
from app.services.crisis_warning_service import CrisisWarningService, RiskAssessmentResult
from app.schemas.crisis_warning import (
    CrisisWarningResponse, 
    RiskAssessmentResponse,
    WarningCreateRequest,
    WarningResolveRequest
)

# 新增：AI增强分析请求模型
class EnhancedRiskAssessmentRequest(BaseModel):
    content: str
    scene: Optional[str] = ""
    keyword_score: Optional[float] = 0
    enable_ai_analysis: Optional[bool] = True

# 新增：AI增强分析响应模型  
class EnhancedRiskAssessmentResponse(BaseModel):
    content: str
    risk_level: str
    risk_score: float
    keyword_score: float
    ai_analysis: Optional[str]
    detected_keywords: List[str]
    fuzzy_matches: List[str]
    scene: Optional[str]
    timestamp: datetime

router = APIRouter()
logger = logging.getLogger(__name__)

# 临时测试端点：无需认证的危机检测（用于测试修复效果）
@router.post("/assess-risk-test", response_model=EnhancedRiskAssessmentResponse)
async def assess_content_risk_test(
    request: EnhancedRiskAssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    临时测试端点：无认证的AI增强型内容风险评估
    仅用于测试修复效果，生产环境应删除此端点
    """
    try:
        service = CrisisWarningService(db)
        assessment = await service.analyze_content_with_ai(
            content=request.content,
            scene=request.scene,
            keyword_score=request.keyword_score,
            enable_ai_analysis=request.enable_ai_analysis
        )
        
        return EnhancedRiskAssessmentResponse(
            content=assessment.content,
            risk_level=assessment.risk_level.value,
            risk_score=assessment.risk_score,
            keyword_score=assessment.keyword_score,
            ai_analysis=assessment.ai_analysis,
            detected_keywords=assessment.detected_keywords,
            fuzzy_matches=assessment.fuzzy_matches,
            scene=assessment.scene,
            timestamp=assessment.timestamp
        )
        
    except Exception as e:
        logger.error(f"AI风险评估测试失败: {e}")
        # 返回基础安全响应
        return EnhancedRiskAssessmentResponse(
            content=request.content,
            risk_level="low",
            risk_score=0,
            keyword_score=request.keyword_score,
            ai_analysis=f"分析服务暂时不可用: {str(e)}",
            detected_keywords=[],
            fuzzy_matches=[],
            scene=request.scene,
            timestamp=datetime.now()
        )

@router.post("/assess-risk", response_model=EnhancedRiskAssessmentResponse)
async def assess_content_risk(
    request: EnhancedRiskAssessmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    AI增强型内容风险评估
    
    Args:
        request: 风险评估请求，包含内容、场景等信息
    """
    try:
        service = CrisisWarningService(db)
        assessment = await service.analyze_content_with_ai(
            content=request.content,
            scene=request.scene,
            keyword_score=request.keyword_score,
            enable_ai_analysis=request.enable_ai_analysis
        )
        
        # 如果风险等级为中等以上，自动创建预警记录
        if assessment.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]:
            service.create_warning(
                user_id=current_user.user_id,
                assessment=RiskAssessmentResult(
                    risk_level=assessment.risk_level,
                    score=assessment.risk_score,
                    reasons=[f"AI分析检测到风险内容: {assessment.content[:50]}..."],
                    recommendations=["建议寻求专业心理健康支持"],
                    ai_analysis=assessment.ai_analysis,
                    detected_keywords=assessment.detected_keywords
                ),
                warning_type=WarningType.CONTENT_ANALYSIS,
                source_data=assessment.content
            )
        
        return EnhancedRiskAssessmentResponse(
            content=assessment.content,
            risk_level=assessment.risk_level.value,
            risk_score=assessment.risk_score,
            keyword_score=assessment.keyword_score,
            ai_analysis=assessment.ai_analysis,
            detected_keywords=assessment.detected_keywords,
            fuzzy_matches=assessment.fuzzy_matches,
            scene=assessment.scene,
            timestamp=assessment.timestamp
        )
        
    except Exception as e:
        logger.error(f"AI风险评估失败: {e}")
        # 返回基础安全响应
        return EnhancedRiskAssessmentResponse(
            content=request.content,
            risk_level="low",
            risk_score=0,
            keyword_score=request.keyword_score,
            ai_analysis="分析服务暂时不可用",
            detected_keywords=[],
            fuzzy_matches=[],
            scene=request.scene,
            timestamp=datetime.now()
        )

@router.post("/assess-user-risk", response_model=RiskAssessmentResponse)  
async def assess_user_risk(
    days: int = 14,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    评估用户整体心理风险（原有功能保留）
    
    Args:
        days: 分析天数，默认14天
    """
    try:
        service = CrisisWarningService(db)
        assessment = service.analyze_user_risk(current_user.user_id, days)
        
        # 如果风险等级为高或紧急，自动创建预警记录
        if assessment.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            service.create_warning(
                user_id=current_user.user_id,
                assessment=assessment,
                warning_type=WarningType.AI_ANALYSIS,
                source_data=f"风险评估 - {days}天数据分析"
            )
        
        return RiskAssessmentResponse(
            risk_level=assessment.risk_level.value,
            score=assessment.score,
            reasons=assessment.reasons,
            recommendations=assessment.recommendations,
            assessment_date=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"风险评估失败: {str(e)}")
        raise HTTPException(status_code=500, detail="风险评估处理失败")

@router.get("/warnings", response_model=List[CrisisWarningResponse])
async def get_user_warnings(
    days: Optional[int] = 30,
    unresolved_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户的危机预警记录
    
    Args:
        days: 获取多少天内的记录，None表示获取全部
        unresolved_only: 是否只获取未解决的预警
    """
    try:
        service = CrisisWarningService(db)
        warnings = service.get_user_warnings(
            user_id=current_user.user_id,
            days=days,
            unresolved_only=unresolved_only
        )
        
        return [
            CrisisWarningResponse(
                warning_id=w.warning_id,
                warning_type=w.warning_type.value,
                risk_level=w.risk_level.value,
                score=w.score,
                title=w.title,
                description=w.description,
                is_resolved=w.is_resolved,
                created_at=w.created_at,
                resolved_at=w.resolved_at
            ) for w in warnings
        ]
        
    except Exception as e:
        logger.error(f"获取预警记录失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取预警记录失败")

@router.post("/warnings/{warning_id}/resolve")
async def resolve_warning(
    warning_id: int,
    request: WarningResolveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    解决预警（标记为已处理）
    """
    try:
        # 验证预警是否属于当前用户
        warning = db.query(CrisisWarning).filter(
            CrisisWarning.warning_id == warning_id,
            CrisisWarning.user_id == current_user.user_id
        ).first()
        
        if not warning:
            raise HTTPException(status_code=404, detail="预警记录不存在")
        
        service = CrisisWarningService(db)
        success = service.resolve_warning(warning_id, request.resolver_notes)
        
        if success:
            return {"message": "预警已标记为解决", "warning_id": warning_id}
        else:
            raise HTTPException(status_code=500, detail="解决预警失败")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"解决预警失败: {str(e)}")
        raise HTTPException(status_code=500, detail="解决预警失败")

@router.post("/background-check")
async def trigger_background_risk_check(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    触发后台风险检查（用于定时任务或实时检查）
    """
    def check_user_risk():
        try:
            service = CrisisWarningService(db)
            assessment = service.analyze_user_risk(current_user.user_id, 7)  # 检查7天数据
            
            # 如果风险等级为中等及以上，创建预警
            if assessment.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]:
                service.create_warning(
                    user_id=current_user.user_id,
                    assessment=assessment,
                    warning_type=WarningType.BEHAVIOR_PATTERN,
                    source_data="后台自动风险检查"
                )
                logger.info(f"为用户 {current_user.user_id} 创建了后台风险预警")
        except Exception as e:
            logger.error(f"后台风险检查失败: {str(e)}")
    
    background_tasks.add_task(check_user_risk)
    return {"message": "后台风险检查已启动"}

@router.get("/statistics")
async def get_risk_statistics(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户的风险统计信息
    """
    try:
        service = CrisisWarningService(db)
        
        # 获取指定天数内的预警记录
        warnings = service.get_user_warnings(current_user.user_id, days, False)
        
        # 统计各种风险等级的数量
        risk_stats = {
            "low": 0,
            "medium": 0, 
            "high": 0,
            "critical": 0
        }
        
        warning_type_stats = {
            "mood_trend": 0,
            "keyword_alert": 0,
            "ai_analysis": 0,
            "behavior_pattern": 0
        }
        
        for warning in warnings:
            risk_stats[warning.risk_level.value] += 1
            warning_type_stats[warning.warning_type.value] += 1
        
        # 计算当前风险评估
        current_assessment = service.analyze_user_risk(current_user.user_id, 7)
        
        return {
            "period_days": days,
            "total_warnings": len(warnings),
            "unresolved_warnings": len([w for w in warnings if not w.is_resolved]),
            "risk_level_distribution": risk_stats,
            "warning_type_distribution": warning_type_stats,
            "current_risk_level": current_assessment.risk_level.value,
            "current_risk_score": current_assessment.score,
            "last_assessment": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"获取风险统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取统计信息失败")
