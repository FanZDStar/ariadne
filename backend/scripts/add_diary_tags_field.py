"""
添加日记标签字段的迁移脚本
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import engine
from sqlalchemy import text


def add_tags_field():
    """为 emotional_diaries 表添加 tags 字段"""
    with engine.connect() as conn:
        try:
            # 添加 tags 字段（JSON 类型，可以存储标签数组）
            conn.execute(
                text(
                    """
                ALTER TABLE emotional_diaries 
                ADD COLUMN tags JSON DEFAULT NULL COMMENT '日记标签'
            """
                )
            )
            conn.commit()
            print("✅ 成功添加 tags 字段到 emotional_diaries 表")
        except Exception as e:
            print(f"❌ 添加字段失败: {e}")
            print("提示：如果字段已存在，请忽略此错误")


if __name__ == "__main__":
    add_tags_field()
