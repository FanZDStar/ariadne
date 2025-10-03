from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
from decimal import Decimal

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.protection_drill_report import (
    ProtectionDrillReportCreate,
    ProtectionDrillReportResponse,
    ProtectionDrillReportList,
    ProtectionDrillStatistics
)
from app.services.ai_analysis_service import ai_analysis_service

router = APIRouter()

@router.post("/reports", response_model=ProtectionDrillReportResponse)
async def create_protection_drill_report(
    report_data: ProtectionDrillReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建防护训练报告"""
    try:
        # 自动生成AI分析
        generated_report_content = None
        
        # 如果用户没有提供report_content，并且提供了答题数据，则生成AI分析
        if not report_data.report_content and report_data.answers and report_data.correct_answers_list:
            try:
                ai_analysis = ai_analysis_service.generate_protection_drill_analysis(
                    drill_type=report_data.drill_type,
                    scenario_name=report_data.scenario_name,
                    total_questions=report_data.total_questions,
                    correct_answers=report_data.correct_answers,
                    score=float(report_data.score),
                    answers=report_data.answers,
                    correct_answers_list=report_data.correct_answers_list,
                    questions_data=report_data.questions_data,
                    completion_time=report_data.completion_time
                )
                generated_report_content = json.dumps(ai_analysis, ensure_ascii=False)
            except Exception as ai_error:
                # 如果AI分析失败，记录错误但继续创建报告
                print(f"AI分析生成失败: {ai_error}")
                generated_report_content = None
        
        # 使用生成的或用户提供的report_content
        final_report_content = generated_report_content or report_data.report_content
        
        insert_sql = """
        INSERT INTO protection_drill_reports 
        (user_id, drill_type, scenario_name, total_questions, correct_answers, 
         score, completion_time, report_content, suggestions)
        VALUES (:user_id, :drill_type, :scenario_name, :total_questions, :correct_answers,
         :score, :completion_time, :report_content, :suggestions)
        """
        
        result = db.execute(text(insert_sql), {
            'user_id': current_user.user_id,
            'drill_type': report_data.drill_type,
            'scenario_name': report_data.scenario_name,
            'total_questions': report_data.total_questions,
            'correct_answers': report_data.correct_answers,
            'score': float(report_data.score),
            'completion_time': report_data.completion_time,
            'report_content': final_report_content,
            'suggestions': report_data.suggestions
        })
        
        db.commit()
        
        # 获取创建的报告
        report_id = result.lastrowid
        select_sql = """
        SELECT * FROM protection_drill_reports WHERE id = :id
        """
        report = db.execute(text(select_sql), {'id': report_id}).fetchone()
        
        return ProtectionDrillReportResponse(
            id=report.id,
            user_id=report.user_id,
            drill_type=report.drill_type,
            scenario_name=report.scenario_name,
            total_questions=report.total_questions,
            correct_answers=report.correct_answers,
            score=Decimal(str(report.score)),
            completion_time=report.completion_time,
            report_content=report.report_content,
            suggestions=report.suggestions,
            created_at=report.created_at,
            updated_at=report.updated_at
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"创建报告失败: {str(e)}")

@router.get("/reports", response_model=ProtectionDrillReportList)
async def get_protection_drill_reports(
    skip: int = Query(default=0, ge=0, description="跳过数量"),
    limit: int = Query(default=20, ge=1, le=100, description="限制数量"),
    drill_type: Optional[str] = Query(default=None, description="训练类型筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的防护训练报告列表"""
    try:
        # 构建查询条件
        where_conditions = ["user_id = :user_id"]
        params = {'user_id': current_user.user_id}
        
        if drill_type:
            where_conditions.append("drill_type = :drill_type")
            params['drill_type'] = drill_type
        
        where_clause = " AND ".join(where_conditions)
        
        # 获取总数
        count_sql = f"""
        SELECT COUNT(*) as total FROM protection_drill_reports 
        WHERE {where_clause}
        """
        total = db.execute(text(count_sql), params).fetchone().total
        
        # 获取报告列表
        select_sql = f"""
        SELECT * FROM protection_drill_reports 
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :skip
        """
        params.update({'skip': skip, 'limit': limit})
        reports = db.execute(text(select_sql), params).fetchall()
        
        report_list = []
        for report in reports:
            report_list.append(ProtectionDrillReportResponse(
                id=report.id,
                user_id=report.user_id,
                drill_type=report.drill_type,
                scenario_name=report.scenario_name,
                total_questions=report.total_questions,
                correct_answers=report.correct_answers,
                score=Decimal(str(report.score)),
                completion_time=report.completion_time,
                report_content=report.report_content,
                suggestions=report.suggestions,
                created_at=report.created_at,
                updated_at=report.updated_at
            ))
        
        return ProtectionDrillReportList(
            reports=report_list,
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取报告列表失败: {str(e)}")

@router.get("/reports/{report_id}", response_model=ProtectionDrillReportResponse)
async def get_protection_drill_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取单个防护训练报告详情"""
    try:
        select_sql = """
        SELECT * FROM protection_drill_reports 
        WHERE id = :id AND user_id = :user_id
        """
        report = db.execute(text(select_sql), {
            'id': report_id,
            'user_id': current_user.user_id
        }).fetchone()
        
        if not report:
            raise HTTPException(status_code=404, detail="报告不存在")
        
        return ProtectionDrillReportResponse(
            id=report.id,
            user_id=report.user_id,
            drill_type=report.drill_type,
            scenario_name=report.scenario_name,
            total_questions=report.total_questions,
            correct_answers=report.correct_answers,
            score=Decimal(str(report.score)),
            completion_time=report.completion_time,
            report_content=report.report_content,
            suggestions=report.suggestions,
            created_at=report.created_at,
            updated_at=report.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取报告详情失败: {str(e)}")

@router.get("/statistics", response_model=ProtectionDrillStatistics)
async def get_protection_drill_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的防护训练统计信息"""
    try:
        # 获取总报告数和平均分
        stats_sql = """
        SELECT 
            COUNT(*) as total_reports,
            AVG(score) as average_score
        FROM protection_drill_reports 
        WHERE user_id = :user_id
        """
        stats = db.execute(text(stats_sql), {'user_id': current_user.user_id}).fetchone()
        
        # 获取训练类型分布
        distribution_sql = """
        SELECT drill_type, COUNT(*) as count
        FROM protection_drill_reports 
        WHERE user_id = :user_id
        GROUP BY drill_type
        ORDER BY count DESC
        """
        distribution = db.execute(text(distribution_sql), {'user_id': current_user.user_id}).fetchall()
        drill_type_distribution = {row.drill_type: row.count for row in distribution}
        
        # 获取最近5个报告
        recent_sql = """
        SELECT * FROM protection_drill_reports 
        WHERE user_id = :user_id
        ORDER BY created_at DESC
        LIMIT 5
        """
        recent_reports = db.execute(text(recent_sql), {'user_id': current_user.user_id}).fetchall()
        
        recent_list = []
        for report in recent_reports:
            recent_list.append(ProtectionDrillReportResponse(
                id=report.id,
                user_id=report.user_id,
                drill_type=report.drill_type,
                scenario_name=report.scenario_name,
                total_questions=report.total_questions,
                correct_answers=report.correct_answers,
                score=Decimal(str(report.score)),
                completion_time=report.completion_time,
                report_content=report.report_content,
                suggestions=report.suggestions,
                created_at=report.created_at,
                updated_at=report.updated_at
            ))
        
        return ProtectionDrillStatistics(
            total_reports=stats.total_reports or 0,
            average_score=float(stats.average_score or 0),
            drill_type_distribution=drill_type_distribution,
            recent_reports=recent_list,
            improvement_trend=[]  # 可以后续添加趋势分析
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取统计信息失败: {str(e)}")

@router.delete("/reports/{report_id}")
async def delete_protection_drill_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除防护训练报告"""
    try:
        # 检查报告是否存在且属于当前用户
        check_sql = """
        SELECT id FROM protection_drill_reports 
        WHERE id = :id AND user_id = :user_id
        """
        existing = db.execute(text(check_sql), {
            'id': report_id,
            'user_id': current_user.user_id
        }).fetchone()
        
        if not existing:
            raise HTTPException(status_code=404, detail="报告不存在")
        
        # 删除报告
        delete_sql = """
        DELETE FROM protection_drill_reports 
        WHERE id = :id AND user_id = :user_id
        """
        db.execute(text(delete_sql), {
            'id': report_id,
            'user_id': current_user.user_id
        })
        
        db.commit()
        
        return {"message": "报告删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"删除报告失败: {str(e)}")
