"""
诊断悄悄话加载失败问题
检查数据库中是否有问题数据（加密损坏、字段缺失等）
"""

import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session, joinedload
from app.database.session import get_db
from app.models.tree_hole import TreeHoleWhisper
from app.utils.encryption import encryption


def diagnose_whispers():
    """诊断所有悄悄话，找出问题数据"""
    db = next(get_db())

    try:
        print("🔍 开始诊断悄悄话数据...")
        print("=" * 60)

        # 获取所有悄悄话
        whispers = (
            db.query(TreeHoleWhisper)
            .options(
                joinedload(TreeHoleWhisper.user), joinedload(TreeHoleWhisper.images)
            )
            .all()
        )

        total = len(whispers)
        problematic = []

        print(f"\n📊 总共 {total} 条悄悄话\n")

        for whisper in whispers:
            issues = []

            # 检查1：content 是否为空
            if not whisper.content:
                issues.append("内容为空")

            # 检查2：如果是匿名的，尝试解密
            if whisper.is_anonymous:
                try:
                    decrypted = encryption.decrypt_text(whisper.content)
                    if not decrypted:
                        issues.append("解密后内容为空")
                except Exception as e:
                    issues.append(f"解密失败: {str(e)}")

            # 检查3：用户是否存在
            if not whisper.user:
                issues.append("用户不存在")

            # 检查4：图片是否有效
            if whisper.images:
                for img in whisper.images:
                    if not img.image_url:
                        issues.append("图片URL为空")

            # 如果有问题，记录下来
            if issues:
                problematic.append(
                    {
                        "whisper_id": whisper.whisper_id,
                        "is_anonymous": whisper.is_anonymous,
                        "user_id": whisper.user_id,
                        "created_at": whisper.created_at,
                        "issues": issues,
                    }
                )

                print(f"⚠️  悄悄话 #{whisper.whisper_id}:")
                for issue in issues:
                    print(f"     - {issue}")
                print()

        print("=" * 60)
        print(f"\n✅ 诊断完成！")
        print(f"   - 正常数据: {total - len(problematic)} 条")
        print(f"   - 问题数据: {len(problematic)} 条")

        if problematic:
            print(f"\n⚠️  发现 {len(problematic)} 条问题数据：")
            for item in problematic:
                print(f"\n   悄悄话 #{item['whisper_id']}:")
                print(f"   - 是否匿名: {item['is_anonymous']}")
                print(f"   - 用户ID: {item['user_id']}")
                print(f"   - 创建时间: {item['created_at']}")
                print(f"   - 问题:")
                for issue in item["issues"]:
                    print(f"     * {issue}")

            print(f"\n💡 建议：")
            print(f"   1. 检查这些帖子的内容是否损坏")
            print(f"   2. 如果是加密问题，可能需要重新加密")
            print(f"   3. 如果是数据缺失，考虑删除或修复")
        else:
            print(f"\n🎉 所有数据正常！")

    except Exception as e:
        print(f"\n❌ 诊断失败: {str(e)}")
        import traceback

        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    diagnose_whispers()
