-- 数据库迁移：为 daily_comment_rewards 表添加发布悄悄话奖励字段
-- 执行日期：2025-10-31

-- 检查并重命名旧列（如果存在 rewards_earned 列）
SET @col_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'daily_comment_rewards' 
      AND COLUMN_NAME = 'rewards_earned'
);

SET @sql = IF(@col_exists > 0,
    'ALTER TABLE daily_comment_rewards CHANGE COLUMN rewards_earned comment_rewards_earned INT NOT NULL DEFAULT 0 COMMENT ''当日评论获得的水滴奖励''',
    'SELECT "Column rewards_earned does not exist, skipping rename" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 whisper_count 列（如果不存在）
SET @col_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'daily_comment_rewards' 
      AND COLUMN_NAME = 'whisper_count'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE daily_comment_rewards ADD COLUMN whisper_count INT NOT NULL DEFAULT 0 COMMENT ''当日发布悄悄话次数'' AFTER comment_rewards_earned',
    'SELECT "Column whisper_count already exists, skipping" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 添加 whisper_rewards_earned 列（如果不存在）
SET @col_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'daily_comment_rewards' 
      AND COLUMN_NAME = 'whisper_rewards_earned'
);

SET @sql = IF(@col_exists = 0,
    'ALTER TABLE daily_comment_rewards ADD COLUMN whisper_rewards_earned INT NOT NULL DEFAULT 0 COMMENT ''当日发布悄悄话获得的水滴奖励'' AFTER whisper_count',
    'SELECT "Column whisper_rewards_earned already exists, skipping" AS message'
);

PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 更新表注释
ALTER TABLE daily_comment_rewards COMMENT='每日互动奖励记录表（评论+发布悄悄话）';

-- 更新 comment_date 列的注释
ALTER TABLE daily_comment_rewards 
    MODIFY COLUMN comment_date DATE NOT NULL COMMENT '日期';

-- 验证修改
SELECT 
    COLUMN_NAME, 
    COLUMN_TYPE, 
    COLUMN_COMMENT,
    COLUMN_DEFAULT,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = DATABASE() 
  AND TABLE_NAME = 'daily_comment_rewards'
ORDER BY ORDINAL_POSITION;
