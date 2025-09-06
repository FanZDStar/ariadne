# 风险评估报告服务
# file: ariadne/backend/app/services/risk_assessment_service.py

from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import logging
from statistics import mean

from app.models.risk_assessment_report import RiskAssessmentReport, ReportStatus
from app.models.chat_history import ChatSession, ChatMessage
from app.models.crisis_warning import CrisisWarning, RiskLevel
from app.models.user import User
from app.services.crisis_warning_service import CrisisWarningService
from app.core.ai_service import AIService

logger = logging.getLogger(__name__)

class RiskAssessmentService:
    """风险评估报告服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.crisis_service = CrisisWarningService(db)
        self.ai_service = AIService()
    
    async def generate_session_report(
        self, 
        user_id: int, 
        session_id: str, 
        scene: str,
        conversation_start_time: datetime = None
    ) -> RiskAssessmentReport:
        """
        生成对话会话的风险评估报告
        
        Args:
            user_id: 用户ID
            session_id: 会话ID
            scene: 对话场景
            conversation_start_time: 对话开始时间
            
        Returns:
            RiskAssessmentReport: 风险评估报告
        """
        try:
            # 1. 获取会话中的所有消息
            messages = await self._get_session_messages(user_id, session_id)
            
            if not messages:
                logger.warning(f"未找到会话 {session_id} 的消息")
                return None
            
            # 2. 分析消息内容
            analysis_result = await self._analyze_session_messages(messages, scene)
            
            # 3. 生成AI综合分析
            ai_analysis = await self._generate_ai_session_analysis(messages, analysis_result, scene)
            
            # 4. 生成报告内容
            report_content = self._generate_report_content(analysis_result, ai_analysis)
            
            # 5. 检查是否已存在该会话的报告
            existing_report = self.db.query(RiskAssessmentReport).filter(
                and_(
                    RiskAssessmentReport.user_id == user_id,
                    RiskAssessmentReport.session_id == session_id
                )
            ).first()
            
            conversation_end_time = datetime.utcnow()
            
            if existing_report:
                # 更新现有报告
                existing_report.report_content = report_content
                existing_report.summary = analysis_result.get('summary', '')
                existing_report.overall_risk_level = analysis_result.get('overall_risk_level', 'low')
                existing_report.overall_risk_score = analysis_result.get('overall_risk_score', 0.0)
                existing_report.total_messages = len(messages)
                existing_report.risk_messages_count = analysis_result.get('risk_messages_count', 0)
                existing_report.detected_keywords = analysis_result.get('all_keywords', [])
                existing_report.risk_trends = analysis_result.get('risk_trends', [])
                existing_report.ai_analysis = ai_analysis
                existing_report.recommendations = analysis_result.get('recommendations', [])
                existing_report.conversation_end_time = conversation_end_time
                existing_report.report_generated_time = datetime.utcnow()
                existing_report.status = ReportStatus.COMPLETED.value
                existing_report.is_viewed = False  # 标记为未查看，下次进入时会显示
                existing_report.version += 1
                
                self.db.commit()
                return existing_report
            
            else:
                # 创建新报告
                report = RiskAssessmentReport(
                    user_id=user_id,
                    session_id=session_id,
                    scene=scene,
                    report_title=f"{self._get_scene_name(scene)}对话风险评估报告",
                    report_content=report_content,
                    summary=analysis_result.get('summary', ''),
                    overall_risk_level=analysis_result.get('overall_risk_level', 'low'),
                    overall_risk_score=analysis_result.get('overall_risk_score', 0.0),
                    total_messages=len(messages),
                    risk_messages_count=analysis_result.get('risk_messages_count', 0),
                    detected_keywords=analysis_result.get('all_keywords', []),
                    risk_trends=analysis_result.get('risk_trends', []),
                    ai_analysis=ai_analysis,
                    recommendations=analysis_result.get('recommendations', []),
                    conversation_start_time=conversation_start_time or messages[0].get('timestamp'),
                    conversation_end_time=conversation_end_time,
                    report_generated_time=datetime.utcnow(),
                    status=ReportStatus.COMPLETED.value,
                    is_viewed=False
                )
                
                self.db.add(report)
                self.db.commit()
                self.db.refresh(report)
                
                return report
                
        except Exception as e:
            logger.error(f"生成风险评估报告失败: {e}")
            self.db.rollback()
            return None
    
    async def _get_session_messages(self, user_id: int, session_id: str) -> List[Dict]:
        """获取会话中的所有消息"""
        try:
            # 首先获取会话
            session = self.db.query(ChatSession).filter(
                and_(
                    ChatSession.user_id == user_id,
                    ChatSession.id == session_id
                )
            ).first()
            
            if not session:
                logger.warning(f"未找到会话: user_id={user_id}, session_id={session_id}")
                return []
            
            # 获取会话中的所有消息
            chat_messages = self.db.query(ChatMessage).filter(
                ChatMessage.session_id == session.id
            ).order_by(ChatMessage.created_at).all()
            
            messages = []
            for msg in chat_messages:
                messages.append({
                    'role': msg.role,
                    'content': msg.decrypted_content,  # 使用解密后的内容
                    'timestamp': msg.created_at
                })
            
            return messages
            
        except Exception as e:
            logger.error(f"获取会话消息失败: {e}")
            return []
    
    async def _analyze_session_messages(self, messages: List[Dict], scene: str) -> Dict:
        """分析会话消息"""
        try:
            analysis_result = {
                'risk_messages_count': 0,
                'all_keywords': [],
                'risk_scores': [],
                'risk_trends': [],
                'overall_risk_level': 'low',
                'overall_risk_score': 0.0,
                'summary': '',
                'recommendations': []
            }
            
            user_messages = [msg for msg in messages if msg['role'] == 'user']
            
            for i, message in enumerate(user_messages):
                # 使用危机检测服务分析每条消息
                risk_result = await self.crisis_service.analyze_content_with_ai(
                    content=message['content'],
                    scene=scene,
                    enable_ai_analysis=False  # 单条消息不需要AI分析
                )
                
                if risk_result.risk_level != RiskLevel.LOW:
                    analysis_result['risk_messages_count'] += 1
                    analysis_result['all_keywords'].extend(risk_result.detected_keywords)
                
                analysis_result['risk_scores'].append(risk_result.risk_score)
                analysis_result['risk_trends'].append({
                    'message_index': i + 1,
                    'risk_level': risk_result.risk_level.value,
                    'risk_score': risk_result.risk_score,
                    'timestamp': message['timestamp'].isoformat() if message['timestamp'] else None
                })
            
            # 计算整体风险
            if analysis_result['risk_scores']:
                analysis_result['overall_risk_score'] = mean(analysis_result['risk_scores'])
                analysis_result['overall_risk_level'] = self._determine_overall_risk_level(
                    analysis_result['overall_risk_score'],
                    analysis_result['risk_messages_count'],
                    len(user_messages)
                )
            
            # 去重关键词
            analysis_result['all_keywords'] = list(set(analysis_result['all_keywords']))
            
            # 生成摘要
            analysis_result['summary'] = self._generate_summary(analysis_result, len(user_messages))
            
            # 生成建议
            analysis_result['recommendations'] = self._generate_recommendations(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"分析会话消息失败: {e}")
            return {}
    
    async def _generate_ai_session_analysis(self, messages: List[Dict], analysis_result: Dict, scene: str) -> str:
        """生成AI综合分析"""
        try:
            user_messages = [msg['content'] for msg in messages if msg['role'] == 'user']
            conversation_text = '\n'.join(user_messages[:10])  # 只取前10条消息避免过长
            
            prompt = f"""
请作为专业心理健康顾问，对以下用户在{self._get_scene_name(scene)}场景中的完整对话进行综合心理状态评估：

对话内容：
{conversation_text}

统计数据：
- 总消息数：{analysis_result.get('total_messages', 0)}
- 风险消息数：{analysis_result.get('risk_messages_count', 0)}
- 检测关键词：{', '.join(analysis_result.get('all_keywords', [])[:5])}
- 整体风险分数：{analysis_result.get('overall_risk_score', 0):.1f}

请从以下角度进行专业分析：
1. 整体心理状态评估
2. 情绪变化趋势
3. 风险因素识别
4. 积极因素识别
5. 专业建议

请用专业、温暖的语言给出200字左右的综合评估。
"""
            
            ai_analysis = await self.ai_service.get_response([
                {"role": "user", "content": prompt}
            ], "session_analysis")
            
            return ai_analysis
            
        except Exception as e:
            logger.error(f"生成AI会话分析失败: {e}")
            return "AI分析暂时不可用，建议关注用户整体心理状态变化。"
    
    def _determine_overall_risk_level(self, avg_score: float, risk_count: int, total_count: int) -> str:
        """确定整体风险等级"""
        risk_ratio = risk_count / total_count if total_count > 0 else 0
        
        if avg_score >= 30 or risk_ratio >= 0.5:
            return 'critical'
        elif avg_score >= 20 or risk_ratio >= 0.3:
            return 'high'
        elif avg_score >= 10 or risk_ratio >= 0.1:
            return 'medium'
        else:
            return 'low'
    
    def _generate_summary(self, analysis_result: Dict, total_messages: int) -> str:
        """生成摘要"""
        risk_count = analysis_result.get('risk_messages_count', 0)
        risk_level = analysis_result.get('overall_risk_level', 'low')
        
        if risk_level == 'critical':
            return f"在{total_messages}条消息中检测到{risk_count}条风险消息，整体呈现高风险状态，需要立即关注。"
        elif risk_level == 'high':
            return f"在{total_messages}条消息中检测到{risk_count}条风险消息，存在明显心理健康风险。"
        elif risk_level == 'medium':
            return f"在{total_messages}条消息中检测到{risk_count}条风险消息，建议关注情绪变化。"
        else:
            return f"在{total_messages}条消息中检测到{risk_count}条风险消息，整体心理状态相对稳定。"
    
    def _generate_recommendations(self, analysis_result: Dict) -> List[str]:
        """生成建议"""
        recommendations = []
        risk_level = analysis_result.get('overall_risk_level', 'low')
        
        if risk_level == 'critical':
            recommendations.extend([
                "立即寻求专业心理健康支持",
                "联系心理危机干预热线",
                "告知信任的朋友或家人",
                "考虑医院心理科就诊"
            ])
        elif risk_level == 'high':
            recommendations.extend([
                "建议咨询专业心理健康专家",
                "保持规律的作息和运动",
                "与亲友保持沟通",
                "学习情绪调节技巧"
            ])
        elif risk_level == 'medium':
            recommendations.extend([
                "继续关注自己的情绪变化",
                "尝试放松和减压活动",
                "保持健康的生活方式",
                "必要时寻求支持"
            ])
        else:
            recommendations.extend([
                "保持当前积极的心理状态",
                "继续进行自我关爱练习",
                "维护良好的社交关系",
                "定期进行自我反思"
            ])
        
        return recommendations
    
    def _generate_report_content(self, analysis_result: Dict, ai_analysis: str) -> str:
        """生成报告内容"""
        content = f"""
## 对话风险评估报告

### 基本信息
- **整体风险等级**: {analysis_result.get('overall_risk_level', 'low').upper()}
- **风险分数**: {analysis_result.get('overall_risk_score', 0):.1f}/100
- **消息分析**: 共{analysis_result.get('total_messages', 0)}条消息，其中{analysis_result.get('risk_messages_count', 0)}条检测到风险

### 检测结果
- **关键词**: {', '.join(analysis_result.get('all_keywords', [])[:10]) if analysis_result.get('all_keywords') else '无'}

### AI专业分析
{ai_analysis}

### 建议
{chr(10).join([f"• {rec}" for rec in analysis_result.get('recommendations', [])])}

---
*此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。*
"""
        return content
    
    def _get_scene_name(self, scene: str) -> str:
        """获取场景中文名称"""
        scene_names = {
            'self-dialog': '自我对话',
            'love-experiment': '恋爱实验',
            'self-love': '自爱练习',
            'tree-hole': '树洞聊天'
        }
        return scene_names.get(scene, '对话')
    
    def get_user_latest_report(self, user_id: int, session_id: str) -> Optional[RiskAssessmentReport]:
        """获取用户指定会话的最新报告"""
        try:
            report = self.db.query(RiskAssessmentReport).filter(
                and_(
                    RiskAssessmentReport.user_id == user_id,
                    RiskAssessmentReport.session_id == session_id,
                    RiskAssessmentReport.status == ReportStatus.COMPLETED.value
                )
            ).order_by(desc(RiskAssessmentReport.version)).first()
            
            return report
            
        except Exception as e:
            logger.error(f"获取用户最新报告失败: {e}")
            return None
    
    def mark_report_as_viewed(self, report_id: int, user_id: int) -> bool:
        """标记报告为已查看"""
        try:
            report = self.db.query(RiskAssessmentReport).filter(
                and_(
                    RiskAssessmentReport.report_id == report_id,
                    RiskAssessmentReport.user_id == user_id
                )
            ).first()
            
            if report:
                report.is_viewed = True
                report.last_viewed_time = datetime.utcnow()
                self.db.commit()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"标记报告已查看失败: {e}")
            self.db.rollback()
            return False
    
    def get_user_reports_history(self, user_id: int, limit: int = 10, page: int = 1) -> List[RiskAssessmentReport]:
        """获取用户的报告历史"""
        try:
            offset = (page - 1) * limit
            reports = self.db.query(RiskAssessmentReport).filter(
                RiskAssessmentReport.user_id == user_id
            ).order_by(desc(RiskAssessmentReport.report_generated_time)).offset(offset).limit(limit).all()
            
            return reports
            
        except Exception as e:
            logger.error(f"获取用户报告历史失败: {e}")
            return []

    def get_report_by_id(self, report_id: int, user_id: int) -> Optional[RiskAssessmentReport]:
        """根据报告ID获取报告详情（验证用户权限）"""
        try:
            report = self.db.query(RiskAssessmentReport).filter(
                RiskAssessmentReport.report_id == report_id,
                RiskAssessmentReport.user_id == user_id  # 确保用户只能访问自己的报告
            ).first()
            
            return report
            
        except Exception as e:
            logger.error(f"获取报告详情失败: {e}")
            return None
