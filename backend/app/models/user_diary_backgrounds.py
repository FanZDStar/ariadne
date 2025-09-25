# backend/app/models/user_diary_backgrounds.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.session import Base

class UserDiaryBackground(Base):
    """用户自定义日记背景图片模型"""
    __tablename__ = "user_diary_backgrounds"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)  # 存储的文件名
    original_filename = Column(String(255), nullable=False)  # 原始文件名
    file_path = Column(String(500), nullable=False)  # 文件存储路径
    file_size = Column(Integer, nullable=False)  # 文件大小（字节）
    upload_time = Column(DateTime, server_default=func.now())  # 上传时间
    is_active = Column(Boolean, default=True)  # 是否激活使用
    
    # 关联用户
    user = relationship("User", back_populates="diary_backgrounds")
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "upload_time": self.upload_time.isoformat() if self.upload_time else None,
            "is_active": self.is_active,
            "url": f"/uploads/diary-backgrounds/{self.filename}"
        }