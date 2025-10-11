# #file:ariadne/backend/app/models/tree_hole.py
# from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from app.database.session import Base

# class TreeHoleWhisper(Base):
#     __tablename__ = "tree_hole_whispers"
    
#     whisper_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
#     content = Column(Text, nullable=False)
#     is_anonymous = Column(Boolean, default=True)
#     like_count = Column(Integer, default=0)
#     comment_count = Column(Integer, default=0)
#     created_at = Column(DateTime, server_default=func.now())
#     updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
#     chatted = Column(Boolean, default=False)
    
#     # 关联评论
#     comments = relationship("TreeHoleComment", back_populates="whisper")
#     # 关联点赞
#     likes = relationship("TreeHoleLike", back_populates="whisper")
#     # 关联用户
#     user = relationship("User")

# class TreeHoleComment(Base):
#     __tablename__ = "tree_hole_comments"
    
#     comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
#     content = Column(Text, nullable=False)
#     is_anonymous = Column(Boolean, default=True)
#     created_at = Column(DateTime, server_default=func.now())
    
#     # 反向关系
#     whisper = relationship("TreeHoleWhisper", back_populates="comments")
#     user = relationship("User")

# class TreeHoleLike(Base):
#     __tablename__ = "tree_hole_likes"
    
#     like_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
#     created_at = Column(DateTime, server_default=func.now())
    
#     # 反向关系
#     whisper = relationship("TreeHoleWhisper", back_populates="likes")
#     user = relationship("User")

from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey, String, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from app.database.session import Base
from app.utils.encryption import encryption
import enum

class MoodEnum(str, enum.Enum):
    very_happy = "very_happy"
    happy = "happy" 
    neutral = "neutral"
    sad = "sad"
    very_sad = "very_sad"

class TreeHoleWhisper(Base):
    __tablename__ = "tree_hole_whispers"
    
    whisper_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(255), nullable=True)  # 新增：标题字段
    content = Column(Text, nullable=False)
    mood = Column(Enum(MoodEnum), default=MoodEnum.neutral)  # 新增：心情字段
    tags = Column(JSON, nullable=True)  # 新增：标签字段
    is_anonymous = Column(Boolean, default=True)
    anonymous_name = Column(String(100), nullable=True)  # 新增：匿名名称
    anonymous_avatar = Column(String(500), nullable=True)  # 新增：匿名头像
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    chatted = Column(Boolean, default=False)
    
    # 关联评论 - 添加 cascade
    comments = relationship("TreeHoleComment", back_populates="whisper", cascade="all, delete-orphan")
    # 关联点赞 - 添加 cascade
    likes = relationship("TreeHoleLike", back_populates="whisper", cascade="all, delete-orphan")
    # 关联图片 - 新增
    images = relationship("TreeHoleWhisperImage", back_populates="whisper", cascade="all, delete-orphan")
    # 关联用户
    user = relationship("User") # user 关系不需要 cascade
    
    # 加密属性处理
    @hybrid_property
    def decrypted_content(self):
        """获取解密后的内容（匿名悄悄话会被加密）"""
        if self.is_anonymous:
            return encryption.decrypt_text(self.content)
        return self.content
    
    @decrypted_content.setter
    def decrypted_content(self, value):
        """设置内容（自动加密匿名悄悄话）"""
        if self.is_anonymous:
            self.content = encryption.encrypt_text(value)
        else:
            self.content = value

# ... 后面的 TreeHoleComment 和 TreeHoleLike 模型不需要修改 ...

class TreeHoleComment(Base):
    __tablename__ = "tree_hole_comments"
    
    comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # 反向关系
    whisper = relationship("TreeHoleWhisper", back_populates="comments")
    user = relationship("User")
    
    # 加密属性处理
    @hybrid_property
    def decrypted_content(self):
        """获取解密后的内容（匿名评论会被加密）"""
        if self.is_anonymous:
            return encryption.decrypt_text(self.content)
        return self.content
    
    @decrypted_content.setter
    def decrypted_content(self, value):
        """设置内容（自动加密匿名评论）"""
        if self.is_anonymous:
            self.content = encryption.encrypt_text(value)
        else:
            self.content = value

class TreeHoleLike(Base):
    __tablename__ = "tree_hole_likes"
    
    like_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # 反向关系
    whisper = relationship("TreeHoleWhisper", back_populates="likes")
    user = relationship("User")

class TreeHoleWhisperImage(Base):
    __tablename__ = "tree_hole_whisper_images"
    
    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    image_order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # 反向关系
    whisper = relationship("TreeHoleWhisper", back_populates="images")


class UserWhisperInteraction(Base):
    """用户与悄悄话的互动关系表
    
    用于记录用户互动过的悄悄话（点赞或评论），支持链接式管理。
    - is_active: 互动链接是否有效（用户可删除链接，但不影响原悄悄话）
    - has_liked: 是否点赞过
    - has_commented: 是否评论过
    - last_interaction_at: 最后一次互动时间（用于排序）
    """
    __tablename__ = "user_whisper_interactions"
    
    interaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False, index=True)
    
    # 互动状态
    is_active = Column(Boolean, default=True, comment="互动链接是否有效（用户可删除）")
    has_liked = Column(Boolean, default=False, comment="是否点赞过")
    has_commented = Column(Boolean, default=False, comment="是否评论过")
    
    # 时间戳
    first_interaction_at = Column(DateTime, server_default=func.now(), comment="首次互动时间")
    last_interaction_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="最后互动时间")
    
    # 关系
    user = relationship("User")
    whisper = relationship("TreeHoleWhisper")
