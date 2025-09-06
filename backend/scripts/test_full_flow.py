#!/usr/bin/env python3
"""
测试风险评估功能 - 创建新用户并测试
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.models.chat_history import ChatSession, ChatMessage
from app.models.risk_assessment_report import RiskAssessmentReport
from app.utils.password import get_password_hash
from app.utils.encryption import encryption
from app.services.psychological_assessment_service import PsychologicalAssessmentService
import uuid
from datetime import datetime

async def test_full_flow():
    """测试完整的心理评估流程"""
    
    print("============================================================")
    print("🔬 完整心理评估流程测试")
    print("============================================================")
    
    db: Session = SessionLocal()
    
    try:
        # 1. 创建一个新用户（用于测试）
        test_username = f"test_user_{uuid.uuid4().hex[:8]}"
        test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        
        print(f"👤 创建测试用户: {test_username}")
        test_user = User(
            username=test_username,
            password_hash=get_password_hash("test123"),
            email=test_email,
            nickname="测试用户",
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ 测试用户创建成功: {test_user.user_id}")
        
        # 2. 为该用户创建一个会话和消息
        print("💬 创建测试会话...")
        chat_session = ChatSession(
            user_id=test_user.user_id,
            scene="self-dialog",
            title="测试会话",
            created_at=datetime.now()
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        print(f"✅ 会话创建成功: {chat_session.id}")
        
        # 3. 添加包含敏感词的消息
        print("📝 添加测试消息...")
        test_messages = [
            {"role": "user", "content": "我今天心情很不好"},
            {"role": "assistant", "content": "我理解你的感受，可以告诉我发生了什么吗？"},
            {"role": "user", "content": "我觉得活着没有意义，想死"},
            {"role": "assistant", "content": "我很担心你，你的生命很珍贵..."},
            {"role": "user", "content": "我想自残，感觉绝望"},
            {"role": "assistant", "content": "请不要伤害自己，让我们一起寻找解决办法..."}
        ]
        
        for msg in test_messages:
            chat_message = ChatMessage(
                session_id=chat_session.id,
                role=msg["role"],
                content=encryption.encrypt_text(msg["content"])
            )
            db.add(chat_message)
        
        db.commit()
        print(f"✅ 添加测试消息: {len(test_messages)}条")
        
        # 4. 生成心理评估报告
        print("🧠 生成心理评估报告...")
        psychological_assessment_service = PsychologicalAssessmentService()
        report = await psychological_assessment_service.generate_report(chat_session.id, db)
        
        if report:
            print(f"✅ 心理评估报告生成成功!")
            print(f"   报告ID: {report.report_id}")
            print(f"   用户ID: {report.user_id}")
            print(f"   风险等级: {report.overall_risk_level}")
            print(f"   风险分数: {report.overall_risk_score}")
        else:
            print("❌ 心理评估报告生成失败")
            return False
        
        # 5. 现在测试API服务
        print("\n🔍 测试风险评估服务...")
        from app.services.risk_assessment_service import RiskAssessmentService
        service = RiskAssessmentService(db)
        
        # 测试获取用户报告历史
        user_reports = service.get_user_reports_history(test_user.user_id, limit=10)
        print(f"✅ 用户报告历史: {len(user_reports)} 条")
        
        for report in user_reports:
            print(f"   - 报告ID: {report.report_id}, 标题: {report.report_title}")
        
        # 6. 清理测试数据
        print("\n🧹 清理测试数据...")
        db.delete(chat_session)  # 由于cascade，会删除关联的消息和报告
        db.delete(test_user)
        db.commit()
        print("✅ 测试数据清理完成")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = asyncio.run(test_full_flow())
    if success:
        print("\n" + "="*60)
        print("🎉 完整流程测试成功！")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
