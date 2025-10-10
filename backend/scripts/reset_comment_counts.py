"""
重置所有悄悄话的评论数为0，并同步为实际的评论数量
这个脚本会：
1. 将所有悄悄话的 comment_count 重置为 0
2. 根据 TreeHoleComment 表中的实际评论数重新计算
3. 更新数据库
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.tree_hole import TreeHoleWhisper, TreeHoleComment


def reset_and_sync_comment_counts():
    """重置并同步所有悄悄话的评论数量"""
    db = next(get_db())

    try:
        print("🚀 开始重置评论计数...")
        print("=" * 60)

        # 获取所有悄悄话
        whispers = db.query(TreeHoleWhisper).all()
        total_whispers = len(whispers)

        print(f"📊 找到 {total_whispers} 条悄悄话记录\n")

        # 第一步：将所有评论数重置为0
        print("🔄 步骤1: 重置所有评论数为0...")
        for whisper in whispers:
            whisper.comment_count = 0

        db.commit()
        print("✅ 所有评论数已重置为0\n")

        # 第二步：根据实际评论数重新计算
        print("🔄 步骤2: 根据实际评论重新计算...")
        updated_count = 0
        has_comments = 0

        for whisper in whispers:
            # 统计实际的评论数
            actual_comment_count = (
                db.query(TreeHoleComment)
                .filter(TreeHoleComment.whisper_id == whisper.whisper_id)
                .count()
            )

            # 更新评论数
            if actual_comment_count > 0:
                whisper.comment_count = actual_comment_count
                print(
                    f"  ✓ 悄悄话 #{whisper.whisper_id}: {actual_comment_count} 条评论"
                )
                has_comments += 1
                updated_count += actual_comment_count

        # 提交更改
        db.commit()

        print("\n" + "=" * 60)
        print("🎉 同步完成！")
        print(f"📊 统计信息:")
        print(f"   - 总悄悄话数: {total_whispers}")
        print(f"   - 有评论的悄悄话: {has_comments}")
        print(f"   - 总评论数: {updated_count}")
        print(f"   - 无评论的悄悄话: {total_whispers - has_comments}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ 操作失败: {str(e)}")
        import traceback

        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  重置悄悄话评论计数工具")
    print("=" * 60 + "\n")

    response = input("⚠️  警告: 此操作将重置所有评论计数！是否继续？(yes/no): ")

    if response.lower() in ["yes", "y"]:
        reset_and_sync_comment_counts()
    else:
        print("\n❌ 操作已取消")
