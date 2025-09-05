#!/usr/bin/env python3
"""
风险评估报告表快速迁移脚本
使用已知数据库配置直接创建表

运行方式：
python scripts/quick_migrate_risk.py
"""

import mysql.connector
from datetime import datetime

def create_risk_assessment_tables():
    """创建风险评估报告相关表"""
    
    # 使用已知的数据库配置
    db_config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'admin123',
        'database': 'ariadne',
        'charset': 'utf8mb4'
    }
    
    connection = None
    cursor = None
    
    try:
        print("🚀 开始创建风险评估报告表...")
        
        # 连接数据库
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        print(f"✅ 已连接到数据库: {db_config['host']}/{db_config['database']}")
        
        # 1. 创建风险评估报告表
        print("📋 创建 risk_assessment_reports 表...")
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
            
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
        cursor.execute(create_risk_assessment_table)
        print("✅ risk_assessment_reports 表创建成功")
        
        # 2. 检查并添加用户表的新字段
        print("🔧 检查用户表字段...")
        
        # 检查现有字段
        cursor.execute("SHOW COLUMNS FROM users LIKE 'last_risk_assessment'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE users ADD COLUMN last_risk_assessment DATETIME NULL")
            print("✅ 添加 last_risk_assessment 字段")
        else:
            print("ℹ️  last_risk_assessment 字段已存在")
        
        cursor.execute("SHOW COLUMNS FROM users LIKE 'total_risk_reports'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE users ADD COLUMN total_risk_reports INT NOT NULL DEFAULT 0")
            print("✅ 添加 total_risk_reports 字段")
        else:
            print("ℹ️  total_risk_reports 字段已存在")
        
        # 3. 创建触发器
        print("⚡ 创建触发器...")
        try:
            cursor.execute("DROP TRIGGER IF EXISTS update_user_risk_stats")
            create_trigger = """
            CREATE TRIGGER update_user_risk_stats
            AFTER INSERT ON risk_assessment_reports
            FOR EACH ROW
            BEGIN
                UPDATE users 
                SET 
                    last_risk_assessment = NEW.report_generated_time,
                    total_risk_reports = total_risk_reports + 1
                WHERE user_id = NEW.user_id;
            END;
            """
            cursor.execute(create_trigger)
            print("✅ 用户风险统计触发器创建成功")
        except mysql.connector.Error as e:
            print(f"⚠️  触发器创建失败: {e}")
        
        # 4. 插入示例数据
        print("📝 插入示例数据...")
        
        # 获取第一个用户ID
        cursor.execute("SELECT user_id FROM users LIMIT 1")
        user_result = cursor.fetchone()
        
        if user_result:
            user_id = user_result[0]
            
            # 检查是否已有示例数据
            cursor.execute("SELECT COUNT(*) FROM risk_assessment_reports WHERE user_id = %s", (user_id,))
            count = cursor.fetchone()[0]
            
            if count == 0:
                sample_reports = [
                    (user_id, 'demo_session_001', 'medium', 65.5, 
                     '用户在对话中表现出一定程度的焦虑情绪，主要集中在学业压力方面。',
                     '根据对话分析，用户目前处于中等风险水平。建议关注情绪变化，必要时寻求专业帮助。',
                     '["焦虑", "压力", "失眠"]', '["保持规律作息", "适度运动", "与朋友交流"]',
                     25, 3, 1),
                    (user_id, 'demo_session_002', 'low', 25.0,
                     '用户情绪状态良好，对话内容积极正面。',
                     '用户展现出良好的心理状态，建议继续保持积极的生活方式。',
                     '["开心", "积极", "希望"]', '["继续保持良好心态", "分享正能量"]',
                     18, 0, 1)
                ]
                
                insert_query = """
                INSERT INTO risk_assessment_reports 
                (user_id, session_id, overall_risk_level, overall_risk_score, summary, ai_analysis, 
                 detected_keywords, recommendations, total_messages, risk_messages_count, version)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                cursor.executemany(insert_query, sample_reports)
                print(f"✅ 插入了 {len(sample_reports)} 条示例数据")
            else:
                print("ℹ️  示例数据已存在，跳过插入")
        else:
            print("⚠️  没有找到用户，跳过示例数据插入")
        
        # 提交所有更改
        connection.commit()
        print("🎉 风险评估报告表迁移完成！")
        
        # 显示表信息
        cursor.execute("SELECT COUNT(*) FROM risk_assessment_reports")
        count = cursor.fetchone()[0]
        print(f"📊 当前报告数量: {count}")
        
    except mysql.connector.Error as e:
        print(f"❌ 数据库错误: {e}")
        if connection:
            connection.rollback()
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        if connection:
            connection.rollback()
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 Ariadne 风险评估报告表快速迁移")
    print("=" * 60)
    
    # 确认执行
    print("数据库: localhost:3306/ariadne")
    confirm = input("\n是否继续执行迁移? (y/n): ")
    if confirm.lower() != 'y':
        print("❌ 迁移已取消")
        return
    
    # 执行迁移
    if create_risk_assessment_tables():
        print("\n🎉 迁移成功完成！")
        print("💡 现在可以测试风险评估功能了")
    else:
        print("\n❌ 迁移失败")

if __name__ == "__main__":
    main()
