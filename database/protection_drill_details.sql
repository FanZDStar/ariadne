-- 创建防护训练答题详情表
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
    INDEX `idx_question_id`(`question_id` ASC) USING BTREE,
    CONSTRAINT `fk_question_details_report` FOREIGN KEY (`report_id`) REFERENCES `protection_drill_reports` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic COMMENT = '防护训练答题详情表';

-- 为现有的防护训练报告表添加AI建议字段
ALTER TABLE `protection_drill_reports` 
ADD COLUMN `ai_analysis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT 'AI深度分析和建议' AFTER `suggestions`;

-- 添加索引优化查询性能
ALTER TABLE `protection_drill_reports` 
ADD INDEX `idx_user_created`(`user_id`, `created_at` DESC) USING BTREE;
