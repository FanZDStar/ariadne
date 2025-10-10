"""
同步悄悄话的评论数量
将所有悄悄话的 comment_count 字段更新为实际的评论数量（从 TreeHoleComment 表统计）
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.tree_hole import TreeHoleWhisper, TreeHoleComment


def sync_comment_counts():
    """同步所有悄悄话的评论数量"""
    db = next(get_db())

    try:
        # 获取所有悄悄话
        whispers = db.query(TreeHoleWhisper).all()

        updated_count = 0
        for whisper in whispers:
            # 统计实际的评论数
            actual_comment_count = (
                db.query(TreeHoleComment)
                .filter(TreeHoleComment.whisper_id == whisper.whisper_id)
                .count()
            )

            # 如果数量不一致，则更新
            if whisper.comment_count != actual_comment_count:
                old_count = whisper.comment_count
                whisper.comment_count = actual_comment_count
                print(
                    f"✅ 更新悄悄话 #{whisper.whisper_id}: {old_count} → {actual_comment_count}"
                )
                updated_count += 1
            else:
                print(
                    f"✓ 悄悄话 #{whisper.whisper_id} 评论数已同步: {actual_comment_count}"
                )

        # 提交更改
        db.commit()
        print(f"\n🎉 同步完成！共更新 {updated_count} 条记录。")

    except Exception as e:
        db.rollback()
        print(f"❌ 同步失败: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("开始同步悄悄话评论数量...")
    print("=" * 50)
    sync_comment_counts()
