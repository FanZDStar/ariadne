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

from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base

class TreeHoleWhisper(Base):
    __tablename__ = "tree_hole_whispers"
    
    whisper_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    is_anonymous = Column(Boolean, default=True)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    chatted = Column(Boolean, default=False)
    
    # 关联评论 - 添加 cascade
    comments = relationship("TreeHoleComment", back_populates="whisper", cascade="all, delete-orphan")
    # 关联点赞 - 添加 cascade
    likes = relationship("TreeHoleLike", back_populates="whisper", cascade="all, delete-orphan")
    # 关联用户
    user = relationship("User") # user 关系不需要 cascade

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

class TreeHoleLike(Base):
    __tablename__ = "tree_hole_likes"
    
    like_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # 反向关系
    whisper = relationship("TreeHoleWhisper", back_populates="likes")
    user = relationship("User")
