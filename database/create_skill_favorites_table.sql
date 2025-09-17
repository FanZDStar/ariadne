-- 创建技能收藏表
DROP TABLE IF EXISTS `skill_favorites`;
CREATE TABLE `skill_favorites` (
  `favorite_id` int NOT NULL AUTO_INCREMENT COMMENT '收藏记录ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `skill_id` varchar(50) NOT NULL COMMENT '技能ID（对应JSON文件中的技能ID）',
  `category` varchar(50) NOT NULL COMMENT '技能分类（communication, emotional_expression, relationship_building, special_scenarios）',
  `skill_name` varchar(255) NOT NULL COMMENT '技能名称（冗余存储，便于查询显示）',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`favorite_id`) USING BTREE,
  UNIQUE KEY `unique_user_skill` (`user_id`, `skill_id`) USING BTREE COMMENT '同一用户不能重复收藏同一技能',
  KEY `idx_user_id` (`user_id`) USING BTREE,
  KEY `idx_skill_id` (`skill_id`) USING BTREE,
  KEY `idx_category` (`category`) USING BTREE,
  CONSTRAINT `skill_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '技能收藏表' ROW_FORMAT = Dynamic;
