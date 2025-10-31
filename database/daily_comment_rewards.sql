-- 每日互动奖励记录表（评论+发布悄悄话）
CREATE TABLE IF NOT EXISTS daily_comment_rewards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    comment_date DATE NOT NULL COMMENT '日期',
    comment_count INT NOT NULL DEFAULT 0 COMMENT '当日评论次数',
    comment_rewards_earned INT NOT NULL DEFAULT 0 COMMENT '当日评论获得的水滴奖励',
    whisper_count INT NOT NULL DEFAULT 0 COMMENT '当日发布悄悄话次数',
    whisper_rewards_earned INT NOT NULL DEFAULT 0 COMMENT '当日发布悄悄话获得的水滴奖励',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_date (user_id, comment_date),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, comment_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日互动奖励记录表';
