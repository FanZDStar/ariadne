#!/usr/bin/env python3
"""
初始化防护训练相关数据库表
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from app.core.database import get_db_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_protection_drill_tables():
    """创建防护训练相关表"""
    
    # 防护训练报告表
    create_reports_table_sql = """
    CREATE TABLE IF NOT EXISTS `protection_drill_reports` (
        `id` int NOT NULL AUTO_INCREMENT,
        `user_id` int NOT NULL COMMENT '用户ID',
        `drill_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '防护训练类型',
        `scenario_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '场景名称',
        `total_questions` int NOT NULL COMMENT '总题数',
        `correct_answers` int NOT NULL COMMENT '正确答案数',
        `score` decimal(5, 2) NOT NULL COMMENT '得分',
        `completion_time` int NULL DEFAULT NULL COMMENT '完成时间(秒)',
        `report_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '详细报告内容(JSON格式)',
        `suggestions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '改进建议',
        `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
        PRIMARY KEY (`id`) USING BTREE,
        INDEX `ix_protection_drill_reports_user_id`(`user_id` ASC) USING BTREE,
        INDEX `ix_protection_drill_reports_id`(`id` ASC) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic COMMENT = '防护训练报告表';
    """
    
    # 防护训练会话表
    create_sessions_table_sql = """
    CREATE TABLE IF NOT EXISTS `protection_drill_sessions` (
        `id` int NOT NULL AUTO_INCREMENT,
        `session_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会话唯一标识',
        `user_id` int NULL DEFAULT NULL COMMENT '用户ID（可选）',
        `drill_type_id` int NOT NULL COMMENT '训练类型ID',
        `start_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
        `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
        `status` enum('active','completed','abandoned') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'active' COMMENT '会话状态',
        `total_questions` int NULL DEFAULT 0 COMMENT '总题数',
        `answered_questions` int NULL DEFAULT 0 COMMENT '已答题数',
        `correct_answers` int NULL DEFAULT 0 COMMENT '正确答案数',
        `session_data` json NULL COMMENT '会话数据(JSON格式)',
        `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
        PRIMARY KEY (`id`) USING BTREE,
        UNIQUE INDEX `ix_protection_drill_sessions_session_id`(`session_id` ASC) USING BTREE,
        INDEX `ix_protection_drill_sessions_user_id`(`user_id` ASC) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic COMMENT = '防护训练会话表';
    """

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 创建报告表
            logger.info("创建防护训练报告表...")
            cursor.execute(create_reports_table_sql)
            logger.info("防护训练报告表创建成功")
            
            # 创建会话表
            logger.info("创建防护训练会话表...")
            cursor.execute(create_sessions_table_sql)
            logger.info("防护训练会话表创建成功")
            
            # 提交事务
            conn.commit()
            logger.info("所有表创建完成")
            
            # 检查表是否存在
            cursor.execute("SHOW TABLES LIKE 'protection_drill%'")
            tables = cursor.fetchall()
            logger.info(f"已创建的防护训练相关表: {tables}")
            
    except Exception as e:
        logger.error(f"创建表时出错: {e}")
        raise

def verify_tables():
    """验证表结构"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 检查reports表结构
            cursor.execute("DESCRIBE protection_drill_reports")
            reports_columns = cursor.fetchall()
            logger.info("protection_drill_reports表结构:")
            for col in reports_columns:
                logger.info(f"  {col}")
            
            # 检查sessions表结构
            cursor.execute("DESCRIBE protection_drill_sessions")
            sessions_columns = cursor.fetchall()
            logger.info("protection_drill_sessions表结构:")
            for col in sessions_columns:
                logger.info(f"  {col}")
                
    except Exception as e:
        logger.error(f"验证表结构时出错: {e}")
        raise

if __name__ == "__main__":
    logger.info("开始初始化防护训练数据库表...")
    create_protection_drill_tables()
    verify_tables()
    logger.info("初始化完成！")
