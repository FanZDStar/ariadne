"""
AI心理评估报告生成服务
基于聊天会话内容生成专业的心理状态评估报告
"""
import asyncio
import aiohttp
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.chat_history import ChatSession, ChatMessage
from app.models.risk_assessment_report import RiskAssessmentReport
from app.utils.encryption import encryption

class PsychologicalAssessmentService:
    """心理评估服务"""
    
    def __init__(self):
        self.risk_keywords = [
            # 自杀相关
            "自杀", "想死", "死了算了", "不想活", "结束生命", "了结自己", "自我了断", 
            "想要死", "我想死", "去死", "寻死", "轻生", "自尽", "一死了之",
            
            # 自残相关  
            "自残", "自伤", "割腕", "割手", "伤害自己", "弄伤自己", "自己伤害",
            "切割自己", "划伤自己", "撞墙", "撞头",
            
            # 绝望相关
            "没有希望", "绝望", "无望", "看不到未来", "没有未来", "活着没意思",
            "人生无意义", "生无可恋", "痛不欲生", "万念俱灰", "心如死灰",
            
            # 药物滥用
            "过量服药", "吃安眠药", "药物自杀", "服毒", "吞药",
            
            # 其他危险行为
            "跳楼", "跳河", "撞车", "上吊", "跳桥", "煤气中毒"
        ]
    
    def analyze_message_content(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """分析消息内容，提取风险指标"""
        
        analysis = {
            "total_messages": len(messages),
            "user_messages": 0,
            "risk_messages": [],
            "detected_keywords": [],
            "risk_score": 0.0,
            "risk_level": "low",
            "emotional_patterns": [],
            "concerning_phrases": []
        }
        
        for i, msg in enumerate(messages):
            if msg["role"] == "user":
                analysis["user_messages"] += 1
                content = msg["content"].lower()
                
                # 检测风险关键词
                detected_keywords_in_msg = []
                for keyword in self.risk_keywords:
                    if keyword in content:
                        detected_keywords_in_msg.append(keyword)
                        if keyword not in analysis["detected_keywords"]:
                            analysis["detected_keywords"].append(keyword)
                
                # 如果检测到风险关键词，记录为风险消息
                if detected_keywords_in_msg:
                    analysis["risk_messages"].append({
                        "message_index": i,
                        "content": msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"],
                        "keywords": detected_keywords_in_msg,
                        "risk_weight": len(detected_keywords_in_msg)
                    })
                    analysis["risk_score"] += len(detected_keywords_in_msg) * 10
        
        # 计算风险等级
        if analysis["risk_score"] >= 50:
            analysis["risk_level"] = "critical"
        elif analysis["risk_score"] >= 30:
            analysis["risk_level"] = "high"
        elif analysis["risk_score"] >= 15:
            analysis["risk_level"] = "medium"
        else:
            analysis["risk_level"] = "low"
        
        return analysis
    
    async def generate_ai_analysis(self, messages: List[Dict[str, str]], analysis: Dict[str, Any]) -> str:
        """使用AI生成心理状态分析"""
        
        # 构建对话内容摘要
        conversation_summary = ""
        for msg in messages[:10]:  # 最多分析前10条消息
            role_name = "用户" if msg["role"] == "user" else "助手"
            conversation_summary += f"{role_name}: {msg['content'][:200]}\n"
        
        # 构建AI分析的prompt
        ai_prompt = f"""
作为专业的心理健康评估师，请基于以下对话内容进行心理状态评估：

对话内容：
{conversation_summary}

检测到的风险关键词：{', '.join(analysis['detected_keywords'])}
风险消息数量：{len(analysis['risk_messages'])}
整体风险评分：{analysis['risk_score']}
风险等级：{analysis['risk_level']}

请从以下几个维度进行专业分析：

1. **情绪状态评估**：分析用户当前的情绪状态、情感波动程度
2. **心理健康风险**：评估潜在的心理健康风险，包括自伤、自杀风险等
3. **应对机制**：分析用户现有的应对方式和心理韧性
4. **社会支持**：评估用户的社会支持系统状况
5. **专业建议**：提供具体的心理健康建议和干预措施

要求：
- 语言专业但易懂，体现关怀
- 避免过度诊断，重点关注风险预警
- 提供具体可行的建议
- 长度控制在800-1200字

分析报告："""

        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {settings.ai_api_key}',
                    'Content-Type': 'application/json'
                }
                
                data = {
                    "model": "qwen-plus",
                    "messages": [
                        {
                            "role": "user",
                            "content": ai_prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1500
                }
                
                async with session.post(
                    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content'].strip()
                    else:
                        return "AI分析生成失败，请稍后重试。"
                        
        except Exception as e:
            print(f"AI分析生成失败: {e}")
            return "AI分析暂时不可用，请稍后重试。"
    
    def generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """根据风险等级生成建议"""
        
        recommendations = []
        risk_level = analysis["risk_level"]
        
        if risk_level == "critical":
            recommendations.extend([
                "🆘 紧急建议：请立即联系专业心理健康服务或拨打心理危机干预热线：400-161-9995",
                "🏥 建议尽快前往医院心理科或精神科寻求专业帮助",
                "👥 告知信任的朋友或家人您的现状，寻求陪伴和支持",
                "🚫 避免独处，确保身边有人陪伴",
                "📱 删除或远离可能用于自伤的物品"
            ])
        elif risk_level == "high":
            recommendations.extend([
                "⚠️ 强烈建议联系心理健康专业人士进行评估",
                "🤝 与信任的朋友、家人或心理咨询师交流您的感受",
                "📞 保存心理危机干预热线号码：400-161-9995",
                "🧘 尝试放松技巧，如深呼吸、冥想或轻度运动",
                "📝 记录情绪变化，了解触发因素"
            ])
        elif risk_level == "medium":
            recommendations.extend([
                "💚 建议关注自己的心理健康状态",
                "🗣️ 与信任的人分享您的感受",
                "🏃 保持规律的作息和适度运动",
                "🎨 参与喜欢的活动，培养兴趣爱好",
                "📚 学习情绪管理技巧"
            ])
        else:
            recommendations.extend([
                "😊 继续保持积极的心理状态",
                "🌱 关注个人成长和自我提升",
                "🤗 维护良好的人际关系",
                "⚖️ 保持工作与生活的平衡",
                "🎯 设定合理的目标和期望"
            ])
        
        # 通用建议
        recommendations.extend([
            "📱 如需专业支持，可使用心理健康应用或在线咨询服务",
            "📖 推荐阅读心理健康相关书籍和资料",
            "🕰️ 给自己时间，心理康复是一个渐进的过程"
        ])
        
        return recommendations
    
    async def generate_report(self, session_id: int, db: Session) -> Optional[RiskAssessmentReport]:
        """为指定会话生成心理评估报告"""
        
        try:
            # 获取会话信息
            chat_session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
            if not chat_session:
                print(f"❌ 会话 {session_id} 不存在")
                return None
            
            # 获取会话消息
            messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session_id
            ).order_by(ChatMessage.created_at.asc()).all()
            
            if not messages:
                print(f"❌ 会话 {session_id} 没有消息")
                return None
            
            # 转换消息格式
            message_list = [
                {"role": msg.role, "content": encryption.decrypt_text(msg.content)}
                for msg in messages
            ]
            
            print(f"📊 开始分析会话 {session_id}，消息数量：{len(message_list)}")
            
            # 分析消息内容
            analysis = self.analyze_message_content(message_list)
            
            # 只有检测到风险才生成报告
            if len(analysis["risk_messages"]) == 0:
                print(f"ℹ️ 会话 {session_id} 未检测到风险，跳过报告生成")
                return None
            
            print(f"🚨 检测到风险：风险等级 {analysis['risk_level']}，风险分数 {analysis['risk_score']}")
            
            # 生成AI分析
            ai_analysis = await self.generate_ai_analysis(message_list, analysis)
            
            # 生成建议
            recommendations = self.generate_recommendations(analysis)
            
            # 检查是否已存在该会话的报告
            existing_report = db.query(RiskAssessmentReport).filter(
                RiskAssessmentReport.session_id == session_id
            ).first()
            
            if existing_report:
                # 更新现有报告
                print(f"🔄 更新现有报告：report_id={existing_report.report_id}")
                existing_report.report_title = f"心理状态评估报告 - {analysis['risk_level'].upper()}风险"
                existing_report.report_content = ai_analysis
                existing_report.summary = f"基于{analysis['total_messages']}条消息的分析，检测到{len(analysis['risk_messages'])}条风险消息，整体风险等级为{analysis['risk_level']}。"
                existing_report.overall_risk_level = analysis['risk_level']
                existing_report.overall_risk_score = analysis['risk_score']
                existing_report.total_messages = analysis['total_messages']
                existing_report.risk_messages_count = len(analysis['risk_messages'])
                existing_report.detected_keywords = analysis['detected_keywords']
                existing_report.risk_trends = {"risk_messages": analysis['risk_messages']}
                existing_report.ai_analysis = ai_analysis
                existing_report.recommendations = recommendations
                existing_report.conversation_end_time = datetime.utcnow()
                existing_report.report_generated_time = datetime.utcnow()  # 更新生成时间
                existing_report.version = (existing_report.version or 1) + 1  # 增加版本号
                
                db.commit()
                db.refresh(existing_report)
                
                print(f"✅ 心理评估报告更新成功：report_id={existing_report.report_id}, 版本={existing_report.version}")
                return existing_report
            else:
                # 创建新报告
                print(f"📝 创建新报告...")
                report = RiskAssessmentReport(
                    user_id=chat_session.user_id,
                    session_id=session_id,
                    scene=chat_session.scene,
                    report_title=f"心理状态评估报告 - {analysis['risk_level'].upper()}风险",
                    report_content=ai_analysis,
                    summary=f"基于{analysis['total_messages']}条消息的分析，检测到{len(analysis['risk_messages'])}条风险消息，整体风险等级为{analysis['risk_level']}。",
                    overall_risk_level=analysis['risk_level'],
                    overall_risk_score=analysis['risk_score'],
                    total_messages=analysis['total_messages'],
                    risk_messages_count=len(analysis['risk_messages']),
                    detected_keywords=analysis['detected_keywords'],
                    risk_trends={"risk_messages": analysis['risk_messages']},
                    ai_analysis=ai_analysis,
                    recommendations=recommendations,
                    conversation_start_time=chat_session.created_at,
                    conversation_end_time=datetime.utcnow(),
                    report_generated_time=datetime.utcnow(),
                    status="completed",
                    is_viewed=False,
                    version=1
                )
                
                db.add(report)
                db.commit()
                db.refresh(report)
                
                print(f"✅ 心理评估报告生成成功：report_id={report.report_id}")
                return report
            return report
            
        except Exception as e:
            print(f"❌ 心理评估报告生成失败: {str(e)}")
            db.rollback()
            return None

# 创建全局实例
psychological_assessment_service = PsychologicalAssessmentService()
