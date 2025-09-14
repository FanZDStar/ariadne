-- 创建心情晴雨表数据库表
CREATE TABLE IF NOT EXISTS `mood_tracker` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int NOT NULL COMMENT '用户ID',
  `mood_date` date NOT NULL COMMENT '心情记录日期',
  `mood_level` tinyint NOT NULL COMMENT '心情档位(1-5档)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_date` (`user_id`, `mood_date`) COMMENT '用户每天只能记录一次心情',
  KEY `idx_user_id` (`user_id`),
  KEY `idx_mood_date` (`mood_date`),
  CONSTRAINT `mood_tracker_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='心情晴雨表';

-- 插入一些测试数据（可选）
INSERT INTO `mood_tracker` (`user_id`, `mood_date`, `mood_level`) VALUES
(2, '2025-09-14', 4),
(2, '2025-09-13', 3),
(2, '2025-09-12', 5),
(2, '2025-09-11', 2),
(2, '2025-09-10', 4),
(2, '2025-09-09', 3),
(2, '2025-09-08', 4);
