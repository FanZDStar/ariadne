#file:ariadne/backend/app/models/crisis_warning.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base
# from app.utils.encryption import encryption  # 暂时注释掉加密功能
from sqlalchemy.ext.hybrid import hybrid_property
import enum

class RiskLevel(enum.Enum):
    """风险等级枚举"""
    LOW = "low"           # 低风险
    MEDIUM = "medium"     # 中风险 
    HIGH = "high"         # 高风险
    CRITICAL = "critical" # 紧急风险

class WarningType(enum.Enum):
    """预警类型枚举"""
    MOOD_TREND = "mood_trend"         # 心情趋势预警
    KEYWORD_ALERT = "keyword_alert"   # 关键词预警
    CONTENT_ANALYSIS = "content_analysis"  # 内容分析预警
    AI_ANALYSIS = "ai_analysis"       # AI分析预警
    BEHAVIOR_PATTERN = "behavior_pattern"  # 行为模式预警

class CrisisWarning(Base):
    """心理危机预警记录"""
    __tablename__ = "crisis_warnings"
    
    warning_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    warning_type = Column(Enum(WarningType), nullable=False)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    score = Column(Float, nullable=False)  # 风险评分 0-100
    title = Column(String(255), nullable=False)  # 预警标题
    description = Column(Text, nullable=False)   # 预警描述
    source_data = Column(Text)  # 触发预警的源数据（加密存储）
    keywords_detected = Column(Text)  # 检测到的关键词（JSON格式）
    is_resolved = Column(Boolean, default=False)  # 是否已解决
    resolved_at = Column(DateTime)  # 解决时间
    resolver_notes = Column(Text)   # 解决备注
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # 关联关系
    user = relationship("User", back_populates="crisis_warnings")
    
    # 加密属性处理（暂时禁用）
    @hybrid_property
    def decrypted_source_data(self):
        """获取解密后的源数据"""
        # 暂时直接返回原数据，禁用加密功能
        return self.source_data
    
    @decrypted_source_data.setter
    def decrypted_source_data(self, value):
        """设置源数据（暂时禁用加密）"""
        self.source_data = value

class MoodTrendAnalysis(Base):
    """心情趋势分析记录"""
    __tablename__ = "mood_trend_analyses"
    
    analysis_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    period_days = Column(Integer, nullable=False)  # 分析周期（天）
    avg_mood_score = Column(Float, nullable=False)  # 平均心情评分
    mood_trend = Column(String(50), nullable=False)  # 趋势：declining, stable, improving
    consecutive_low_days = Column(Integer, default=0)  # 连续低心情天数
    risk_indicators = Column(Text)  # 风险指标（JSON格式）
    recommendations = Column(Text)  # 建议（加密存储）
    created_at = Column(DateTime, server_default=func.now())
    
    # 关联关系
    user = relationship("User")
    
    # 加密属性处理（暂时禁用）
    @hybrid_property
    def decrypted_recommendations(self):
        """获取解密后的建议"""
        # 暂时直接返回原数据，禁用加密功能
        return self.recommendations
    
    @decrypted_recommendations.setter
    def decrypted_recommendations(self, value):
        """设置建议（暂时禁用加密）"""
        self.recommendations = value
