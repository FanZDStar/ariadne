"""
测试日记标题和标签功能
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.models.emotional_diary import EmotionalDiary
from app.models.user import User


def test_diary_with_tags():
    """测试创建带标签的日记"""
    db = SessionLocal()

    try:
        # 查找一个测试用户
        user = db.query(User).first()
        if not user:
            print("❌ 没有找到测试用户")
            return

        # 创建带标签的日记
        test_diary = EmotionalDiary(
            user_id=user.user_id,
            mood="happy",
            is_private=False,
            image_count=0,
            tags=["测试", "功能", "标签"],  # JSON 数组
        )

        test_diary.decrypted_title = "测试日记标题和标签功能"
        test_diary.decrypted_content = (
            "这是一条测试日记，用于验证标题和标签功能是否正常工作。"
        )

        db.add(test_diary)
        db.commit()
        db.refresh(test_diary)

        print("✅ 成功创建测试日记")
        print(f"   日记ID: {test_diary.diary_id}")
        print(f"   标题: {test_diary.decrypted_title}")
        print(f"   内容: {test_diary.decrypted_content}")
        print(f"   标签: {test_diary.tags}")

        # 查询验证
        diary_check = (
            db.query(EmotionalDiary)
            .filter(EmotionalDiary.diary_id == test_diary.diary_id)
            .first()
        )

        if diary_check and diary_check.tags:
            print(f"✅ 标签存储和查询正常: {diary_check.tags}")
        else:
            print("❌ 标签存储或查询失败")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_diary_with_tags()
