"""
心灵预警检测组件
可复用的危机检测服务，支持悄悄话、日记、聊天等多种场景
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import logging

from sqlalchemy.orm import Session
from app.services.crisis_warning_service import CrisisWarningService, EnhancedRiskAssessment
from app.models.crisis_warning import RiskLevel

logger = logging.getLogger(__name__)


@dataclass
class CrisisDetectionResult:
    """危机检测结果（用于前端显示）"""
    has_risk: bool  # 是否存在风险
    risk_level: str  # 风险等级：low, medium, high, critical
    risk_score: float  # 风险分数 0-100
    ai_brief_analysis: Optional[str]  # AI简短分析（约30字）
    should_show_bubble: bool  # 是否显示看板娘气泡
    bubble_message: Optional[str]  # 气泡消息内容
    detected_keywords: list  # 检测到的关键词
    recommendations: list  # 建议
    

class CrisisDetectorComponent:
    """可复用的危机检测组件"""
    
    # 气泡消息模板
    BUBBLE_TEMPLATES = {
        RiskLevel.CRITICAL: [
            "我注意到你的状态似乎不太好，我很担心你。如果愿意的话，可以和我聊聊吗？💕",
            "小念一直在你身边，无论何时都可以倾诉哦。你并不孤单！🌟",
            "感觉你现在可能需要一些支持，我会一直陪着你的。💖"
        ],
        RiskLevel.HIGH: [
            "注意到你最近情绪波动比较大，要好好照顾自己哦～✨",
            "如果遇到困难，记得小念一直都在这里陪伴你！💫",
            "感觉你承受了不少压力呢，适当放松一下吧～🌸"
        ],
        RiskLevel.MEDIUM: [
            "小念感受到你有些情绪起伏，记得多关注自己的感受哦～🌈",
            "心情不好的时候，可以多和朋友聊聊天哦！💕",
            "适当的情绪宣泄是健康的，小念支持你！✨"
        ],
        RiskLevel.LOW: [
            "记录情绪是很好的习惯，继续保持哦～💖",
            "小念看到你在努力照顾自己的情绪，真棒！🌟",
        ]
    }
    
    def __init__(self, db: Session):
        self.db = db
        self.crisis_service = CrisisWarningService(db)
    
    async def detect_content_risk(
        self,
        content: str,
        scene: str = "tree-hole",
        user_id: Optional[int] = None,
        enable_ai: bool = True
    ) -> CrisisDetectionResult:
        """
        检测内容的心理风险
        
        Args:
            content: 待检测内容
            scene: 场景类型（tree-hole, diary, chat等）
            user_id: 用户ID（可选，用于记录）
            enable_ai: 是否启用AI分析
            
        Returns:
            CrisisDetectionResult: 检测结果
        """
        try:
            # 使用增强型风险评估
            assessment = await self.crisis_service.analyze_content_with_ai(
                content=content,
                scene=scene,
                keyword_score=0,
                enable_ai_analysis=enable_ai
            )
            
            # 确定是否显示气泡
            should_show = self._should_show_bubble(assessment)
            
            # 生成气泡消息
            bubble_message = self._generate_bubble_message(assessment) if should_show else None
            
            # 生成简短AI分析（30字左右）
            brief_analysis = self._generate_brief_analysis(assessment)
            
            # 生成建议
            recommendations = self._generate_recommendations(assessment)
            
            # 记录高风险内容（可选）
            if assessment.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL] and user_id:
                await self._log_high_risk_content(user_id, assessment, scene)
            
            return CrisisDetectionResult(
                has_risk=assessment.risk_level != RiskLevel.LOW or len(assessment.detected_keywords) > 0,
                risk_level=assessment.risk_level.value,
                risk_score=assessment.risk_score,
                ai_brief_analysis=brief_analysis,
                should_show_bubble=should_show,
                bubble_message=bubble_message,
                detected_keywords=assessment.detected_keywords,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"危机检测失败: {e}")
            # 返回安全的默认结果
            return CrisisDetectionResult(
                has_risk=False,
                risk_level="low",
                risk_score=0,
                ai_brief_analysis=None,
                should_show_bubble=False,
                bubble_message=None,
                detected_keywords=[],
                recommendations=[]
            )
    
    def _should_show_bubble(self, assessment: EnhancedRiskAssessment) -> bool:
        """判断是否应该显示看板娘气泡"""
        # 中等及以上风险显示气泡
        return assessment.risk_level in [
            RiskLevel.MEDIUM,
            RiskLevel.HIGH, 
            RiskLevel.CRITICAL
        ]
    
    def _generate_bubble_message(self, assessment: EnhancedRiskAssessment) -> str:
        """生成看板娘气泡消息"""
        import random
        
        templates = self.BUBBLE_TEMPLATES.get(
            assessment.risk_level,
            self.BUBBLE_TEMPLATES[RiskLevel.LOW]
        )
        
        return random.choice(templates)
    
    def _generate_brief_analysis(self, assessment: EnhancedRiskAssessment) -> Optional[str]:
        """生成简短AI分析（约30字）"""
        if not assessment.ai_analysis:
            return None
        
        # 截取AI分析的前30-40字
        full_analysis = assessment.ai_analysis
        if len(full_analysis) <= 40:
            return full_analysis
        
        # 智能截断，尽量在句号或逗号处
        truncated = full_analysis[:40]
        for punct in ['。', '，', '！', '？']:
            if punct in truncated:
                return truncated[:truncated.rfind(punct) + 1]
        
        return truncated + "..."
    
    def _generate_recommendations(self, assessment: EnhancedRiskAssessment) -> list:
        """生成建议列表"""
        recommendations = []
        
        if assessment.risk_level == RiskLevel.CRITICAL:
            recommendations.extend([
                "建议立即联系心理健康热线：400-161-9995",
                "与信任的亲友保持联系",
                "考虑寻求专业心理咨询帮助"
            ])
        elif assessment.risk_level == RiskLevel.HIGH:
            recommendations.extend([
                "建议预约专业心理咨询师",
                "保持与朋友家人的联系",
                "尝试一些放松技巧，如深呼吸、冥想"
            ])
        elif assessment.risk_level == RiskLevel.MEDIUM:
            recommendations.extend([
                "适当宣泄情绪是健康的",
                "可以尝试写日记记录感受",
                "保持规律的作息和运动"
            ])
        else:
            recommendations.append("继续保持良好的情绪管理习惯")
        
        return recommendations
    
    async def _log_high_risk_content(
        self,
        user_id: int,
        assessment: EnhancedRiskAssessment,
        scene: str
    ):
        """记录高风险内容到数据库"""
        try:
            from app.models.crisis_warning import CrisisWarning, WarningType
            import json
            
            warning_types = {
                'tree-hole': WarningType.KEYWORD_ALERT,
                'diary': WarningType.KEYWORD_ALERT,
                'chat': WarningType.KEYWORD_ALERT
            }
            
            # 构建描述信息,包含AI分析
            description_parts = [f"检测到{assessment.risk_level.value}级别风险"]
            if assessment.ai_analysis:
                description_parts.append(f"AI分析: {assessment.ai_analysis}")
            
            warning = CrisisWarning(
                user_id=user_id,
                warning_type=warning_types.get(scene, WarningType.KEYWORD_ALERT),
                risk_level=assessment.risk_level,
                score=assessment.risk_score,
                title=f"{scene}内容风险检测",
                description="\n".join(description_parts),  # 🔧 修复: 将AI分析放入description
                keywords_detected=json.dumps(
                    assessment.detected_keywords,
                    ensure_ascii=False
                )
                # 🔧 移除: ai_analysis=assessment.ai_analysis (字段不存在)
            )
            
            self.db.add(warning)
            self.db.commit()
            
            logger.info(f"已记录用户{user_id}的高风险内容 - {scene}")
            
        except Exception as e:
            logger.error(f"记录高风险内容失败: {e}")
            # 不抛出异常，不影响主流程


def get_crisis_detector(db: Session) -> CrisisDetectorComponent:
    """获取危机检测器实例"""
    return CrisisDetectorComponent(db)
