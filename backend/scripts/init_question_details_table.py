#!/usr/bin/env python3
"""
创建防护训练答题详情表和AI分析功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_question_details_table():
    """创建答题详情表和相关功能"""
    
    # 防护训练答题详情表
    create_details_table_sql = """
    CREATE TABLE IF NOT EXISTS `protection_drill_question_details` (
        `id` int NOT NULL AUTO_INCREMENT,
        `report_id` int NOT NULL COMMENT '关联的训练报告ID',
        `question_id` int NULL DEFAULT NULL COMMENT '题目ID',
        `question_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '题目标题',
        `question_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '题目内容',
        `selected_option_id` int NULL DEFAULT NULL COMMENT '用户选择的选项ID',
        `selected_option_text` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户选择的选项文本',
        `correct_option_id` int NULL DEFAULT NULL COMMENT '正确答案选项ID',
        `correct_option_text` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '正确答案选项文本',
        `is_correct` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否回答正确',
        `score_gained` int NOT NULL DEFAULT 0 COMMENT '本题获得分数',
        `explanation` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '答案解释',
        `risk_explanation` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '风险解释',
        `ai_feedback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT 'AI个性化反馈建议',
        `options_data` json NULL COMMENT '所有选项数据(JSON格式)',
        `question_order` int NOT NULL DEFAULT 0 COMMENT '题目顺序',
        `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
        PRIMARY KEY (`id`) USING BTREE,
        INDEX `idx_report_id`(`report_id` ASC) USING BTREE,
        INDEX `idx_question_id`(`question_id` ASC) USING BTREE
    ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic COMMENT = '防护训练答题详情表';
    """
    
    # 添加AI分析字段
    add_ai_analysis_sql = """
    ALTER TABLE `protection_drill_reports` 
    ADD COLUMN `ai_analysis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT 'AI深度分析和建议' AFTER `suggestions`;
    """
    
    # 添加索引
    add_index_sql = """
    CREATE INDEX `idx_user_created` ON `protection_drill_reports`(`user_id`, `created_at` DESC) USING BTREE;
    """

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 创建答题详情表
            logger.info("创建防护训练答题详情表...")
            cursor.execute(create_details_table_sql)
            logger.info("答题详情表创建成功")
            
            # 添加AI分析字段
            logger.info("添加AI分析字段...")
            try:
                cursor.execute(add_ai_analysis_sql)
                logger.info("AI分析字段添加成功")
            except Exception as e:
                if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                    logger.info("AI分析字段已存在，跳过")
                else:
                    raise e
            
            # 添加索引
            logger.info("添加查询索引...")
            try:
                cursor.execute(add_index_sql)
                logger.info("索引添加成功")
            except Exception as e:
                if "Duplicate key name" in str(e) or "already exists" in str(e).lower():
                    logger.info("索引已存在，跳过")
                else:
                    raise e
            
            # 提交事务
            conn.commit()
            logger.info("所有修改完成")
            
            # 检查表结构
            cursor.execute("SHOW TABLES LIKE 'protection_drill%'")
            tables = cursor.fetchall()
            logger.info(f"现有的防护训练相关表: {[table[0] for table in tables]}")
            
    except Exception as e:
        logger.error(f"创建表时出错: {e}")
        raise

if __name__ == "__main__":
    logger.info("开始创建防护训练答题详情表...")
    create_question_details_table()
    logger.info("创建完成！")
