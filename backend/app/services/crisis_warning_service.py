#file:ariadne/backend/app/services/crisis_warning_service.py
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
import json
import re
import logging
from dataclasses import dataclass
import requests
import asyncio
from functools import lru_cache

from app.models.crisis_warning import CrisisWarning, MoodTrendAnalysis, RiskLevel, WarningType
from app.models.emotional_diary import EmotionalDiary
from app.models.chat_history import ChatMessage, ChatSession
from app.models.user import User
from app.core.config import settings

logger = logging.getLogger(__name__)

@dataclass
class RiskAssessmentResult:
    """风险评估结果"""
    risk_level: RiskLevel
    score: float
    reasons: List[str]
    recommendations: List[str]
    ai_analysis: Optional[str] = None
    detected_keywords: Optional[List[str]] = None

@dataclass 
class EnhancedRiskAssessment:
    """增强型风险评估结果"""
    content: str
    risk_level: RiskLevel
    risk_score: float
    keyword_score: float
    ai_analysis: Optional[str]
    detected_keywords: List[str]
    fuzzy_matches: List[str]
    scene: Optional[str]
    timestamp: datetime

class CrisisWarningService:
    """心理危机预警服务（增强版）"""
    
    # 危机关键词配置（增强版）
    CRISIS_KEYWORDS = {
        "自伤": [
            "自杀", "自残", "自伤", "结束生命", "不想活", "想死", "自我了断", 
            "轻生", "了结", "自了", "了断", "去死", "想去死", "要去死",
            "寻死", "找死", "赴死", "死了算了", "一死了之", "以死解脱"
        ],
        "绝望": [
            "绝望", "无望", "没有希望", "看不到未来", "一片黑暗", "无路可走", 
            "走投无路", "没救", "完了", "没意思", "活着没意义", "没活路"
        ],
        "孤独": [
            "孤独", "孤单", "没人理解", "没人关心", "被遗弃", "被抛弃", 
            "无人陪伴", "一个人", "形只影单", "无依无靠", "孑然一身"
        ],
        "无价值感": [
            "没用", "无价值", "废物", "垃圾", "拖累", "负担", "没意义", 
            "多余", "无能", "失败者", "活该", "该死", "不配"
        ],
        "极端情绪": [
            "崩溃", "疯了", "受不了", "痛苦", "煎熬", "折磨", "地狱", 
            "末日", "撑不住", "要疯", "要死", "快死了", "死掉算了"
        ]
    }
    
    # 同音字和模糊匹配模式（扩充版）
    FUZZY_PATTERNS = {
        "自杀": ["zi sha", "自 杀", "自_杀", "自-杀", "自*杀", "zi4", "zisha", "zs"],
        "想死": ["想 死", "想4", "想si", "xiang死", "想sǐ", "xiang si", "xiangsi"],
        "去死": ["去 死", "去4", "qu死", "去si", "qu si", "qusi", "qs"],
        "要死": ["要 死", "要4", "yao死", "要si", "yao si", "yaosi"],
        "绝望": ["绝 望", "jue望", "绝wang", "jué望", "juewang"],
        "崩溃": ["崩 溃", "beng溃", "崩kui", "běng溃", "bengkui"],
        "痛苦": ["痛 苦", "tong苦", "痛ku", "tòng苦", "tongku"],
        "不想活": ["不想 活", "不 想活", "b想活", "不xiang活"],
        "活着没意义": ["活着 没意义", "活 着没意义", "没 意义"]
    }
    
    # 心情评分映射
    MOOD_SCORES = {
        "very_happy": 90,
        "happy": 70,
        "neutral": 50,
        "sad": 30,
        "very_sad": 10
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    async def analyze_content_with_ai(
        self, 
        content: str, 
        scene: str = "", 
        keyword_score: float = 0,
        enable_ai_analysis: bool = True
    ) -> EnhancedRiskAssessment:
        """
        AI增强型内容风险分析
        
        Args:
            content: 用户输入内容
            scene: 聊天场景（self-dialog, love-experiment等）
            keyword_score: 前端关键词得分
            enable_ai_analysis: 是否启用AI分析
            
        Returns:
            EnhancedRiskAssessment: 增强型风险评估结果
        """
        # 1. 传统关键词检测（包含模糊匹配）
        keyword_result = self._enhanced_keyword_detection(content)
        
        # 2. AI分析（如果启用）
        ai_analysis = None
        if enable_ai_analysis:
            ai_analysis = await self._perform_ai_analysis(content, scene, keyword_result)
        
        # 3. 综合评分计算
        final_score = self._calculate_enhanced_risk_score(
            keyword_result, 
            keyword_score, 
            ai_analysis
        )
        
        # 4. 确定风险等级
        risk_level = self._determine_risk_level(final_score, keyword_result)
        
        return EnhancedRiskAssessment(
            content=content,
            risk_level=risk_level,
            risk_score=final_score,
            keyword_score=keyword_score,
            ai_analysis=ai_analysis,
            detected_keywords=keyword_result.get('keywords', []),
            fuzzy_matches=keyword_result.get('fuzzy_matches', []),
            scene=scene,
            timestamp=datetime.now()
        )

    def _enhanced_keyword_detection(self, content: str) -> Dict:
        """
        增强型关键词检测（支持模糊匹配、同音字等）
        """
        detected_keywords = []
        fuzzy_matches = []
        categories = []
        total_score = 0
        
        # 标准化文本
        normalized_content = self._normalize_text(content)
        logger.info(f"🔍 关键词检测 - 原始内容: {content}")
        logger.info(f"🔍 关键词检测 - 标准化后: {normalized_content}")
        
        # 1. 精确关键词匹配
        for category, keywords in self.CRISIS_KEYWORDS.items():
            category_matches = []
            for keyword in keywords:
                if keyword in normalized_content:
                    category_matches.append(keyword)
                    total_score += self._get_keyword_weight(keyword, category)
            
            if category_matches:
                detected_keywords.extend(category_matches)
                categories.append(category)
        
        logger.info(f"🔍 关键词检测 - 精确匹配: {detected_keywords}, 分类: {categories}")
        
        # 2. 模糊匹配
        for keyword, patterns in self.FUZZY_PATTERNS.items():
            for pattern in patterns:
                # 🔧 修复: 对模糊匹配的pattern也进行标准化处理
                normalized_pattern = self._normalize_text(pattern)
                if normalized_pattern in normalized_content:
                    fuzzy_matches.append(pattern)
                    # 模糊匹配也应该添加到对应的类别中
                    category = self._get_keyword_category(keyword)
                    if category not in categories:
                        categories.append(category)
                    total_score += self._get_keyword_weight(keyword, category) * 0.8  # 模糊匹配权重稍低
                    logger.info(f"✅ 模糊匹配成功: '{pattern}' (标准化: '{normalized_pattern}') → 关键词: '{keyword}', 分类: '{category}'")
        
        logger.info(f"🔍 关键词检测 - 模糊匹配: {fuzzy_matches}")
        logger.info(f"🔍 关键词检测 - 最终分类: {categories}, 总分: {total_score}")
        
        return {
            'keywords': detected_keywords,
            'fuzzy_matches': fuzzy_matches,
            'categories': list(set(categories)),
            'score': total_score
        }

    def _normalize_text(self, text: str) -> str:
        """文本标准化处理"""
        # 移除标点符号、空格，转为小写
        import string
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = ''.join(text.split())  # 移除所有空格
        return text.lower()

    def _get_keyword_weight(self, keyword: str, category: str) -> float:
        """获取关键词权重"""
        weights = {
            '自伤': 10.0,
            '绝望': 8.0,
            '极端情绪': 6.0,
            '无价值感': 5.0,
            '孤独': 4.0
        }
        return weights.get(category, 3.0)

    def _get_keyword_category(self, keyword: str) -> str:
        """获取关键词所属类别"""
        for category, keywords in self.CRISIS_KEYWORDS.items():
            if keyword in keywords:
                return category
        return '其他'

    async def _perform_ai_analysis(self, content: str, scene: str, keyword_result: Dict) -> Optional[str]:
        """
        执行AI分析
        """
        try:
            # 构造AI分析prompt
            analysis_prompt = self._build_ai_analysis_prompt(content, scene, keyword_result)
            
            # 调用AI服务（这里使用与对话相同的AI服务）
            ai_response = await self._call_ai_service(analysis_prompt)
            
            return ai_response
            
        except Exception as e:
            logger.error(f"AI分析失败: {e}")
            return None

    def _build_ai_analysis_prompt(self, content: str, scene: str, keyword_result: Dict) -> str:
        """构建AI分析提示词"""
        detected_info = ""
        if keyword_result['keywords']:
            detected_info = f"检测到关键词：{', '.join(keyword_result['keywords'][:3])}"
        
        scene_context = {
            'self-dialog': '用户正在进行自我情感对话',
            'love-experiment': '用户正在进行恋爱交际练习',
            'self-love': '用户正在学习自我关爱',
            'tree-hole': '用户在匿名树洞中倾诉'
        }.get(scene, '用户正在进行情感对话')
        
        return f"""
请作为专业的心理健康顾问，分析以下用户输入的心理健康风险：

用户输入："{content}"
对话场景：{scene_context}
{detected_info}

请从以下角度进行分析：
1. 情绪状态评估
2. 自伤风险评估  
3. 社会支持需求
4. 危机干预建议

请用简洁、专业、温暖的语言给出分析，控制在100字以内。如果没有明显风险，请给出积极引导。
"""

    async def _call_ai_service(self, prompt: str) -> str:
        """
        调用AI服务进行分析
        """
        # 这里可以复用现有的AI服务
        try:
            # 导入AI服务模块
            from app.core.ai_service import AIService
            
            ai_service = AIService()
            response = await ai_service.get_response([
                {"role": "user", "content": prompt}
            ], "crisis_analysis")
            
            return response
            
        except Exception as e:
            logger.error(f"调用AI服务失败: {e}")
            return "AI分析暂时不可用，建议关注用户情绪变化。"

    def _calculate_enhanced_risk_score(
        self, 
        keyword_result: Dict, 
        frontend_score: float, 
        ai_analysis: Optional[str]
    ) -> float:
        """
        计算增强型风险分数
        """
        # 基础关键词分数
        base_score = keyword_result['score']
        
        # 前端检测分数
        frontend_weight = min(frontend_score, 50)  # 限制前端分数影响
        
        # AI分析额外分数
        ai_bonus = 0
        if ai_analysis:
            # 简单的AI分析分数计算（可以更复杂化）
            risk_indicators = ['高风险', '危机', '紧急', '严重', '立即']
            for indicator in risk_indicators:
                if indicator in ai_analysis:
                    ai_bonus += 10
        
        # 综合计算
        total_score = base_score + frontend_weight * 0.3 + ai_bonus
        
        return min(total_score, 100)  # 限制最高分数

    def _determine_risk_level(self, score: float, keyword_result: Dict) -> RiskLevel:
        """
        确定风险等级
        """
        # 自伤类关键词直接判定为极高风险
        if '自伤' in keyword_result.get('categories', []):
            return RiskLevel.CRITICAL
        
        # 基于分数判定
        if score >= 80:
            return RiskLevel.CRITICAL
        elif score >= 60:
            return RiskLevel.HIGH
        elif score >= 40:
            return RiskLevel.MEDIUM
        elif score > 0:
            return RiskLevel.LOW
        else:
            return RiskLevel.LOW
    
    def analyze_user_risk(self, user_id: int, days: int = 14) -> RiskAssessmentResult:
        """
        综合分析用户心理风险
        
        Args:
            user_id: 用户ID
            days: 分析天数，默认14天
            
        Returns:
            RiskAssessmentResult: 风险评估结果
        """
        reasons = []
        recommendations = []
        total_score = 0
        
        # 1. 心情趋势分析
        mood_risk = self._analyze_mood_trend(user_id, days)
        total_score += mood_risk.score * 0.4  # 40%权重
        reasons.extend(mood_risk.reasons)
        recommendations.extend(mood_risk.recommendations)
        
        # 2. 对话内容分析
        chat_risk = self._analyze_chat_content(user_id, days)
        total_score += chat_risk.score * 0.3  # 30%权重
        reasons.extend(chat_risk.reasons)
        recommendations.extend(chat_risk.recommendations)
        
        # 3. 日记内容分析
        diary_risk = self._analyze_diary_content(user_id, days)
        total_score += diary_risk.score * 0.3  # 30%权重
        reasons.extend(diary_risk.reasons)
        recommendations.extend(diary_risk.recommendations)
        
        # 确定风险等级
        if total_score >= 80:
            risk_level = RiskLevel.CRITICAL
        elif total_score >= 60:
            risk_level = RiskLevel.HIGH
        elif total_score >= 40:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
            
        return RiskAssessmentResult(
            risk_level=risk_level,
            score=total_score,
            reasons=list(set(reasons)),  # 去重
            recommendations=list(set(recommendations))  # 去重
        )
    
    def _analyze_mood_trend(self, user_id: int, days: int) -> RiskAssessmentResult:
        """分析心情趋势"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取时间段内的情绪日记
        diaries = self.db.query(EmotionalDiary).filter(
            and_(
                EmotionalDiary.user_id == user_id,
                EmotionalDiary.created_at >= start_date,
                EmotionalDiary.created_at <= end_date
            )
        ).order_by(EmotionalDiary.created_at).all()
        
        if not diaries:
            return RiskAssessmentResult(RiskLevel.LOW, 0, [], [])
        
        # 计算心情评分
        mood_scores = [self.MOOD_SCORES.get(diary.mood, 50) for diary in diaries]
        avg_score = sum(mood_scores) / len(mood_scores)
        
        # 计算连续低心情天数
        consecutive_low_days = self._calculate_consecutive_low_days(mood_scores)
        
        reasons = []
        recommendations = []
        risk_score = 0
        
        # 评估平均心情
        if avg_score < 30:
            risk_score += 40
            reasons.append(f"近{days}天平均心情偏低({avg_score:.1f}分)")
            recommendations.append("建议寻求专业心理咨询师的帮助")
        elif avg_score < 40:
            risk_score += 20
            reasons.append(f"近{days}天心情状态不佳({avg_score:.1f}分)")
            recommendations.append("尝试进行一些愉快的活动，如散步、听音乐")
        
        # 评估连续低心情天数
        if consecutive_low_days >= 7:
            risk_score += 30
            reasons.append(f"连续{consecutive_low_days}天心情低落")
            recommendations.append("持续的低落情绪需要重视，建议咨询专业人士")
        elif consecutive_low_days >= 5:
            risk_score += 15
            reasons.append(f"连续{consecutive_low_days}天心情不佳")
            recommendations.append("注意调节情绪，保持规律作息")
        
        # 评估心情趋势
        if len(mood_scores) >= 3:
            recent_trend = self._calculate_trend(mood_scores[-7:])  # 最近7天趋势
            if recent_trend < -5:
                risk_score += 25
                reasons.append("心情呈明显下降趋势")
                recommendations.append("情绪下滑需要关注，建议与亲友交流")
        
        risk_level = RiskLevel.HIGH if risk_score >= 60 else RiskLevel.MEDIUM if risk_score >= 30 else RiskLevel.LOW
        
        return RiskAssessmentResult(risk_level, risk_score, reasons, recommendations)
    
    def _analyze_chat_content(self, user_id: int, days: int) -> RiskAssessmentResult:
        """分析聊天内容中的危机信号"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取用户的聊天消息
        messages = self.db.query(ChatMessage).join(ChatSession).filter(
            and_(
                ChatSession.user_id == user_id,
                ChatMessage.role == "user",  # 只分析用户消息
                ChatMessage.created_at >= start_date,
                ChatMessage.created_at <= end_date
            )
        ).all()
        
        if not messages:
            return RiskAssessmentResult(RiskLevel.LOW, 0, [], [])
        
        all_content = " ".join([msg.content for msg in messages])
        return self._analyze_text_for_crisis(all_content, "聊天记录")
    
    def _analyze_diary_content(self, user_id: int, days: int) -> RiskAssessmentResult:
        """分析日记内容中的危机信号"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # 获取用户的日记
        diaries = self.db.query(EmotionalDiary).filter(
            and_(
                EmotionalDiary.user_id == user_id,
                EmotionalDiary.created_at >= start_date,
                EmotionalDiary.created_at <= end_date
            )
        ).all()
        
        if not diaries:
            return RiskAssessmentResult(RiskLevel.LOW, 0, [], [])
        
        # 解密并合并所有日记内容
        all_content = ""
        for diary in diaries:
            try:
                content = diary.decrypted_content
                title = diary.decrypted_title
                all_content += f"{title} {content} "
            except Exception as e:
                logger.warning(f"解密日记失败: {e}")
                continue
        
        return self._analyze_text_for_crisis(all_content, "日记内容")
    
    def _analyze_text_for_crisis(self, text: str, source: str) -> RiskAssessmentResult:
        """分析文本中的危机关键词"""
        if not text.strip():
            return RiskAssessmentResult(RiskLevel.LOW, 0, [], [])
        
        detected_keywords = {}
        total_risk_score = 0
        reasons = []
        recommendations = []
        
        # 检测各类危机关键词
        for category, keywords in self.CRISIS_KEYWORDS.items():
            found_keywords = []
            for keyword in keywords:
                if keyword in text:
                    found_keywords.append(keyword)
            
            if found_keywords:
                detected_keywords[category] = found_keywords
                # 根据关键词类型和数量计算风险分数
                category_score = self._calculate_keyword_risk_score(category, len(found_keywords))
                total_risk_score += category_score
                
                reasons.append(f"{source}中检测到{category}相关表达")
                recommendations.extend(self._get_keyword_recommendations(category))
        
        # 风险等级判定
        if total_risk_score >= 60:
            risk_level = RiskLevel.CRITICAL
        elif total_risk_score >= 40:
            risk_level = RiskLevel.HIGH
        elif total_risk_score >= 20:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return RiskAssessmentResult(risk_level, total_risk_score, reasons, recommendations)
    
    def _calculate_keyword_risk_score(self, category: str, count: int) -> float:
        """根据关键词类别和数量计算风险分数"""
        base_scores = {
            "自伤": 40,      # 提高自伤类别的基础分数
            "绝望": 25,
            "孤独": 15,
            "无价值感": 20,
            "极端情绪": 10
        }
        
        base_score = base_scores.get(category, 10)
        # 数量越多，分数越高，但有上限
        multiplier = min(1 + (count - 1) * 0.3, 2.0)
        return base_score * multiplier
    
    def _get_keyword_recommendations(self, category: str) -> List[str]:
        """根据关键词类别获取建议"""
        recommendations_map = {
            "自伤": [
                "立即寻求专业心理危机干预帮助",
                "联系心理健康热线：400-161-9995",
                "与信任的亲友保持联系"
            ],
            "绝望": [
                "建议预约专业心理咨询师",
                "尝试制定小的、可实现的目标",
                "参与支持性社群活动"
            ],
            "孤独": [
                "主动与朋友家人联系",
                "参加兴趣小组或社交活动",
                "考虑在线心理支持社区"
            ],
            "无价值感": [
                "记录每日的小成就",
                "寻求认知行为疗法帮助",
                "培养自我关爱的习惯"
            ],
            "极端情绪": [
                "学习情绪调节技巧",
                "保持规律的生活作息",
                "考虑短期心理咨询"
            ]
        }
        
        return recommendations_map.get(category, ["建议关注心理健康"])
    
    def _calculate_consecutive_low_days(self, mood_scores: List[float]) -> int:
        """计算连续低心情天数"""
        consecutive_days = 0
        max_consecutive = 0
        
        for score in reversed(mood_scores):  # 从最新的开始
            if score <= 35:  # 低心情阈值
                consecutive_days += 1
                max_consecutive = max(max_consecutive, consecutive_days)
            else:
                break  # 遇到非低心情就停止
        
        return consecutive_days
    
    def _calculate_trend(self, scores: List[float]) -> float:
        """计算心情趋势（简单线性回归斜率）"""
        if len(scores) < 2:
            return 0
        
        n = len(scores)
        x = list(range(n))
        y = scores
        
        # 计算线性回归斜率
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0
        
        slope = numerator / denominator
        return slope
    
    def create_warning(self, user_id: int, assessment: RiskAssessmentResult, 
                      warning_type: WarningType, source_data: str = None) -> CrisisWarning:
        """创建危机预警记录"""
        warning = CrisisWarning(
            user_id=user_id,
            warning_type=warning_type,
            risk_level=assessment.risk_level,
            score=assessment.score,
            title=f"{assessment.risk_level.value.upper()}风险预警",
            description="; ".join(assessment.reasons),
            keywords_detected=json.dumps(assessment.reasons, ensure_ascii=False)
        )
        
        if source_data:
            warning.decrypted_source_data = source_data
        
        self.db.add(warning)
        self.db.commit()
        self.db.refresh(warning)
        
        logger.info(f"为用户 {user_id} 创建了 {assessment.risk_level.value} 级别的预警")
        return warning
    
    def get_user_warnings(self, user_id: int, days: int = 30, 
                         unresolved_only: bool = False) -> List[CrisisWarning]:
        """获取用户的预警记录"""
        query = self.db.query(CrisisWarning).filter(CrisisWarning.user_id == user_id)
        
        if unresolved_only:
            query = query.filter(CrisisWarning.is_resolved == False)
        
        if days:
            start_date = datetime.now() - timedelta(days=days)
            query = query.filter(CrisisWarning.created_at >= start_date)
        
        return query.order_by(desc(CrisisWarning.created_at)).all()
    
    def resolve_warning(self, warning_id: int, resolver_notes: str = None) -> bool:
        """解决预警"""
        warning = self.db.query(CrisisWarning).filter(
            CrisisWarning.warning_id == warning_id
        ).first()
        
        if warning:
            warning.is_resolved = True
            warning.resolved_at = datetime.now()
            if resolver_notes:
                warning.resolver_notes = resolver_notes
            
            self.db.commit()
            return True
        
        return False
