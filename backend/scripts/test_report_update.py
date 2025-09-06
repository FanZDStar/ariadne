#!/usr/bin/env python3
"""
测试报告更新逻辑
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

async def test_report_update_logic():
    """测试报告更新逻辑"""
    
    print("============================================================")
    print("🔄 测试报告更新逻辑")
    print("============================================================")
    
    db: Session = SessionLocal()
    
    try:
        # 1. 创建测试用户
        test_username = f"update_test_{uuid.uuid4().hex[:6]}"
        
        test_user = User(
            username=test_username,
            password_hash=get_password_hash("test123"),
            email=f"{test_username}@example.com",
            nickname="更新测试",
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ 测试用户创建成功: {test_user.user_id} - {test_username}")
        
        # 2. 创建会话
        chat_session = ChatSession(
            user_id=test_user.user_id,
            scene="self-dialog",
            title="报告更新测试会话",
            created_at=datetime.now()
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        print(f"✅ 会话创建成功: {chat_session.id}")
        
        # 3. 添加初始消息
        initial_messages = [
            {"role": "user", "content": "我感觉很绝望"},
            {"role": "assistant", "content": "我理解你的感受..."},
        ]
        
        for msg in initial_messages:
            chat_message = ChatMessage(
                session_id=chat_session.id,
                role=msg["role"],
                content=encryption.encrypt_text(msg["content"])
            )
            db.add(chat_message)
        
        db.commit()
        print(f"✅ 添加了 {len(initial_messages)} 条初始消息")
        
        # 4. 第一次生成报告
        print("\n📝 第一次生成报告...")
        psychological_assessment_service = PsychologicalAssessmentService()
        
        first_report = await psychological_assessment_service.generate_report(chat_session.id, db)
        if first_report:
            print(f"✅ 第一次报告生成成功: ID={first_report.report_id}, 版本={first_report.version}")
            print(f"   风险分数: {first_report.overall_risk_score}")
            print(f"   消息数量: {first_report.total_messages}")
        
        # 5. 检查数据库中的报告数量
        report_count = db.query(RiskAssessmentReport).filter(
            RiskAssessmentReport.session_id == chat_session.id
        ).count()
        print(f"📊 数据库中该会话的报告数量: {report_count}")
        
        # 6. 添加更多消息
        print("\n➕ 添加更多消息...")
        additional_messages = [
            {"role": "user", "content": "我想死，活着没意义"},
            {"role": "assistant", "content": "请不要这样想..."},
            {"role": "user", "content": "我想自残"},
        ]
        
        for msg in additional_messages:
            chat_message = ChatMessage(
                session_id=chat_session.id,
                role=msg["role"],
                content=encryption.encrypt_text(msg["content"])
            )
            db.add(chat_message)
        
        db.commit()
        print(f"✅ 添加了 {len(additional_messages)} 条新消息")
        
        # 7. 第二次生成报告（应该更新现有报告）
        print("\n🔄 第二次生成报告（应该更新现有报告）...")
        
        second_report = await psychological_assessment_service.generate_report(chat_session.id, db)
        if second_report:
            print(f"✅ 第二次报告处理成功: ID={second_report.report_id}, 版本={second_report.version}")
            print(f"   风险分数: {second_report.overall_risk_score}")
            print(f"   消息数量: {second_report.total_messages}")
            
            # 检查是否是同一个报告
            if first_report.report_id == second_report.report_id:
                print("✅ 正确：更新了现有报告而不是创建新报告")
            else:
                print("❌ 错误：创建了新报告而不是更新现有报告")
        
        # 8. 再次检查数据库中的报告数量
        final_report_count = db.query(RiskAssessmentReport).filter(
            RiskAssessmentReport.session_id == chat_session.id
        ).count()
        print(f"📊 最终数据库中该会话的报告数量: {final_report_count}")
        
        if final_report_count == 1:
            print("✅ 成功：始终只有一个报告")
        else:
            print(f"❌ 失败：有 {final_report_count} 个报告")
        
        # 9. 清理测试数据
        print("\n🧹 清理测试数据...")
        db.delete(chat_session)  # 级联删除消息和报告
        db.delete(test_user)
        db.commit()
        print("✅ 测试数据清理完成")
        
        return final_report_count == 1
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = asyncio.run(test_report_update_logic())
    if success:
        print("\n" + "="*60)
        print("🎉 报告更新逻辑测试成功！")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
