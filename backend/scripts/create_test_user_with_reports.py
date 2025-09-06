#!/usr/bin/env python3
"""
创建带有报告的测试用户并测试API
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.user import User
from app.models.chat_history import ChatSession, ChatMessage
from app.utils.password import get_password_hash
from app.utils.encryption import encryption
from app.services.psychological_assessment_service import PsychologicalAssessmentService
import requests
import uuid
from datetime import datetime

async def create_user_with_reports():
    """创建带有报告的测试用户"""
    
    print("============================================================")
    print("👤 创建带有报告的测试用户")
    print("============================================================")
    
    db: Session = SessionLocal()
    
    try:
        # 1. 创建新用户
        test_username = f"frontend_test_{uuid.uuid4().hex[:6]}"
        
        test_user = User(
            username=test_username,
            password_hash=get_password_hash("test123"),
            email=f"{test_username}@example.com",
            nickname="前端测试",
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ 测试用户创建成功: {test_user.user_id} - {test_username}")
        
        # 2. 创建会话和报告
        print("📋 创建测试报告...")
        psychological_assessment_service = PsychologicalAssessmentService()
        
        for i in range(2):
            # 创建会话
            chat_session = ChatSession(
                user_id=test_user.user_id,
                scene="self-dialog",
                title=f"前端测试会话 {i+1}",
                created_at=datetime.now()
            )
            db.add(chat_session)
            db.commit()
            db.refresh(chat_session)
            
            # 添加消息
            test_messages = [
                {"role": "user", "content": f"我感觉很绝望，想死 - 会话{i+1}"},
                {"role": "assistant", "content": "我理解你的感受，请不要放弃..."},
                {"role": "user", "content": "我想自残，活着没意义"},
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
        
        # 3. 测试API
        print(f"\n🔍 测试API...")
        base_url = "http://localhost:8000"
        
        # 登录
        login_data = {
            "username": test_username,
            "password": "test123"
        }
        
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ 登录成功")
            
            # 测试reports-history
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(
                f"{base_url}/risk-assessment/reports-history?page=1&page_size=10",
                headers=headers
            )
            print(f"API状态码: {response.status_code}")
            
            if response.status_code == 500:
                print(f"🚨 500错误: {response.text}")
            elif response.status_code == 200:
                reports = response.json()
                print(f"✅ 成功获取 {len(reports)} 个报告")
                for report in reports:
                    print(f"   - 报告ID: {report['report_id']}, 会话ID: {report['session_id']}")
            else:
                print(f"其他响应: {response.text}")
        else:
            print(f"❌ 登录失败: {login_response.text}")
        
        print(f"\n📝 用户信息:")
        print(f"   用户名: {test_username}")
        print(f"   密码: test123")
        print(f"   用户ID: {test_user.user_id}")
        
        return test_user.user_id, test_username
        
    except Exception as e:
        print(f"❌ 创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None, None
    finally:
        db.close()

if __name__ == "__main__":
    user_id, username = asyncio.run(create_user_with_reports())
    if user_id:
        print("\n" + "="*60)
        print(f"🎉 测试用户创建成功！用户名: {username}")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 创建失败！请检查错误信息")
        print("="*60)
