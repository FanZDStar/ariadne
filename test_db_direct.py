#!/usr/bin/env python3
"""
直接测试数据库连接和防护训练数据
"""
import mysql.connector
import json
import os
from urllib.parse import urlparse

# 从环境变量获取数据库连接信息
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:123456@localhost:3306/ariadne")

def test_database_connection():
    """测试数据库连接和查询防护训练数据"""
    try:
        # 处理SQLAlchemy格式的数据库URL
        db_url = DATABASE_URL
        if 'mysql+pymysql://' in db_url:
            db_url = db_url.replace('mysql+pymysql://', 'mysql://')
            
        # 解析数据库URL
        parsed = urlparse(db_url)
        
        connection = mysql.connector.connect(
            host=parsed.hostname or 'localhost',
            port=parsed.port or 3306,
            user=parsed.username or 'root',
            password=parsed.password or 'password',
            database=parsed.path.lstrip('/') or 'ariadne'
        )
        
        print("✓ 数据库连接成功")
        
        cursor = connection.cursor(dictionary=True)
        
        # 测试查询防护训练类型
        query = "SELECT * FROM protection_training_types"
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"✓ 查询到 {len(results)} 条防护训练类型记录")
        
        # 处理第一条记录，测试JSON解析
        if results:
            first_record = results[0]
            print(f"第一条记录ID: {first_record['id']}")
            print(f"标题: {first_record['title']}")
            
            # 测试JSON字段解析
            try:
                skills = json.loads(first_record['skills'])
                objectives = json.loads(first_record['objectives'])
                risk_signals = json.loads(first_record['risk_signals'])
                strategies = json.loads(first_record['strategies'])
                
                print("✓ JSON字段解析成功")
                print(f"技能数量: {len(skills)}")
                print(f"目标数量: {len(objectives)}")
                print(f"风险信号数量: {len(risk_signals)}")
                print(f"策略数量: {len(strategies)}")
                
                # 构造返回格式
                formatted_record = {
                    "id": first_record['id'],
                    "title": first_record['title'],
                    "icon": first_record['icon'],
                    "description": first_record['description'],
                    "level": first_record['level'],
                    "duration": first_record['duration'],
                    "skills": skills,
                    "objectives": objectives,
                    "risk_signals": risk_signals,
                    "strategies": strategies
                }
                
                print("✓ 数据格式化成功")
                print("格式化后的记录:")
                print(json.dumps(formatted_record, ensure_ascii=False, indent=2))
                
            except json.JSONDecodeError as e:
                print(f"✗ JSON解析失败: {e}")
                print(f"skills字段内容: {first_record['skills']}")
        
        cursor.close()
        connection.close()
        print("✓ 数据库连接已关闭")
        
    except Exception as e:
        print(f"✗ 数据库测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database_connection()
