"""
数据库迁移脚本：修复 risk_assessment_reports 表的 session_id 字段类型并添加外键
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings

def fix_risk_assessment_session_relation():
    """修复风险评估报告与聊天会话的关联"""
    
    # 创建数据库连接
    engine = create_engine(settings.database_url)
    
    try:
        with engine.connect() as connection:
            print("🔧 开始修复 risk_assessment_reports 表...")
            
            # 1. 删除现有数据（如果有的话）
            print("清理现有数据...")
            connection.execute(text("DELETE FROM risk_assessment_reports"))
            
            # 2. 修改 session_id 字段类型从 VARCHAR(255) 改为 INT
            print("修改 session_id 字段类型...")
            connection.execute(text("""
                ALTER TABLE risk_assessment_reports 
                MODIFY COLUMN session_id INT NOT NULL
            """))
            
            # 3. 添加外键约束
            print("添加外键约束...")
            try:
                connection.execute(text("""
                    ALTER TABLE risk_assessment_reports 
                    ADD CONSTRAINT fk_risk_reports_session 
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(id) 
                    ON DELETE CASCADE ON UPDATE RESTRICT
                """))
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print("外键约束已存在，跳过...")
                else:
                    raise e
            
            # 4. 添加索引
            print("添加索引...")
            try:
                connection.execute(text("""
                    CREATE INDEX idx_risk_reports_session_id ON risk_assessment_reports(session_id)
                """))
            except Exception as e:
                if "Duplicate key name" in str(e):
                    print("索引已存在，跳过...")
                else:
                    raise e
            
            connection.commit()
            print("✅ risk_assessment_reports 表修复完成！")
            return True
            
    except Exception as e:
        print(f"❌ 数据库迁移失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_risk_assessment_session_relation()
    if success:
        print("🎉 数据库迁移完成！")
    else:
        print("💥 数据库迁移失败！")
        sys.exit(1)
