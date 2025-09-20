#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL版本的日记背景图片数据库表创建和测试脚本
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sqlalchemy import create_engine, text
    from app.core.config import settings
    from app.models.diary_background import DiaryBackground
    from app.database.session import Base
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保已安装所有必要的依赖包")
    sys.exit(1)


def create_diary_backgrounds_table():
    """创建日记背景图片表"""
    try:
        engine = create_engine(settings.database_url, echo=True)

        # 创建表
        DiaryBackground.__table__.create(engine, checkfirst=True)
        print("✅ diary_backgrounds 表创建成功")

        # 验证表是否存在
        with engine.connect() as conn:
            # MySQL查询表是否存在的语法
            result = conn.execute(
                text(
                    """
                SELECT TABLE_NAME 
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'diary_backgrounds'
            """
                )
            )

            table_exists = result.fetchone() is not None

            if table_exists:
                print("✅ 表验证成功：diary_backgrounds 表已存在")

                # 获取表结构（MySQL版本）
                result = conn.execute(
                    text(
                        """
                    DESCRIBE diary_backgrounds
                """
                    )
                )
                columns = result.fetchall()

                print("📋 表结构:")
                for col in columns:
                    print(
                        f"   {col[0]} - {col[1]} {col[2] if col[2] != 'YES' else ''} {col[3] if col[3] else ''}"
                    )

            else:
                print("❌ 表验证失败：diary_backgrounds 表不存在")

    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        print("请检查：")
        print("1. MySQL服务是否正在运行")
        print("2. 数据库连接配置是否正确")
        print("3. 用户是否有创建表的权限")


def test_table_operations():
    """测试表的基本操作"""
    try:
        from sqlalchemy.orm import sessionmaker
        from app.database.session import get_db

        engine = create_engine(settings.database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        db = SessionLocal()

        # 测试查询（应该返回空结果）
        backgrounds = db.query(DiaryBackground).limit(5).all()
        print(f"✅ 查询测试成功，当前记录数: {len(backgrounds)}")

        db.close()

    except Exception as e:
        print(f"❌ 表操作测试失败: {e}")


if __name__ == "__main__":
    print("🚀 开始创建 diary_backgrounds 表...")
    create_diary_backgrounds_table()

    print("\n🧪 测试表操作...")
    test_table_operations()

    print("\n✨ 完成！你现在可以使用日记背景图片功能了。")
