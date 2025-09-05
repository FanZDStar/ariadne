# 风险评估报告API路由
# file: ariadne/backend/app/api/routes/risk_assessment.py

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.database.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.risk_assessment_report import RiskAssessmentReport
from app.services.risk_assessment_service import RiskAssessmentService

router = APIRouter()

# 请求模型
class GenerateReportRequest(BaseModel):
    session_id: str
    scene: str
    conversation_start_time: Optional[datetime] = None

class MarkViewedRequest(BaseModel):
    report_id: int

# 响应模型
class RiskAssessmentReportResponse(BaseModel):
    report_id: int
    session_id: str
    scene: str
    report_title: str
    report_content: str
    summary: str
    overall_risk_level: str
    overall_risk_score: float
    total_messages: int
    risk_messages_count: int
    detected_keywords: List[str]
    ai_analysis: str
    recommendations: List[str]
    conversation_start_time: Optional[datetime]
    conversation_end_time: Optional[datetime]
    report_generated_time: datetime
    is_viewed: bool
    version: int

class StatisticsResponse(BaseModel):
    total_reports: int
    avg_risk_score: float
    improvement_trend: float

@router.post("/generate-report", response_model=RiskAssessmentReportResponse)
async def generate_session_report(
    request: GenerateReportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    生成对话会话风险评估报告
    """
    try:
        service = RiskAssessmentService(db)
        
        # 异步生成报告
        report = await service.generate_session_report(
            user_id=current_user.user_id,
            session_id=request.session_id,
            scene=request.scene,
            conversation_start_time=request.conversation_start_time
        )
        
        if not report:
            raise HTTPException(status_code=400, detail="报告生成失败")
        
        return RiskAssessmentReportResponse(
            report_id=report.report_id,
            session_id=report.session_id,
            scene=report.scene,
            report_title=report.report_title,
            report_content=report.report_content,
            summary=report.summary,
            overall_risk_level=report.overall_risk_level,
            overall_risk_score=report.overall_risk_score,
            total_messages=report.total_messages,
            risk_messages_count=report.risk_messages_count,
            detected_keywords=report.detected_keywords or [],
            ai_analysis=report.ai_analysis or "",
            recommendations=report.recommendations or [],
            conversation_start_time=report.conversation_start_time,
            conversation_end_time=report.conversation_end_time,
            report_generated_time=report.report_generated_time,
            is_viewed=report.is_viewed,
            version=report.version
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成报告失败: {str(e)}")

@router.get("/latest-report/{session_id}", response_model=Optional[RiskAssessmentReportResponse])
async def get_latest_report(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定会话的最新风险评估报告
    """
    try:
        service = RiskAssessmentService(db)
        report = service.get_user_latest_report(current_user.user_id, session_id)
        
        if not report:
            return None
        
        return RiskAssessmentReportResponse(
            report_id=report.report_id,
            session_id=report.session_id,
            scene=report.scene,
            report_title=report.report_title,
            report_content=report.report_content,
            summary=report.summary,
            overall_risk_level=report.overall_risk_level,
            overall_risk_score=report.overall_risk_score,
            total_messages=report.total_messages,
            risk_messages_count=report.risk_messages_count,
            detected_keywords=report.detected_keywords or [],
            ai_analysis=report.ai_analysis or "",
            recommendations=report.recommendations or [],
            conversation_start_time=report.conversation_start_time,
            conversation_end_time=report.conversation_end_time,
            report_generated_time=report.report_generated_time,
            is_viewed=report.is_viewed,
            version=report.version
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报告失败: {str(e)}")

@router.post("/mark-viewed")
async def mark_report_viewed(
    request: MarkViewedRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    标记报告为已查看
    """
    try:
        service = RiskAssessmentService(db)
        success = service.mark_report_as_viewed(request.report_id, current_user.user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="报告不存在")
        
        return {"message": "报告已标记为已查看"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"标记失败: {str(e)}")

@router.get("/reports-history", response_model=List[RiskAssessmentReportResponse])
async def get_reports_history(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户的风险评估报告历史
    """
    try:
        service = RiskAssessmentService(db)
        reports = service.get_user_reports_history(current_user.user_id, limit)
        
        return [
            RiskAssessmentReportResponse(
                report_id=report.report_id,
                session_id=report.session_id,
                scene=report.scene,
                report_title=report.report_title,
                report_content=report.report_content,
                summary=report.summary,
                overall_risk_level=report.overall_risk_level,
                overall_risk_score=report.overall_risk_score,
                total_messages=report.total_messages,
                risk_messages_count=report.risk_messages_count,
                detected_keywords=report.detected_keywords or [],
                ai_analysis=report.ai_analysis or "",
                recommendations=report.recommendations or [],
                conversation_start_time=report.conversation_start_time,
                conversation_end_time=report.conversation_end_time,
                report_generated_time=report.report_generated_time,
                is_viewed=report.is_viewed,
                version=report.version
            )
            for report in reports
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取报告历史失败: {str(e)}")

@router.get("/statistics", response_model=StatisticsResponse)
async def get_risk_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户风险评估统计信息"""
    try:
        # 获取用户所有报告
        reports = db.query(RiskAssessmentReport).filter(
            RiskAssessmentReport.user_id == current_user.user_id
        ).order_by(RiskAssessmentReport.report_generated_time.desc()).all()
        
        if not reports:
            return StatisticsResponse(
                total_reports=0,
                avg_risk_score=0.0,
                improvement_trend=0.0
            )
        
        # 计算总报告数
        total_reports = len(reports)
        
        # 计算平均风险分数
        avg_risk_score = sum(report.overall_risk_score for report in reports) / total_reports
        
        # 计算改善趋势（比较最近和较早的报告）
        improvement_trend = 0.0
        if total_reports >= 2:
            # 取最近25%的报告作为近期数据
            recent_count = max(1, total_reports // 4)
            recent_reports = reports[:recent_count]
            earlier_reports = reports[recent_count:]
            
            if earlier_reports:
                recent_avg = sum(r.overall_risk_score for r in recent_reports) / len(recent_reports)
                earlier_avg = sum(r.overall_risk_score for r in earlier_reports) / len(earlier_reports)
                
                # 计算改善百分比（分数降低表示改善）
                if earlier_avg > 0:
                    improvement_trend = ((earlier_avg - recent_avg) / earlier_avg) * 100
        
        return StatisticsResponse(
            total_reports=total_reports,
            avg_risk_score=round(avg_risk_score, 2),
            improvement_trend=round(improvement_trend, 1)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")
