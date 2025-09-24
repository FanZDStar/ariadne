# 关系健康评估报告模型
# file: ariadne/backend/app/models/relationship_assessment_report.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
import enum

class AssessmentStatus(enum.Enum):
    """评估报告状态枚举"""
    PROCESSING = "processing"   # AI分析中
    COMPLETED = "completed"     # 分析完成
    FAILED = "failed"          # 分析失败

class RelationshipAssessmentReport(Base):
    """关系健康评估报告"""
    __tablename__ = "relationship_health_reports"  # 匹配实际创建的表名
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    session_token = Column(String(255), nullable=False, index=True, unique=True)  # 评估会话标识
    
    # 评估基本信息
    relationship_type = Column(String(50), nullable=False, index=True)  # family, friendship, romantic, mentor
    relationship_name = Column(String(100), nullable=False)  # 关系类型中文名称
    
    # 评估结果 - 分数数据
    total_score = Column(Float, nullable=False)  # 总体得分百分比 (0-100)
    total_level = Column(Text, nullable=False)   # 等级信息存储为JSON字符串
    dimension_scores = Column(Text, nullable=False)  # 各维度得分详情存储为JSON字符串
    questions_answered = Column(Integer, nullable=False, default=0)  # 回答题目数量
    
    # AI分析结果 - 异步生成
    ai_analysis = Column(Text, nullable=True)  # AI生成的分析文本
    recommendations = Column(Text, nullable=True)  # AI生成的建议列表存储为JSON字符串
    
    # 状态管理
    status = Column(String(20), nullable=False, default=AssessmentStatus.PROCESSING.value, index=True)
    
    # 时间戳
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)  # 评估创建时间
    ai_started_at = Column(DateTime, nullable=True)  # AI分析开始时间
    ai_completed_at = Column(DateTime, nullable=True)  # AI分析完成时间
    last_viewed_at = Column(DateTime, nullable=True)  # 最后查看时间
    
    # 错误处理
    error_message = Column(Text, nullable=True)  # 如果分析失败，存储错误信息
    retry_count = Column(Integer, nullable=False, default=0)  # 重试次数
    
    # 版本控制
    version = Column(Integer, nullable=False, default=1)  # 报告版本
    
    # 关联关系
    user = relationship("User", back_populates="relationship_reports")
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_token": self.session_token,
            "relationship_type": self.relationship_type,
            "relationship_name": self.relationship_name,
            "total_score": self.total_score,
            "total_level": self.total_level,
            "dimension_scores": self.dimension_scores,
            "questions_answered": self.questions_answered,
            "ai_analysis": self.ai_analysis,
            "recommendations": self.recommendations,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "ai_started_at": self.ai_started_at.isoformat() if self.ai_started_at else None,
            "ai_completed_at": self.ai_completed_at.isoformat() if self.ai_completed_at else None,
            "last_viewed_at": self.last_viewed_at.isoformat() if self.last_viewed_at else None,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "version": self.version
        }
    
    def is_processing(self):
        """是否正在处理中"""
        return self.status == AssessmentStatus.PROCESSING.value
    
    def is_completed(self):
        """是否已完成"""
        return self.status == AssessmentStatus.COMPLETED.value
    
    def is_failed(self):
        """是否失败"""
        return self.status == AssessmentStatus.FAILED.value
    
    def mark_viewed(self):
        """标记为已查看"""
        self.last_viewed_at = datetime.utcnow()
    
    def start_ai_analysis(self):
        """开始AI分析"""
        self.ai_started_at = datetime.utcnow()
        self.status = AssessmentStatus.PROCESSING.value
    
    def complete_ai_analysis(self, ai_analysis: str, recommendations: list):
        """完成AI分析"""
        self.ai_analysis = ai_analysis
        self.recommendations = recommendations
        self.ai_completed_at = datetime.utcnow()
        self.status = AssessmentStatus.COMPLETED.value
        self.error_message = None
    
    def fail_ai_analysis(self, error_message: str):
        """AI分析失败"""
        self.error_message = error_message
        self.status = AssessmentStatus.FAILED.value
        self.retry_count += 1