# backend/app/models/tree_hole_chat.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class TreeHoleChat(Base):
    __tablename__ = "tree_hole_chats"

    chat_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    whisper = relationship("TreeHoleWhisper")
    user = relationship("User")

class TreeHoleChatParticipant(Base):
    __tablename__ = "tree_hole_chat_participants"

    participant_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    whisper_id = Column(Integer, ForeignKey("tree_hole_whispers.whisper_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    anonymous_nickname = Column(String(255), nullable=False)
    anonymous_avatar = Column(String(255), nullable=False)

    whisper = relationship("TreeHoleWhisper")
    user = relationship("User")