-- ================================================================
-- 阿里阿德涅数据库性能优化脚本
-- 执行前请务必备份数据库！
-- ================================================================

-- 备份建议：mysqldump -u root -p ariadne > ariadne_backup_$(date +%Y%m%d_%H%M%S).sql

-- ================================================================
-- 第一阶段：安全的索引优化（可以直接执行，不影响现有数据）
-- ================================================================

-- 1. 添加复合索引优化查询
-- 1. 添加复合索引优化查询（安全操作）
-- 检查是否已存在索引，避免重复创建
SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE table_schema = 'ariadne' 
     AND table_name = 'emotional_diaries' 
     AND index_name = 'idx_user_mood_date') > 0,
    'SELECT "索引 idx_user_mood_date 已存在"',
    'ALTER TABLE emotional_diaries ADD INDEX idx_user_mood_date (user_id, mood, created_at)'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE table_schema = 'ariadne' 
     AND table_name = 'chat_messages' 
     AND index_name = 'idx_session_created') > 0,
    'SELECT "索引 idx_session_created 已存在"',
    'ALTER TABLE chat_messages ADD INDEX idx_session_created (session_id, created_at)'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @sql = (SELECT IF(
    (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
     WHERE table_schema = 'ariadne' 
     AND table_name = 'tree_hole_whispers' 
     AND index_name = 'idx_created_likes') > 0,
    'SELECT "索引 idx_created_likes 已存在"',
    'ALTER TABLE tree_hole_whispers ADD INDEX idx_created_likes (created_at, like_count)'
));
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ================================================================
-- 第二阶段：全文搜索索引（可选，根据需要执行）
-- ================================================================

-- 2. 添加全文搜索索引（用于内容搜索）
-- 注意：这会影响写入性能，请根据实际需求决定是否执行
/*
ALTER TABLE emotional_diaries ADD FULLTEXT(title, content);
ALTER TABLE tree_hole_whispers ADD FULLTEXT(content);
*/

-- ================================================================
-- 第三阶段：数据分区（高级操作，需要谨慎执行）
-- ================================================================

-- 3. 优化大数据表的分区（按时间分区）
-- 警告：这是高风险操作，执行前必须备份数据库！
-- 建议在测试环境先验证
/*
-- 对emotional_diaries表按月分区
ALTER TABLE emotional_diaries 
PARTITION BY RANGE (YEAR(created_at) * 100 + MONTH(created_at)) (
    PARTITION p202408 VALUES LESS THAN (202409),
    PARTITION p202409 VALUES LESS THAN (202410),
    PARTITION p202410 VALUES LESS THAN (202411),
    PARTITION p202411 VALUES LESS THAN (202412),
    PARTITION p202412 VALUES LESS THAN (202501),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
*/

-- ================================================================
-- 第四阶段：数据归档和清理（定期维护）
-- ================================================================

-- 4. 数据归档策略（删除一年以前的数据）
-- 注意：这会永久删除数据，请谨慎执行
/*
CREATE EVENT IF NOT EXISTS archive_old_data
ON SCHEDULE EVERY 1 MONTH
DO
BEGIN
    -- 归档一年前的聊天记录
    DELETE FROM chat_messages 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR);
    
    -- 归档一年前的匿名树洞记录
    DELETE FROM tree_hole_whispers 
    WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR) AND is_anonymous = 1;
END;
*/

-- ================================================================
-- 第五阶段：表结构优化（结构性改动）
-- ================================================================

-- 5. 优化表结构
-- 将大文本字段单独存储（可选优化）
/*
CREATE TABLE diary_content_archive (
    diary_id INT PRIMARY KEY,
    content LONGTEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (diary_id) REFERENCES emotional_diaries(diary_id) ON DELETE CASCADE
);
*/

-- ================================================================
-- 性能监控查询（用于评估优化效果）
-- ================================================================

-- 查看表大小和行数
SELECT 
    table_name as '表名',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) as '大小(MB)',
    table_rows as '行数'
FROM information_schema.tables 
WHERE table_schema = 'ariadne' 
ORDER BY (data_length + index_length) DESC;

-- 查看索引使用情况
SELECT 
    table_name as '表名',
    index_name as '索引名',
    column_name as '列名',
    cardinality as '基数'
FROM information_schema.statistics 
WHERE table_schema = 'ariadne' 
ORDER BY table_name, index_name;
