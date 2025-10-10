from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal

class QuestionAnalysis(BaseModel):
    """单题分析数据模式"""
    question_id: Optional[int] = Field(None, description="题目ID")
    question_title: Optional[str] = Field(None, description="题目标题")
    question_text: Optional[str] = Field(None, description="题目内容")
    selected_option_id: Optional[int] = Field(None, description="用户选择的选项ID")
    selected_option: Optional[str] = Field(None, description="用户选择的选项文本")
    correct_option_id: Optional[int] = Field(None, description="正确答案选项ID")
    correct_option: Optional[str] = Field(None, description="正确答案选项文本")
    is_correct: bool = Field(False, description="是否回答正确")
    score_gained: int = Field(0, description="本题获得分数")
    explanation: Optional[str] = Field(None, description="答案解释")
    risk_explanation: Optional[str] = Field(None, description="风险解释")
    options: List[Dict[str, Any]] = Field(default_factory=list, description="所有选项数据")

class ProtectionDrillReportBase(BaseModel):
    """防护训练报告基础模式"""
    drill_type: str = Field(..., description="防护训练类型")
    scenario_name: Optional[str] = Field(None, description="场景名称")
    total_questions: int = Field(..., description="总题数")
    correct_answers: int = Field(..., description="正确答案数")
    score: Decimal = Field(..., description="得分")
    completion_time: Optional[int] = Field(None, description="完成时间(秒)")
    suggestions: Optional[str] = Field(None, description="改进建议")

class ProtectionDrillReportCreate(ProtectionDrillReportBase):
    """创建防护训练报告模式"""
    report_content: Optional[str] = Field(None, description="详细报告内容(JSON格式)")
    answers: Optional[List[int]] = Field(None, description="用户答题选择列表")
    correct_answers_list: Optional[List[int]] = Field(None, description="正确答案列表")
    questions_data: Optional[List[Dict[str, Any]]] = Field(None, description="题目详细数据")
    question_analysis: Optional[List[QuestionAnalysis]] = Field(None, description="详细答题分析")

class ProtectionDrillReportUpdate(BaseModel):
    """更新防护训练报告模式"""
    drill_type: Optional[str] = Field(None, description="防护训练类型")
    scenario_name: Optional[str] = Field(None, description="场景名称")
    total_questions: Optional[int] = Field(None, description="总题数")
    correct_answers: Optional[int] = Field(None, description="正确答案数")
    score: Optional[Decimal] = Field(None, description="得分")
    completion_time: Optional[int] = Field(None, description="完成时间(秒)")
    report_content: Optional[str] = Field(None, description="详细报告内容(JSON格式)")
    suggestions: Optional[str] = Field(None, description="改进建议")

class ProtectionDrillReportResponse(ProtectionDrillReportBase):
    """防护训练报告响应模式"""
    id: int = Field(..., description="报告ID")
    user_id: int = Field(..., description="用户ID")
    report_content: Optional[str] = Field(None, description="详细报告内容(JSON格式)")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    star_reward: Optional[Dict[str, Any]] = Field(None, description="积分奖励信息")

    class Config:
        from_attributes = True

class ProtectionDrillReportList(BaseModel):
    """防护训练报告列表响应模式"""
    reports: List[ProtectionDrillReportResponse] = Field(..., description="报告列表")
    total: int = Field(..., description="总数")
    skip: int = Field(..., description="跳过数量")
    limit: int = Field(..., description="限制数量")

class ProtectionDrillStatistics(BaseModel):
    """防护训练统计模式"""
    total_reports: int = Field(..., description="总报告数")
    average_score: float = Field(..., description="平均得分")
    drill_type_distribution: Dict[str, int] = Field(..., description="训练类型分布")
    recent_reports: List[ProtectionDrillReportResponse] = Field(..., description="最近报告")
    improvement_trend: List[Dict[str, Any]] = Field(..., description="改进趋势")
