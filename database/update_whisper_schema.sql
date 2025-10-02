-- ============================================
-- 悄悄话功能数据库更新脚本
-- 更新日期: 2025-10-02
-- 说明: 为悄悄话功能添加标题、心情、标签、图片和匿名信息支持
-- ============================================

-- 1. 为 tree_hole_whispers 表添加新字段
ALTER TABLE `tree_hole_whispers` 
ADD COLUMN `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '悄悄话标题' AFTER `user_id`,
ADD COLUMN `mood` enum('very_happy','happy','neutral','sad','very_sad') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'neutral' COMMENT '心情状态' AFTER `content`,
ADD COLUMN `tags` json NULL COMMENT '标签(JSON格式)' AFTER `mood`,
ADD COLUMN `anonymous_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '匿名名称' AFTER `is_anonymous`,
ADD COLUMN `anonymous_avatar` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '匿名头像路径' AFTER `anonymous_name`;

-- 2. 创建悄悄话图片表
CREATE TABLE `tree_hole_whisper_images`  (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `whisper_id` int NOT NULL,
  `image_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `image_order` int NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`image_id`) USING BTREE,
  INDEX `idx_whisper_images_whisper_id`(`whisper_id` ASC) USING BTREE,
  CONSTRAINT `tree_hole_whisper_images_ibfk_1` FOREIGN KEY (`whisper_id`) REFERENCES `tree_hole_whispers` (`whisper_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- 3. 为现有数据设置默认值
UPDATE `tree_hole_whispers` SET 
  `mood` = 'neutral'
WHERE `mood` IS NULL;

-- 为现有数据生成标题（从内容前20个字符）
UPDATE `tree_hole_whispers` SET 
  `title` = CONCAT(LEFT(REPLACE(REPLACE(`content`, '\n', ''), '\r', ''), 20), IF(LENGTH(REPLACE(REPLACE(`content`, '\n', ''), '\r', '')) > 20, '...', ''))
WHERE `title` IS NULL AND `content` IS NOT NULL;

-- ============================================
-- 后端API更新说明
-- ============================================
-- 
-- 以下是需要在后端更新的主要部分：
-- 
-- 1. 模型更新 (app/models/tree_hole.py):
--    - 添加新字段：title, mood, tags, anonymous_name, anonymous_avatar
--    - 添加图片关系：images
--    - 创建 TreeHoleWhisperImage 模型
--
-- 2. Schema更新 (app/schemas/tree_hole.py):
--    - 更新 WhisperBase, WhisperCreate, WhisperUpdate, WhisperResponse
--    - 添加 MoodEnum, WhisperImageBase, WhisperImageCreate, WhisperImageResponse
--
-- 3. API更新 (app/api/routes/tree_hole.py):
--    - create_whisper: 支持创建图片关联
--    - 所有查询方法: 添加 joinedload(TreeHoleWhisper.images)
--    - 确保返回完整的悄悄话数据结构
--
-- ============================================
-- 更新完成
-- ============================================
