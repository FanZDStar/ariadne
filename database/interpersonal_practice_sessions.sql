-- 创建人际智慧练习会话表
CREATE TABLE `interpersonal_practice_sessions` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '练习会话ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `scenario_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '练习场景ID',
  `scenario_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '练习场景名称',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '对话标题',
  `messages` json NOT NULL COMMENT '完整对话记录(JSON格式)',
  `practice_type` enum('communication','emotional_expression','relationship_building','special_scenarios') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'communication' COMMENT '练习类型',
  `difficulty_level` enum('beginner','intermediate','advanced') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'beginner' COMMENT '难度等级',
  `session_duration` int NULL DEFAULT NULL COMMENT '会话时长(秒)',
  `message_count` int NOT NULL DEFAULT 0 COMMENT '消息总数',
  `quality_score` decimal(3,2) NULL DEFAULT NULL COMMENT '练习质量评分(0-10)',
  `ai_feedback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'AI反馈内容',
  `improvement_suggestions` json NULL COMMENT '改进建议(JSON格式)',
  `skills_practiced` json NULL COMMENT '练习的技能点(JSON格式)',
  `is_completed` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否完成练习',
  `is_favorite` tinyint(1) NOT NULL DEFAULT 0 COMMENT '是否收藏',
  `tags` json NULL COMMENT '标签(JSON格式)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `completed_at` timestamp NULL DEFAULT NULL COMMENT '完成时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_interpersonal_practice_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_interpersonal_practice_scenario`(`scenario_id` ASC) USING BTREE,
  INDEX `idx_interpersonal_practice_type`(`practice_type` ASC) USING BTREE,
  INDEX `idx_interpersonal_practice_created`(`created_at` ASC) USING BTREE,
  INDEX `idx_interpersonal_practice_user_created`(`user_id` ASC, `created_at` DESC) USING BTREE,
  CONSTRAINT `interpersonal_practice_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人际智慧练习会话表' ROW_FORMAT = DYNAMIC;

-- 示例数据
INSERT INTO `interpersonal_practice_sessions` VALUES 
(1, 1, 'workplace_communication', '职场沟通', '与同事讨论项目进度', 
'[
  {"role": "assistant", "content": "你好！我是你的练习伙伴。今天我们来练习职场沟通场景。假设我是你的同事小王，我们需要讨论一个项目的进度。你可以开始对话了。", "timestamp": "2024-10-01T10:00:00"},
  {"role": "user", "content": "小王你好，我想和你聊聊我们项目的进度情况。", "timestamp": "2024-10-01T10:01:00"},
  {"role": "assistant", "content": "好的，我也正想和你聊这个呢。目前我这边的任务进展得还算顺利，你那边情况怎么样？", "timestamp": "2024-10-01T10:01:30"}
]', 
'communication', 'intermediate', 300, 3, 8.5, 
'你在这次练习中表现很好，能够主动发起对话并保持礼貌的语调。建议在表达具体问题时可以更加详细一些。', 
'["主动沟通", "礼貌表达", "项目协调"]', 
'["主动倾听", "清晰表达", "团队协作"]', 
1, 0, '["职场", "沟通", "团队合作"]', 
'2024-10-01 10:00:00', '2024-10-01 10:05:00', '2024-10-01 10:05:00');
