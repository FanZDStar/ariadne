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

 Date: 17/08/2025 16:28:30
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_contexts
-- ----------------------------
INSERT INTO `chat_contexts` VALUES (1, '自己与自己的对话', '反思感情中的言行举止，获得AI引导和建议', '/static/self-dialog-icon.png', '2025-08-14 16:25:31');
INSERT INTO `chat_contexts` VALUES (2, '恋爱小尝试', '帮助胆小没有经验的人迈出第一步', '/static/experience-icon.png', '2025-08-14 16:25:31');
INSERT INTO `chat_contexts` VALUES (3, '爱他人先爱自己', '探讨如何在爱他人之前先学会爱自己', '/static/love-icon.png', '2025-08-14 16:25:31');

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
  CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `chat_sessions` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_messages
-- ----------------------------

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
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_chat_sessions_user_scene`(`user_id` ASC, `scene` ASC) USING BTREE,
  INDEX `idx_chat_sessions_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of chat_sessions
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of diary_images
-- ----------------------------
INSERT INTO `diary_images` VALUES (14, 6, '/uploads/1166c4f0-dd84-430a-bc4d-fecafa1948a1.png', 0, '2025-08-15 21:16:15');
INSERT INTO `diary_images` VALUES (15, 6, '/uploads/170a2137-b246-405f-a7d4-5c2e851315d8.png', 1, '2025-08-15 21:16:15');
INSERT INTO `diary_images` VALUES (16, 6, '/uploads/c04a82b7-3362-415f-9dc3-15ddf684566a.png', 2, '2025-08-15 21:16:15');
INSERT INTO `diary_images` VALUES (17, 6, '/uploads/31d21a99-702e-4a29-b23a-db5d268dc28f.png', 3, '2025-08-15 21:16:15');
INSERT INTO `diary_images` VALUES (18, 6, '/uploads/76c4bccb-cf14-4221-a165-6fb144b66f02.png', 4, '2025-08-15 21:16:15');
INSERT INTO `diary_images` VALUES (19, 6, '/uploads/096e9208-bd4a-4545-a0d9-38fa0d08921d.png', 5, '2025-08-15 21:16:15');
INSERT INTO `diary_images` VALUES (20, 7, '/uploads/768bd7c4-5b87-4ed4-89f9-258c63843a2b.jpg', 0, '2025-08-15 22:16:06');
INSERT INTO `diary_images` VALUES (21, 7, '/uploads/e3efa9ab-6f81-4a4c-8e30-366ce21d14a7.jpg', 1, '2025-08-15 22:16:06');
INSERT INTO `diary_images` VALUES (22, 8, '/uploads/6bef56b8-727d-45b3-be8c-719f93bb4ba5.webp', 0, '2025-08-16 00:38:52');

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
  PRIMARY KEY (`diary_id`) USING BTREE,
  INDEX `idx_emotional_diaries_user_date`(`user_id` ASC, `created_at` ASC) USING BTREE,
  CONSTRAINT `emotional_diaries_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 749 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of emotional_diaries
-- ----------------------------
INSERT INTO `emotional_diaries` VALUES (6, 6, '你好 两位', '你好 两位', 'neutral', '2025-08-15 21:16:15', '2025-08-15 21:16:15', 1, 6);
INSERT INTO `emotional_diaries` VALUES (7, 6, '啦啦啦啦', '啦啦啦啦', 'neutral', '2025-08-15 22:16:06', '2025-08-15 22:16:06', 1, 2);
INSERT INTO `emotional_diaries` VALUES (8, 6, '今天的我是佩奇哦', '今天的我是佩奇哦', 'very_happy', '2025-08-16 00:38:52', '2025-08-16 00:38:52', 1, 1);
INSERT INTO `emotional_diaries` VALUES (9, 6, '11111', '11111', 'neutral', '2025-08-16 00:46:21', '2025-08-16 00:46:21', 1, 0);
INSERT INTO `emotional_diaries` VALUES (10, 1, '测试日记1', '今天很开心', 'very_happy', '2025-08-14 10:30:00', '2025-08-16 14:59:03', 1, 0);
INSERT INTO `emotional_diaries` VALUES (11, 1, '测试日记2', '今天一般般', 'neutral', '2025-08-14 15:45:00', '2025-08-16 14:59:03', 1, 0);
INSERT INTO `emotional_diaries` VALUES (12, 1, '测试日记3', '今天有点难过', 'sad', '2025-08-13 09:20:00', '2025-08-16 14:59:03', 1, 0);
INSERT INTO `emotional_diaries` VALUES (13, 6, '测试日记1', '今天很开心', 'very_happy', '2025-08-14 10:30:00', '2025-08-16 15:10:16', 1, 0);
INSERT INTO `emotional_diaries` VALUES (14, 6, '测试日记2', '今天一般般', 'neutral', '2025-08-14 15:45:00', '2025-08-16 15:10:16', 1, 0);
INSERT INTO `emotional_diaries` VALUES (15, 6, '测试日记3', '今天有点难过', 'sad', '2025-08-13 09:20:00', '2025-08-16 15:10:16', 1, 0);
INSERT INTO `emotional_diaries` VALUES (16, 6, '测试日记5', '今天很开心', 'very_happy', '2025-08-12 10:30:00', '2025-08-16 15:11:10', 1, 0);
INSERT INTO `emotional_diaries` VALUES (17, 6, '测试日记6', '今天一般般', 'neutral', '2025-08-11 15:45:00', '2025-08-16 15:11:10', 1, 0);
INSERT INTO `emotional_diaries` VALUES (18, 6, '测试日记7', '今天有点难过', 'sad', '2025-08-10 09:20:00', '2025-08-16 15:11:10', 1, 0);
INSERT INTO `emotional_diaries` VALUES (19, 1, '测试日记1', '今天的心情是 neutral', 'neutral', '2025-08-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (20, 1, '测试日记2', '今天的心情是 very sad', 'very_sad', '2025-08-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (21, 1, '测试日记3', '今天的心情是 very happy', 'very_happy', '2025-08-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (22, 1, '测试日记4', '今天的心情是 happy', 'happy', '2025-08-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (23, 1, '测试日记5', '今天的心情是 happy', 'happy', '2025-08-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (24, 1, '测试日记6', '今天的心情是 sad', 'sad', '2025-08-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (25, 1, '测试日记7', '今天的心情是 sad', 'sad', '2025-08-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (26, 1, '测试日记8', '今天的心情是 very happy', 'very_happy', '2025-08-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (27, 1, '测试日记9', '今天的心情是 very happy', 'very_happy', '2025-08-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (28, 1, '测试日记10', '今天的心情是 happy', 'happy', '2025-08-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (29, 1, '测试日记11', '今天的心情是 neutral', 'neutral', '2025-08-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (30, 1, '测试日记12', '今天的心情是 happy', 'happy', '2025-08-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (31, 1, '测试日记13', '今天的心情是 very happy', 'very_happy', '2025-08-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (32, 1, '测试日记14', '今天的心情是 happy', 'happy', '2025-08-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (33, 1, '测试日记15', '今天的心情是 very sad', 'very_sad', '2025-08-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (34, 1, '测试日记16', '今天的心情是 neutral', 'neutral', '2025-08-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (35, 1, '测试日记17', '今天的心情是 very sad', 'very_sad', '2025-07-31 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (36, 1, '测试日记18', '今天的心情是 very happy', 'very_happy', '2025-07-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (37, 1, '测试日记19', '今天的心情是 very sad', 'very_sad', '2025-07-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (38, 1, '测试日记20', '今天的心情是 sad', 'sad', '2025-07-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (39, 1, '测试日记21', '今天的心情是 happy', 'happy', '2025-07-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (40, 1, '测试日记22', '今天的心情是 sad', 'sad', '2025-07-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (41, 1, '测试日记23', '今天的心情是 neutral', 'neutral', '2025-07-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (42, 1, '测试日记24', '今天的心情是 very sad', 'very_sad', '2025-07-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (43, 1, '测试日记25', '今天的心情是 very sad', 'very_sad', '2025-07-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (44, 1, '测试日记26', '今天的心情是 very happy', 'very_happy', '2025-07-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (45, 1, '测试日记27', '今天的心情是 neutral', 'neutral', '2025-07-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (46, 1, '测试日记28', '今天的心情是 very happy', 'very_happy', '2025-07-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (47, 1, '测试日记29', '今天的心情是 neutral', 'neutral', '2025-07-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (48, 1, '测试日记30', '今天的心情是 very sad', 'very_sad', '2025-07-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (49, 1, '测试日记31', '今天的心情是 very sad', 'very_sad', '2025-07-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (50, 1, '测试日记32', '今天的心情是 neutral', 'neutral', '2025-07-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (51, 1, '测试日记33', '今天的心情是 happy', 'happy', '2025-07-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (52, 1, '测试日记34', '今天的心情是 very happy', 'very_happy', '2025-07-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (53, 1, '测试日记35', '今天的心情是 sad', 'sad', '2025-07-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (54, 1, '测试日记36', '今天的心情是 happy', 'happy', '2025-07-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (55, 1, '测试日记37', '今天的心情是 very sad', 'very_sad', '2025-07-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (56, 1, '测试日记38', '今天的心情是 very sad', 'very_sad', '2025-07-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (57, 1, '测试日记39', '今天的心情是 very happy', 'very_happy', '2025-07-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (58, 1, '测试日记40', '今天的心情是 happy', 'happy', '2025-07-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (59, 1, '测试日记41', '今天的心情是 very happy', 'very_happy', '2025-07-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (60, 1, '测试日记42', '今天的心情是 sad', 'sad', '2025-07-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (61, 1, '测试日记43', '今天的心情是 happy', 'happy', '2025-07-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (62, 1, '测试日记44', '今天的心情是 happy', 'happy', '2025-07-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (63, 1, '测试日记45', '今天的心情是 very sad', 'very_sad', '2025-07-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (64, 1, '测试日记46', '今天的心情是 very happy', 'very_happy', '2025-07-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (65, 1, '测试日记47', '今天的心情是 very sad', 'very_sad', '2025-07-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (66, 1, '测试日记48', '今天的心情是 happy', 'happy', '2025-06-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (67, 1, '测试日记49', '今天的心情是 sad', 'sad', '2025-06-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (68, 1, '测试日记50', '今天的心情是 neutral', 'neutral', '2025-06-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (69, 1, '测试日记51', '今天的心情是 neutral', 'neutral', '2025-06-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (70, 1, '测试日记52', '今天的心情是 sad', 'sad', '2025-06-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (71, 1, '测试日记53', '今天的心情是 sad', 'sad', '2025-06-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (72, 1, '测试日记54', '今天的心情是 happy', 'happy', '2025-06-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (73, 1, '测试日记55', '今天的心情是 happy', 'happy', '2025-06-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (74, 1, '测试日记56', '今天的心情是 happy', 'happy', '2025-06-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (75, 1, '测试日记57', '今天的心情是 sad', 'sad', '2025-06-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (76, 1, '测试日记58', '今天的心情是 neutral', 'neutral', '2025-06-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (77, 1, '测试日记59', '今天的心情是 very happy', 'very_happy', '2025-06-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (78, 1, '测试日记60', '今天的心情是 very sad', 'very_sad', '2025-06-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (79, 1, '测试日记61', '今天的心情是 very sad', 'very_sad', '2025-06-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (80, 1, '测试日记62', '今天的心情是 neutral', 'neutral', '2025-06-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (81, 1, '测试日记63', '今天的心情是 happy', 'happy', '2025-06-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (82, 1, '测试日记64', '今天的心情是 sad', 'sad', '2025-06-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (83, 1, '测试日记65', '今天的心情是 very sad', 'very_sad', '2025-06-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (84, 1, '测试日记66', '今天的心情是 neutral', 'neutral', '2025-06-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (85, 1, '测试日记67', '今天的心情是 very happy', 'very_happy', '2025-06-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (86, 1, '测试日记68', '今天的心情是 very sad', 'very_sad', '2025-06-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (87, 1, '测试日记69', '今天的心情是 sad', 'sad', '2025-06-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (88, 1, '测试日记70', '今天的心情是 very happy', 'very_happy', '2025-06-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (89, 1, '测试日记71', '今天的心情是 very happy', 'very_happy', '2025-06-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (90, 1, '测试日记72', '今天的心情是 neutral', 'neutral', '2025-06-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (91, 1, '测试日记73', '今天的心情是 neutral', 'neutral', '2025-06-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (92, 1, '测试日记74', '今天的心情是 sad', 'sad', '2025-06-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (93, 1, '测试日记75', '今天的心情是 very sad', 'very_sad', '2025-06-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (94, 1, '测试日记76', '今天的心情是 sad', 'sad', '2025-06-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (95, 1, '测试日记77', '今天的心情是 happy', 'happy', '2025-06-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (96, 1, '测试日记78', '今天的心情是 sad', 'sad', '2025-05-31 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (97, 1, '测试日记79', '今天的心情是 sad', 'sad', '2025-05-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (98, 1, '测试日记80', '今天的心情是 happy', 'happy', '2025-05-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (99, 1, '测试日记81', '今天的心情是 happy', 'happy', '2025-05-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (100, 1, '测试日记82', '今天的心情是 sad', 'sad', '2025-05-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (101, 1, '测试日记83', '今天的心情是 sad', 'sad', '2025-05-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (102, 1, '测试日记84', '今天的心情是 sad', 'sad', '2025-05-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (103, 1, '测试日记85', '今天的心情是 happy', 'happy', '2025-05-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (104, 1, '测试日记86', '今天的心情是 sad', 'sad', '2025-05-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (105, 1, '测试日记87', '今天的心情是 neutral', 'neutral', '2025-05-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (106, 1, '测试日记88', '今天的心情是 neutral', 'neutral', '2025-05-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (107, 1, '测试日记89', '今天的心情是 neutral', 'neutral', '2025-05-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (108, 1, '测试日记90', '今天的心情是 very sad', 'very_sad', '2025-05-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (109, 1, '测试日记91', '今天的心情是 very sad', 'very_sad', '2025-05-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (110, 1, '测试日记92', '今天的心情是 very happy', 'very_happy', '2025-05-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (111, 1, '测试日记93', '今天的心情是 sad', 'sad', '2025-05-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (112, 1, '测试日记94', '今天的心情是 sad', 'sad', '2025-05-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (113, 1, '测试日记95', '今天的心情是 very sad', 'very_sad', '2025-05-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (114, 1, '测试日记96', '今天的心情是 neutral', 'neutral', '2025-05-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (115, 1, '测试日记97', '今天的心情是 very sad', 'very_sad', '2025-05-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (116, 1, '测试日记98', '今天的心情是 neutral', 'neutral', '2025-05-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (117, 1, '测试日记99', '今天的心情是 happy', 'happy', '2025-05-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (118, 1, '测试日记100', '今天的心情是 happy', 'happy', '2025-05-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (119, 1, '测试日记101', '今天的心情是 sad', 'sad', '2025-05-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (120, 1, '测试日记102', '今天的心情是 neutral', 'neutral', '2025-05-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (121, 1, '测试日记103', '今天的心情是 sad', 'sad', '2025-05-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (122, 1, '测试日记104', '今天的心情是 very sad', 'very_sad', '2025-05-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (123, 1, '测试日记105', '今天的心情是 very happy', 'very_happy', '2025-05-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (124, 1, '测试日记106', '今天的心情是 happy', 'happy', '2025-05-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (125, 1, '测试日记107', '今天的心情是 very happy', 'very_happy', '2025-05-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (126, 1, '测试日记108', '今天的心情是 neutral', 'neutral', '2025-05-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (127, 1, '测试日记109', '今天的心情是 very sad', 'very_sad', '2025-04-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (128, 1, '测试日记110', '今天的心情是 very happy', 'very_happy', '2025-04-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (129, 1, '测试日记111', '今天的心情是 sad', 'sad', '2025-04-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (130, 1, '测试日记112', '今天的心情是 very happy', 'very_happy', '2025-04-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (131, 1, '测试日记113', '今天的心情是 happy', 'happy', '2025-04-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (132, 1, '测试日记114', '今天的心情是 neutral', 'neutral', '2025-04-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (133, 1, '测试日记115', '今天的心情是 sad', 'sad', '2025-04-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (134, 1, '测试日记116', '今天的心情是 sad', 'sad', '2025-04-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (135, 1, '测试日记117', '今天的心情是 neutral', 'neutral', '2025-04-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (136, 1, '测试日记118', '今天的心情是 very sad', 'very_sad', '2025-04-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (137, 1, '测试日记119', '今天的心情是 very happy', 'very_happy', '2025-04-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (138, 1, '测试日记120', '今天的心情是 happy', 'happy', '2025-04-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (139, 1, '测试日记121', '今天的心情是 sad', 'sad', '2025-04-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (140, 1, '测试日记122', '今天的心情是 very sad', 'very_sad', '2025-04-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (141, 1, '测试日记123', '今天的心情是 very happy', 'very_happy', '2025-04-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (142, 1, '测试日记124', '今天的心情是 neutral', 'neutral', '2025-04-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (143, 1, '测试日记125', '今天的心情是 neutral', 'neutral', '2025-04-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (144, 1, '测试日记126', '今天的心情是 neutral', 'neutral', '2025-04-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (145, 1, '测试日记127', '今天的心情是 very happy', 'very_happy', '2025-04-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (146, 1, '测试日记128', '今天的心情是 very happy', 'very_happy', '2025-04-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (147, 1, '测试日记129', '今天的心情是 sad', 'sad', '2025-04-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (148, 1, '测试日记130', '今天的心情是 neutral', 'neutral', '2025-04-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (149, 1, '测试日记131', '今天的心情是 very sad', 'very_sad', '2025-04-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (150, 1, '测试日记132', '今天的心情是 happy', 'happy', '2025-04-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (151, 1, '测试日记133', '今天的心情是 happy', 'happy', '2025-04-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (152, 1, '测试日记134', '今天的心情是 very sad', 'very_sad', '2025-04-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (153, 1, '测试日记135', '今天的心情是 sad', 'sad', '2025-04-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (154, 1, '测试日记136', '今天的心情是 sad', 'sad', '2025-04-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (155, 1, '测试日记137', '今天的心情是 neutral', 'neutral', '2025-04-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (156, 1, '测试日记138', '今天的心情是 very happy', 'very_happy', '2025-04-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (157, 1, '测试日记139', '今天的心情是 happy', 'happy', '2025-03-31 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (158, 1, '测试日记140', '今天的心情是 very happy', 'very_happy', '2025-03-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (159, 1, '测试日记141', '今天的心情是 happy', 'happy', '2025-03-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (160, 1, '测试日记142', '今天的心情是 very sad', 'very_sad', '2025-03-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (161, 1, '测试日记143', '今天的心情是 very happy', 'very_happy', '2025-03-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (162, 1, '测试日记144', '今天的心情是 happy', 'happy', '2025-03-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (163, 1, '测试日记145', '今天的心情是 happy', 'happy', '2025-03-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (164, 1, '测试日记146', '今天的心情是 very happy', 'very_happy', '2025-03-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (165, 1, '测试日记147', '今天的心情是 sad', 'sad', '2025-03-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (166, 1, '测试日记148', '今天的心情是 happy', 'happy', '2025-03-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (167, 1, '测试日记149', '今天的心情是 very sad', 'very_sad', '2025-03-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (168, 1, '测试日记150', '今天的心情是 very happy', 'very_happy', '2025-03-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (169, 1, '测试日记151', '今天的心情是 happy', 'happy', '2025-03-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (170, 1, '测试日记152', '今天的心情是 sad', 'sad', '2025-03-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (171, 1, '测试日记153', '今天的心情是 very sad', 'very_sad', '2025-03-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (172, 1, '测试日记154', '今天的心情是 happy', 'happy', '2025-03-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (173, 1, '测试日记155', '今天的心情是 very sad', 'very_sad', '2025-03-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (174, 1, '测试日记156', '今天的心情是 happy', 'happy', '2025-03-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (175, 1, '测试日记157', '今天的心情是 neutral', 'neutral', '2025-03-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (176, 1, '测试日记158', '今天的心情是 happy', 'happy', '2025-03-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (177, 1, '测试日记159', '今天的心情是 very happy', 'very_happy', '2025-03-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (178, 1, '测试日记160', '今天的心情是 happy', 'happy', '2025-03-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (179, 1, '测试日记161', '今天的心情是 sad', 'sad', '2025-03-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (180, 1, '测试日记162', '今天的心情是 very sad', 'very_sad', '2025-03-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (181, 1, '测试日记163', '今天的心情是 very happy', 'very_happy', '2025-03-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (182, 1, '测试日记164', '今天的心情是 very sad', 'very_sad', '2025-03-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (183, 1, '测试日记165', '今天的心情是 neutral', 'neutral', '2025-03-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (184, 1, '测试日记166', '今天的心情是 neutral', 'neutral', '2025-03-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (185, 1, '测试日记167', '今天的心情是 happy', 'happy', '2025-03-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (186, 1, '测试日记168', '今天的心情是 happy', 'happy', '2025-03-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (187, 1, '测试日记169', '今天的心情是 very sad', 'very_sad', '2025-03-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (188, 1, '测试日记170', '今天的心情是 very happy', 'very_happy', '2025-02-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (189, 1, '测试日记171', '今天的心情是 very happy', 'very_happy', '2025-02-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (190, 1, '测试日记172', '今天的心情是 neutral', 'neutral', '2025-02-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (191, 1, '测试日记173', '今天的心情是 very happy', 'very_happy', '2025-02-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (192, 1, '测试日记174', '今天的心情是 very sad', 'very_sad', '2025-02-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (193, 1, '测试日记175', '今天的心情是 very sad', 'very_sad', '2025-02-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (194, 1, '测试日记176', '今天的心情是 very sad', 'very_sad', '2025-02-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (195, 1, '测试日记177', '今天的心情是 sad', 'sad', '2025-02-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (196, 1, '测试日记178', '今天的心情是 happy', 'happy', '2025-02-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (197, 1, '测试日记179', '今天的心情是 very sad', 'very_sad', '2025-02-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (198, 1, '测试日记180', '今天的心情是 neutral', 'neutral', '2025-02-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (199, 1, '测试日记181', '今天的心情是 sad', 'sad', '2025-02-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (200, 1, '测试日记182', '今天的心情是 neutral', 'neutral', '2025-02-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (201, 1, '测试日记183', '今天的心情是 very sad', 'very_sad', '2025-02-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (202, 1, '测试日记184', '今天的心情是 very sad', 'very_sad', '2025-02-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (203, 1, '测试日记185', '今天的心情是 sad', 'sad', '2025-02-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (204, 1, '测试日记186', '今天的心情是 sad', 'sad', '2025-02-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (205, 1, '测试日记187', '今天的心情是 neutral', 'neutral', '2025-02-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (206, 1, '测试日记188', '今天的心情是 happy', 'happy', '2025-02-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (207, 1, '测试日记189', '今天的心情是 very happy', 'very_happy', '2025-02-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (208, 1, '测试日记190', '今天的心情是 happy', 'happy', '2025-02-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (209, 1, '测试日记191', '今天的心情是 neutral', 'neutral', '2025-02-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (210, 1, '测试日记192', '今天的心情是 very sad', 'very_sad', '2025-02-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (211, 1, '测试日记193', '今天的心情是 very happy', 'very_happy', '2025-02-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (212, 1, '测试日记194', '今天的心情是 very happy', 'very_happy', '2025-02-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (213, 1, '测试日记195', '今天的心情是 very sad', 'very_sad', '2025-02-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (214, 1, '测试日记196', '今天的心情是 neutral', 'neutral', '2025-02-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (215, 1, '测试日记197', '今天的心情是 sad', 'sad', '2025-02-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (216, 1, '测试日记198', '今天的心情是 neutral', 'neutral', '2025-01-31 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (217, 1, '测试日记199', '今天的心情是 very sad', 'very_sad', '2025-01-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (218, 1, '测试日记200', '今天的心情是 very sad', 'very_sad', '2025-01-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (219, 1, '测试日记201', '今天的心情是 neutral', 'neutral', '2025-01-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (220, 1, '测试日记202', '今天的心情是 very happy', 'very_happy', '2025-01-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (221, 1, '测试日记203', '今天的心情是 very sad', 'very_sad', '2025-01-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (222, 1, '测试日记204', '今天的心情是 happy', 'happy', '2025-01-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (223, 1, '测试日记205', '今天的心情是 very sad', 'very_sad', '2025-01-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (224, 1, '测试日记206', '今天的心情是 sad', 'sad', '2025-01-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (225, 1, '测试日记207', '今天的心情是 neutral', 'neutral', '2025-01-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (226, 1, '测试日记208', '今天的心情是 very sad', 'very_sad', '2025-01-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (227, 1, '测试日记209', '今天的心情是 sad', 'sad', '2025-01-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (228, 1, '测试日记210', '今天的心情是 very sad', 'very_sad', '2025-01-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (229, 1, '测试日记211', '今天的心情是 very sad', 'very_sad', '2025-01-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (230, 1, '测试日记212', '今天的心情是 very sad', 'very_sad', '2025-01-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (231, 1, '测试日记213', '今天的心情是 sad', 'sad', '2025-01-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (232, 1, '测试日记214', '今天的心情是 sad', 'sad', '2025-01-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (233, 1, '测试日记215', '今天的心情是 neutral', 'neutral', '2025-01-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (234, 1, '测试日记216', '今天的心情是 sad', 'sad', '2025-01-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (235, 1, '测试日记217', '今天的心情是 very happy', 'very_happy', '2025-01-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (236, 1, '测试日记218', '今天的心情是 very sad', 'very_sad', '2025-01-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (237, 1, '测试日记219', '今天的心情是 happy', 'happy', '2025-01-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (238, 1, '测试日记220', '今天的心情是 sad', 'sad', '2025-01-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (239, 1, '测试日记221', '今天的心情是 sad', 'sad', '2025-01-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (240, 1, '测试日记222', '今天的心情是 neutral', 'neutral', '2025-01-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (241, 1, '测试日记223', '今天的心情是 very happy', 'very_happy', '2025-01-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (242, 1, '测试日记224', '今天的心情是 very sad', 'very_sad', '2025-01-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (243, 1, '测试日记225', '今天的心情是 very happy', 'very_happy', '2025-01-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (244, 1, '测试日记226', '今天的心情是 neutral', 'neutral', '2025-01-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (245, 1, '测试日记227', '今天的心情是 neutral', 'neutral', '2025-01-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (246, 1, '测试日记228', '今天的心情是 very happy', 'very_happy', '2025-01-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (247, 1, '测试日记229', '今天的心情是 very sad', 'very_sad', '2024-12-31 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (248, 1, '测试日记230', '今天的心情是 very sad', 'very_sad', '2024-12-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (249, 1, '测试日记231', '今天的心情是 very happy', 'very_happy', '2024-12-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (250, 1, '测试日记232', '今天的心情是 very happy', 'very_happy', '2024-12-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (251, 1, '测试日记233', '今天的心情是 happy', 'happy', '2024-12-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (252, 1, '测试日记234', '今天的心情是 happy', 'happy', '2024-12-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (253, 1, '测试日记235', '今天的心情是 sad', 'sad', '2024-12-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (254, 1, '测试日记236', '今天的心情是 very happy', 'very_happy', '2024-12-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (255, 1, '测试日记237', '今天的心情是 neutral', 'neutral', '2024-12-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (256, 1, '测试日记238', '今天的心情是 sad', 'sad', '2024-12-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (257, 1, '测试日记239', '今天的心情是 neutral', 'neutral', '2024-12-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (258, 1, '测试日记240', '今天的心情是 very sad', 'very_sad', '2024-12-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (259, 1, '测试日记241', '今天的心情是 sad', 'sad', '2024-12-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (260, 1, '测试日记242', '今天的心情是 very happy', 'very_happy', '2024-12-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (261, 1, '测试日记243', '今天的心情是 happy', 'happy', '2024-12-17 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (262, 1, '测试日记244', '今天的心情是 happy', 'happy', '2024-12-16 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (263, 1, '测试日记245', '今天的心情是 very happy', 'very_happy', '2024-12-15 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (264, 1, '测试日记246', '今天的心情是 very sad', 'very_sad', '2024-12-14 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (265, 1, '测试日记247', '今天的心情是 very sad', 'very_sad', '2024-12-13 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (266, 1, '测试日记248', '今天的心情是 very happy', 'very_happy', '2024-12-12 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (267, 1, '测试日记249', '今天的心情是 very happy', 'very_happy', '2024-12-11 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (268, 1, '测试日记250', '今天的心情是 very sad', 'very_sad', '2024-12-10 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (269, 1, '测试日记251', '今天的心情是 very sad', 'very_sad', '2024-12-09 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (270, 1, '测试日记252', '今天的心情是 sad', 'sad', '2024-12-08 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (271, 1, '测试日记253', '今天的心情是 sad', 'sad', '2024-12-07 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (272, 1, '测试日记254', '今天的心情是 sad', 'sad', '2024-12-06 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (273, 1, '测试日记255', '今天的心情是 neutral', 'neutral', '2024-12-05 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (274, 1, '测试日记256', '今天的心情是 neutral', 'neutral', '2024-12-04 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (275, 1, '测试日记257', '今天的心情是 neutral', 'neutral', '2024-12-03 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (276, 1, '测试日记258', '今天的心情是 neutral', 'neutral', '2024-12-02 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (277, 1, '测试日记259', '今天的心情是 sad', 'sad', '2024-12-01 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (278, 1, '测试日记260', '今天的心情是 neutral', 'neutral', '2024-11-30 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (279, 1, '测试日记261', '今天的心情是 neutral', 'neutral', '2024-11-29 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (280, 1, '测试日记262', '今天的心情是 very sad', 'very_sad', '2024-11-28 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (281, 1, '测试日记263', '今天的心情是 sad', 'sad', '2024-11-27 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (282, 1, '测试日记264', '今天的心情是 sad', 'sad', '2024-11-26 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (283, 1, '测试日记265', '今天的心情是 very happy', 'very_happy', '2024-11-25 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (284, 1, '测试日记266', '今天的心情是 neutral', 'neutral', '2024-11-24 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (285, 1, '测试日记267', '今天的心情是 very happy', 'very_happy', '2024-11-23 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (286, 1, '测试日记268', '今天的心情是 happy', 'happy', '2024-11-22 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (287, 1, '测试日记269', '今天的心情是 very happy', 'very_happy', '2024-11-21 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (288, 1, '测试日记270', '今天的心情是 very happy', 'very_happy', '2024-11-20 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (289, 1, '测试日记271', '今天的心情是 very sad', 'very_sad', '2024-11-19 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (290, 1, '测试日记272', '今天的心情是 neutral', 'neutral', '2024-11-18 18:24:03', '2025-08-16 18:25:37', 1, 0);
INSERT INTO `emotional_diaries` VALUES (291, 1, '测试日记273', '今天的心情是 sad', 'sad', '2024-11-17 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (292, 1, '测试日记274', '今天的心情是 happy', 'happy', '2024-11-16 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (293, 1, '测试日记275', '今天的心情是 very happy', 'very_happy', '2024-11-15 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (294, 1, '测试日记276', '今天的心情是 neutral', 'neutral', '2024-11-14 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (295, 1, '测试日记277', '今天的心情是 very sad', 'very_sad', '2024-11-13 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (296, 1, '测试日记278', '今天的心情是 very sad', 'very_sad', '2024-11-12 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (297, 1, '测试日记279', '今天的心情是 very happy', 'very_happy', '2024-11-11 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (298, 1, '测试日记280', '今天的心情是 very sad', 'very_sad', '2024-11-10 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (299, 1, '测试日记281', '今天的心情是 very happy', 'very_happy', '2024-11-09 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (300, 1, '测试日记282', '今天的心情是 very sad', 'very_sad', '2024-11-08 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (301, 1, '测试日记283', '今天的心情是 sad', 'sad', '2024-11-07 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (302, 1, '测试日记284', '今天的心情是 happy', 'happy', '2024-11-06 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (303, 1, '测试日记285', '今天的心情是 very happy', 'very_happy', '2024-11-05 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (304, 1, '测试日记286', '今天的心情是 happy', 'happy', '2024-11-04 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (305, 1, '测试日记287', '今天的心情是 sad', 'sad', '2024-11-03 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (306, 1, '测试日记288', '今天的心情是 neutral', 'neutral', '2024-11-02 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (307, 1, '测试日记289', '今天的心情是 very happy', 'very_happy', '2024-11-01 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (308, 1, '测试日记290', '今天的心情是 sad', 'sad', '2024-10-31 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (309, 1, '测试日记291', '今天的心情是 very sad', 'very_sad', '2024-10-30 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (310, 1, '测试日记292', '今天的心情是 sad', 'sad', '2024-10-29 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (311, 1, '测试日记293', '今天的心情是 sad', 'sad', '2024-10-28 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (312, 1, '测试日记294', '今天的心情是 sad', 'sad', '2024-10-27 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (313, 1, '测试日记295', '今天的心情是 sad', 'sad', '2024-10-26 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (314, 1, '测试日记296', '今天的心情是 very sad', 'very_sad', '2024-10-25 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (315, 1, '测试日记297', '今天的心情是 very sad', 'very_sad', '2024-10-24 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (316, 1, '测试日记298', '今天的心情是 happy', 'happy', '2024-10-23 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (317, 1, '测试日记299', '今天的心情是 happy', 'happy', '2024-10-22 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (318, 1, '测试日记300', '今天的心情是 sad', 'sad', '2024-10-21 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (319, 1, '测试日记301', '今天的心情是 very sad', 'very_sad', '2024-10-20 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (320, 1, '测试日记302', '今天的心情是 sad', 'sad', '2024-10-19 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (321, 1, '测试日记303', '今天的心情是 very sad', 'very_sad', '2024-10-18 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (322, 1, '测试日记304', '今天的心情是 neutral', 'neutral', '2024-10-17 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (323, 1, '测试日记305', '今天的心情是 very sad', 'very_sad', '2024-10-16 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (324, 1, '测试日记306', '今天的心情是 happy', 'happy', '2024-10-15 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (325, 1, '测试日记307', '今天的心情是 very happy', 'very_happy', '2024-10-14 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (326, 1, '测试日记308', '今天的心情是 very happy', 'very_happy', '2024-10-13 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (327, 1, '测试日记309', '今天的心情是 happy', 'happy', '2024-10-12 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (328, 1, '测试日记310', '今天的心情是 very sad', 'very_sad', '2024-10-11 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (329, 1, '测试日记311', '今天的心情是 very sad', 'very_sad', '2024-10-10 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (330, 1, '测试日记312', '今天的心情是 very sad', 'very_sad', '2024-10-09 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (331, 1, '测试日记313', '今天的心情是 happy', 'happy', '2024-10-08 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (332, 1, '测试日记314', '今天的心情是 very sad', 'very_sad', '2024-10-07 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (333, 1, '测试日记315', '今天的心情是 neutral', 'neutral', '2024-10-06 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (334, 1, '测试日记316', '今天的心情是 very happy', 'very_happy', '2024-10-05 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (335, 1, '测试日记317', '今天的心情是 neutral', 'neutral', '2024-10-04 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (336, 1, '测试日记318', '今天的心情是 very sad', 'very_sad', '2024-10-03 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (337, 1, '测试日记319', '今天的心情是 very sad', 'very_sad', '2024-10-02 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (338, 1, '测试日记320', '今天的心情是 sad', 'sad', '2024-10-01 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (339, 1, '测试日记321', '今天的心情是 sad', 'sad', '2024-09-30 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (340, 1, '测试日记322', '今天的心情是 very happy', 'very_happy', '2024-09-29 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (341, 1, '测试日记323', '今天的心情是 very happy', 'very_happy', '2024-09-28 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (342, 1, '测试日记324', '今天的心情是 very sad', 'very_sad', '2024-09-27 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (343, 1, '测试日记325', '今天的心情是 very happy', 'very_happy', '2024-09-26 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (344, 1, '测试日记326', '今天的心情是 very sad', 'very_sad', '2024-09-25 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (345, 1, '测试日记327', '今天的心情是 very happy', 'very_happy', '2024-09-24 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (346, 1, '测试日记328', '今天的心情是 neutral', 'neutral', '2024-09-23 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (347, 1, '测试日记329', '今天的心情是 very sad', 'very_sad', '2024-09-22 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (348, 1, '测试日记330', '今天的心情是 happy', 'happy', '2024-09-21 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (349, 1, '测试日记331', '今天的心情是 sad', 'sad', '2024-09-20 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (350, 1, '测试日记332', '今天的心情是 neutral', 'neutral', '2024-09-19 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (351, 1, '测试日记333', '今天的心情是 very happy', 'very_happy', '2024-09-18 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (352, 1, '测试日记334', '今天的心情是 very sad', 'very_sad', '2024-09-17 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (353, 1, '测试日记335', '今天的心情是 neutral', 'neutral', '2024-09-16 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (354, 1, '测试日记336', '今天的心情是 happy', 'happy', '2024-09-15 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (355, 1, '测试日记337', '今天的心情是 very happy', 'very_happy', '2024-09-14 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (356, 1, '测试日记338', '今天的心情是 very sad', 'very_sad', '2024-09-13 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (357, 1, '测试日记339', '今天的心情是 very sad', 'very_sad', '2024-09-12 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (358, 1, '测试日记340', '今天的心情是 neutral', 'neutral', '2024-09-11 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (359, 1, '测试日记341', '今天的心情是 happy', 'happy', '2024-09-10 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (360, 1, '测试日记342', '今天的心情是 very happy', 'very_happy', '2024-09-09 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (361, 1, '测试日记343', '今天的心情是 happy', 'happy', '2024-09-08 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (362, 1, '测试日记344', '今天的心情是 very sad', 'very_sad', '2024-09-07 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (363, 1, '测试日记345', '今天的心情是 very sad', 'very_sad', '2024-09-06 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (364, 1, '测试日记346', '今天的心情是 very happy', 'very_happy', '2024-09-05 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (365, 1, '测试日记347', '今天的心情是 neutral', 'neutral', '2024-09-04 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (366, 1, '测试日记348', '今天的心情是 neutral', 'neutral', '2024-09-03 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (367, 1, '测试日记349', '今天的心情是 happy', 'happy', '2024-09-02 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (368, 1, '测试日记350', '今天的心情是 very happy', 'very_happy', '2024-09-01 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (369, 1, '测试日记351', '今天的心情是 sad', 'sad', '2024-08-31 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (370, 1, '测试日记352', '今天的心情是 happy', 'happy', '2024-08-30 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (371, 1, '测试日记353', '今天的心情是 sad', 'sad', '2024-08-29 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (372, 1, '测试日记354', '今天的心情是 sad', 'sad', '2024-08-28 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (373, 1, '测试日记355', '今天的心情是 happy', 'happy', '2024-08-27 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (374, 1, '测试日记356', '今天的心情是 sad', 'sad', '2024-08-26 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (375, 1, '测试日记357', '今天的心情是 neutral', 'neutral', '2024-08-25 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (376, 1, '测试日记358', '今天的心情是 very sad', 'very_sad', '2024-08-24 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (377, 1, '测试日记359', '今天的心情是 happy', 'happy', '2024-08-23 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (378, 1, '测试日记360', '今天的心情是 very happy', 'very_happy', '2024-08-22 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (379, 1, '测试日记361', '今天的心情是 very happy', 'very_happy', '2024-08-21 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (380, 1, '测试日记362', '今天的心情是 happy', 'happy', '2024-08-20 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (381, 1, '测试日记363', '今天的心情是 very sad', 'very_sad', '2024-08-19 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (382, 1, '测试日记364', '今天的心情是 neutral', 'neutral', '2024-08-18 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (383, 1, '测试日记365', '今天的心情是 very sad', 'very_sad', '2024-08-17 18:24:03', '2025-08-16 18:25:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (384, 6, '测试日记1', '今天的心情是 sad', 'sad', '2025-08-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (385, 6, '测试日记2', '今天的心情是 neutral', 'neutral', '2025-08-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (386, 6, '测试日记3', '今天的心情是 very happy', 'very_happy', '2025-08-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (387, 6, '测试日记4', '今天的心情是 sad', 'sad', '2025-08-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (388, 6, '测试日记5', '今天的心情是 neutral', 'neutral', '2025-08-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (389, 6, '测试日记6', '今天的心情是 very sad', 'very_sad', '2025-08-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (390, 6, '测试日记7', '今天的心情是 very happy', 'very_happy', '2025-08-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (391, 6, '测试日记8', '今天的心情是 sad', 'sad', '2025-08-09 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (392, 6, '测试日记9', '今天的心情是 sad', 'sad', '2025-08-08 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (393, 6, '测试日记10', '今天的心情是 very sad', 'very_sad', '2025-08-07 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (394, 6, '测试日记11', '今天的心情是 very sad', 'very_sad', '2025-08-06 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (395, 6, '测试日记12', '今天的心情是 happy', 'happy', '2025-08-05 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (396, 6, '测试日记13', '今天的心情是 happy', 'happy', '2025-08-04 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (397, 6, '测试日记14', '今天的心情是 very happy', 'very_happy', '2025-08-03 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (398, 6, '测试日记15', '今天的心情是 happy', 'happy', '2025-08-02 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (399, 6, '测试日记16', '今天的心情是 very happy', 'very_happy', '2025-08-01 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (400, 6, '测试日记17', '今天的心情是 very happy', 'very_happy', '2025-07-31 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (401, 6, '测试日记18', '今天的心情是 very happy', 'very_happy', '2025-07-30 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (402, 6, '测试日记19', '今天的心情是 happy', 'happy', '2025-07-29 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (403, 6, '测试日记20', '今天的心情是 very sad', 'very_sad', '2025-07-28 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (404, 6, '测试日记21', '今天的心情是 happy', 'happy', '2025-07-27 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (405, 6, '测试日记22', '今天的心情是 sad', 'sad', '2025-07-26 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (406, 6, '测试日记23', '今天的心情是 very sad', 'very_sad', '2025-07-25 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (407, 6, '测试日记24', '今天的心情是 very sad', 'very_sad', '2025-07-24 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (408, 6, '测试日记25', '今天的心情是 very sad', 'very_sad', '2025-07-23 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (409, 6, '测试日记26', '今天的心情是 happy', 'happy', '2025-07-22 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (410, 6, '测试日记27', '今天的心情是 sad', 'sad', '2025-07-21 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (411, 6, '测试日记28', '今天的心情是 neutral', 'neutral', '2025-07-20 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (412, 6, '测试日记29', '今天的心情是 very happy', 'very_happy', '2025-07-19 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (413, 6, '测试日记30', '今天的心情是 happy', 'happy', '2025-07-18 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (414, 6, '测试日记31', '今天的心情是 sad', 'sad', '2025-07-17 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (415, 6, '测试日记32', '今天的心情是 happy', 'happy', '2025-07-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (416, 6, '测试日记33', '今天的心情是 sad', 'sad', '2025-07-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (417, 6, '测试日记34', '今天的心情是 neutral', 'neutral', '2025-07-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (418, 6, '测试日记35', '今天的心情是 happy', 'happy', '2025-07-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (419, 6, '测试日记36', '今天的心情是 neutral', 'neutral', '2025-07-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (420, 6, '测试日记37', '今天的心情是 very happy', 'very_happy', '2025-07-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (421, 6, '测试日记38', '今天的心情是 very sad', 'very_sad', '2025-07-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (422, 6, '测试日记39', '今天的心情是 very happy', 'very_happy', '2025-07-09 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (423, 6, '测试日记40', '今天的心情是 neutral', 'neutral', '2025-07-08 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (424, 6, '测试日记41', '今天的心情是 sad', 'sad', '2025-07-07 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (425, 6, '测试日记42', '今天的心情是 very happy', 'very_happy', '2025-07-06 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (426, 6, '测试日记43', '今天的心情是 neutral', 'neutral', '2025-07-05 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (427, 6, '测试日记44', '今天的心情是 very sad', 'very_sad', '2025-07-04 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (428, 6, '测试日记45', '今天的心情是 neutral', 'neutral', '2025-07-03 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (429, 6, '测试日记46', '今天的心情是 very sad', 'very_sad', '2025-07-02 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (430, 6, '测试日记47', '今天的心情是 happy', 'happy', '2025-07-01 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (431, 6, '测试日记48', '今天的心情是 very happy', 'very_happy', '2025-06-30 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (432, 6, '测试日记49', '今天的心情是 happy', 'happy', '2025-06-29 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (433, 6, '测试日记50', '今天的心情是 happy', 'happy', '2025-06-28 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (434, 6, '测试日记51', '今天的心情是 neutral', 'neutral', '2025-06-27 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (435, 6, '测试日记52', '今天的心情是 sad', 'sad', '2025-06-26 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (436, 6, '测试日记53', '今天的心情是 very happy', 'very_happy', '2025-06-25 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (437, 6, '测试日记54', '今天的心情是 neutral', 'neutral', '2025-06-24 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (438, 6, '测试日记55', '今天的心情是 happy', 'happy', '2025-06-23 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (439, 6, '测试日记56', '今天的心情是 sad', 'sad', '2025-06-22 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (440, 6, '测试日记57', '今天的心情是 neutral', 'neutral', '2025-06-21 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (441, 6, '测试日记58', '今天的心情是 happy', 'happy', '2025-06-20 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (442, 6, '测试日记59', '今天的心情是 very happy', 'very_happy', '2025-06-19 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (443, 6, '测试日记60', '今天的心情是 very happy', 'very_happy', '2025-06-18 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (444, 6, '测试日记61', '今天的心情是 very happy', 'very_happy', '2025-06-17 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (445, 6, '测试日记62', '今天的心情是 neutral', 'neutral', '2025-06-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (446, 6, '测试日记63', '今天的心情是 very sad', 'very_sad', '2025-06-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (447, 6, '测试日记64', '今天的心情是 very happy', 'very_happy', '2025-06-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (448, 6, '测试日记65', '今天的心情是 very happy', 'very_happy', '2025-06-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (449, 6, '测试日记66', '今天的心情是 neutral', 'neutral', '2025-06-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (450, 6, '测试日记67', '今天的心情是 sad', 'sad', '2025-06-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (451, 6, '测试日记68', '今天的心情是 neutral', 'neutral', '2025-06-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (452, 6, '测试日记69', '今天的心情是 very happy', 'very_happy', '2025-06-09 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (453, 6, '测试日记70', '今天的心情是 happy', 'happy', '2025-06-08 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (454, 6, '测试日记71', '今天的心情是 happy', 'happy', '2025-06-07 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (455, 6, '测试日记72', '今天的心情是 sad', 'sad', '2025-06-06 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (456, 6, '测试日记73', '今天的心情是 happy', 'happy', '2025-06-05 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (457, 6, '测试日记74', '今天的心情是 very sad', 'very_sad', '2025-06-04 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (458, 6, '测试日记75', '今天的心情是 very sad', 'very_sad', '2025-06-03 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (459, 6, '测试日记76', '今天的心情是 very sad', 'very_sad', '2025-06-02 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (460, 6, '测试日记77', '今天的心情是 happy', 'happy', '2025-06-01 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (461, 6, '测试日记78', '今天的心情是 very sad', 'very_sad', '2025-05-31 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (462, 6, '测试日记79', '今天的心情是 neutral', 'neutral', '2025-05-30 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (463, 6, '测试日记80', '今天的心情是 sad', 'sad', '2025-05-29 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (464, 6, '测试日记81', '今天的心情是 neutral', 'neutral', '2025-05-28 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (465, 6, '测试日记82', '今天的心情是 very happy', 'very_happy', '2025-05-27 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (466, 6, '测试日记83', '今天的心情是 very happy', 'very_happy', '2025-05-26 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (467, 6, '测试日记84', '今天的心情是 sad', 'sad', '2025-05-25 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (468, 6, '测试日记85', '今天的心情是 very happy', 'very_happy', '2025-05-24 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (469, 6, '测试日记86', '今天的心情是 very happy', 'very_happy', '2025-05-23 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (470, 6, '测试日记87', '今天的心情是 very happy', 'very_happy', '2025-05-22 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (471, 6, '测试日记88', '今天的心情是 very happy', 'very_happy', '2025-05-21 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (472, 6, '测试日记89', '今天的心情是 happy', 'happy', '2025-05-20 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (473, 6, '测试日记90', '今天的心情是 happy', 'happy', '2025-05-19 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (474, 6, '测试日记91', '今天的心情是 sad', 'sad', '2025-05-18 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (475, 6, '测试日记92', '今天的心情是 happy', 'happy', '2025-05-17 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (476, 6, '测试日记93', '今天的心情是 very sad', 'very_sad', '2025-05-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (477, 6, '测试日记94', '今天的心情是 sad', 'sad', '2025-05-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (478, 6, '测试日记95', '今天的心情是 very sad', 'very_sad', '2025-05-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (479, 6, '测试日记96', '今天的心情是 neutral', 'neutral', '2025-05-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (480, 6, '测试日记97', '今天的心情是 very happy', 'very_happy', '2025-05-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (481, 6, '测试日记98', '今天的心情是 sad', 'sad', '2025-05-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (482, 6, '测试日记99', '今天的心情是 sad', 'sad', '2025-05-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (483, 6, '测试日记100', '今天的心情是 sad', 'sad', '2025-05-09 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (484, 6, '测试日记101', '今天的心情是 happy', 'happy', '2025-05-08 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (485, 6, '测试日记102', '今天的心情是 very happy', 'very_happy', '2025-05-07 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (486, 6, '测试日记103', '今天的心情是 happy', 'happy', '2025-05-06 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (487, 6, '测试日记104', '今天的心情是 very sad', 'very_sad', '2025-05-05 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (488, 6, '测试日记105', '今天的心情是 sad', 'sad', '2025-05-04 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (489, 6, '测试日记106', '今天的心情是 very sad', 'very_sad', '2025-05-03 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (490, 6, '测试日记107', '今天的心情是 neutral', 'neutral', '2025-05-02 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (491, 6, '测试日记108', '今天的心情是 very sad', 'very_sad', '2025-05-01 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (492, 6, '测试日记109', '今天的心情是 happy', 'happy', '2025-04-30 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (493, 6, '测试日记110', '今天的心情是 very happy', 'very_happy', '2025-04-29 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (494, 6, '测试日记111', '今天的心情是 very happy', 'very_happy', '2025-04-28 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (495, 6, '测试日记112', '今天的心情是 sad', 'sad', '2025-04-27 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (496, 6, '测试日记113', '今天的心情是 very happy', 'very_happy', '2025-04-26 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (497, 6, '测试日记114', '今天的心情是 very happy', 'very_happy', '2025-04-25 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (498, 6, '测试日记115', '今天的心情是 very happy', 'very_happy', '2025-04-24 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (499, 6, '测试日记116', '今天的心情是 sad', 'sad', '2025-04-23 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (500, 6, '测试日记117', '今天的心情是 very sad', 'very_sad', '2025-04-22 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (501, 6, '测试日记118', '今天的心情是 very sad', 'very_sad', '2025-04-21 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (502, 6, '测试日记119', '今天的心情是 very happy', 'very_happy', '2025-04-20 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (503, 6, '测试日记120', '今天的心情是 sad', 'sad', '2025-04-19 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (504, 6, '测试日记121', '今天的心情是 happy', 'happy', '2025-04-18 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (505, 6, '测试日记122', '今天的心情是 very sad', 'very_sad', '2025-04-17 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (506, 6, '测试日记123', '今天的心情是 very happy', 'very_happy', '2025-04-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (507, 6, '测试日记124', '今天的心情是 very sad', 'very_sad', '2025-04-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (508, 6, '测试日记125', '今天的心情是 very sad', 'very_sad', '2025-04-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (509, 6, '测试日记126', '今天的心情是 very happy', 'very_happy', '2025-04-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (510, 6, '测试日记127', '今天的心情是 sad', 'sad', '2025-04-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (511, 6, '测试日记128', '今天的心情是 sad', 'sad', '2025-04-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (512, 6, '测试日记129', '今天的心情是 neutral', 'neutral', '2025-04-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (513, 6, '测试日记130', '今天的心情是 sad', 'sad', '2025-04-09 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (514, 6, '测试日记131', '今天的心情是 sad', 'sad', '2025-04-08 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (515, 6, '测试日记132', '今天的心情是 sad', 'sad', '2025-04-07 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (516, 6, '测试日记133', '今天的心情是 happy', 'happy', '2025-04-06 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (517, 6, '测试日记134', '今天的心情是 very sad', 'very_sad', '2025-04-05 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (518, 6, '测试日记135', '今天的心情是 neutral', 'neutral', '2025-04-04 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (519, 6, '测试日记136', '今天的心情是 neutral', 'neutral', '2025-04-03 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (520, 6, '测试日记137', '今天的心情是 sad', 'sad', '2025-04-02 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (521, 6, '测试日记138', '今天的心情是 very happy', 'very_happy', '2025-04-01 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (522, 6, '测试日记139', '今天的心情是 very sad', 'very_sad', '2025-03-31 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (523, 6, '测试日记140', '今天的心情是 very happy', 'very_happy', '2025-03-30 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (524, 6, '测试日记141', '今天的心情是 sad', 'sad', '2025-03-29 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (525, 6, '测试日记142', '今天的心情是 very sad', 'very_sad', '2025-03-28 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (526, 6, '测试日记143', '今天的心情是 neutral', 'neutral', '2025-03-27 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (527, 6, '测试日记144', '今天的心情是 very happy', 'very_happy', '2025-03-26 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (528, 6, '测试日记145', '今天的心情是 neutral', 'neutral', '2025-03-25 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (529, 6, '测试日记146', '今天的心情是 sad', 'sad', '2025-03-24 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (530, 6, '测试日记147', '今天的心情是 very sad', 'very_sad', '2025-03-23 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (531, 6, '测试日记148', '今天的心情是 neutral', 'neutral', '2025-03-22 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (532, 6, '测试日记149', '今天的心情是 neutral', 'neutral', '2025-03-21 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (533, 6, '测试日记150', '今天的心情是 very sad', 'very_sad', '2025-03-20 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (534, 6, '测试日记151', '今天的心情是 very sad', 'very_sad', '2025-03-19 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (535, 6, '测试日记152', '今天的心情是 very sad', 'very_sad', '2025-03-18 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (536, 6, '测试日记153', '今天的心情是 sad', 'sad', '2025-03-17 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (537, 6, '测试日记154', '今天的心情是 neutral', 'neutral', '2025-03-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (538, 6, '测试日记155', '今天的心情是 very sad', 'very_sad', '2025-03-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (539, 6, '测试日记156', '今天的心情是 neutral', 'neutral', '2025-03-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (540, 6, '测试日记157', '今天的心情是 neutral', 'neutral', '2025-03-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (541, 6, '测试日记158', '今天的心情是 sad', 'sad', '2025-03-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (542, 6, '测试日记159', '今天的心情是 sad', 'sad', '2025-03-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (543, 6, '测试日记160', '今天的心情是 very happy', 'very_happy', '2025-03-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (544, 6, '测试日记161', '今天的心情是 very sad', 'very_sad', '2025-03-09 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (545, 6, '测试日记162', '今天的心情是 sad', 'sad', '2025-03-08 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (546, 6, '测试日记163', '今天的心情是 very happy', 'very_happy', '2025-03-07 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (547, 6, '测试日记164', '今天的心情是 neutral', 'neutral', '2025-03-06 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (548, 6, '测试日记165', '今天的心情是 neutral', 'neutral', '2025-03-05 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (549, 6, '测试日记166', '今天的心情是 neutral', 'neutral', '2025-03-04 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (550, 6, '测试日记167', '今天的心情是 very happy', 'very_happy', '2025-03-03 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (551, 6, '测试日记168', '今天的心情是 very sad', 'very_sad', '2025-03-02 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (552, 6, '测试日记169', '今天的心情是 sad', 'sad', '2025-03-01 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (553, 6, '测试日记170', '今天的心情是 sad', 'sad', '2025-02-28 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (554, 6, '测试日记171', '今天的心情是 sad', 'sad', '2025-02-27 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (555, 6, '测试日记172', '今天的心情是 happy', 'happy', '2025-02-26 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (556, 6, '测试日记173', '今天的心情是 very sad', 'very_sad', '2025-02-25 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (557, 6, '测试日记174', '今天的心情是 very happy', 'very_happy', '2025-02-24 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (558, 6, '测试日记175', '今天的心情是 very happy', 'very_happy', '2025-02-23 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (559, 6, '测试日记176', '今天的心情是 very sad', 'very_sad', '2025-02-22 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (560, 6, '测试日记177', '今天的心情是 very happy', 'very_happy', '2025-02-21 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (561, 6, '测试日记178', '今天的心情是 very sad', 'very_sad', '2025-02-20 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (562, 6, '测试日记179', '今天的心情是 very happy', 'very_happy', '2025-02-19 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (563, 6, '测试日记180', '今天的心情是 very happy', 'very_happy', '2025-02-18 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (564, 6, '测试日记181', '今天的心情是 sad', 'sad', '2025-02-17 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (565, 6, '测试日记182', '今天的心情是 very sad', 'very_sad', '2025-02-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (566, 6, '测试日记183', '今天的心情是 happy', 'happy', '2025-02-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (567, 6, '测试日记184', '今天的心情是 very sad', 'very_sad', '2025-02-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (568, 6, '测试日记185', '今天的心情是 very sad', 'very_sad', '2025-02-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (569, 6, '测试日记186', '今天的心情是 happy', 'happy', '2025-02-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (570, 6, '测试日记187', '今天的心情是 happy', 'happy', '2025-02-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (571, 6, '测试日记188', '今天的心情是 sad', 'sad', '2025-02-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (572, 6, '测试日记189', '今天的心情是 sad', 'sad', '2025-02-09 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (573, 6, '测试日记190', '今天的心情是 sad', 'sad', '2025-02-08 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (574, 6, '测试日记191', '今天的心情是 happy', 'happy', '2025-02-07 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (575, 6, '测试日记192', '今天的心情是 neutral', 'neutral', '2025-02-06 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (576, 6, '测试日记193', '今天的心情是 neutral', 'neutral', '2025-02-05 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (577, 6, '测试日记194', '今天的心情是 neutral', 'neutral', '2025-02-04 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (578, 6, '测试日记195', '今天的心情是 very happy', 'very_happy', '2025-02-03 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (579, 6, '测试日记196', '今天的心情是 very sad', 'very_sad', '2025-02-02 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (580, 6, '测试日记197', '今天的心情是 very sad', 'very_sad', '2025-02-01 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (581, 6, '测试日记198', '今天的心情是 happy', 'happy', '2025-01-31 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (582, 6, '测试日记199', '今天的心情是 neutral', 'neutral', '2025-01-30 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (583, 6, '测试日记200', '今天的心情是 sad', 'sad', '2025-01-29 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (584, 6, '测试日记201', '今天的心情是 neutral', 'neutral', '2025-01-28 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (585, 6, '测试日记202', '今天的心情是 very sad', 'very_sad', '2025-01-27 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (586, 6, '测试日记203', '今天的心情是 sad', 'sad', '2025-01-26 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (587, 6, '测试日记204', '今天的心情是 sad', 'sad', '2025-01-25 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (588, 6, '测试日记205', '今天的心情是 neutral', 'neutral', '2025-01-24 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (589, 6, '测试日记206', '今天的心情是 happy', 'happy', '2025-01-23 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (590, 6, '测试日记207', '今天的心情是 very happy', 'very_happy', '2025-01-22 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (591, 6, '测试日记208', '今天的心情是 very happy', 'very_happy', '2025-01-21 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (592, 6, '测试日记209', '今天的心情是 happy', 'happy', '2025-01-20 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (593, 6, '测试日记210', '今天的心情是 very sad', 'very_sad', '2025-01-19 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (594, 6, '测试日记211', '今天的心情是 happy', 'happy', '2025-01-18 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (595, 6, '测试日记212', '今天的心情是 sad', 'sad', '2025-01-17 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (596, 6, '测试日记213', '今天的心情是 neutral', 'neutral', '2025-01-16 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (597, 6, '测试日记214', '今天的心情是 very sad', 'very_sad', '2025-01-15 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (598, 6, '测试日记215', '今天的心情是 sad', 'sad', '2025-01-14 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (599, 6, '测试日记216', '今天的心情是 very sad', 'very_sad', '2025-01-13 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (600, 6, '测试日记217', '今天的心情是 very happy', 'very_happy', '2025-01-12 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (601, 6, '测试日记218', '今天的心情是 very sad', 'very_sad', '2025-01-11 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (602, 6, '测试日记219', '今天的心情是 neutral', 'neutral', '2025-01-10 18:26:13', '2025-08-16 18:26:38', 1, 0);
INSERT INTO `emotional_diaries` VALUES (603, 6, '测试日记220', '今天的心情是 happy', 'happy', '2025-01-09 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (604, 6, '测试日记221', '今天的心情是 sad', 'sad', '2025-01-08 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (605, 6, '测试日记222', '今天的心情是 neutral', 'neutral', '2025-01-07 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (606, 6, '测试日记223', '今天的心情是 sad', 'sad', '2025-01-06 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (607, 6, '测试日记224', '今天的心情是 sad', 'sad', '2025-01-05 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (608, 6, '测试日记225', '今天的心情是 happy', 'happy', '2025-01-04 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (609, 6, '测试日记226', '今天的心情是 very sad', 'very_sad', '2025-01-03 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (610, 6, '测试日记227', '今天的心情是 sad', 'sad', '2025-01-02 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (611, 6, '测试日记228', '今天的心情是 very sad', 'very_sad', '2025-01-01 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (612, 6, '测试日记229', '今天的心情是 neutral', 'neutral', '2024-12-31 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (613, 6, '测试日记230', '今天的心情是 very happy', 'very_happy', '2024-12-30 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (614, 6, '测试日记231', '今天的心情是 neutral', 'neutral', '2024-12-29 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (615, 6, '测试日记232', '今天的心情是 very sad', 'very_sad', '2024-12-28 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (616, 6, '测试日记233', '今天的心情是 happy', 'happy', '2024-12-27 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (617, 6, '测试日记234', '今天的心情是 very happy', 'very_happy', '2024-12-26 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (618, 6, '测试日记235', '今天的心情是 sad', 'sad', '2024-12-25 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (619, 6, '测试日记236', '今天的心情是 very sad', 'very_sad', '2024-12-24 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (620, 6, '测试日记237', '今天的心情是 sad', 'sad', '2024-12-23 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (621, 6, '测试日记238', '今天的心情是 sad', 'sad', '2024-12-22 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (622, 6, '测试日记239', '今天的心情是 very happy', 'very_happy', '2024-12-21 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (623, 6, '测试日记240', '今天的心情是 sad', 'sad', '2024-12-20 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (624, 6, '测试日记241', '今天的心情是 neutral', 'neutral', '2024-12-19 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (625, 6, '测试日记242', '今天的心情是 very sad', 'very_sad', '2024-12-18 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (626, 6, '测试日记243', '今天的心情是 sad', 'sad', '2024-12-17 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (627, 6, '测试日记244', '今天的心情是 very happy', 'very_happy', '2024-12-16 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (628, 6, '测试日记245', '今天的心情是 sad', 'sad', '2024-12-15 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (629, 6, '测试日记246', '今天的心情是 neutral', 'neutral', '2024-12-14 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (630, 6, '测试日记247', '今天的心情是 very happy', 'very_happy', '2024-12-13 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (631, 6, '测试日记248', '今天的心情是 happy', 'happy', '2024-12-12 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (632, 6, '测试日记249', '今天的心情是 very sad', 'very_sad', '2024-12-11 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (633, 6, '测试日记250', '今天的心情是 sad', 'sad', '2024-12-10 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (634, 6, '测试日记251', '今天的心情是 sad', 'sad', '2024-12-09 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (635, 6, '测试日记252', '今天的心情是 neutral', 'neutral', '2024-12-08 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (636, 6, '测试日记253', '今天的心情是 sad', 'sad', '2024-12-07 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (637, 6, '测试日记254', '今天的心情是 happy', 'happy', '2024-12-06 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (638, 6, '测试日记255', '今天的心情是 happy', 'happy', '2024-12-05 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (639, 6, '测试日记256', '今天的心情是 happy', 'happy', '2024-12-04 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (640, 6, '测试日记257', '今天的心情是 sad', 'sad', '2024-12-03 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (641, 6, '测试日记258', '今天的心情是 very sad', 'very_sad', '2024-12-02 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (642, 6, '测试日记259', '今天的心情是 happy', 'happy', '2024-12-01 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (643, 6, '测试日记260', '今天的心情是 happy', 'happy', '2024-11-30 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (644, 6, '测试日记261', '今天的心情是 very happy', 'very_happy', '2024-11-29 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (645, 6, '测试日记262', '今天的心情是 sad', 'sad', '2024-11-28 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (646, 6, '测试日记263', '今天的心情是 very sad', 'very_sad', '2024-11-27 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (647, 6, '测试日记264', '今天的心情是 sad', 'sad', '2024-11-26 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (648, 6, '测试日记265', '今天的心情是 very sad', 'very_sad', '2024-11-25 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (649, 6, '测试日记266', '今天的心情是 happy', 'happy', '2024-11-24 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (650, 6, '测试日记267', '今天的心情是 very sad', 'very_sad', '2024-11-23 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (651, 6, '测试日记268', '今天的心情是 very sad', 'very_sad', '2024-11-22 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (652, 6, '测试日记269', '今天的心情是 very happy', 'very_happy', '2024-11-21 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (653, 6, '测试日记270', '今天的心情是 very sad', 'very_sad', '2024-11-20 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (654, 6, '测试日记271', '今天的心情是 very sad', 'very_sad', '2024-11-19 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (655, 6, '测试日记272', '今天的心情是 very happy', 'very_happy', '2024-11-18 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (656, 6, '测试日记273', '今天的心情是 very sad', 'very_sad', '2024-11-17 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (657, 6, '测试日记274', '今天的心情是 happy', 'happy', '2024-11-16 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (658, 6, '测试日记275', '今天的心情是 very sad', 'very_sad', '2024-11-15 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (659, 6, '测试日记276', '今天的心情是 sad', 'sad', '2024-11-14 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (660, 6, '测试日记277', '今天的心情是 neutral', 'neutral', '2024-11-13 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (661, 6, '测试日记278', '今天的心情是 happy', 'happy', '2024-11-12 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (662, 6, '测试日记279', '今天的心情是 neutral', 'neutral', '2024-11-11 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (663, 6, '测试日记280', '今天的心情是 sad', 'sad', '2024-11-10 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (664, 6, '测试日记281', '今天的心情是 sad', 'sad', '2024-11-09 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (665, 6, '测试日记282', '今天的心情是 neutral', 'neutral', '2024-11-08 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (666, 6, '测试日记283', '今天的心情是 sad', 'sad', '2024-11-07 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (667, 6, '测试日记284', '今天的心情是 happy', 'happy', '2024-11-06 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (668, 6, '测试日记285', '今天的心情是 very happy', 'very_happy', '2024-11-05 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (669, 6, '测试日记286', '今天的心情是 very happy', 'very_happy', '2024-11-04 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (670, 6, '测试日记287', '今天的心情是 sad', 'sad', '2024-11-03 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (671, 6, '测试日记288', '今天的心情是 neutral', 'neutral', '2024-11-02 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (672, 6, '测试日记289', '今天的心情是 neutral', 'neutral', '2024-11-01 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (673, 6, '测试日记290', '今天的心情是 neutral', 'neutral', '2024-10-31 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (674, 6, '测试日记291', '今天的心情是 sad', 'sad', '2024-10-30 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (675, 6, '测试日记292', '今天的心情是 neutral', 'neutral', '2024-10-29 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (676, 6, '测试日记293', '今天的心情是 neutral', 'neutral', '2024-10-28 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (677, 6, '测试日记294', '今天的心情是 sad', 'sad', '2024-10-27 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (678, 6, '测试日记295', '今天的心情是 very happy', 'very_happy', '2024-10-26 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (679, 6, '测试日记296', '今天的心情是 sad', 'sad', '2024-10-25 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (680, 6, '测试日记297', '今天的心情是 happy', 'happy', '2024-10-24 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (681, 6, '测试日记298', '今天的心情是 neutral', 'neutral', '2024-10-23 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (682, 6, '测试日记299', '今天的心情是 neutral', 'neutral', '2024-10-22 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (683, 6, '测试日记300', '今天的心情是 sad', 'sad', '2024-10-21 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (684, 6, '测试日记301', '今天的心情是 very happy', 'very_happy', '2024-10-20 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (685, 6, '测试日记302', '今天的心情是 neutral', 'neutral', '2024-10-19 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (686, 6, '测试日记303', '今天的心情是 happy', 'happy', '2024-10-18 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (687, 6, '测试日记304', '今天的心情是 sad', 'sad', '2024-10-17 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (688, 6, '测试日记305', '今天的心情是 neutral', 'neutral', '2024-10-16 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (689, 6, '测试日记306', '今天的心情是 very happy', 'very_happy', '2024-10-15 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (690, 6, '测试日记307', '今天的心情是 very sad', 'very_sad', '2024-10-14 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (691, 6, '测试日记308', '今天的心情是 neutral', 'neutral', '2024-10-13 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (692, 6, '测试日记309', '今天的心情是 very happy', 'very_happy', '2024-10-12 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (693, 6, '测试日记310', '今天的心情是 very sad', 'very_sad', '2024-10-11 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (694, 6, '测试日记311', '今天的心情是 very sad', 'very_sad', '2024-10-10 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (695, 6, '测试日记312', '今天的心情是 very sad', 'very_sad', '2024-10-09 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (696, 6, '测试日记313', '今天的心情是 sad', 'sad', '2024-10-08 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (697, 6, '测试日记314', '今天的心情是 very sad', 'very_sad', '2024-10-07 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (698, 6, '测试日记315', '今天的心情是 happy', 'happy', '2024-10-06 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (699, 6, '测试日记316', '今天的心情是 sad', 'sad', '2024-10-05 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (700, 6, '测试日记317', '今天的心情是 very sad', 'very_sad', '2024-10-04 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (701, 6, '测试日记318', '今天的心情是 sad', 'sad', '2024-10-03 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (702, 6, '测试日记319', '今天的心情是 sad', 'sad', '2024-10-02 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (703, 6, '测试日记320', '今天的心情是 neutral', 'neutral', '2024-10-01 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (704, 6, '测试日记321', '今天的心情是 sad', 'sad', '2024-09-30 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (705, 6, '测试日记322', '今天的心情是 happy', 'happy', '2024-09-29 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (706, 6, '测试日记323', '今天的心情是 very happy', 'very_happy', '2024-09-28 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (707, 6, '测试日记324', '今天的心情是 very happy', 'very_happy', '2024-09-27 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (708, 6, '测试日记325', '今天的心情是 very happy', 'very_happy', '2024-09-26 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (709, 6, '测试日记326', '今天的心情是 happy', 'happy', '2024-09-25 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (710, 6, '测试日记327', '今天的心情是 very happy', 'very_happy', '2024-09-24 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (711, 6, '测试日记328', '今天的心情是 neutral', 'neutral', '2024-09-23 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (712, 6, '测试日记329', '今天的心情是 sad', 'sad', '2024-09-22 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (713, 6, '测试日记330', '今天的心情是 very happy', 'very_happy', '2024-09-21 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (714, 6, '测试日记331', '今天的心情是 neutral', 'neutral', '2024-09-20 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (715, 6, '测试日记332', '今天的心情是 happy', 'happy', '2024-09-19 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (716, 6, '测试日记333', '今天的心情是 sad', 'sad', '2024-09-18 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (717, 6, '测试日记334', '今天的心情是 very sad', 'very_sad', '2024-09-17 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (718, 6, '测试日记335', '今天的心情是 very sad', 'very_sad', '2024-09-16 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (719, 6, '测试日记336', '今天的心情是 sad', 'sad', '2024-09-15 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (720, 6, '测试日记337', '今天的心情是 neutral', 'neutral', '2024-09-14 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (721, 6, '测试日记338', '今天的心情是 neutral', 'neutral', '2024-09-13 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (722, 6, '测试日记339', '今天的心情是 sad', 'sad', '2024-09-12 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (723, 6, '测试日记340', '今天的心情是 very happy', 'very_happy', '2024-09-11 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (724, 6, '测试日记341', '今天的心情是 very happy', 'very_happy', '2024-09-10 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (725, 6, '测试日记342', '今天的心情是 neutral', 'neutral', '2024-09-09 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (726, 6, '测试日记343', '今天的心情是 sad', 'sad', '2024-09-08 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (727, 6, '测试日记344', '今天的心情是 very sad', 'very_sad', '2024-09-07 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (728, 6, '测试日记345', '今天的心情是 very happy', 'very_happy', '2024-09-06 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (729, 6, '测试日记346', '今天的心情是 very happy', 'very_happy', '2024-09-05 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (730, 6, '测试日记347', '今天的心情是 neutral', 'neutral', '2024-09-04 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (731, 6, '测试日记348', '今天的心情是 happy', 'happy', '2024-09-03 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (732, 6, '测试日记349', '今天的心情是 sad', 'sad', '2024-09-02 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (733, 6, '测试日记350', '今天的心情是 very sad', 'very_sad', '2024-09-01 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (734, 6, '测试日记351', '今天的心情是 sad', 'sad', '2024-08-31 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (735, 6, '测试日记352', '今天的心情是 very happy', 'very_happy', '2024-08-30 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (736, 6, '测试日记353', '今天的心情是 happy', 'happy', '2024-08-29 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (737, 6, '测试日记354', '今天的心情是 very happy', 'very_happy', '2024-08-28 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (738, 6, '测试日记355', '今天的心情是 very sad', 'very_sad', '2024-08-27 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (739, 6, '测试日记356', '今天的心情是 neutral', 'neutral', '2024-08-26 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (740, 6, '测试日记357', '今天的心情是 sad', 'sad', '2024-08-25 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (741, 6, '测试日记358', '今天的心情是 neutral', 'neutral', '2024-08-24 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (742, 6, '测试日记359', '今天的心情是 happy', 'happy', '2024-08-23 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (743, 6, '测试日记360', '今天的心情是 happy', 'happy', '2024-08-22 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (744, 6, '测试日记361', '今天的心情是 sad', 'sad', '2024-08-21 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (745, 6, '测试日记362', '今天的心情是 happy', 'happy', '2024-08-20 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (746, 6, '测试日记363', '今天的心情是 sad', 'sad', '2024-08-19 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (747, 6, '测试日记364', '今天的心情是 very happy', 'very_happy', '2024-08-18 18:26:13', '2025-08-16 18:26:39', 1, 0);
INSERT INTO `emotional_diaries` VALUES (748, 6, '测试日记365', '今天的心情是 very happy', 'very_happy', '2024-08-17 18:26:13', '2025-08-16 18:26:39', 1, 0);

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of experience_summaries
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of feedback_images
-- ----------------------------
INSERT INTO `feedback_images` VALUES (1, 1, '/uploads/c0d8e5be-2622-471b-b496-ae2037183e87.png', '2025-08-17 16:05:24');

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of growth_tracks
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of journey_categories
-- ----------------------------
INSERT INTO `journey_categories` VALUES (1, '情感日记', '记录每天的情感变化和感悟', '/static/diary-icon.png', '2025-08-14 16:25:41');
INSERT INTO `journey_categories` VALUES (2, '成长轨迹', '查看你在情感方面的成长变化', '/static/growth-icon.png', '2025-08-14 16:25:41');
INSERT INTO `journey_categories` VALUES (3, '经验总结', '总结从每段感情中获得的经验', '/static/summary-icon.png', '2025-08-14 16:25:41');

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of journey_favorites
-- ----------------------------

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_configs
-- ----------------------------
INSERT INTO `system_configs` VALUES ('ai_model_name', 'gpt-3.5-turbo', '默认AI模型', '2025-08-14 16:26:19');
INSERT INTO `system_configs` VALUES ('app_name', '恋恋有声', '应用名称', '2025-08-14 16:26:19');
INSERT INTO `system_configs` VALUES ('app_version', '1.0.0', '应用版本', '2025-08-14 16:26:19');
INSERT INTO `system_configs` VALUES ('max_chat_history', '50', '最大聊天历史记录数', '2025-08-14 16:26:19');

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_logs
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_feedbacks
-- ----------------------------
INSERT INTO `user_feedbacks` VALUES (1, 6, '速度好慢', '运行好差', NULL, 'pending', '2025-08-17 16:05:24', '2025-08-17 16:05:24');

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_sessions
-- ----------------------------

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
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE,
  INDEX `idx_users_username`(`username` ASC) USING BTREE,
  INDEX `idx_users_email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'root', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', 'admin@example.com', NULL, '管理员', NULL, '2025-08-14 16:26:19', '2025-08-14 16:26:19', NULL, 1);
INSERT INTO `users` VALUES (2, 'testuser', '$2b$12$FYDMwXzKwgleEL8h9e3j4OVB8XoTtgmz0Rtw3/mQSkmqZroLyLkOe', 'test@example.com', NULL, '测试用户', '这是一个测试用户', '2025-08-14 17:21:35', '2025-08-14 17:22:29', '2025-08-14 17:22:29', 1);
INSERT INTO `users` VALUES (3, 'hello', '$2b$12$DdBrrRwq6RNbRHikpHdj5.SYNJ/LFHtPYZacAkFjqUiMNuDK1kH4m', NULL, NULL, NULL, '佩奇', '2025-08-14 17:44:46', '2025-08-14 22:16:16', '2025-08-14 22:16:07', 1);
INSERT INTO `users` VALUES (4, 'pig', '$2b$12$M5CYvMhbaxllGS68J2Fjo.ywj.SQL4HT/H/hnV9SwrQ.P2U4Fh00S', NULL, NULL, NULL, NULL, '2025-08-14 21:41:18', '2025-08-15 17:14:12', '2025-08-15 17:14:12', 1);
INSERT INTO `users` VALUES (5, 'haha', '$2b$12$yXEj18aiN0wZeQBup.CpceiOK5PUh0.xZTRrk758bWdvfxBNufikG', NULL, NULL, NULL, NULL, '2025-08-14 21:41:38', '2025-08-14 21:41:38', NULL, 1);
INSERT INTO `users` VALUES (6, 'peppa', '$2b$12$5h9h9saW.jXFUFob6s5pW.acUzKRSGdJlpEossjY3WMn322eZChiS', NULL, '/uploads/eaed2b4d-e60c-4e84-bfb5-2b9680effcb4.jpg', '小猪', '是佩奇鸭', '2025-08-14 22:29:17', '2025-08-17 16:02:00', '2025-08-17 16:02:00', 1);

SET FOREIGN_KEY_CHECKS = 1;
