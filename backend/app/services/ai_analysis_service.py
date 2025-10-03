"""
AI分析服务
用于生成防护训练报告的智能分析
"""

import json
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AIAnalysisService:
    """AI分析服务类"""
    
    def __init__(self):
        """初始化AI分析服务"""
        pass
    
    def generate_protection_drill_analysis(
        self,
        drill_type: str,
        scenario_name: str,
        total_questions: int,
        correct_answers: int,
        score: float,
        answers: List[int],
        correct_answers_list: List[int],
        questions_data: Optional[List[Dict]] = None,
        completion_time: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        生成防护训练的AI分析报告
        
        Args:
            drill_type: 训练类型
            scenario_name: 场景名称
            total_questions: 总题数
            correct_answers: 正确答案数
            score: 得分
            answers: 用户答案列表
            correct_answers_list: 正确答案列表
            questions_data: 题目数据（可选）
            completion_time: 完成时间（秒）
            
        Returns:
            包含AI分析的字典
        """
        try:
            # 计算基础统计
            accuracy_rate = (correct_answers / total_questions) * 100
            wrong_answers = total_questions - correct_answers
            
            # 生成详细分析
            analysis = {
                "overall_analysis": self._generate_overall_analysis(
                    drill_type, scenario_name, score, accuracy_rate, completion_time
                ),
                "question_analysis": self._generate_question_analysis(
                    answers, correct_answers_list, questions_data
                ),
                "strength_analysis": self._generate_strength_analysis(
                    drill_type, answers, correct_answers_list, score
                ),
                "weakness_analysis": self._generate_weakness_analysis(
                    drill_type, answers, correct_answers_list, score
                ),
                "improvement_suggestions": self._generate_improvement_suggestions(
                    drill_type, scenario_name, score, accuracy_rate, wrong_answers
                ),
                "knowledge_points": self._generate_knowledge_points(
                    drill_type, answers, correct_answers_list
                ),
                "performance_evaluation": self._generate_performance_evaluation(
                    score, accuracy_rate, completion_time, total_questions
                )
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"生成AI分析失败: {e}")
            return self._generate_fallback_analysis(drill_type, score, accuracy_rate)
    
    def _generate_overall_analysis(
        self, 
        drill_type: str, 
        scenario_name: str, 
        score: float, 
        accuracy_rate: float, 
        completion_time: Optional[int]
    ) -> str:
        """生成总体分析"""
        performance_level = self._get_performance_level(score)
        time_analysis = ""
        
        if completion_time:
            time_per_question = completion_time / 10  # 假设平均题目数
            if time_per_question < 30:
                time_analysis = "答题速度较快，显示了良好的反应能力，"
            elif time_per_question > 60:
                time_analysis = "答题较为谨慎，体现了认真思考的态度，"
            else:
                time_analysis = "答题节奏适中，"
        
        scenario_specific = ""
        if scenario_name:
            scenario_specific = f"在{scenario_name}中，"
        
        analysis = f"""
        本次{drill_type}训练中，{scenario_specific}您的总体表现达到了{performance_level}水平，得分{score}%。
        {time_analysis}正确率为{accuracy_rate:.1f}%。
        
        通过此次训练，可以看出您在{self._get_drill_type_description(drill_type)}方面的认知能力和应对策略。
        您的表现{self._get_score_evaluation(score)}，显示了{self._get_capability_assessment(score)}的防护意识。
        """
        
        return analysis.strip()
    
    def _generate_question_analysis(
        self, 
        answers: List[int], 
        correct_answers: List[int], 
        questions_data: Optional[List[Dict]]
    ) -> List[Dict[str, Any]]:
        """生成题目详细分析"""
        question_analysis = []
        
        for i, (user_answer, correct_answer) in enumerate(zip(answers, correct_answers)):
            is_correct = user_answer == correct_answer
            
            # 基础题目信息
            question_info = {
                "question_number": i + 1,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "analysis": self._generate_single_question_analysis(
                    i + 1, user_answer, correct_answer, is_correct
                )
            }
            
            # 如果有题目数据，添加详细信息
            if questions_data and i < len(questions_data):
                question_data = questions_data[i]
                question_info.update({
                    "question": question_data.get("question", f"第{i+1}题"),
                    "options": question_data.get("options", []),
                    "explanation": self._generate_explanation(
                        question_data, user_answer, correct_answer, is_correct
                    )
                })
            
            question_analysis.append(question_info)
        
        return question_analysis
    
    def _generate_single_question_analysis(
        self, 
        question_num: int, 
        user_answer: int, 
        correct_answer: int, 
        is_correct: bool
    ) -> str:
        """生成单题分析"""
        if is_correct:
            return f"第{question_num}题回答正确，显示了良好的判断能力。"
        else:
            return f"第{question_num}题需要改进，您选择了选项{user_answer}，正确答案是选项{correct_answer}。建议重点关注此类题型。"
    
    def _generate_explanation(
        self, 
        question_data: Dict, 
        user_answer: int, 
        correct_answer: int, 
        is_correct: bool
    ) -> str:
        """生成题目解释"""
        question_type = question_data.get("type", "判断题")
        
        if is_correct:
            return f"您正确识别了这道{question_type}的关键信息，体现了良好的防护意识。"
        else:
            return f"这道{question_type}考查的是重要的防护知识点。正确答案的选择理由是基于风险识别的原则，建议加强相关知识的学习。"
    
    def _generate_strength_analysis(
        self, 
        drill_type: str, 
        answers: List[int], 
        correct_answers: List[int], 
        score: float
    ) -> List[str]:
        """生成优势分析"""
        strengths = []
        correct_count = sum(1 for a, c in zip(answers, correct_answers) if a == c)
        
        if score >= 90:
            strengths.extend([
                f"在{drill_type}方面表现优秀，具备很强的识别能力",
                "决策准确，风险意识敏锐",
                "能够快速识别关键信息和潜在威胁"
            ])
        elif score >= 80:
            strengths.extend([
                f"{drill_type}技能掌握良好，基础扎实",
                "大部分情况下能够做出正确判断",
                "具备一定的防护意识和应对能力"
            ])
        elif score >= 70:
            strengths.extend([
                f"在{drill_type}方面有一定基础",
                "能够识别部分风险信号",
                "学习态度积极，有提升空间"
            ])
        else:
            strengths.extend([
                "参与训练的积极态度值得肯定",
                "通过练习正在逐步提升认知能力"
            ])
        
        return strengths
    
    def _generate_weakness_analysis(
        self, 
        drill_type: str, 
        answers: List[int], 
        correct_answers: List[int], 
        score: float
    ) -> List[str]:
        """生成薄弱环节分析"""
        weaknesses = []
        wrong_count = sum(1 for a, c in zip(answers, correct_answers) if a != c)
        
        if score < 60:
            weaknesses.extend([
                f"{drill_type}的基础知识需要加强",
                "风险识别能力有待提升",
                "需要更多练习来增强判断准确性"
            ])
        elif score < 70:
            weaknesses.extend([
                f"在{drill_type}的某些方面还需要改进",
                "部分风险信号的识别不够敏感",
                "建议针对性地学习相关知识"
            ])
        elif score < 80:
            weaknesses.extend([
                "个别知识点掌握不够牢固",
                "在复杂情况下的判断还需要提升"
            ])
        else:
            weaknesses.extend([
                "整体表现良好，个别细节可以更加完善"
            ])
        
        return weaknesses
    
    def _generate_improvement_suggestions(
        self, 
        drill_type: str, 
        scenario_name: str, 
        score: float, 
        accuracy_rate: float, 
        wrong_answers: int
    ) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        # 基于得分的建议
        if score < 60:
            suggestions.extend([
                f"建议系统学习{drill_type}相关的基础知识",
                "多参与类似训练，提升实践经验",
                "关注日常生活中的风险信号，培养警觉性",
                "可以寻求专业指导，制定个人防护计划"
            ])
        elif score < 80:
            suggestions.extend([
                f"继续深入学习{drill_type}的进阶技巧",
                "针对错误题目进行专项练习",
                "在实际生活中应用所学知识",
                "定期参与训练保持技能水平"
            ])
        else:
            suggestions.extend([
                "保持当前良好的防护意识",
                "可以尝试更复杂的训练场景",
                "分享经验帮助他人提升防护能力",
                "持续关注新的风险类型和防护方法"
            ])
        
        # 基于场景的建议
        if scenario_name:
            scenario_suggestions = self._get_scenario_specific_suggestions(scenario_name, score)
            suggestions.extend(scenario_suggestions)
        
        return suggestions
    
    def _generate_knowledge_points(
        self, 
        drill_type: str, 
        answers: List[int], 
        correct_answers: List[int]
    ) -> List[str]:
        """生成相关知识点"""
        knowledge_points = []
        
        # 基于训练类型的知识点
        if "情感欺诈" in drill_type:
            knowledge_points.extend([
                "情感操控的常见手段识别",
                "网络交往中的风险信号",
                "个人信息保护原则",
                "情感诈骗的心理机制",
                "如何建立健康的网络关系"
            ])
        elif "边界设定" in drill_type:
            knowledge_points.extend([
                "个人边界的重要性",
                "如何明确表达自己的界限",
                "识别他人越界行为",
                "在不同关系中设置适当边界",
                "边界维护的沟通技巧"
            ])
        elif "情感操控" in drill_type:
            knowledge_points.extend([
                "情感操控的识别标志",
                "操控者常用的心理策略",
                "如何保护自己免受操控",
                "建立健康的自我认知",
                "寻求支持和帮助的渠道"
            ])
        else:
            knowledge_points.extend([
                "基础防护意识培养",
                "风险评估方法",
                "安全行为准则",
                "应急处理策略"
            ])
        
        return knowledge_points
    
    def _generate_performance_evaluation(
        self, 
        score: float, 
        accuracy_rate: float, 
        completion_time: Optional[int], 
        total_questions: int
    ) -> Dict[str, Any]:
        """生成表现评估"""
        evaluation = {
            "score_level": self._get_performance_level(score),
            "accuracy_assessment": self._get_accuracy_assessment(accuracy_rate),
            "speed_assessment": None,
            "overall_rating": self._get_overall_rating(score),
            "improvement_potential": self._get_improvement_potential(score)
        }
        
        if completion_time:
            avg_time_per_question = completion_time / total_questions
            evaluation["speed_assessment"] = self._get_speed_assessment(avg_time_per_question)
        
        return evaluation
    
    def _get_performance_level(self, score: float) -> str:
        """获取表现水平"""
        if score >= 90:
            return "优秀"
        elif score >= 80:
            return "良好"
        elif score >= 70:
            return "中等"
        elif score >= 60:
            return "及格"
        else:
            return "待提升"
    
    def _get_score_evaluation(self, score: float) -> str:
        """获取得分评价"""
        if score >= 90:
            return "非常出色"
        elif score >= 80:
            return "表现良好"
        elif score >= 70:
            return "基本达标"
        elif score >= 60:
            return "需要改进"
        else:
            return "有很大提升空间"
    
    def _get_capability_assessment(self, score: float) -> str:
        """获取能力评估"""
        if score >= 90:
            return "很强"
        elif score >= 80:
            return "较强"
        elif score >= 70:
            return "一般"
        else:
            return "较弱"
    
    def _get_drill_type_description(self, drill_type: str) -> str:
        """获取训练类型描述"""
        descriptions = {
            "情感欺诈识别": "情感欺诈防范",
            "关系边界设定": "人际边界管理",
            "情感操控识别": "情感操控防护",
            "风险评估": "风险识别和评估",
            "安全意识": "安全防护意识"
        }
        return descriptions.get(drill_type, "防护技能")
    
    def _get_scenario_specific_suggestions(self, scenario_name: str, score: float) -> List[str]:
        """获取场景特定建议"""
        suggestions = []
        
        if "网恋" in scenario_name:
            suggestions.extend([
                "在网络交往中保持理性，避免过快建立深度情感联系",
                "注意核实对方身份，警惕虚假信息",
                "不要轻易透露个人敏感信息"
            ])
        elif "职场" in scenario_name:
            suggestions.extend([
                "在职场关系中保持专业性",
                "明确工作与私人生活的界限",
                "学会说不，避免承担过多责任"
            ])
        elif "友情" in scenario_name:
            suggestions.extend([
                "在友谊中保持平等和尊重",
                "识别利用型关系的特征",
                "学会保护自己的情感需求"
            ])
        
        return suggestions
    
    def _get_accuracy_assessment(self, accuracy_rate: float) -> str:
        """获取准确率评估"""
        if accuracy_rate >= 90:
            return "准确率很高，判断能力优秀"
        elif accuracy_rate >= 80:
            return "准确率良好，判断基本准确"
        elif accuracy_rate >= 70:
            return "准确率中等，有改进空间"
        else:
            return "准确率较低，需要加强练习"
    
    def _get_speed_assessment(self, avg_time: float) -> str:
        """获取速度评估"""
        if avg_time < 30:
            return "答题速度很快，反应敏捷"
        elif avg_time < 60:
            return "答题速度适中，思考充分"
        else:
            return "答题较为谨慎，思考深入"
    
    def _get_overall_rating(self, score: float) -> int:
        """获取整体评级（1-5星）"""
        if score >= 90:
            return 5
        elif score >= 80:
            return 4
        elif score >= 70:
            return 3
        elif score >= 60:
            return 2
        else:
            return 1
    
    def _get_improvement_potential(self, score: float) -> str:
        """获取提升潜力评估"""
        if score >= 90:
            return "已达到很高水平，可以挑战更复杂场景"
        elif score >= 80:
            return "具有进一步提升的潜力"
        elif score >= 70:
            return "有较大的提升空间"
        else:
            return "有很大的提升潜力，建议加强练习"
    
    def _generate_fallback_analysis(self, drill_type: str, score: float, accuracy_rate: float) -> Dict[str, Any]:
        """生成备用分析（当AI分析失败时）"""
        return {
            "overall_analysis": f"本次{drill_type}训练得分{score}%，正确率{accuracy_rate:.1f}%。",
            "question_analysis": [],
            "strength_analysis": ["参与训练的积极态度"],
            "weakness_analysis": ["需要继续练习提升"],
            "improvement_suggestions": ["建议多参加类似训练", "加强相关知识学习"],
            "knowledge_points": ["基础防护知识", "风险识别技能"],
            "performance_evaluation": {
                "score_level": self._get_performance_level(score),
                "accuracy_assessment": self._get_accuracy_assessment(accuracy_rate),
                "overall_rating": self._get_overall_rating(score),
                "improvement_potential": self._get_improvement_potential(score)
            }
        }

# 创建全局实例
ai_analysis_service = AIAnalysisService()
