from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base

class ProtectionDrillReport(Base):
    __tablename__ = "protection_drill_reports"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True, comment='用户ID')
    drill_type = Column(String(100), nullable=False, comment='防护训练类型')
    scenario_name = Column(String(200), comment='场景名称')
    total_questions = Column(Integer, nullable=False, default=0, comment='总题数')
    correct_answers = Column(Integer, nullable=False, default=0, comment='正确答案数')
    score = Column(Numeric(5,2), nullable=False, default=0.00, comment='得分')
    completion_time = Column(Integer, comment='完成时间(秒)')
    report_content = Column(Text, comment='详细报告内容(JSON格式)')
    suggestions = Column(Text, comment='改进建议')
    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')
