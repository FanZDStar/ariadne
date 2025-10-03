-- ----------------------------
-- Table structure for protection_drill_reports
-- ----------------------------
DROP TABLE IF EXISTS `protection_drill_reports`;
CREATE TABLE `protection_drill_reports` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `drill_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '防护训练类型',
  `scenario_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '场景名称',
  `total_questions` int NOT NULL DEFAULT 0 COMMENT '总题数',
  `correct_answers` int NOT NULL DEFAULT 0 COMMENT '正确答案数',
  `score` decimal(5,2) NOT NULL DEFAULT 0.00 COMMENT '得分',
  `completion_time` int NULL COMMENT '完成时间(秒)',
  `report_content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '详细报告内容(JSON格式)',
  `suggestions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '改进建议',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_drill_type`(`drill_type` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '防护训练报告表' ROW_FORMAT = DYNAMIC;
