"""
创建用户树洞能量表
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db_connection

def create_tree_energy_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # 创建表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS user_tree_energy (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL UNIQUE,
                energy INT NOT NULL DEFAULT 0 COMMENT '当前能量值',
                level INT NOT NULL DEFAULT 1 COMMENT '浇水等级',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT fk_tree_energy_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户树洞能量表';
            """
            
            cursor.execute(create_table_sql)
            conn.commit()
            print("✅ 用户树洞能量表创建成功！")
            
        except Exception as e:
            print(f"❌ 创建表失败: {e}")
            conn.rollback()
        finally:
            cursor.close()

if __name__ == "__main__":
    create_tree_energy_table()
