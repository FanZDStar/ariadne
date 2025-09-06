# 风险评估报告模型
# file: ariadne/backend/app/models/risk_assessment_report.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
import enum

class ReportStatus(enum.Enum):
    """报告状态枚举"""
    PENDING = "pending"       # 待处理
    COMPLETED = "completed"   # 已完成
    REVIEWED = "reviewed"     # 已查看

class RiskAssessmentReport(Base):
    """风险评估报告"""
    __tablename__ = "risk_assessment_reports"
    
    report_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)  # 对话会话ID - 修改为INT类型并添加外键
    scene = Column(String(100), nullable=False)  # 对话场景
    
    # 报告基本信息
    report_title = Column(String(255), nullable=False)
    report_content = Column(Text, nullable=False)  # 详细报告内容
    summary = Column(Text)  # 报告摘要
    
    # 风险评估结果
    overall_risk_level = Column(String(50), nullable=False)  # 整体风险等级
    overall_risk_score = Column(Float, default=0.0)  # 整体风险分数
    
    # 分析数据
    total_messages = Column(Integer, default=0)  # 消息总数
    risk_messages_count = Column(Integer, default=0)  # 风险消息数量
    detected_keywords = Column(JSON)  # 检测到的关键词列表
    risk_trends = Column(JSON)  # 风险趋势数据
    
    # AI分析结果
    ai_analysis = Column(Text)  # AI综合分析
    recommendations = Column(JSON)  # 建议列表
    
    # 时间信息
    conversation_start_time = Column(DateTime)  # 对话开始时间
    conversation_end_time = Column(DateTime)  # 对话结束时间
    report_generated_time = Column(DateTime, default=datetime.utcnow)  # 报告生成时间
    last_viewed_time = Column(DateTime)  # 最后查看时间
    
    # 状态信息
    status = Column(String(50), default=ReportStatus.PENDING.value)  # 报告状态
    is_viewed = Column(Boolean, default=False)  # 是否已查看
    version = Column(Integer, default=1)  # 报告版本号
    
    # 关联关系
    user = relationship("User", back_populates="risk_reports")
    session = relationship("ChatSession", back_populates="risk_reports")  # 添加与聊天会话的关联
    
    def to_dict(self):
        return {
            "report_id": self.report_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "scene": self.scene,
            "report_title": self.report_title,
            "report_content": self.report_content,
            "summary": self.summary,
            "overall_risk_level": self.overall_risk_level,
            "overall_risk_score": self.overall_risk_score,
            "total_messages": self.total_messages,
            "risk_messages_count": self.risk_messages_count,
            "detected_keywords": self.detected_keywords,
            "risk_trends": self.risk_trends,
            "ai_analysis": self.ai_analysis,
            "recommendations": self.recommendations,
            "conversation_start_time": self.conversation_start_time.isoformat() if self.conversation_start_time else None,
            "conversation_end_time": self.conversation_end_time.isoformat() if self.conversation_end_time else None,
            "report_generated_time": self.report_generated_time.isoformat() if self.report_generated_time else None,
            "last_viewed_time": self.last_viewed_time.isoformat() if self.last_viewed_time else None,
            "status": self.status,
            "is_viewed": self.is_viewed,
            "version": self.version
        }
