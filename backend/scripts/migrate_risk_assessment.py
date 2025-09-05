#!/usr/bin/env python3
"""
风险评估报告表迁移脚本
为 ariadne 数据库添加风险评估报告功能

运行方式：
python scripts/migrate_risk_assessment.py
"""

import sys
import os
import mysql.connector
from datetime import datetime
from urllib.parse import urlparse

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_env_file():
    """手动加载.env文件"""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def get_database_config():
    """获取数据库配置"""
    # 先尝试加载.env文件
    load_env_file()
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("未找到DATABASE_URL环境变量")
    
    parsed = urlparse(database_url)
    
    return {
        'host': parsed.hostname,
        'port': parsed.port or 3306,
        'user': parsed.username,
        'password': parsed.password,
        'database': parsed.path.lstrip('/'),
        'charset': 'utf8mb4'
    }

def create_risk_assessment_tables():
    """创建风险评估报告相关表"""
    
    connection = None
    cursor = None
    
    try:
        # 获取数据库配置
        db_config = get_database_config()
        
        # 连接数据库
        connection = mysql.connector.connect(**db_config)
        
        cursor = connection.cursor()
        
        print("🚀 开始创建风险评估报告表...")
        
        # 1. 创建风险评估报告表
        create_risk_assessment_table = """
        CREATE TABLE IF NOT EXISTS risk_assessment_reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            session_id VARCHAR(255) NOT NULL,
            overall_risk_level ENUM('low', 'medium', 'high', 'critical') NOT NULL DEFAULT 'low',
            overall_risk_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
            summary TEXT,
            ai_analysis TEXT,
            detected_keywords JSON,
            recommendations JSON,
            total_messages INT NOT NULL DEFAULT 0,
            risk_messages_count INT NOT NULL DEFAULT 0,
            conversation_start_time DATETIME,
            conversation_end_time DATETIME,
            report_generated_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            version INT NOT NULL DEFAULT 1,
            status ENUM('generated', 'viewed', 'shared') NOT NULL DEFAULT 'generated',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_user_id (user_id),
            INDEX idx_session_id (session_id),
            INDEX idx_risk_level (overall_risk_level),
            INDEX idx_report_time (report_generated_time),
            INDEX idx_status (status),
            
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_risk_assessment_table)
        print("✅ 风险评估报告表创建成功")
        
        # 2. 检查并添加用户表的新字段（如果需要）
        check_user_fields = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s 
        AND TABLE_NAME = 'users' 
        AND COLUMN_NAME IN ('last_risk_assessment', 'total_risk_reports')
        """
        
        db_config = get_database_config()
        cursor.execute(check_user_fields, (db_config['database'],))
        existing_fields = [row[0] for row in cursor.fetchall()]
        
        if 'last_risk_assessment' not in existing_fields:
            alter_user_table_1 = """
            ALTER TABLE users 
            ADD COLUMN last_risk_assessment DATETIME NULL
            """
            cursor.execute(alter_user_table_1)
            print("✅ 添加用户最后风险评估时间字段")
        
        if 'total_risk_reports' not in existing_fields:
            alter_user_table_2 = """
            ALTER TABLE users 
            ADD COLUMN total_risk_reports INT NOT NULL DEFAULT 0
            """
            cursor.execute(alter_user_table_2)
            print("✅ 添加用户总风险报告数字段")
        
        # 3. 创建触发器，自动更新用户风险报告统计
        create_trigger = """
        CREATE TRIGGER IF NOT EXISTS update_user_risk_stats
        AFTER INSERT ON risk_assessment_reports
        FOR EACH ROW
        BEGIN
            UPDATE users 
            SET 
                last_risk_assessment = NEW.report_generated_time,
                total_risk_reports = total_risk_reports + 1
            WHERE id = NEW.user_id;
        END;
        """
        
        cursor.execute(create_trigger)
        print("✅ 用户风险统计触发器创建成功")
        
        # 4. 插入示例数据（可选）
        if input("是否插入示例数据? (y/n): ").lower() == 'y':
            insert_sample_data(cursor)
        
        # 提交所有更改
        connection.commit()
        print("🎉 风险评估报告表迁移完成！")
        
        # 显示表结构信息
        show_table_info(cursor)
        
    except mysql.connector.Error as e:
        print(f"❌ 数据库错误: {e}")
        if connection:
            connection.rollback()
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        if connection:
            connection.rollback()
        sys.exit(1)
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_sample_data(cursor):
    """插入示例数据"""
    print("📝 插入示例数据...")
    
    # 获取第一个用户ID（如果存在）
    cursor.execute("SELECT id FROM users LIMIT 1")
    user_result = cursor.fetchone()
    
    if not user_result:
        print("⚠️  没有找到用户，跳过示例数据插入")
        return
    
    user_id = user_result[0]
    
    sample_reports = [
        {
            'user_id': user_id,
            'session_id': 'sample_session_001',
            'overall_risk_level': 'medium',
            'overall_risk_score': 65.5,
            'summary': '用户在对话中表现出一定程度的焦虑情绪，主要集中在学业压力方面。',
            'ai_analysis': '根据对话分析，用户目前处于中等风险水平。建议关注情绪变化，必要时寻求专业帮助。',
            'detected_keywords': '["焦虑", "压力", "失眠"]',
            'recommendations': '["保持规律作息", "适度运动", "与朋友交流"]',
            'total_messages': 25,
            'risk_messages_count': 3,
            'version': 1
        },
        {
            'user_id': user_id,
            'session_id': 'sample_session_002',
            'overall_risk_level': 'low',
            'overall_risk_score': 25.0,
            'summary': '用户情绪状态良好，对话内容积极正面。',
            'ai_analysis': '用户展现出良好的心理状态，建议继续保持积极的生活方式。',
            'detected_keywords': '["开心", "积极", "希望"]',
            'recommendations': '["继续保持良好心态", "分享正能量"]',
            'total_messages': 18,
            'risk_messages_count': 0,
            'version': 1
        }
    ]
    
    insert_query = """
    INSERT INTO risk_assessment_reports 
    (user_id, session_id, overall_risk_level, overall_risk_score, summary, ai_analysis, 
     detected_keywords, recommendations, total_messages, risk_messages_count, version)
    VALUES (%(user_id)s, %(session_id)s, %(overall_risk_level)s, %(overall_risk_score)s, 
            %(summary)s, %(ai_analysis)s, %(detected_keywords)s, %(recommendations)s, 
            %(total_messages)s, %(risk_messages_count)s, %(version)s)
    """
    
    cursor.executemany(insert_query, sample_reports)
    print(f"✅ 插入了 {len(sample_reports)} 条示例数据")

def show_table_info(cursor):
    """显示表结构信息"""
    print("\n📊 表结构信息:")
    
    cursor.execute("DESCRIBE risk_assessment_reports")
    columns = cursor.fetchall()
    
    print("\n风险评估报告表 (risk_assessment_reports):")
    print("-" * 80)
    print(f"{'字段名':<25} {'类型':<20} {'可空':<10} {'键':<10} {'默认值':<15}")
    print("-" * 80)
    
    for column in columns:
        field, type_, null, key, default, extra = column
        print(f"{field:<25} {type_:<20} {null:<10} {key:<10} {str(default):<15}")
    
    # 显示索引信息
    print(f"\n📑 索引信息:")
    cursor.execute("SHOW INDEX FROM risk_assessment_reports")
    indexes = cursor.fetchall()
    
    index_names = set()
    for index in indexes:
        index_names.add(index[2])  # Key_name
    
    for index_name in index_names:
        print(f"  • {index_name}")

def check_prerequisites():
    """检查前置条件"""
    print("🔍 检查前置条件...")
    
    # 检查数据库URL环境变量
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ 缺少数据库配置: DATABASE_URL")
        print("💡 请在.env文件中设置 DATABASE_URL")
        return False
    
    # 尝试解析数据库URL
    try:
        db_config = get_database_config()
        if not all([db_config['host'], db_config['user'], db_config['database']]):
            print("❌ 数据库URL格式无效")
            return False
    except Exception as e:
        print(f"❌ 数据库URL解析失败: {e}")
        return False
    
    print("✅ 配置检查通过")
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 Ariadne 风险评估报告表迁移工具")
    print("=" * 50)
    
    if not check_prerequisites():
        sys.exit(1)
    
    db_config = get_database_config()
    print(f"数据库: {db_config['host']}:{db_config['port']}/{db_config['database']}")
    
    # 确认执行
    confirm = input("\n是否继续执行迁移? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ 迁移已取消")
        sys.exit(0)
    
    # 执行迁移
    create_risk_assessment_tables()

if __name__ == "__main__":
    main()
