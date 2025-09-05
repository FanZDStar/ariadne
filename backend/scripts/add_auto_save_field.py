"""
数据库迁移脚本：为 chat_sessions 表添加 auto_save_enabled 字段
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def add_auto_save_field():
    """为 chat_sessions 表添加 auto_save_enabled 字段"""
    
    # 创建数据库连接
    engine = create_engine(settings.database_url)
    
    try:
        with engine.connect() as connection:
            # 检查字段是否已存在
            check_query = text("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'chat_sessions' 
                AND COLUMN_NAME = 'auto_save_enabled'
            """)
            
            result = connection.execute(check_query)
            field_exists = result.fetchone()[0] > 0
            
            if field_exists:
                print("✅ auto_save_enabled 字段已存在，无需添加")
                return True
            
            # 添加字段
            add_field_query = text("""
                ALTER TABLE chat_sessions 
                ADD COLUMN auto_save_enabled BOOLEAN NOT NULL DEFAULT FALSE
            """)
            
            connection.execute(add_field_query)
            connection.commit()
            
            print("✅ 成功添加 auto_save_enabled 字段到 chat_sessions 表")
            return True
            
    except Exception as e:
        print(f"❌ 数据库迁移失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = add_auto_save_field()
    if success:
        print("🎉 数据库迁移完成！")
    else:
        print("💥 数据库迁移失败！")
        sys.exit(1)
