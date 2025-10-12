"""
创建浇水冷却记录表
记录每个用户的最后浇水时间，用于实现20分钟冷却机制
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db_connection

def create_watering_cooldown_table():
    """创建用户浇水冷却记录表"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 创建浇水冷却记录表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS user_watering_cooldown (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                last_watering_time DATETIME NOT NULL COMMENT '最后一次浇水时间',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE KEY unique_user (user_id),
                INDEX idx_user_id (user_id),
                INDEX idx_last_watering_time (last_watering_time)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户浇水冷却记录表';
            """
            
            cursor.execute(create_table_sql)
            conn.commit()
            cursor.close()
            
            print("✅ 浇水冷却记录表创建成功！")
            print("📋 表结构:")
            print("  - id: 主键")
            print("  - user_id: 用户ID（外键关联users表）")
            print("  - last_watering_time: 最后一次浇水时间")
            print("  - created_at: 记录创建时间")
            print("  - updated_at: 记录更新时间")
            print("\n⏰ 冷却机制: 用户每20分钟可以浇水一次")
        
    except Exception as e:
        print(f"❌ 创建表失败: {str(e)}")
        raise

if __name__ == "__main__":
    create_watering_cooldown_table()
