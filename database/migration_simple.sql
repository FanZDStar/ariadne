-- 简化版数据库迁移脚本
-- 如果执行出错，说明列已存在，可以忽略错误继续执行下一条

-- 步骤1: 重命名旧列（如果表中有 rewards_earned 列）
-- 如果出现错误 "Unknown column 'rewards_earned'"，说明已经是新版本，跳过
ALTER TABLE daily_comment_rewards 
    CHANGE COLUMN rewards_earned comment_rewards_earned INT NOT NULL DEFAULT 0 COMMENT '当日评论获得的水滴奖励';

-- 步骤2: 添加发布次数列
-- 如果出现错误 "Duplicate column name"，说明列已存在，跳过
ALTER TABLE daily_comment_rewards 
    ADD COLUMN whisper_count INT NOT NULL DEFAULT 0 COMMENT '当日发布悄悄话次数' AFTER comment_rewards_earned;

-- 步骤3: 添加发布奖励列
-- 如果出现错误 "Duplicate column name"，说明列已存在，跳过
ALTER TABLE daily_comment_rewards 
    ADD COLUMN whisper_rewards_earned INT NOT NULL DEFAULT 0 COMMENT '当日发布悄悄话获得的水滴奖励' AFTER whisper_count;

-- 步骤4: 更新表注释
ALTER TABLE daily_comment_rewards COMMENT='每日互动奖励记录表（评论+发布悄悄话）';

-- 步骤5: 查看最终结构
DESCRIBE daily_comment_rewards;
