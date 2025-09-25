#!/usr/bin/env python3
"""
检查用户日记背景数据库表的脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import engine, SessionLocal
from app.models.user_diary_backgrounds import UserDiaryBackground
from sqlalchemy import inspect

def check_table():
    """检查用户日记背景表是否存在"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("📊 数据库表列表:")
    for table in sorted(tables):
        print(f"  ✅ {table}")
    
    # 检查具体表
    table_name = 'user_diary_backgrounds'
    if table_name in tables:
        print(f"\n✅ 表 '{table_name}' 存在")
        
        # 获取表结构
        columns = inspector.get_columns(table_name)
        print(f"\n📋 表 '{table_name}' 结构:")
        for column in columns:
            print(f"  - {column['name']}: {column['type']} {'(主键)' if column.get('primary_key') else ''}")
    else:
        print(f"\n❌ 表 '{table_name}' 不存在")
        print("需要运行数据库迁移脚本创建表")
    
    # 检查数据
    db = SessionLocal()
    try:
        count = db.query(UserDiaryBackground).count()
        print(f"\n📈 表 '{table_name}' 中的记录数: {count}")
    except Exception as e:
        print(f"\n❌ 查询数据时出错: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔍 检查用户日记背景数据库表...")
    check_table()
    print("\n✅ 检查完成!")