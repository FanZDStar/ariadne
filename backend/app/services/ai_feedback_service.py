"""
AI反馈建议服务
为防护训练提供个性化的AI反馈和建议
"""
from typing import List, Dict, Any, Optional
import json
import asyncio
from app.core.ai_service import AIService

class AIFeedbackService:
    def __init__(self):
        self.ai_service = AIService()
    
    def get_completion(self, prompt: str) -> str:
        """同步获取AI完成文本"""
        try:
            # 创建新的事件循环来运行异步函数
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            messages = [{"role": "user", "content": prompt}]
            result = loop.run_until_complete(
                self.ai_service.get_response(messages, scene="feedback_generation")
            )
            
            loop.close()
            return result
        except Exception as e:
            print(f"AI完成文本获取失败: {e}")
            return ""
    
    def generate_question_feedback(
        self,
        question_title: str,
        question_text: str,
        selected_option: str,
        correct_option: str,
        is_correct: bool,
        explanation: str,
        risk_explanation: str,
        drill_type: str = "防护训练"
    ) -> str:
        """
        为单个题目生成AI个性化反馈
        
        Args:
            question_title: 题目标题
            question_text: 题目内容
            selected_option: 用户选择的选项
            correct_option: 正确选项
            is_correct: 是否回答正确
            explanation: 答案解释
            risk_explanation: 风险解释
            drill_type: 训练类型
            
        Returns:
            AI生成的个性化反馈建议
        """
        try:
            prompt = f"""
作为一名专业的心理健康与人际关系安全指导师，请为用户的这道{drill_type}题目提供个性化的反馈和建议。

题目信息：
- 标题：{question_title}
- 内容：{question_text}
- 用户选择：{selected_option}
- 正确答案：{correct_option}
- 回答结果：{'正确' if is_correct else '错误'}
- 答案解释：{explanation}
- 风险说明：{risk_explanation}

请根据以上信息，为用户提供以下内容：

1. **针对性反馈**：根据用户的选择，给出具体的反馈
2. **学习要点**：从这道题目中应该学到的关键知识点
3. **实际应用**：在真实生活中如何运用这些知识
4. **进一步建议**：针对用户的表现，提供个性化的改进建议

要求：
- 语言温和、鼓励性，避免过度批评
- 提供具体、可操作的建议
- 重点关注安全防护和自我保护
- 内容简洁明了，不超过200字
- 使用友好的语调，就像一位经验丰富的导师在指导

请直接提供反馈内容，不需要格式标记：
"""

            response = self.get_completion(prompt)
            return response.strip() if response else "继续加油！每道题都是学习的机会。"
            
        except Exception as e:
            print(f"生成题目反馈失败: {e}")
            # 提供基础反馈
            if is_correct:
                return f"回答正确！你很好地识别了{question_title}中的关键要点。{explanation[:50]}... 继续保持这种敏锐的观察力！"
            else:
                return f"这道题目需要再仔细思考。{explanation[:50]}... 建议多关注风险信号的识别，在日常生活中提高警觉性。"
    
    def generate_overall_analysis(
        self,
        drill_type: str,
        scenario_name: str,
        total_questions: int,
        correct_answers: int,
        accuracy_rate: float,
        question_analysis: List[Dict[str, Any]],
        completion_time: Optional[int] = None
    ) -> str:
        """
        生成整体训练分析和建议
        
        Args:
            drill_type: 训练类型
            scenario_name: 场景名称
            total_questions: 总题数
            correct_answers: 正确答案数
            accuracy_rate: 准确率
            question_analysis: 详细答题分析
            completion_time: 完成时间（秒）
            
        Returns:
            AI生成的整体分析和建议
        """
        try:
            # 分析错误题目的模式
            wrong_questions = [q for q in question_analysis if not q.get('is_correct', False)]
            common_issues = self._analyze_common_issues(wrong_questions)
            
            time_info = f"，用时{completion_time//60}分钟{completion_time%60}秒" if completion_time else ""
            
            prompt = f"""
作为一名专业的心理健康与人际关系安全指导师，请为用户的{drill_type}训练结果提供深度分析和个性化建议。

训练概况：
- 训练类型：{drill_type}
- 场景：{scenario_name}
- 成绩：{correct_answers}/{total_questions}题正确，准确率{accuracy_rate:.1f}%{time_info}

错误题目分析：
{self._format_wrong_questions(wrong_questions)}

常见问题模式：
{common_issues}

请提供以下分析：

1. **优势表现**：用户在哪些方面表现突出
2. **改进空间**：需要加强的关键领域
3. **学习重点**：下一步应该重点学习的内容
4. **实践建议**：在日常生活中如何运用所学知识
5. **训练计划**：针对性的后续训练建议

要求：
- 基于具体的答题表现给出分析
- 提供可操作的改进建议
- 语言鼓励且专业
- 重点关注安全防护能力的提升
- 内容控制在300字以内

请直接提供分析内容：
"""

            response = self.get_completion(prompt)
            return response.strip() if response else self._generate_basic_analysis(accuracy_rate, common_issues)
            
        except Exception as e:
            print(f"生成整体分析失败: {e}")
            return self._generate_basic_analysis(accuracy_rate, "需要进一步提升风险识别能力")
    
    def _analyze_common_issues(self, wrong_questions: List[Dict[str, Any]]) -> str:
        """分析错误题目的共同问题"""
        if not wrong_questions:
            return "本次训练表现优秀，没有明显的问题模式。"
        
        issues = []
        
        # 分析错误模式
        risk_identification_errors = 0
        response_strategy_errors = 0
        boundary_setting_errors = 0
        
        for question in wrong_questions:
            question_title = question.get('question_title', '')
            if '识别' in question_title or '信号' in question_title:
                risk_identification_errors += 1
            elif '应对' in question_title or '策略' in question_title:
                response_strategy_errors += 1
            elif '边界' in question_title or '拒绝' in question_title:
                boundary_setting_errors += 1
        
        if risk_identification_errors > 0:
            issues.append("风险信号识别能力需要加强")
        if response_strategy_errors > 0:
            issues.append("应对策略选择需要改进")
        if boundary_setting_errors > 0:
            issues.append("个人边界设定技巧需要提升")
        
        return "；".join(issues) if issues else "错误分布相对平均，需要全面提升"
    
    def _format_wrong_questions(self, wrong_questions: List[Dict[str, Any]]) -> str:
        """格式化错误题目信息"""
        if not wrong_questions:
            return "本次训练全部答对！"
        
        formatted = []
        for i, question in enumerate(wrong_questions[:3], 1):  # 只显示前3个错误
            title = question.get('question_title', f'题目{i}')
            selected = question.get('selected_option', '未知选择')
            correct = question.get('correct_option', '未知答案')
            formatted.append(f"- {title}：选择了\"{selected}\"，正确答案是\"{correct}\"")
        
        if len(wrong_questions) > 3:
            formatted.append(f"- 以及其他{len(wrong_questions)-3}道题目...")
        
        return "\n".join(formatted)
    
    def _generate_basic_analysis(self, accuracy_rate: float, common_issues: str) -> str:
        """生成基础分析（当AI服务不可用时）"""
        if accuracy_rate >= 90:
            performance = "优秀"
            suggestion = "继续保持高度的安全意识，可以尝试更高难度的训练。"
        elif accuracy_rate >= 80:
            performance = "良好"
            suggestion = "基础防护能力扎实，建议针对薄弱环节进行专项训练。"
        elif accuracy_rate >= 70:
            performance = "中等"
            suggestion = "需要加强对风险信号的敏感度，多练习识别和应对技巧。"
        elif accuracy_rate >= 60:
            performance = "及格"
            suggestion = "建议系统学习人际关系安全知识，重点练习风险识别。"
        else:
            performance = "需努力"
            suggestion = "建议从基础知识开始学习，逐步提升安全防护意识。"
        
        return f"""
**训练表现**: {performance}（准确率{accuracy_rate:.1f}%）

**主要问题**: {common_issues}

**改进建议**: {suggestion}

**下步重点**: 建议重点学习风险信号识别、边界设定和应对策略，在日常生活中多加练习和应用。
"""

# 创建全局实例
ai_feedback_service = AIFeedbackService()
