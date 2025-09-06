#!/usr/bin/env python3
"""
测试修复后的风险评估API
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
from app.services.risk_assessment_service import RiskAssessmentService
import uuid
from datetime import datetime

async def test_api_with_pagination():
    """测试带分页的API"""
    
    print("============================================================")
    print("🔍 测试分页API功能")
    print("============================================================")
    
    db: Session = SessionLocal()
    
    try:
        # 1. 创建测试用户
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
        
        # 2. 创建多个会话和报告
        print("📋 创建多个测试报告...")
        psychological_assessment_service = PsychologicalAssessmentService()
        
        for i in range(3):
            # 创建会话
            chat_session = ChatSession(
                user_id=test_user.user_id,
                scene="self-dialog",
                title=f"测试会话 {i+1}",
                created_at=datetime.now()
            )
            db.add(chat_session)
            db.commit()
            db.refresh(chat_session)
            
            # 添加消息
            test_messages = [
                {"role": "user", "content": f"测试消息 {i+1} - 我感觉很绝望"},
                {"role": "assistant", "content": "我理解你的感受..."},
            ]
            
            for msg in test_messages:
                chat_message = ChatMessage(
                    session_id=chat_session.id,
                    role=msg["role"],
                    content=encryption.encrypt_text(msg["content"])
                )
                db.add(chat_message)
            
            db.commit()
            
            # 生成报告
            report = await psychological_assessment_service.generate_report(chat_session.id, db)
            print(f"   ✅ 报告 {i+1} 创建成功: ID {report.report_id}")
        
        # 3. 测试分页功能
        print("\n🔍 测试分页功能...")
        service = RiskAssessmentService(db)
        
        # 测试第1页，每页2条
        page1_reports = service.get_user_reports_history(test_user.user_id, limit=2, page=1)
        print(f"✅ 第1页报告数量: {len(page1_reports)}")
        
        # 测试第2页，每页2条
        page2_reports = service.get_user_reports_history(test_user.user_id, limit=2, page=2)
        print(f"✅ 第2页报告数量: {len(page2_reports)}")
        
        # 确保分页不重复
        page1_ids = [r.report_id for r in page1_reports]
        page2_ids = [r.report_id for r in page2_reports]
        
        print(f"   第1页报告IDs: {page1_ids}")
        print(f"   第2页报告IDs: {page2_ids}")
        
        # 检查是否有重复
        overlap = set(page1_ids) & set(page2_ids)
        if not overlap:
            print("✅ 分页功能正常，无重复数据")
        else:
            print(f"❌ 分页有重复数据: {overlap}")
        
        # 4. 清理测试数据
        print("\n🧹 清理测试数据...")
        # 删除所有测试用户的会话（会级联删除消息和报告）
        sessions = db.query(ChatSession).filter(ChatSession.user_id == test_user.user_id).all()
        for session in sessions:
            db.delete(session)
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
    success = asyncio.run(test_api_with_pagination())
    if success:
        print("\n" + "="*60)
        print("🎉 分页API测试成功！")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
