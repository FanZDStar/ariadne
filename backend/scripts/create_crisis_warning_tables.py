#file:ariadne/backend/scripts/create_crisis_warning_tables.py
"""
心理危机预警系统数据表创建脚本
"""
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from app.core.config import settings
from app.database.session import Base
from app.models.crisis_warning import CrisisWarning, MoodTrendAnalysis

def create_crisis_warning_tables():
    """创建心理危机预警相关数据表"""
    
    # 创建数据库引擎
    engine = create_engine(settings.database_url)
    
    try:
        # 创建表
        print("开始创建心理危机预警数据表...")
        
        # 创建CrisisWarning表
        crisis_warning_sql = """
        CREATE TABLE IF NOT EXISTS crisis_warnings (
            warning_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            warning_type ENUM('mood_trend', 'keyword_alert', 'ai_analysis', 'behavior_pattern') NOT NULL,
            risk_level ENUM('low', 'medium', 'high', 'critical') NOT NULL,
            score FLOAT NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            source_data TEXT,
            keywords_detected TEXT,
            is_resolved BOOLEAN DEFAULT FALSE,
            resolved_at DATETIME NULL,
            resolver_notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_risk_level (risk_level),
            INDEX idx_created_at (created_at),
            INDEX idx_is_resolved (is_resolved),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        # 创建MoodTrendAnalysis表
        mood_trend_sql = """
        CREATE TABLE IF NOT EXISTS mood_trend_analyses (
            analysis_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            period_days INT NOT NULL,
            avg_mood_score FLOAT NOT NULL,
            mood_trend VARCHAR(50) NOT NULL,
            consecutive_low_days INT DEFAULT 0,
            risk_indicators TEXT,
            recommendations TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_created_at (created_at),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        with engine.connect() as connection:
            # 执行SQL
            connection.execute(text(crisis_warning_sql))
            print("✓ crisis_warnings 表创建成功")
            
            connection.execute(text(mood_trend_sql))
            print("✓ mood_trend_analyses 表创建成功")
            
            # 提交事务
            connection.commit()
        
        print("心理危机预警数据表创建完成！")
        
    except Exception as e:
        print(f"创建数据表时发生错误: {str(e)}")
        return False
    
    return True

def add_sample_data():
    """添加示例数据（可选）"""
    engine = create_engine(settings.database_url)
    
    sample_data_sql = """
    -- 插入一些示例的危机关键词配置（如果需要存储在数据库中）
    CREATE TABLE IF NOT EXISTS crisis_keywords (
        keyword_id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50) NOT NULL,
        keyword VARCHAR(100) NOT NULL,
        risk_weight FLOAT DEFAULT 1.0,
        is_active BOOLEAN DEFAULT TRUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_category (category),
        INDEX idx_keyword (keyword)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    
    -- 插入危机关键词
    INSERT IGNORE INTO crisis_keywords (category, keyword, risk_weight) VALUES
    ('自伤', '自杀', 3.0),
    ('自伤', '自残', 3.0),
    ('自伤', '自伤', 3.0),
    ('自伤', '结束生命', 3.0),
    ('自伤', '不想活', 2.5),
    ('自伤', '想死', 2.5),
    ('绝望', '绝望', 2.0),
    ('绝望', '无望', 2.0),
    ('绝望', '没有希望', 2.0),
    ('绝望', '看不到未来', 1.8),
    ('孤独', '孤独', 1.5),
    ('孤独', '孤单', 1.5),
    ('孤独', '没人理解', 1.5),
    ('无价值感', '没用', 1.2),
    ('无价值感', '无价值', 1.5),
    ('无价值感', '废物', 1.8),
    ('极端情绪', '崩溃', 1.2),
    ('极端情绪', '疯了', 1.5),
    ('极端情绪', '受不了', 1.0);
    """
    
    try:
        with engine.connect() as connection:
            # 分割SQL语句并执行
            statements = sample_data_sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    connection.execute(text(statement))
            
            connection.commit()
        
        print("✓ 示例数据添加成功")
        return True
        
    except Exception as e:
        print(f"添加示例数据时发生错误: {str(e)}")
        return False

def main():
    """主函数"""
    print("心理危机预警系统数据库初始化")
    print("=" * 50)
    
    # 创建数据表
    if create_crisis_warning_tables():
        print("\n数据表创建成功！")
        
        # 询问是否添加示例数据
        response = input("\n是否添加示例关键词数据？(y/n): ").lower().strip()
        if response in ['y', 'yes']:
            add_sample_data()
    else:
        print("\n数据表创建失败！")
        return
    
    print("\n初始化完成！")
    print("\n接下来你可以：")
    print("1. 启动应用并测试危机预警API")
    print("2. 配置定时监控任务")
    print("3. 集成到现有的日记和聊天功能中")

if __name__ == "__main__":
    main()
