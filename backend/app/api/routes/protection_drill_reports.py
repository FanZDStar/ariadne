from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List, Optional, Dict, Any
import json
from datetime import datetime, date
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
from app.services.ai_feedback_service import ai_feedback_service
from app.services.star_point_service import StarPointService
from app.utils.star_point_types import StarPointAction, SourceType

router = APIRouter()

@router.post("/reports", response_model=ProtectionDrillReportResponse)
async def create_protection_drill_report(
    report_data: ProtectionDrillReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建防护训练报告"""
    try:
        print(f"=== 开始创建防护技能训练报告 ===")
        print(f"当前用户ID: {current_user.user_id}")
        print(f"接收到的报告数据: {report_data}")
        print(f"question_analysis字段存在: {hasattr(report_data, 'question_analysis')}")
        if hasattr(report_data, 'question_analysis'):
            print(f"question_analysis数据: {report_data.question_analysis}")
        
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
        
        # 获取创建的报告ID
        report_id = result.lastrowid
        
        # 保存详细的答题分析（如果有的话）
        print(f"检查question_analysis字段: {hasattr(report_data, 'question_analysis')}")
        if hasattr(report_data, 'question_analysis') and report_data.question_analysis:
            print(f"question_analysis数据: {report_data.question_analysis}")
            await save_question_details(db, report_id, report_data.question_analysis)
        else:
            print("没有question_analysis数据或数据为空")
        
        db.commit()
        
        # 获取创建的报告
        select_sql = """
        SELECT * FROM protection_drill_reports WHERE id = :id
        """
        report = db.execute(text(select_sql), {'id': report_id}).fetchone()
        
        # 处理积分奖励逻辑
        star_reward_info = {"earned_points": 0, "is_rewarded": False, "message": "", "show_toast": False}
        
        try:
            print(f"=== 开始处理积分奖励逻辑 ===")
            star_service = StarPointService(db)
            daily_limits = star_service.get_daily_limits(current_user.user_id)
            
            print(f"当前用户今日防护训练状态: {daily_limits.protection_training}")
            
            # 检查今天是否已经获得过防护技能训练积分
            if not daily_limits.protection_training:
                # 奖励1个星星
                user_points = star_service.get_or_create_user_points(current_user.user_id)
                user_points.current_points += 1
                user_points.total_earned += 1
                
                # 更新每日限制记录
                daily_limits.protection_training = True
                
                # 添加积分日志
                star_service.add_point_log(
                    user_id=current_user.user_id,
                    action=StarPointAction.PROTECTION_TRAINING,
                    points_change=1,
                    source_type=SourceType.SKILL,
                    source_id=str(report_id),
                    description="防护技能训练完成"
                )
                
                db.commit()
                
                star_reward_info = {
                    "earned_points": 1,
                    "is_rewarded": True,
                    "message": "完成防护技能训练，获得1个星星！",
                    "show_toast": True
                }
                print(f"⭐ 防护技能训练积分奖励成功: +1星星 (用户ID: {current_user.user_id}, 报告ID: {report_id})")
                print(f"⭐ 今日第一次完成防护技能训练")
            else:
                print(f"⭐ 不是今日第一次生成报告 (用户ID: {current_user.user_id})")
                
        except Exception as e:
            print(f"❌ 防护技能训练积分奖励处理失败: {str(e)}")
            star_reward_info = {
                "earned_points": 0,
                "is_rewarded": False,
                "message": "积分奖励处理异常",
                "show_toast": False
            }
        
        # 创建响应，包含积分奖励信息
        response = ProtectionDrillReportResponse(
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
            updated_at=report.updated_at,
            star_reward=star_reward_info  # 直接在构造函数中传入积分奖励信息
        )
        
        return response
        
    except Exception as e:
        db.rollback()
        print(f"创建报告失败: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"创建报告失败: {str(e)}")


async def save_question_details(db: Session, report_id: int, question_analysis: List[Dict[str, Any]]):
    """保存答题详情到数据库"""
    try:
        print(f"开始保存答题详情，report_id: {report_id}, 题目数量: {len(question_analysis)}")
        
        for index, question_detail in enumerate(question_analysis):
            print(f"处理第{index+1}题: {question_detail}")
            print(f"question_detail类型: {type(question_detail)}")
            
            # 处理Pydantic模型或字典
            if hasattr(question_detail, 'dict'):
                # 如果是Pydantic模型，转换为字典
                detail_dict = question_detail.dict()
            else:
                # 如果已经是字典，直接使用
                detail_dict = question_detail
            
            print(f"转换后的字典: {detail_dict}")
            
            # 生成AI个性化反馈
            ai_feedback = ""
            try:
                ai_feedback = ai_feedback_service.generate_question_feedback(
                    question_title=detail_dict.get('question_title', ''),
                    question_text=detail_dict.get('question_text', ''),
                    selected_option=detail_dict.get('selected_option', ''),
                    correct_option=detail_dict.get('correct_option', ''),
                    is_correct=detail_dict.get('is_correct', False),
                    explanation=detail_dict.get('explanation', ''),
                    risk_explanation=detail_dict.get('risk_explanation', ''),
                    drill_type="防护技能训练"
                )
                print(f"生成AI反馈成功: {ai_feedback[:50]}...")
            except Exception as e:
                print(f"生成AI反馈失败: {e}")
                ai_feedback = "继续努力，每道题都是宝贵的学习机会！"
            
            insert_detail_sql = """
            INSERT INTO protection_drill_question_details 
            (report_id, question_id, question_title, question_text, 
             selected_option_id, selected_option_text, correct_option_id, correct_option_text,
             is_correct, score_gained, explanation, risk_explanation, ai_feedback,
             options_data, question_order)
            VALUES (:report_id, :question_id, :question_title, :question_text,
             :selected_option_id, :selected_option_text, :correct_option_id, :correct_option_text,
             :is_correct, :score_gained, :explanation, :risk_explanation, :ai_feedback,
             :options_data, :question_order)
            """
            
            insert_params = {
                'report_id': report_id,
                'question_id': detail_dict.get('question_id'),
                'question_title': detail_dict.get('question_title'),
                'question_text': detail_dict.get('question_text'),
                'selected_option_id': detail_dict.get('selected_option_id'),
                'selected_option_text': detail_dict.get('selected_option'),
                'correct_option_id': detail_dict.get('correct_option_id'),
                'correct_option_text': detail_dict.get('correct_option'),
                'is_correct': detail_dict.get('is_correct', False),
                'score_gained': detail_dict.get('score_gained', 0),
                'explanation': detail_dict.get('explanation'),
                'risk_explanation': detail_dict.get('risk_explanation'),
                'ai_feedback': ai_feedback,
                'options_data': json.dumps(detail_dict.get('options', []), ensure_ascii=False),
                'question_order': index + 1
            }
            
            print(f"执行插入，参数: {insert_params}")
            
            db.execute(text(insert_detail_sql), insert_params)
            print(f"第{index+1}题保存成功")
            
        print(f"所有答题详情保存完成，共{len(question_analysis)}题")
            
    except Exception as e:
        print(f"保存答题详情失败: {e}")
        import traceback
        traceback.print_exc()
        raise e

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

@router.get("/reports/{report_id}/details")
async def get_protection_drill_report_details(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取防护训练报告的详细答题分析"""
    try:
        # 获取报告基本信息
        select_report_sql = """
        SELECT * FROM protection_drill_reports 
        WHERE id = :id AND user_id = :user_id
        """
        report = db.execute(text(select_report_sql), {
            'id': report_id,
            'user_id': current_user.user_id
        }).fetchone()
        
        if not report:
            raise HTTPException(status_code=404, detail="报告不存在")
        
        # 获取详细答题分析
        select_details_sql = """
        SELECT * FROM protection_drill_question_details
        WHERE report_id = :report_id
        ORDER BY question_order ASC
        """
        question_details = db.execute(text(select_details_sql), {
            'report_id': report_id
        }).fetchall()
        
        # 格式化答题详情
        formatted_details = []
        for detail in question_details:
            options_data = json.loads(detail.options_data) if detail.options_data else []
            
            formatted_details.append({
                'id': detail.id,
                'question_id': detail.question_id,
                'question_title': detail.question_title,
                'question_text': detail.question_text,
                'selected_option_id': detail.selected_option_id,
                'selected_option_text': detail.selected_option_text,
                'correct_option_id': detail.correct_option_id,
                'correct_option_text': detail.correct_option_text,
                'is_correct': detail.is_correct,
                'score_gained': detail.score_gained,
                'explanation': detail.explanation,
                'risk_explanation': detail.risk_explanation,
                'ai_feedback': detail.ai_feedback,
                'options': options_data,
                'question_order': detail.question_order
            })
        
        # 生成整体AI分析（如果还没有的话）
        overall_ai_analysis = None
        if not report.ai_analysis and formatted_details:
            try:
                overall_ai_analysis = ai_feedback_service.generate_overall_analysis(
                    drill_type=report.drill_type,
                    scenario_name=report.scenario_name or "防护训练",
                    total_questions=report.total_questions,
                    correct_answers=report.correct_answers,
                    accuracy_rate=(report.correct_answers / report.total_questions * 100) if report.total_questions > 0 else 0,
                    question_analysis=formatted_details,
                    completion_time=report.completion_time
                )
                
                # 保存整体分析到数据库
                update_analysis_sql = """
                UPDATE protection_drill_reports 
                SET ai_analysis = :ai_analysis 
                WHERE id = :id
                """
                db.execute(text(update_analysis_sql), {
                    'ai_analysis': overall_ai_analysis,
                    'id': report_id
                })
                db.commit()
                
            except Exception as e:
                print(f"生成整体AI分析失败: {e}")
                overall_ai_analysis = "训练完成！继续努力提升防护技能。"
        else:
            overall_ai_analysis = report.ai_analysis
        
        return {
            'report': {
                'id': report.id,
                'drill_type': report.drill_type,
                'scenario_name': report.scenario_name,
                'total_questions': report.total_questions,
                'correct_answers': report.correct_answers,
                'score': float(report.score),
                'completion_time': report.completion_time,
                'suggestions': report.suggestions,
                'ai_analysis': overall_ai_analysis,
                'created_at': report.created_at,
                'updated_at': report.updated_at
            },
            'question_details': formatted_details,
            'statistics': {
                'accuracy_rate': (report.correct_answers / report.total_questions * 100) if report.total_questions > 0 else 0,
                'total_score': sum(detail.get('score_gained', 0) for detail in formatted_details),
                'correct_count': len([d for d in formatted_details if d.get('is_correct', False)]),
                'wrong_count': len([d for d in formatted_details if not d.get('is_correct', False)])
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取详细报告失败: {str(e)}")

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
