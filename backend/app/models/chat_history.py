from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
import enum
# from app.utils.encryption import encryption  # 暂时注释掉加密功能

class MessageType(str, enum.Enum):
    """消息类型枚举"""
    TEXT = "text"
    IMG = "img"
    MULTIMODAL = "multimodal"

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    scene = Column(String(50), nullable=False)  # self-dialog, love-experiment, love-yourself
    title = Column(String(255), nullable=False)  # 对话标题（第一条消息的前30字符）
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    auto_save_enabled = Column(Boolean, default=False, nullable=False)  # 是否启用自动保存（检测到风险后自动标记）
    
    # 关联关系
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    user = relationship("User", back_populates="chat_sessions")
    risk_reports = relationship("RiskAssessmentReport", back_populates="session", cascade="all, delete-orphan")  # 添加与风险评估报告的关联

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user 或 assistant
    msg_type = Column(Enum("text", "img", "multimodal"), nullable=False, default="text")  # 消息类型
    content = Column(Text, nullable=False)
    img_urls = Column(JSON, nullable=True)  # 图片URL数组
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关联关系
    session = relationship("ChatSession", back_populates="messages")
    
    # 临时禁用加密功能
    @hybrid_property
    def decrypted_content(self):
        """获取解密后的内容"""
        return self.content  # 暂时直接返回原内容
    
    @decrypted_content.setter
    def decrypted_content(self, value):
        """设置内容（自动加密）"""
        self.content = value  # 暂时直接设置原内容
