/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80038 (8.0.38)
 Source Host           : localhost:3306
 Source Schema         : ariadne

 Target Server Type    : MySQL
 Target Server Version : 80038 (8.0.38)
 File Encoding         : 65001

 Date: 10/10/2025 23:40:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for achievements
-- ----------------------------
DROP TABLE IF EXISTS `achievements`;
CREATE TABLE `achievements`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '成就名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '成就描述',
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '成就图标',
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '成就分类',
  `unlock_conditions` json NULL COMMENT '解锁条件',
  `reward_points` int NULL DEFAULT NULL COMMENT '奖励积分',
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `sort_order` int NULL DEFAULT NULL COMMENT '排序序号',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_achievements_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for chat_contexts
-- ----------------------------
DROP TABLE IF EXISTS `chat_contexts`;
CREATE TABLE `chat_contexts`  (
  `context_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `icon_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`context_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for chat_messages
-- ----------------------------
DROP TABLE IF EXISTS `chat_messages`;
CREATE TABLE `chat_messages`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL,
  `role` enum('user','assistant') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_chat_messages_session`(`session_id` ASC) USING BTREE,
  INDEX `idx_session_created`(`session_id` ASC, `created_at` ASC) USING BTREE,
  CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `chat_sessions` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 646 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for chat_sessions
-- ----------------------------
DROP TABLE IF EXISTS `chat_sessions`;
CREATE TABLE `chat_sessions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `scene` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `auto_save_enabled` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_chat_sessions_user_scene`(`user_id` ASC, `scene` ASC) USING BTREE,
  INDEX `idx_chat_sessions_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for crisis_keywords
-- ----------------------------
DROP TABLE IF EXISTS `crisis_keywords`;
CREATE TABLE `crisis_keywords`  (
  `keyword_id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `keyword` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `risk_weight` float NULL DEFAULT 1,
  `is_active` tinyint(1) NULL DEFAULT 1,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`keyword_id`) USING BTREE,
  INDEX `idx_category`(`category` ASC) USING BTREE,
  INDEX `idx_keyword`(`keyword` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for crisis_warnings
-- ----------------------------
DROP TABLE IF EXISTS `crisis_warnings`;
CREATE TABLE `crisis_warnings`  (
  `warning_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `warning_type` enum('mood_trend','keyword_alert','ai_analysis','behavior_pattern') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `risk_level` enum('low','medium','high','critical') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` float NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `keywords_detected` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `is_resolved` tinyint(1) NULL DEFAULT 0,
  `resolved_at` datetime NULL DEFAULT NULL,
  `resolver_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`warning_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_risk_level`(`risk_level` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  INDEX `idx_is_resolved`(`is_resolved` ASC) USING BTREE,
  CONSTRAINT `crisis_warnings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for daily_star_limits
-- ----------------------------
DROP TABLE IF EXISTS `daily_star_limits`;
CREATE TABLE `daily_star_limits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `date` date NOT NULL COMMENT '日期',
  `daily_login` tinyint(1) NULL DEFAULT 0 COMMENT '每日登录(1星)',
  `mood_tracking` tinyint(1) NULL DEFAULT 0 COMMENT '晴雨表打卡(1星)',
  `diary_count` tinyint NULL DEFAULT 0 COMMENT '日记篇数(第1篇3星,第2-3篇各1星)',
  `background_change` tinyint(1) NULL DEFAULT 0 COMMENT '背景修改(1星)',
  `emotion_chat_count` tinyint NULL DEFAULT 0 COMMENT '情感对话次数',
  `emotion_chat_points` tinyint NULL DEFAULT 0 COMMENT '情感对话获得积分',
  `skill_training` tinyint(1) NULL DEFAULT 0 COMMENT '技能综合训练(3星)',
  `relationship_assessment` tinyint(1) NULL DEFAULT 0 COMMENT '关系健康评估(2星)',
  `personalized_advice` tinyint(1) NULL DEFAULT 0 COMMENT '个性化建议(2星)',
  `ai_scenario_training` tinyint(1) NULL DEFAULT 0 COMMENT 'AI情景模拟训练(2星)',
  `protection_training` tinyint(1) NULL DEFAULT 0 COMMENT '防护技能训练(1星)',
  `tree_hole_interaction_count` tinyint NULL DEFAULT 0 COMMENT '树洞互动次数',
  `tree_hole_whisper` tinyint(1) NULL DEFAULT 0 COMMENT '发表悄悄话(2星)',
  `skill_favorite` tinyint(1) NULL DEFAULT 0 COMMENT '技能收藏(1星)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_user_date`(`user_id` ASC, `date` ASC) USING BTREE,
  CONSTRAINT `fk_daily_star_limits_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '每日星星积分限制表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for diary_backgrounds
-- ----------------------------
DROP TABLE IF EXISTS `diary_backgrounds`;
CREATE TABLE `diary_backgrounds`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `original_filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_size` int NOT NULL,
  `mime_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_active` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `ix_diary_backgrounds_id`(`id` ASC) USING BTREE,
  CONSTRAINT `diary_backgrounds_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for diary_images
-- ----------------------------
DROP TABLE IF EXISTS `diary_images`;
CREATE TABLE `diary_images`  (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `diary_id` int NOT NULL,
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_order` int NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `idx_diary_images_diary_id`(`diary_id` ASC) USING BTREE,
  CONSTRAINT `diary_images_ibfk_1` FOREIGN KEY (`diary_id`) REFERENCES `emotional_diaries` (`diary_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 45 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for emotional_diaries
-- ----------------------------
DROP TABLE IF EXISTS `emotional_diaries`;
CREATE TABLE `emotional_diaries`  (
  `diary_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mood` enum('very_happy','happy','neutral','sad','very_sad') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_private` tinyint(1) NULL DEFAULT 1,
  `image_count` int NULL DEFAULT 0,
  `tags` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '日记标签',
  PRIMARY KEY (`diary_id`) USING BTREE,
  INDEX `idx_emotional_diaries_user_date`(`user_id` ASC, `created_at` ASC) USING BTREE,
  INDEX `idx_user_mood_date`(`user_id` ASC, `mood` ASC, `created_at` ASC) USING BTREE,
  CONSTRAINT `emotional_diaries_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 845 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for experience_summaries
-- ----------------------------
DROP TABLE IF EXISTS `experience_summaries`;
CREATE TABLE `experience_summaries`  (
  `summary_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `tags` json NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_private` tinyint(1) NULL DEFAULT 1,
  PRIMARY KEY (`summary_id`) USING BTREE,
  INDEX `idx_experience_summaries_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `experience_summaries_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for feedback_images
-- ----------------------------
DROP TABLE IF EXISTS `feedback_images`;
CREATE TABLE `feedback_images`  (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `feedback_id` int NOT NULL,
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `feedback_id`(`feedback_id` ASC) USING BTREE,
  INDEX `ix_feedback_images_image_id`(`image_id` ASC) USING BTREE,
  CONSTRAINT `feedback_images_ibfk_1` FOREIGN KEY (`feedback_id`) REFERENCES `user_feedbacks` (`feedback_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for growth_tracks
-- ----------------------------
DROP TABLE IF EXISTS `growth_tracks`;
CREATE TABLE `growth_tracks`  (
  `track_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `date` date NOT NULL,
  `emotional_index` int NULL DEFAULT NULL,
  `reflection` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`track_id`) USING BTREE,
  UNIQUE INDEX `unique_user_date`(`user_id` ASC, `date` ASC) USING BTREE,
  INDEX `idx_growth_tracks_user_date`(`user_id` ASC, `date` ASC) USING BTREE,
  CONSTRAINT `growth_tracks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `growth_tracks_chk_1` CHECK ((`emotional_index` >= 1) and (`emotional_index` <= 10))
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for interpersonal_practice_sessions
-- ----------------------------
DROP TABLE IF EXISTS `interpersonal_practice_sessions`;
CREATE TABLE `interpersonal_practice_sessions`  (
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
  `quality_score` decimal(3, 2) NULL DEFAULT NULL COMMENT '练习质量评分(0-10)',
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
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人际智慧练习会话表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for journey_categories
-- ----------------------------
DROP TABLE IF EXISTS `journey_categories`;
CREATE TABLE `journey_categories`  (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `icon_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`category_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for journey_favorites
-- ----------------------------
DROP TABLE IF EXISTS `journey_favorites`;
CREATE TABLE `journey_favorites`  (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `favorite_type` enum('diary','summary') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `favorite_id_ref` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`favorite_id`) USING BTREE,
  UNIQUE INDEX `unique_user_favorite`(`user_id` ASC, `favorite_type` ASC, `favorite_id_ref` ASC) USING BTREE,
  CONSTRAINT `journey_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for learning_paths
-- ----------------------------
DROP TABLE IF EXISTS `learning_paths`;
CREATE TABLE `learning_paths`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '学习路径名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '学习路径描述',
  `level` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '适用水平: beginner/intermediate/advanced',
  `estimated_duration` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '预估完成时间',
  `skill_sequence` json NULL COMMENT '技能学习序列',
  `milestones` json NULL COMMENT '里程碑节点',
  `prerequisites` json NULL COMMENT '前置要求',
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `sort_order` int NULL DEFAULT NULL COMMENT '排序序号',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_learning_paths_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for mascot_outfits
-- ----------------------------
DROP TABLE IF EXISTS `mascot_outfits`;
CREATE TABLE `mascot_outfits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '服装名称',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '服装描述',
  `preview_image` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '预览图片路径',
  `mascot_image` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '看板娘完整图片路径',
  `star_cost` int NULL DEFAULT NULL COMMENT '星星消费数量，0表示免费',
  `is_default` tinyint(1) NULL DEFAULT NULL COMMENT '是否为默认服装',
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `sort_order` int NULL DEFAULT NULL COMMENT '排序序号',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_mascot_outfits_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mood_tracker
-- ----------------------------
DROP TABLE IF EXISTS `mood_tracker`;
CREATE TABLE `mood_tracker`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` int NOT NULL COMMENT '用户ID',
  `mood_date` date NOT NULL COMMENT '心情记录日期',
  `mood_level` tinyint NOT NULL COMMENT '心情档位(1-5档)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_user_date`(`user_id` ASC, `mood_date` ASC) USING BTREE COMMENT '用户每天只能记录一次心情',
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_mood_date`(`mood_date` ASC) USING BTREE,
  CONSTRAINT `mood_tracker_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '心情晴雨表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mood_trend_analyses
-- ----------------------------
DROP TABLE IF EXISTS `mood_trend_analyses`;
CREATE TABLE `mood_trend_analyses`  (
  `analysis_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `period_days` int NOT NULL,
  `avg_mood_score` float NOT NULL,
  `mood_trend` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `consecutive_low_days` int NULL DEFAULT 0,
  `risk_indicators` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `recommendations` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`analysis_id`) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `mood_trend_analyses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for protection_drill_answers
-- ----------------------------
DROP TABLE IF EXISTS `protection_drill_answers`;
CREATE TABLE `protection_drill_answers`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会话ID',
  `question_id` int NOT NULL COMMENT '题目ID',
  `selected_option` int NOT NULL COMMENT '选择的选项ID',
  `is_correct` tinyint(1) NOT NULL COMMENT '是否正确',
  `answer_time` int NULL DEFAULT NULL COMMENT '答题用时（秒）',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `question_id`(`question_id` ASC) USING BTREE,
  INDEX `idx_protection_answers_session`(`session_id` ASC) USING BTREE,
  CONSTRAINT `protection_drill_answers_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `protection_drill_questions` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for protection_drill_question_details
-- ----------------------------
DROP TABLE IF EXISTS `protection_drill_question_details`;
CREATE TABLE `protection_drill_question_details`  (
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
  INDEX `idx_question_id`(`question_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 179 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '防护训练答题详情表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for protection_drill_questions
-- ----------------------------
DROP TABLE IF EXISTS `protection_drill_questions`;
CREATE TABLE `protection_drill_questions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `training_type_id` int NOT NULL COMMENT '关联训练类型ID',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '题目标题',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '场景描述',
  `dialogue` json NOT NULL COMMENT '对话内容',
  `question_title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '问题标题',
  `question_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '问题内容',
  `options` json NOT NULL COMMENT '选项列表',
  `correct_analysis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '正确答案分析',
  `risk_explanation` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '风险解释',
  `protection_advice` json NOT NULL COMMENT '防护建议',
  `better_choice` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '更好的选择提示',
  `difficulty` int NULL DEFAULT 1 COMMENT '题目难度 1-简单 2-中等 3-困难',
  `is_active` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_protection_questions_type`(`training_type_id` ASC) USING BTREE,
  CONSTRAINT `protection_drill_questions_ibfk_1` FOREIGN KEY (`training_type_id`) REFERENCES `protection_training_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 55 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for protection_drill_reports
-- ----------------------------
DROP TABLE IF EXISTS `protection_drill_reports`;
CREATE TABLE `protection_drill_reports`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `drill_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '防护训练类型',
  `scenario_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '场景名称',
  `total_questions` int NOT NULL COMMENT '总题数',
  `correct_answers` int NOT NULL COMMENT '正确答案数',
  `score` decimal(5, 2) NOT NULL COMMENT '得分',
  `completion_time` int NULL DEFAULT NULL COMMENT '完成时间(秒)',
  `report_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '详细报告内容(JSON格式)',
  `suggestions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '改进建议',
  `ai_analysis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT 'AI深度分析和建议',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_protection_drill_reports_user_id`(`user_id` ASC) USING BTREE,
  INDEX `ix_protection_drill_reports_id`(`id` ASC) USING BTREE,
  INDEX `idx_user_created`(`user_id` ASC, `created_at` DESC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for protection_drill_sessions
-- ----------------------------
DROP TABLE IF EXISTS `protection_drill_sessions`;
CREATE TABLE `protection_drill_sessions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会话唯一标识',
  `user_id` int NULL DEFAULT NULL COMMENT '用户ID（可选）',
  `training_type_id` int NOT NULL COMMENT '训练类型ID',
  `total_questions` int NOT NULL COMMENT '总题目数',
  `correct_count` int NULL DEFAULT 0 COMMENT '正确答题数',
  `current_question` int NULL DEFAULT 0 COMMENT '当前题目索引',
  `status` enum('active','completed','paused') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'active' COMMENT '会话状态',
  `start_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
  `end_time` timestamp NULL DEFAULT NULL COMMENT '结束时间',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `session_id`(`session_id` ASC) USING BTREE,
  INDEX `training_type_id`(`training_type_id` ASC) USING BTREE,
  INDEX `idx_protection_sessions_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `protection_drill_sessions_ibfk_1` FOREIGN KEY (`training_type_id`) REFERENCES `protection_training_types` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for protection_training_types
-- ----------------------------
DROP TABLE IF EXISTS `protection_training_types`;
CREATE TABLE `protection_training_types`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '训练类型标题',
  `icon` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图标emoji',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '描述',
  `level` int NOT NULL DEFAULT 1 COMMENT '难度等级 1-入门 2-进阶 3-高级',
  `duration` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '预计用时',
  `skills` json NOT NULL COMMENT '训练技能列表',
  `objectives` json NOT NULL COMMENT '训练目标列表',
  `risk_signals` json NOT NULL COMMENT '风险信号列表',
  `strategies` json NOT NULL COMMENT '保护策略列表',
  `is_active` tinyint(1) NULL DEFAULT 1 COMMENT '是否启用',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for relationship_health_reports
-- ----------------------------
DROP TABLE IF EXISTS `relationship_health_reports`;
CREATE TABLE `relationship_health_reports`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `session_token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `relationship_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `relationship_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_score` decimal(5, 2) NOT NULL,
  `total_level` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `dimension_scores` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `questions_answered` int NOT NULL DEFAULT 0,
  `ai_analysis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `recommendations` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'processing',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ai_started_at` datetime NULL DEFAULT NULL,
  `ai_completed_at` datetime NULL DEFAULT NULL,
  `last_viewed_at` datetime NULL DEFAULT NULL,
  `error_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `retry_count` int NOT NULL DEFAULT 0,
  `version` int NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `session_token`(`session_token` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_session_token`(`session_token` ASC) USING BTREE,
  INDEX `idx_relationship_type`(`relationship_type` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE,
  INDEX `idx_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `relationship_health_reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for risk_assessment_reports
-- ----------------------------
DROP TABLE IF EXISTS `risk_assessment_reports`;
CREATE TABLE `risk_assessment_reports`  (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `session_id` int NOT NULL,
  `scene` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `report_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `report_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `overall_risk_level` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `overall_risk_score` float NULL DEFAULT NULL,
  `total_messages` int NULL DEFAULT NULL,
  `risk_messages_count` int NULL DEFAULT NULL,
  `detected_keywords` json NULL,
  `risk_trends` json NULL,
  `ai_analysis` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `recommendations` json NULL,
  `conversation_start_time` datetime NULL DEFAULT NULL,
  `conversation_end_time` datetime NULL DEFAULT NULL,
  `report_generated_time` datetime NULL DEFAULT NULL,
  `last_viewed_time` datetime NULL DEFAULT NULL,
  `status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `is_viewed` tinyint(1) NULL DEFAULT NULL,
  `version` int NULL DEFAULT NULL,
  PRIMARY KEY (`report_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `ix_risk_assessment_reports_report_id`(`report_id` ASC) USING BTREE,
  INDEX `ix_risk_assessment_reports_session_id`(`session_id` ASC) USING BTREE,
  INDEX `idx_risk_reports_session_id`(`session_id` ASC) USING BTREE,
  CONSTRAINT `fk_risk_reports_session` FOREIGN KEY (`session_id`) REFERENCES `chat_sessions` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `risk_assessment_reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for skill_categories
-- ----------------------------
DROP TABLE IF EXISTS `skill_categories`;
CREATE TABLE `skill_categories`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分类名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '分类描述',
  `icon` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '分类图标',
  `sort_order` int NULL DEFAULT NULL COMMENT '排序序号',
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_skill_categories_id`(`id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for skill_favorites
-- ----------------------------
DROP TABLE IF EXISTS `skill_favorites`;
CREATE TABLE `skill_favorites`  (
  `favorite_id` int NOT NULL AUTO_INCREMENT COMMENT '收藏记录ID',
  `user_id` int NOT NULL COMMENT '用户ID',
  `skill_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技能ID（对应JSON文件中的技能ID）',
  `category` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技能分类（communication, emotional_expression, relationship_building, special_scenarios）',
  `skill_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技能名称（冗余存储，便于查询显示）',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
  PRIMARY KEY (`favorite_id`) USING BTREE,
  UNIQUE INDEX `unique_user_skill`(`user_id` ASC, `skill_id` ASC) USING BTREE COMMENT '同一用户不能重复收藏同一技能',
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_skill_id`(`skill_id` ASC) USING BTREE,
  INDEX `idx_category`(`category` ASC) USING BTREE,
  CONSTRAINT `skill_favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 64 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '技能收藏表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for skills
-- ----------------------------
DROP TABLE IF EXISTS `skills`;
CREATE TABLE `skills`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '技能名称',
  `brief` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '技能简介',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '技能详细描述',
  `difficulty` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '难度级别: basic/intermediate/advanced',
  `estimated_time` int NULL DEFAULT NULL COMMENT '预估学习时间(分钟)',
  `learner_count` int NULL DEFAULT NULL COMMENT '学习人数',
  `objectives` json NULL COMMENT '学习目标列表',
  `key_points` json NULL COMMENT '核心要点',
  `practice_steps` json NULL COMMENT '实践步骤',
  `scenarios` json NULL COMMENT '应用场景',
  `tags` json NULL COMMENT '技能标签',
  `category_id` int NOT NULL,
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `sort_order` int NULL DEFAULT NULL COMMENT '排序序号',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `category_id`(`category_id` ASC) USING BTREE,
  INDEX `ix_skills_id`(`id` ASC) USING BTREE,
  CONSTRAINT `skills_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `skill_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for star_point_logs
-- ----------------------------
DROP TABLE IF EXISTS `star_point_logs`;
CREATE TABLE `star_point_logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `action_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '行为类型',
  `points_change` int NOT NULL COMMENT '积分变化(正数为获得，负数为消费)',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '描述信息',
  `source_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '来源ID(如日记ID、会话ID等)',
  `source_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '来源类型',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_star_logs_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_star_logs_action`(`action_type` ASC) USING BTREE,
  INDEX `idx_star_logs_date`(`created_at` ASC) USING BTREE,
  CONSTRAINT `fk_star_point_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 161 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '星星积分变动日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for system_configs
-- ----------------------------
DROP TABLE IF EXISTS `system_configs`;
CREATE TABLE `system_configs`  (
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `config_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`config_key`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for system_logs
-- ----------------------------
DROP TABLE IF EXISTS `system_logs`;
CREATE TABLE `system_logs`  (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `action` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `user_agent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `idx_system_logs_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_system_logs_action`(`action` ASC) USING BTREE,
  CONSTRAINT `system_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tree_hole_chat_participants
-- ----------------------------
DROP TABLE IF EXISTS `tree_hole_chat_participants`;
CREATE TABLE `tree_hole_chat_participants`  (
  `participant_id` int NOT NULL AUTO_INCREMENT,
  `whisper_id` int NOT NULL,
  `user_id` int NOT NULL,
  `anonymous_nickname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `anonymous_avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`participant_id`) USING BTREE,
  UNIQUE INDEX `uk_whisper_user`(`whisper_id` ASC, `user_id` ASC) USING BTREE,
  CONSTRAINT `fk_tree_hole_chat_participants_whisper` FOREIGN KEY (`whisper_id`) REFERENCES `tree_hole_whispers` (`whisper_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tree_hole_chats
-- ----------------------------
DROP TABLE IF EXISTS `tree_hole_chats`;
CREATE TABLE `tree_hole_chats`  (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `whisper_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`chat_id`) USING BTREE,
  INDEX `idx_tree_hole_chats_whisper_id`(`whisper_id` ASC) USING BTREE,
  CONSTRAINT `fk_tree_hole_chats_whisper` FOREIGN KEY (`whisper_id`) REFERENCES `tree_hole_whispers` (`whisper_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tree_hole_comments
-- ----------------------------
DROP TABLE IF EXISTS `tree_hole_comments`;
CREATE TABLE `tree_hole_comments`  (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `whisper_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_anonymous` tinyint(1) NULL DEFAULT 1,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`) USING BTREE,
  INDEX `idx_tree_hole_comments_whisper`(`whisper_id` ASC) USING BTREE,
  INDEX `idx_tree_hole_comments_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_tree_hole_comments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_tree_hole_comments_whisper` FOREIGN KEY (`whisper_id`) REFERENCES `tree_hole_whispers` (`whisper_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tree_hole_likes
-- ----------------------------
DROP TABLE IF EXISTS `tree_hole_likes`;
CREATE TABLE `tree_hole_likes`  (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `whisper_id` int NOT NULL,
  `user_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`like_id`) USING BTREE,
  UNIQUE INDEX `unique_whisper_user_like`(`whisper_id` ASC, `user_id` ASC) USING BTREE,
  INDEX `idx_tree_hole_likes_whisper`(`whisper_id` ASC) USING BTREE,
  INDEX `idx_tree_hole_likes_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_tree_hole_likes_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fk_tree_hole_likes_whisper` FOREIGN KEY (`whisper_id`) REFERENCES `tree_hole_whispers` (`whisper_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 68 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tree_hole_whisper_images
-- ----------------------------
DROP TABLE IF EXISTS `tree_hole_whisper_images`;
CREATE TABLE `tree_hole_whisper_images`  (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `whisper_id` int NOT NULL,
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_order` int NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `idx_whisper_images_whisper_id`(`whisper_id` ASC) USING BTREE,
  CONSTRAINT `tree_hole_whisper_images_ibfk_1` FOREIGN KEY (`whisper_id`) REFERENCES `tree_hole_whispers` (`whisper_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 293 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tree_hole_whispers
-- ----------------------------
DROP TABLE IF EXISTS `tree_hole_whispers`;
CREATE TABLE `tree_hole_whispers`  (
  `whisper_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '悄悄话标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `mood` enum('very_happy','happy','neutral','sad','very_sad') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'neutral' COMMENT '心情状态',
  `tags` json NULL COMMENT '标签(JSON格式)',
  `is_anonymous` tinyint(1) NULL DEFAULT 1,
  `anonymous_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '匿名名称',
  `anonymous_avatar` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '匿名头像路径',
  `like_count` int NULL DEFAULT 0,
  `comment_count` int NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `chatted` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`whisper_id`) USING BTREE,
  INDEX `idx_tree_hole_whispers_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_tree_hole_whispers_created`(`created_at` ASC) USING BTREE,
  INDEX `idx_created_likes`(`created_at` ASC, `like_count` ASC) USING BTREE,
  CONSTRAINT `fk_tree_hole_whispers_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 219 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_achievements
-- ----------------------------
DROP TABLE IF EXISTS `user_achievements`;
CREATE TABLE `user_achievements`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `achievement_id` int NOT NULL,
  `is_unlocked` tinyint(1) NULL DEFAULT NULL COMMENT '是否已解锁',
  `progress_data` json NULL COMMENT '进度数据',
  `unlocked_at` datetime NULL DEFAULT NULL COMMENT '解锁时间',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `achievement_id`(`achievement_id` ASC) USING BTREE,
  INDEX `ix_user_achievements_id`(`id` ASC) USING BTREE,
  CONSTRAINT `user_achievements_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_achievements_ibfk_2` FOREIGN KEY (`achievement_id`) REFERENCES `achievements` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_diary_backgrounds
-- ----------------------------
DROP TABLE IF EXISTS `user_diary_backgrounds`;
CREATE TABLE `user_diary_backgrounds`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `original_filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_path` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `file_size` int NOT NULL,
  `upload_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_user_diary_backgrounds_id`(`id` ASC) USING BTREE,
  INDEX `ix_user_diary_backgrounds_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `user_diary_backgrounds_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_feedbacks
-- ----------------------------
DROP TABLE IF EXISTS `user_feedbacks`;
CREATE TABLE `user_feedbacks`  (
  `feedback_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NULL DEFAULT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `contact_info` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` enum('pending','processing','resolved','closed') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`feedback_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `user_feedbacks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_learning_path_progress
-- ----------------------------
DROP TABLE IF EXISTS `user_learning_path_progress`;
CREATE TABLE `user_learning_path_progress`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `learning_path_id` int NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '状态: not_started/in_progress/completed/paused',
  `progress` float NULL DEFAULT NULL COMMENT '完成进度 0-100',
  `current_step` int NULL DEFAULT NULL COMMENT '当前步骤',
  `completed_skills` json NULL COMMENT '已完成的技能ID列表',
  `milestone_progress` json NULL COMMENT '里程碑完成状态',
  `started_at` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `completed_at` datetime NULL DEFAULT NULL COMMENT '完成时间',
  `last_activity_at` datetime NULL DEFAULT NULL COMMENT '最后活动时间',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `learning_path_id`(`learning_path_id` ASC) USING BTREE,
  INDEX `ix_user_learning_path_progress_id`(`id` ASC) USING BTREE,
  CONSTRAINT `user_learning_path_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_learning_path_progress_ibfk_2` FOREIGN KEY (`learning_path_id`) REFERENCES `learning_paths` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_mascot_outfits
-- ----------------------------
DROP TABLE IF EXISTS `user_mascot_outfits`;
CREATE TABLE `user_mascot_outfits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `outfit_id` int NOT NULL,
  `purchased_at` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '购买时间',
  `is_equipped` tinyint(1) NULL DEFAULT NULL COMMENT '是否装备中',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_user_outfit`(`user_id` ASC, `outfit_id` ASC) USING BTREE,
  INDEX `outfit_id`(`outfit_id` ASC) USING BTREE,
  INDEX `ix_user_mascot_outfits_id`(`id` ASC) USING BTREE,
  CONSTRAINT `user_mascot_outfits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_mascot_outfits_ibfk_2` FOREIGN KEY (`outfit_id`) REFERENCES `mascot_outfits` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_sessions
-- ----------------------------
DROP TABLE IF EXISTS `user_sessions`;
CREATE TABLE `user_sessions`  (
  `session_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `user_id` int NOT NULL,
  `expires_at` timestamp NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `user_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_skill_progress
-- ----------------------------
DROP TABLE IF EXISTS `user_skill_progress`;
CREATE TABLE `user_skill_progress`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '状态: new/learning/mastered',
  `progress` float NULL DEFAULT NULL COMMENT '学习进度 0-100',
  `practice_count` int NULL DEFAULT NULL COMMENT '练习次数',
  `correct_rate` float NULL DEFAULT NULL COMMENT '正确率',
  `total_time_spent` int NULL DEFAULT NULL COMMENT '总学习时间(分钟)',
  `started_at` datetime NULL DEFAULT NULL COMMENT '开始学习时间',
  `last_practiced_at` datetime NULL DEFAULT NULL COMMENT '最后练习时间',
  `mastered_at` datetime NULL DEFAULT NULL COMMENT '掌握时间',
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `skill_id`(`skill_id` ASC) USING BTREE,
  INDEX `ix_user_skill_progress_id`(`id` ASC) USING BTREE,
  CONSTRAINT `user_skill_progress_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_skill_progress_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user_star_points
-- ----------------------------
DROP TABLE IF EXISTS `user_star_points`;
CREATE TABLE `user_star_points`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `current_points` int NOT NULL DEFAULT 10 COMMENT '当前星星积分',
  `total_earned` int NOT NULL DEFAULT 10 COMMENT '总获得积分',
  `total_spent` int NOT NULL DEFAULT 0 COMMENT '总消费积分',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_user_points`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_user_star_points_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '用户星星积分表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT NULL,
  `is_active` tinyint(1) NULL DEFAULT 1,
  `last_risk_assessment` datetime NULL DEFAULT NULL,
  `total_risk_reports` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE,
  INDEX `idx_users_username`(`username` ASC) USING BTREE,
  INDEX `idx_users_email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Triggers structure for table risk_assessment_reports
-- ----------------------------
DROP TRIGGER IF EXISTS `update_user_risk_stats`;
delimiter ;;
CREATE TRIGGER `update_user_risk_stats` AFTER INSERT ON `risk_assessment_reports` FOR EACH ROW BEGIN
                UPDATE users 
                SET 
                    last_risk_assessment = NEW.report_generated_time,
                    total_risk_reports = total_risk_reports + 1
                WHERE user_id = NEW.user_id;
            END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
