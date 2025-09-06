"""
心理评估报告功能测试脚本
用于验证AI生成心理评估报告的功能是否正常
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings
# 导入所有模型以确保关系正确初始化
from app.models import *
from app.services.psychological_assessment_service import psychological_assessment_service
from app.utils.encryption import encryption

# 创建数据库会话
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def test_psychological_assessment():
    """测试心理评估报告生成功能"""
    db = SessionLocal()
    
    try:
        print("🧪 开始测试心理评估报告功能...")
        
        # 1. 创建测试用户（如果不存在）
        test_user = db.query(User).filter(User.username == "test_user").first()
        if not test_user:
            # 检查邮箱是否已被使用
            existing_email_user = db.query(User).filter(User.email == "test@example.com").first()
            if existing_email_user:
                # 如果邮箱被占用，使用该用户
                test_user = existing_email_user
                print(f"✅ 使用现有邮箱用户: {test_user.user_id}")
            else:
                # 创建新用户
                from app.utils.password import get_password_hash
                test_user = User(
                    username="test_user",
                    password_hash=get_password_hash("test123"),
                    email="test@example.com",
                    nickname="测试用户"
                )
                db.add(test_user)
                db.commit()
                db.refresh(test_user)
                print(f"✅ 创建测试用户: {test_user.user_id}")
        else:
            print(f"✅ 使用现有测试用户: {test_user.user_id}")
        
        # 2. 创建包含风险内容的测试会话
        chat_session = ChatSession(
            user_id=test_user.user_id,
            scene="self-dialog",
            title="心理评估测试会话",
            auto_save_enabled=True
        )
        db.add(chat_session)
        db.flush()
        print(f"✅ 创建测试会话: {chat_session.id}")
        
        # 3. 添加测试消息（包含风险关键词）
        test_messages = [
            {"role": "assistant", "content": "你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。"},
            {"role": "user", "content": "你好，我最近感觉很糟糕，我想死了，感觉活着没有意义"},
            {"role": "assistant", "content": "我能感受到你现在正在经历很大的痛苦，你的感受是真实的，我想陪伴你一起面对这些困难。请告诉我，是什么让你感到如此绝望？"},
            {"role": "user", "content": "工作压力太大了，感觉自己一无是处，没有人理解我，我觉得绝望"},
            {"role": "assistant", "content": "工作压力和感到不被理解确实会让人感到非常痛苦。你说你感到绝望，这让我很担心你。你现在是否有过自伤的想法？"},
            {"role": "user", "content": "有时候确实会想到自残，觉得这样能够缓解内心的痛苦"}
        ]
        
        for msg in test_messages:
            chat_message = ChatMessage(
                session_id=chat_session.id,
                role=msg["role"],
                content=encryption.encrypt_text(msg["content"])  # 加密存储
            )
            db.add(chat_message)
        
        db.commit()
        print(f"✅ 添加测试消息: {len(test_messages)}条")
        
        # 4. 生成心理评估报告
        print("🧠 开始生成心理评估报告...")
        report = await psychological_assessment_service.generate_report(chat_session.id, db)
        
        if report:
            print(f"✅ 心理评估报告生成成功!")
            print(f"   报告ID: {report.report_id}")
            print(f"   风险等级: {report.overall_risk_level}")
            print(f"   风险分数: {report.overall_risk_score}")
            print(f"   检测到的关键词: {report.detected_keywords}")
            print(f"   总消息数: {report.total_messages}")
            print(f"   风险消息数: {report.risk_messages_count}")
            print(f"   报告摘要: {report.summary}")
            print(f"   AI分析: {report.ai_analysis[:200]}...")
            print(f"   建议数量: {len(report.recommendations)}")
        else:
            print("❌ 心理评估报告生成失败")
            return False
        
        # 5. 清理测试数据
        print("🧹 清理测试数据...")
        db.delete(chat_session)  # 由于设置了cascade，会自动删除关联的消息和报告
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

async def main():
    """主函数"""
    print("=" * 60)
    print("🧠 心理评估报告功能测试")
    print("=" * 60)
    
    success = await test_psychological_assessment()
    
    print("=" * 60)
    if success:
        print("🎉 所有测试通过！心理评估报告功能正常工作")
    else:
        print("💥 测试失败！请检查错误信息")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
