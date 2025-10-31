-- 水滴系统数据库表
-- 用户水滴表
CREATE TABLE IF NOT EXISTS user_water_drops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    water_drops INT NOT NULL DEFAULT 0 COMMENT '用户当前拥有的水滴数量',
    total_earned INT NOT NULL DEFAULT 0 COMMENT '累计获得的水滴总数',
    total_used INT NOT NULL DEFAULT 0 COMMENT '累计使用的水滴总数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户水滴表';

-- 水滴领取记录表（使用现有的 user_watering_cooldown 表来记录领取时间）
-- user_watering_cooldown 表已存在，用于记录每小时领取水滴的冷却时间
-- 字段说明：
-- user_id: 用户ID
-- last_watering_time: 上次领取水滴的时间
-- created_at: 创建时间
-- updated_at: 更新时间
