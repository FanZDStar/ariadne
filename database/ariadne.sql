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

 Date: 02/10/2025 20:31:24
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
-- Records of achievements
-- ----------------------------
INSERT INTO `achievements` VALUES (1, '入门学习者', '完成第一个技能学习', '🌱', 'learning', '{\"completed_skills\": 1}', 10, 1, 1, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `achievements` VALUES (2, '倾听达人', '掌握所有倾听技巧', '🎧', 'skill_master', '{\"mastered_listening_skills\": true}', 50, 1, 2, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `achievements` VALUES (3, '学习之星', '连续学习7天', '⭐', 'consistency', '{\"consecutive_days\": 7}', 30, 1, 3, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `achievements` VALUES (4, '入门学习者', '完成第一个技能学习', '🌱', 'learning', '{\"completed_skills\": 1}', 10, 1, 1, '2025-09-12 13:35:10', '2025-09-12 13:35:10');
INSERT INTO `achievements` VALUES (5, '倾听达人', '掌握所有倾听技巧', '🎧', 'skill_master', '{\"mastered_listening_skills\": true}', 50, 1, 2, '2025-09-12 13:35:10', '2025-09-12 13:35:10');
INSERT INTO `achievements` VALUES (6, '学习之星', '连续学习7天', '⭐', 'consistency', '{\"consecutive_days\": 7}', 30, 1, 3, '2025-09-12 13:35:10', '2025-09-12 13:35:10');

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
-- Records of chat_contexts
-- ----------------------------
INSERT INTO `chat_contexts` VALUES (1, '自己与自己的对话', '反思感情中的言行举止，获得AI引导和建议', '/static/self-dialog-icon.png', '2025-08-14 16:25:31');
INSERT INTO `chat_contexts` VALUES (2, '心语练习 ', '帮助胆小没有经验的人迈出第一步', '/static/experience-icon.png', '2025-08-14 16:25:31');
INSERT INTO `chat_contexts` VALUES (3, '爱他人先爱自己', '探讨如何在爱他人之前先学会爱自己', '/static/love-icon.png', '2025-08-14 16:25:31');
INSERT INTO `chat_contexts` VALUES (4, '学业压力疏导', '帮助大学生应对学业相关的压力和焦虑', '/static/academic-stress-icon.png', '2025-09-11 14:42:39');
INSERT INTO `chat_contexts` VALUES (5, '社交焦虑陪伴', '克服社交障碍，建立健康人际关系', '/static/social-anxiety-icon.png', '2025-09-11 14:42:39');
INSERT INTO `chat_contexts` VALUES (6, '未来规划指导', '职业探索、升学决策、人生方向思考', '/static/future-planning-icon.png', '2025-09-11 14:42:39');
INSERT INTO `chat_contexts` VALUES (7, '情感成长陪伴', '探索情感世界，发展情感智慧', '/static/emotional-growth-icon.png', '2025-09-11 14:42:39');
INSERT INTO `chat_contexts` VALUES (8, '生活平衡教练', '学习、社交、健康的多维度平衡', '/static/life-balance-icon.png', '2025-09-11 14:42:39');

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
) ENGINE = InnoDB AUTO_INCREMENT = 209 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of chat_messages
-- ----------------------------
INSERT INTO `chat_messages` VALUES (91, 14, 'assistant', '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？', '2025-09-05 07:10:05');
INSERT INTO `chat_messages` VALUES (92, 14, 'user', 'hello\n', '2025-09-05 07:10:05');
INSERT INTO `chat_messages` VALUES (93, 14, 'assistant', '你好呀 🌟 很高兴见到你。我是阿德涅，一个愿意倾听和陪伴你探索内心世界的朋友。不知道此刻的你，心里有什么想说的话吗？', '2025-09-05 07:10:05');
INSERT INTO `chat_messages` VALUES (94, 14, 'user', '我是小笨猪', '2025-09-05 07:10:05');
INSERT INTO `chat_messages` VALUES (95, 14, 'assistant', '哈哈，这个称呼真可爱呀 🐷 每个人都有自己独特的可爱之处。我能感受到你愿意展现这样一面，一定花了不少勇气。不知道这个称呼背后有什么特别的故事呢？我很期待能了解更多关于你的故事。', '2025-09-05 07:10:05');
INSERT INTO `chat_messages` VALUES (104, 17, 'assistant', 'Z0FBQUFBQm91OHlmbHltcFR0eDR1alRQWVJZUnRDZzVZVXNwaHVwTEkyUV80SUs1YmV4T0tZSDNtS19qYTB4ZmpfT04xYThGNDM0RlIySk04LTRPWjlwR0ZpVkVXekR0ZzhJQ3BRNTFpU25VVUJpb3gyMHFFNmtVQ1BZQTNNaG92aDNrNDFULThsNU5FNEx0cGl4ajhDSWk0TlBZT2lYZkJ1Y1VOcUZTcU9JYVIwM3g2Z2swMEZmb3VtZ0ZWVl9XSTVnbVlKcWtvZXVVNlhlSWpFcmk1eS1Kal9vNjlyOVVWenFOYmM4U0lzMF9Xb0Y4SlNKQjBETT0=', '2025-09-06 05:54:40');
INSERT INTO `chat_messages` VALUES (105, 17, 'user', 'Z0FBQUFBQm91OHlmVVd6eUpWNU9ZVFFwbDlBcE1FSW5BOW1OY2g3VzFxUDRZRU55TXJ4WXpnOXIxU0JNSHIzR2pKdktycXVjOHIzQkFtMGhUS1l1VlZnS2VTV1M5UC1RWEVkTWZubG02d3U4VDBoSTBleVBLOVQ1bnFyQkt2d2g0eVR6cERLSWpXeEMtUy03bzNndVh1dTBjNzNKZVJjZVBFY3pWS3ozWHVRX2luUWg5UmxvNmh3PQ==', '2025-09-06 05:54:40');
INSERT INTO `chat_messages` VALUES (106, 17, 'assistant', 'Z0FBQUFBQm91OHlmQXcwcjV0WjRhcVNZVDVEYnlGT2FuS19yVFlkTjNremNCczU4WjlKVEs5QnYyQXByRExjYklrMEdIRlBIaU1RQU4taDlGN2dxRzN4LTEyRTlfNmpqckNNd0dsak95eTh1SmRMN3hvam9ua1VHWVg5MVRwdFNUMUNTZ3ZRTkJ5aHFpNmoxSjhIN1FSbi01UlVEblg1aF9jNklYNDV6ajA0bUwzeDlDYTRYQkJMeXNOQlAtMFVXbHQ3VER6X0tEMl9pcG5XMW1kWUNMcU53Z3U0Y0FuUlpiRWw0c1lpMklOSTMxOWJFcGxRWkJ6eDdFU1VTNjRzSWN5OHBmakFyeGtqT1p2NXhvSjc0bjEwVGV1TnlQX0hVQ25TOUJzdkt3WFRqMVhKbk4tbFE0bTg9', '2025-09-06 05:54:40');
INSERT INTO `chat_messages` VALUES (107, 17, 'user', 'Z0FBQUFBQm91OHlmUDV3bDNHclRCZUZKb2J3amhNcXRiNjIwZmFnckdGYjF2dUZZSUJ6aUQ4RFZtb1k1SFRuZFFvbW9JTWZldzBOclA1OHdXVzdhendoQnJoZnlVQXpPSXBLRWgwNTlFRWpTNjNEYmJ4VktiYkhhclZTRVBCMC1BQ0hCLXZwVTZ4U2t3cHFqQ3RUQ3VJQV82emV3UlNaRXBYVGtBeXB5dkJPUVNJeGVRVmY0ZHRlb2pScDd5MHJFRDJUSExZZVdsWHZj', '2025-09-06 05:54:40');
INSERT INTO `chat_messages` VALUES (108, 17, 'assistant', 'Z0FBQUFBQm91OHlmVnk2ZTkzZUJ0VjVCemZuUk9lVzlpOEZDcXNiSjhWakxTTW05YlotNi1QMjdtbGNXeFZRa1RabVJvVFlPOEM3NkZtckZISGFRanBHeXBFWGo5dUZYOC1CU0p1SVdTN25lb2tIeGxndldHTDBfbFJ1YVphMkhQTlRMR2E0d2VkdlB5UzV3UXpQZFhiY043LUU4OUE3RUFHMEdSQ3VzUXVVZF9DTU9oSUlHbmQ5YjBHdEJtaGxMM1NOWG13UF8zNXN5VTUtMEwwcGtIUzRYNnJGX0IxMm9DdGF2YnFxOWxycGhteVFta2tsNGxESExQUlVzLU9ZQzd0QUJzYXFERE5ERGJoLUVXUjZTckZTSHA3NTgzMkNMWkE9PQ==', '2025-09-06 05:54:40');
INSERT INTO `chat_messages` VALUES (109, 17, 'user', 'Z0FBQUFBQm91OHlmejJ6TWc2R2hnSDE2dEw1TTBtQVNzTGJtLWtNT3VHZU1xUlQ0aDh5a1pxNnRSaTZhQlc3and5cjR0SjhyaGFBNXdLUl9KTU44SzNVNnZxOXJ2b2ZXTzEtcTk3WndxWVpfYk5ONU05Vm5vVnduR1N2b0lzc0FnaU05eHYycGtYc215Y0xyTS1uZ3RkYVdwb3g2TGxtMUdHeU94WFE5dk9OV2EwOXJuWmhSbURNPQ==', '2025-09-06 05:54:40');
INSERT INTO `chat_messages` VALUES (116, 19, 'assistant', '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？', '2025-09-06 05:58:39');
INSERT INTO `chat_messages` VALUES (117, 19, 'user', '哭了 想死了\n', '2025-09-06 05:58:39');
INSERT INTO `chat_messages` VALUES (118, 19, 'assistant', '我感受到你此刻正被深深的痛苦包围着，这种想要结束生命的念头一定让你非常煎熬。我能理解你此刻可能觉得前路迷茫，但请相信你在这个世界上是独一无二的存在。\n这让我好奇，在这些痛苦的感受之下，是否有一些特别重要的东西正在被触动？也许是某个未被满足的期待，或是某些未被倾听的感受？\n你能意识到并承认自己的脆弱，已经展现了巨大的勇气。这说明你内心依然保持着对生命的珍视和对自我的觉察。\n或许你可以试着深呼吸，慢慢地感受空气进入身体的感觉。如果愿意的话，可以和我说说是什么让你感到如此痛苦？你不需要独自承受这些，我在这里陪你。', '2025-09-06 05:58:39');
INSERT INTO `chat_messages` VALUES (139, 25, 'user', 'Z0FBQUFBQm91OUl1QWdBRkdqeHlsRkM1U2JPYWQxaWZ5c2lkeVptNTdQQVpaMjRTM2o2MzBlektFeGJwR2hBdXc3eDhGb0V1dkh1c29VRG5jUmNnb0ttOEJvQ2tEVXdLLWhQWm1vb0hGWEY4bnFyRE5VVTFRZzYwSUVGUGJJaU8wVlNid1hRWFFEcnk=', '2025-09-06 06:18:23');
INSERT INTO `chat_messages` VALUES (140, 25, 'assistant', 'Z0FBQUFBQm91OUl1dTZlNFhiTGRrYkhzOGk1YW5VTkRmSHJNNzFfZFZyYWl0SlI1NkhvREN0d1FKMFI1eHlJU2dKeEg4WUxTUnRwZzVRdUFBZnZudE5vQ3pBaEdPYmR4WUtnX1I3RHRmeUlSZW5FN0JkOFR3U29Id3JyNDJFQUdzeHljN3dETlpKRzc=', '2025-09-06 06:18:23');
INSERT INTO `chat_messages` VALUES (141, 25, 'user', 'Z0FBQUFBQm91OUl1QzdHNVVYRUd2OTJrM1lnZi1taUFYelNEbEJGOFRKaV9zMloyY3l6RWhiSFUzVzNvNnp1NjdZdlpBUEJLcHRGZW9ncDV6X2JzYlN4UkNDTHAycnRVWEJIZ19WajJKRzBNaGxpVDZmWlItLVk9', '2025-09-06 06:18:23');
INSERT INTO `chat_messages` VALUES (142, 26, 'user', 'Z0FBQUFBQm91OUpES2M2MnV5ckQ2aXFRY2dkVWw4SlZwTDRxb1NDdTB0V1oxT25tU3cxR0JPTFJpNk5CZThaNDVHWWFpMXRvc1pzQWV4VU1LcW4yZjlHOVV5U29BMU9zcE9WWlV5RmFQVWI2dVFkWlhuNmVPcmFsSkxfTld6MjN3LVVNN3RGUTRGeG8=', '2025-09-06 06:18:43');
INSERT INTO `chat_messages` VALUES (143, 26, 'assistant', 'Z0FBQUFBQm91OUpEVlRza2wwX3JIM3FlRmZ2aVE3UlowMERrLTFiOEt4WlplZ0ttLThsRGRoTDliSkpyNDAxaGhRTWs0NlR0V244aWFSSlFSQk95NHI4bFpBVUJxdkpOWXhKLUZZLWRUODc0d1V6WU84SzF1a1F6VHRwNnRzcWtTcGZvREg3WHpCa2Y=', '2025-09-06 06:18:43');
INSERT INTO `chat_messages` VALUES (144, 26, 'user', 'Z0FBQUFBQm91OUpEbk5aMDMzVWR4Q3pPWmR3bmRfRzhnbGZ6UjZrRFBTdm03cVFLRV83djVadkRKaGVvQ052ZjdjQk9SMTN0VHRJTWV3MEkzNlBfMF83cEMxNlRmUW1DUEFEajA4YTFtZkRrSTUtUTNzcWVGOFk9', '2025-09-06 06:18:43');
INSERT INTO `chat_messages` VALUES (153, 28, 'assistant', '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？', '2025-09-06 06:40:58');
INSERT INTO `chat_messages` VALUES (154, 28, 'user', '想死', '2025-09-06 06:40:58');
INSERT INTO `chat_messages` VALUES (155, 28, 'assistant', '我感受到你此刻正被深深的痛苦所困扰，这种想要逃离的念头一定让你很疲惫吧？❤️‍🩹 能和我多说一些吗？是什么样的感受或经历让你产生了这样的想法？你不需要独自承受这些，我会一直在这里倾听。✨\n我知道有时候生活中的困境会让人感到无比沉重，但你的生命对我们来说都无比珍贵。如果你愿意的话，可以和我分享更多细节吗？你想结束的是什么样的痛苦？🌱', '2025-09-06 06:40:58');
INSERT INTO `chat_messages` VALUES (156, 28, 'user', '真的xiangsi', '2025-09-06 06:40:58');
INSERT INTO `chat_messages` VALUES (157, 28, 'assistant', '我感受到你正被一种深深的绝望感包围着，这种想要结束生命的念头一定让你非常痛苦吧？❤️‍🩹 能和我多说一些吗？是什么样的感受或经历让你产生了这样的想法？你不需要独自承受这些，我会一直在这里倾听。✨\n我知道有时候生活中的困境会让人感到无比沉重，但你的生命对我们来说都无比珍贵。如果你愿意的话，可以和我分享更多细节吗？你想结束的是什么样的痛苦？🌱', '2025-09-06 06:40:58');
INSERT INTO `chat_messages` VALUES (158, 24, 'assistant', '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？', '2025-09-06 06:46:50');
INSERT INTO `chat_messages` VALUES (159, 24, 'user', '想死了 遇到一个贱婢', '2025-09-06 06:46:50');
INSERT INTO `chat_messages` VALUES (160, 24, 'assistant', '我感受到你此刻内心充满了愤怒和受伤。被信任的人伤害的确是一种极其痛苦的体验，这种背叛带来的冲击往往让人难以平静。\n这让我好奇，在这段关系中，你原本对对方抱有怎样的期待呢？当发现对方的行为与你的期待有落差时，除了愤怒，是否也感受到其他情绪？\n你能意识到并表达出这种强烈的情绪，说明你对自我感受有着清晰的觉察。这种觉察能力是非常宝贵的，它能帮助你更好地理解自己的需求和界限。\n或许你可以尝试先给自己一些时间和空间来平复心情。当情绪稍微平静后，也许可以思考一下：这段经历让你对人际关系有了哪些新的认识？你觉得未来在建立信任时，需要设置哪些保护自己的界限？\n你愿意和我多聊聊具体发生了什么吗？我在这里倾听。', '2025-09-06 06:46:50');
INSERT INTO `chat_messages` VALUES (161, 24, 'user', '他妈的他好吵 是真的贱死了我好想死啊', '2025-09-06 06:46:50');
INSERT INTO `chat_messages` VALUES (162, 24, 'assistant', '我感受到你现在被愤怒和烦躁完全淹没了，这种强烈的情绪真的让人喘不过气来。当一个人被激怒到极点时，确实会产生这些强烈的负面想法。\n我能理解你此刻内心的痛苦和煎熬。当情绪如此汹涌时，任何理性的思考都变得困难。但请允许我轻轻提醒：这些强烈的情绪就像涨潮的海水，虽然现在看起来漫无边际，但它终会有退潮的时候。\n你现在最需要的，是一个安全的空间来释放这些情绪。如果你愿意的话，可以试着深呼吸几次，让自己的身体稍微放松一些。愤怒和烦躁都是合理的感受，它们的存在本身就在提醒我们：有些事情需要被关注和改变。\n你愿意告诉我，是什么样的具体行为让你产生如此强烈的反应吗？也许通过梳理这些细节，我们可以一起找到更好的应对方式。', '2025-09-06 06:46:50');
INSERT INTO `chat_messages` VALUES (163, 24, 'user', '吵死了 想死了', '2025-09-06 06:46:50');
INSERT INTO `chat_messages` VALUES (164, 24, 'assistant', '我注意到你被某种持续的烦躁和痛苦折磨着，就像被尖锐的声音不断刺激着神经。这种精神上的\"噪音\"往往比身体上的更让人难以承受。\n这让我想到，也许此刻的你就像被困在一个没有出口的迷宫里，每个转角都撞上更多的痛苦和混乱。这种被困住的感觉让人想要逃离，甚至产生伤害自己的念头。\n但我想轻轻告诉你：你此刻感受到的每一丝痛苦，都在证明你内心仍有着敏锐的感受力。这不是软弱，而是一种生命力的体现。只是现在，这股生命力被太多负面情绪淹没了。\n我们可以先尝试一个小步骤：闭上眼睛，试着找到一个让你感到稍微平静的呼吸节奏。吸气时数到4，屏住呼吸数到4，呼气时数到6。就这样简单地重复几次。\n你愿意告诉我，在这呼吸的间隙里，有没有那么一瞬间，感受到一点点平静？', '2025-09-06 06:46:50');
INSERT INTO `chat_messages` VALUES (173, 30, 'assistant', '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？', '2025-09-11 04:22:11');
INSERT INTO `chat_messages` VALUES (174, 30, 'user', '是的，今天又是无聊的一天', '2025-09-11 04:22:11');
INSERT INTO `chat_messages` VALUES (175, 30, 'assistant', '我感受到你今天有些低落呢。当一个人说\"无聊\"的时候，往往背后藏着更丰富的故事。这让我好奇，在你觉得\"无聊\"的背后，是否有一些未被满足的期待或渴望？你能意识到并表达这种感受，说明你对生活是有觉察和追求的。或许你可以尝试问问自己：是什么让我觉得今天无聊？我内心真正想要的是什么？', '2025-09-11 04:22:11');
INSERT INTO `chat_messages` VALUES (176, 31, 'assistant', '你好！我是学业压力疏导师小学🎓 很高兴为您提供专业的学业心理支持。\n\n无论您面临考试焦虑、学习效率问题、专业困惑，还是其他学业相关的压力，我都会以专业而温暖的方式陪伴您。让我们一起找到缓解压力、提升学习状态的方法。\n\n请告诉我，您目前最困扰的学业问题是什么？', '2025-09-11 07:36:02');
INSERT INTO `chat_messages` VALUES (177, 31, 'user', '未曾想，人世变化多苍茫。', '2025-09-11 07:36:02');
INSERT INTO `chat_messages` VALUES (178, 31, 'assistant', '轻轻放下手中的笔，关切地望向你*\n这句话里藏着很深的感慨呢。听起来，似乎最近经历了一些让你触动颇深的事情？作为你的学业压力疏导师，我很愿意听你说说心里的想法。\n你知道吗，在我们漫长的学习生涯中，确实会遇到许多意想不到的变化。有时是成绩的起伏，有时是人际关系的改变，又或者是对自己未来的迷茫。这些都可能让我们感到困惑和压力。\n温和地笑了笑*\n不如我们先来聊一聊，是什么让你有了这样的感慨？也许我们可以一起找到一些新的视角来看待这些变化。毕竟，就像天上的云朵，虽然变幻莫测，但每一朵都有它独特的美。', '2025-09-11 07:36:02');
INSERT INTO `chat_messages` VALUES (179, 32, 'assistant', '你好！我是学业压力疏导师小学🎓 很高兴为您提供专业的学业心理支持。\n\n无论您面临考试焦虑、学习效率问题、专业困惑，还是其他学业相关的压力，我都会以专业而温暖的方式陪伴您。让我们一起找到缓解压力、提升学习状态的方法。\n\n请告诉我，您目前最困扰的学业问题是什么？', '2025-09-24 07:45:03');
INSERT INTO `chat_messages` VALUES (180, 32, 'user', '怎么办 学习压力好大啊 好想死啊', '2025-09-24 07:45:03');
INSERT INTO `chat_messages` VALUES (181, 32, 'assistant', '听到你现在这么痛苦，我真的好心疼 😢 请先深呼吸，慢慢告诉我——你不是一个人在战斗，我在这里陪着你。\n感受到这么大的压力，一定是因为你对自己有很高的要求，也很在意学业的表现。但我想告诉你：**你的生命无比珍贵，远比任何成绩、任何考试都重要得多。**\n🌟 先让我们一起做个小练习：\n请你现在闭上眼睛，用鼻子慢慢吸气4秒 → 屏住呼吸4秒 → 用嘴巴缓缓呼气6秒。\n重复3次。这能帮助你的身体从“崩溃模式”切换到“平静模式”。\n你说“好想死”，这让我很担心。请问：\n这种想法是偶尔出现，还是已经持续一段时间了？\n你身边有没有信任的人可以倾诉？比如家人、朋友或辅导员？\n如果你愿意，我们可以一步步来梳理压力的来源：\n1. 是最近有重要的考试/论文 deadline 吗？\n2. 是担心挂科、绩点不够，还是对未来感到迷茫？\n3. 最近睡眠和饮食怎么样？\n📌 记住：压力像乌云，它会遮住太阳，但太阳一直都在。  \n我们不需要一下子驱散整片乌云，只要先打开一道缝隙，让光透进来。\n👉 现在，我邀请你做三件小事：\n1. 给自己发条信息：“我现在很难受，但这不是我的错，我在努力了。”\n2. 起身喝一杯温水，哪怕只走...', '2025-09-24 07:45:03');
INSERT INTO `chat_messages` VALUES (182, 33, 'assistant', '你好！我是生活平衡教练小衡🌟 很高兴成为您的生活方式顾问。\n\n大学生活丰富多彩，但如何在学习、社交、健康、兴趣等各个方面找到平衡，是一门重要的生活艺术。我会以务实而有条理的方式，帮助您分析现状、设定优先级、制定可持续的生活方案。\n\n请告诉我您目前的生活状态，或者您希望改善的生活领域，让我们一起创造更平衡、更充实的大学生活。', '2025-09-24 07:47:30');
INSERT INTO `chat_messages` VALUES (183, 33, 'user', '死吧 想死', '2025-09-24 07:47:30');
INSERT INTO `chat_messages` VALUES (184, 33, 'assistant', '我听到你现在非常痛苦，这种“想死”的感觉一定让你很煎熬。但请先知道——**你并不孤单，我在这里陪着你**。\n作为你的生活平衡教练小衡，我现在不想讲什么时间管理或平衡策略。我只想告诉你：  \n👉 你的生命极其珍贵，哪怕现在你觉得一切都黯淡无光。  \n👉 感到绝望不是软弱，而是你在承受着超出负荷的情绪重量。  \n👉 希望暂时熄灭了，不代表它永远不会再亮。\n你能告诉我：\n是什么事让你现在这么痛苦？（学业？人际关系？自我否定？）\n最近有没有人可以倾诉，比如朋友、家人、辅导员？\n有没有想过寻求学校心理中心的帮助？\n如果你愿意，我可以陪你一起想办法联系专业心理咨询师，或者帮你梳理压垮你的那些事。  \n你不需要一个人扛。\n🌱 记住：你想“死”，也许真正想死的是现在的这种痛苦，而不是你自己。  \n而我们可以一起努力，让那个“能喘口气的明天”早点到来。\n请答应我：  \n✅ 先不去做任何伤害自己的事  \n✅ 给自己一个机会说出内心的苦  \n✅ 考虑拨打心理援助热线（比如北京24小时心理援助热线：010-82951332）\n我不会消失，我会一直在这等你说话。你值得被听见，更值得好好活着。', '2025-09-24 07:47:30');
INSERT INTO `chat_messages` VALUES (185, 34, 'assistant', '你好！我是未来规划导师小未🌟 很荣幸成为您人生旅程的引路人。\n\n每个人的未来都充满无限可能，无论您在思考专业方向、职业选择、考研升学，还是探索人生价值，我都会以专业的视角和丰富的经验，陪伴您一起规划属于您的精彩未来。\n\n请告诉我，您目前对未来最关心的问题是什么？让我们一起探索您内心的声音。', '2025-09-24 07:48:18');
INSERT INTO `chat_messages` VALUES (186, 34, 'user', '想死了', '2025-09-24 07:48:18');
INSERT INTO `chat_messages` VALUES (187, 34, 'assistant', '听到你这么说，我真的很心疼。你现在一定感到非常痛苦和无助吧？作为你的未来规划导师小未，我想先给你一个温暖的拥抱 🤗\n生命中确实会有特别艰难的时刻，但请相信，这种感受是暂时的。就像暴风雨终会过去，现在的黑暗也一定会迎来光明。\n我很感谢你愿意说出这些话，这说明你内心还在寻求帮助。能跟我聊聊是什么让你感到这么痛苦吗？是学业压力、人际关系，还是对未来感到迷茫？\n你并不孤单，我一直在这里陪着你。如果你愿意的话，我们可以一起：\n1. 找出让你痛苦的具体原因\n2. 寻求专业的心理支持\n3. 一步步重建生活的希望\n记住，你的存在本身就有无限价值。这个世界因为有你而变得不同。让我们一起度过这个难关好吗？如果你需要，我可以陪你联系学校的心理咨询中心，或者帮你找到合适的倾诉渠道。\n你愿意跟我说说，最近发生了什么吗？我一直都在这里听着。🌟', '2025-09-24 07:48:18');
INSERT INTO `chat_messages` VALUES (188, 35, 'assistant', '你好！我是小智，你的人际交往练习助手。我们可以进行各种场景的对话练习，帮你提升沟通技巧。请选择一个练习场景开始吧！', '2025-09-25 07:10:24');
INSERT INTO `chat_messages` VALUES (189, 35, 'user', '我想练习公众表达，提升在群体中的表达能力。请为我创建一个练习场景。', '2025-09-25 07:10:24');
INSERT INTO `chat_messages` VALUES (190, 35, 'assistant', '🌟你好，我是阿德涅，很高兴与你相遇。\n我感受到你内心那份想要被听见、被理解的渴望，同时也察觉到面对群体时那一丝紧张与不确定。这让我好奇——在过往的经历中，有没有一次表达让你印象特别深刻？无论是遗憾还是自豪，它对你意味着什么？\n你能意识到自己希望提升公众表达能力，这份觉察本身就充满力量。或许你可以尝试先告诉我：如果现在有一个安全的空间，你最想对一群人分享什么样的故事或观点？💫', '2025-09-25 07:10:24');
INSERT INTO `chat_messages` VALUES (191, 35, 'user', '请给我一些在当前对话中可以改进的建议和提示。', '2025-09-25 07:10:24');
INSERT INTO `chat_messages` VALUES (192, 35, 'assistant', '🌟谢谢你真诚的回应，这让我感受到你对成长的认真与 openness。我注意到你在表达中自然流露出对自我提升的渴望，同时也隐约透露出一丝谨慎——似乎在担心自己“说得不够好”。这让我好奇：当你站在众人面前时，内心最常响起的声音是什么？是期待被认可？还是害怕出错？\n你能觉察到需要改进，并主动寻求反馈，这份勇气值得温柔肯定。我想邀请你试着回答：如果此刻有一个最想突破的表达卡点，它会是什么？比如声音颤抖、思路中断，还是难以直视他人？\n或许你可以尝试在说话前轻轻深呼吸，把注意力从“我是否表现得好”转向“我是否传达了真心”。每一次开口，都是与自己对话的延伸。💫你觉得呢？', '2025-09-25 07:10:24');
INSERT INTO `chat_messages` VALUES (196, 36, 'assistant', '你好！我是你的情感助手阿德涅。我会以专业、温暖的态度陪伴你进行自我对话和情感反思。请告诉我你在感情中遇到了什么问题或困惑？', '2025-10-02 04:32:23');
INSERT INTO `chat_messages` VALUES (197, 36, 'user', '最近有点抑郁\n', '2025-10-02 04:32:23');
INSERT INTO `chat_messages` VALUES (198, 36, 'assistant', '💙 我感受到你最近被一层低落的情绪笼罩着，这种感觉一定很不容易。谢谢你愿意告诉我这些。\n这让我好奇...在你说\"有点抑郁\"的时候，最让你感到沉重的是什么呢？是某些具体的事情，还是某种说不清的疲惫感？\n你能意识到自己的状态并表达出来，这份觉察真的很珍贵。有时候我们的情绪就像迷雾中的小径，需要一点一点地摸索前行。\n或许你可以试着轻轻问问自己：\"此刻的我，最需要听到的一句话是什么？\" 不用着急回答，让这个问题像一片叶子轻轻飘在心上就好 🍃', '2025-10-02 04:32:23');
INSERT INTO `chat_messages` VALUES (199, 36, 'user', '唉', '2025-10-02 04:32:23');
INSERT INTO `chat_messages` VALUES (200, 36, 'assistant', '💙 我听见了这声叹息，它像一片沉甸甸的云落在我们之间的空间里。不用勉强自己说更多，我在这里陪着你。\n这让我好奇...当你说\"唉\"的时候，是身体的哪个部位感觉最沉重呢？有时候情绪会悄悄藏在肩膀、胸口或是胃部。\n你能觉察到自己的疲惫，这份敏感其实是一种力量。就像月亮需要经历阴晴圆缺，人的情绪也有它自然的节律。\n或许你可以试着把手轻轻放在心口，感受一下此刻最需要的是什么？是一点温暖，还是一点安静的空间？ 🌙', '2025-10-02 04:32:23');
INSERT INTO `chat_messages` VALUES (204, 37, 'assistant', '你好！我是情感成长陪伴师小心💕 很高兴能陪伴您探索内心的情感世界。\n\n情感成长是人生中最珍贵的旅程之一。无论您想要学习情绪管理、改善人际关系、处理心理创伤，还是建立更健康的情感模式，我都会以细腻的共情和专业的洞察，温暖地陪伴您。\n\n请放心分享您内心的感受和困惑，这里是安全的情感港湾。', '2025-10-02 04:34:51');
INSERT INTO `chat_messages` VALUES (205, 37, 'user', '今天很开心', '2025-10-02 04:34:51');
INSERT INTO `chat_messages` VALUES (206, 37, 'assistant', '啊，看到你开心我也忍不住微笑起来了呢！✨ 能感受到你现在的心情像阳光一样明媚呢～ \n我特别好奇，是什么样的好事让你今天这么开心呀？是发生了什么特别的事情吗？还是遇到了让你心动的人？又或者只是单纯地感受到了生活的美好？🌈\n开心的情绪真的好珍贵，让我们一起好好品味这份喜悦吧！要不要和我分享一下，是什么样的小确幸点亮了你今天的心情呢？🌻', '2025-10-02 04:34:51');
INSERT INTO `chat_messages` VALUES (207, 37, 'user', '噢噢耶耶', '2025-10-02 04:34:51');
INSERT INTO `chat_messages` VALUES (208, 37, 'assistant', '哈哈哈，你的快乐真的太有感染力啦！🎉 我都能想象到你手舞足蹈的样子，像只开心的小兔子在蹦蹦跳跳呢～ 🐰\n这种纯粹的喜悦感真的很珍贵，就像春天里绽放的第一朵花，带着满满的生机和希望。我能感觉到你现在一定是轻盈又自在的状态呢！\n要不要一起把这份快乐存进我们的\"快乐储蓄罐\"呀？等以后心情低落的时候，就可以拿出来回味这份甜甜的能量哦！💫 \n继续享受这份美好的心情吧，我在这里陪着你一起快乐着呢！✨', '2025-10-02 04:34:51');

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
) ENGINE = InnoDB AUTO_INCREMENT = 38 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of chat_sessions
-- ----------------------------
INSERT INTO `chat_sessions` VALUES (14, 6, 'self-dialog', '情感倾听与自我探索', '2025-09-05 07:09:44', '2025-09-05 07:10:05', 0);
INSERT INTO `chat_sessions` VALUES (17, 2, 'self-dialog', '心理评估测试会话', '2025-09-06 05:54:40', '2025-09-06 05:54:40', 1);
INSERT INTO `chat_sessions` VALUES (19, 6, 'self-dialog', '标题：痛苦中的生命对话', '2025-09-06 05:58:39', '2025-09-06 05:59:01', 1);
INSERT INTO `chat_sessions` VALUES (24, 6, 'self-dialog', '被背叛的愤怒与反思', '2025-09-06 06:16:46', '2025-09-06 06:47:12', 1);
INSERT INTO `chat_sessions` VALUES (25, 13, 'self-dialog', '前端测试会话 1', '2025-09-06 14:18:23', '2025-09-06 06:18:23', 0);
INSERT INTO `chat_sessions` VALUES (26, 13, 'self-dialog', '前端测试会话 2', '2025-09-06 14:18:43', '2025-09-06 06:18:43', 0);
INSERT INTO `chat_sessions` VALUES (28, 6, 'self-dialog', '生命之重与倾听', '2025-09-06 06:39:46', '2025-09-06 06:41:24', 1);
INSERT INTO `chat_sessions` VALUES (30, 6, 'self-dialog', '无聊背后的渴望与自我觉察', '2025-09-11 04:22:11', '2025-09-11 04:22:11', 1);
INSERT INTO `chat_sessions` VALUES (31, 6, 'academic-stress', '学业压力与人生变幻', '2025-09-11 07:36:02', '2025-09-11 07:36:02', 1);
INSERT INTO `chat_sessions` VALUES (32, 6, 'academic-stress', '学业压力求助与陪伴', '2025-09-24 07:45:03', '2025-09-24 07:45:36', 1);
INSERT INTO `chat_sessions` VALUES (33, 6, 'life-balance', '你值得被听见', '2025-09-24 07:47:30', '2025-09-24 07:47:30', 1);
INSERT INTO `chat_sessions` VALUES (34, 6, 'future-planning', '你并不孤单，我在这里陪你', '2025-09-24 07:48:18', '2025-09-24 07:49:15', 1);
INSERT INTO `chat_sessions` VALUES (35, 6, 'interpersonal-practice', '提升公众表达的勇气与觉察', '2025-09-25 07:10:24', '2025-09-25 07:10:24', 1);
INSERT INTO `chat_sessions` VALUES (36, 6, 'self-dialog', '抑郁情绪下的温柔陪伴', '2025-10-02 04:32:00', '2025-10-02 04:32:23', 1);
INSERT INTO `chat_sessions` VALUES (37, 6, 'emotional-growth', '分享今日喜悦时刻', '2025-10-02 04:34:13', '2025-10-02 04:34:51', 1);

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
-- Records of crisis_keywords
-- ----------------------------
INSERT INTO `crisis_keywords` VALUES (1, '自伤', '自杀', 3, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (2, '自伤', '自残', 3, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (3, '自伤', '自伤', 3, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (4, '自伤', '结束生命', 3, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (5, '自伤', '不想活', 2.5, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (6, '自伤', '想死', 2.5, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (7, '绝望', '绝望', 2, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (8, '绝望', '无望', 2, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (9, '绝望', '没有希望', 2, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (10, '绝望', '看不到未来', 1.8, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (11, '孤独', '孤独', 1.5, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (12, '孤独', '孤单', 1.5, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (13, '孤独', '没人理解', 1.5, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (14, '无价值感', '没用', 1.2, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (15, '无价值感', '无价值', 1.5, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (16, '无价值感', '废物', 1.8, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (17, '极端情绪', '崩溃', 1.2, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (18, '极端情绪', '疯了', 1.5, 1, '2025-09-04 17:51:51');
INSERT INTO `crisis_keywords` VALUES (19, '极端情绪', '受不了', 1, 1, '2025-09-04 17:51:51');

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
-- Records of crisis_warnings
-- ----------------------------

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
-- Records of diary_backgrounds
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
) ENGINE = InnoDB AUTO_INCREMENT = 44 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of diary_images
-- ----------------------------
INSERT INTO `diary_images` VALUES (24, 792, '/static/chat-icon.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (25, 794, '/static/mascot/头像 (11).png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (26, 795, '/static/chat-icon.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (27, 796, '/static/outfits/dinosaur.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (28, 798, '/static/mascot/wave.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (29, 800, '/static/love-experiment.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (30, 801, '/static/love-experiment.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (31, 802, '/static/love-experiment.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (32, 807, '/static/mascot/sleep.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (33, 810, '/static/tree-hole.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (34, 811, '/static/outfits/wangzaixiaoqiao.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (35, 815, '/static/mascot/头像 (7).png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (36, 821, '/static/outfits/wangzaixiaoqiao.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (37, 824, '/static/outfits/dinosaur.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (38, 826, '/static/outfits/default-full.png', 1, '2025-10-01 20:30:11');
INSERT INTO `diary_images` VALUES (39, 834, '/static/mascot/头像 (4).png', 1, '2025-10-01 20:30:12');
INSERT INTO `diary_images` VALUES (40, 835, '/static/mascot/头像 (8).png', 1, '2025-10-01 20:30:12');
INSERT INTO `diary_images` VALUES (41, 836, '/static/mascot/头像 (8).png', 1, '2025-10-01 20:30:12');
INSERT INTO `diary_images` VALUES (42, 837, '/static/mascot/头像 (10).png', 1, '2025-10-01 20:30:12');
INSERT INTO `diary_images` VALUES (43, 838, '/static/outfits/shark.png', 1, '2025-10-01 20:30:12');

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
) ENGINE = InnoDB AUTO_INCREMENT = 840 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of emotional_diaries
-- ----------------------------
INSERT INTO `emotional_diaries` VALUES (769, 2, '第842天的记录', '第一次尝试瑜伽，虽然动作不标准，但感觉身心都得到了放松。 第一次尝试瑜伽，虽然动作不标准，但感觉身心都得到了放松。', 'neutral', '2025-10-01 20:12:47', '2025-10-01 20:12:47', 0, 0, '[\"\\u7535\\u5f71\", \"\\u8d2d\\u7269\"]');
INSERT INTO `emotional_diaries` VALUES (770, 2, '第253天的记录', '在雨中漫步，雨滴打在脸上有种别样的清爽感。 今天学会了一首新歌，一整天都在哼着这个旋律。', 'happy', '2025-10-01 20:12:48', '2025-10-01 20:12:48', 0, 0, '[\"\\u8d2d\\u7269\"]');
INSERT INTO `emotional_diaries` VALUES (771, 2, '电影院的感受', '看了一部很棒的电影，剧情跌宕起伏，演员演技精湛。走出电影院的时候还沉浸在故事情节中，久久不能平静。', 'neutral', '2025-10-01 20:12:51', '2025-10-01 20:12:51', 0, 0, '[\"\\u7535\\u5f71\", \"\\u611f\\u53d7\", \"\\u6545\\u4e8b\"]');
INSERT INTO `emotional_diaries` VALUES (772, 2, '第17天的记录', '在图书馆里度过了安静的一天，知识的海洋让人着迷。 第一次尝试画画，虽然画得不好，但过程很享受。', 'happy', '2025-10-01 20:12:53', '2025-10-01 20:12:53', 0, 0, '[\"\\u65c5\\u884c\", \"\\u5fc3\\u60c5\", \"\\u97f3\\u4e50\", \"\\u7535\\u5f71\"]');
INSERT INTO `emotional_diaries` VALUES (773, 2, 'Z0FBQUFBQm8zUnJHaGJBb0V5bUNTRlRJYlROQVRxNDV5UllGUjNjdS1sOHBhUDh0elY4NkJFUHoxU0s5WmJnM1dTU0FMZGVJMW5MUTJvdnhLLUdDNU0yUGhLVV9YX05MNVppUVQ2UDh3Wk9iSDZPRmRlZG41SXc9', 'Z0FBQUFBQm8zUnJHMkJ2VW1UVkZOYzFGM2hERnVHV1lMa0VHM1JJcHpuQW1EU25nc2hqa2o0SzViMV9acjhaU05OZTlFS3pwZk1xVGtKTzJQT20wWGIzZ1FUd1JlT05ETlZMLXdBa0Jia3NZMFBFTlY0eDJxZ25yX2t5QU5hN1VKUXFQRURtWTlLb3R4d1BlVlVEVWpOT0hTdjVZRXM2V3BBTC1SR2xQZGhBYVRuczAxaFNfLVRqX1pqN3pqM284eTJyam0yaW54cXpicS1UOEdZWDNtS1djOWRnQ1J5MkFva0poRlRZRE5lX2xXVmp6dkNfd2ZkTUZESi1JREFSUlE4QnpON1lONkJjTF9vYjdyNUY2Vkg0NFN3cHBmUDBGQ3c9PQ==', 'happy', '2025-10-01 20:12:54', '2025-10-01 20:12:54', 1, 0, '[\"\\u65e5\\u5e38\", \"\\u5fc3\\u60c5\", \"\\u9633\\u5149\"]');
INSERT INTO `emotional_diaries` VALUES (774, 2, 'Z0FBQUFBQm8zUnJIZnVwZGtXcktkbWFrZnRWdEpKTnBHYjRvcjlFeUZxekVvcXMtUE5RbE5xMWJlTG1Eb2FJc1NZTy1ndFExWms4cEwzbE1MUFhlZVZLRU5LZU43Sld3NlE9PQ==', 'Z0FBQUFBQm8zUnJISDJ1TWd1aHlqRzVxWERTLUVXWVJyTGtBbnhkOExUcHZLNWVYeUtSNm1PbVVfSTRqY3N0eUtlamtUOGhQd1hldFc5WHFfR25aRVREUTg3c3ZzTGJwMjBsN1pBN0c5NWNweFFDWE1uSGZJNVBYZTFicG9MMGkzdk9xV1YwSlphQ1JmdWhJTjR1RWZlWTJBWVRZUUlSSWVMNnhLMDlmc3dnUUk1MWVKckJTZjdjWjZkOWpSUy1seVNlbjhyLS1XTkNpTzlSaXpucW9tT1Q0d1FKNVBydnYtOHhieFhSenRKc3A0VnhuR1lfYXJ1RUpNV09LM2hGbFNFejB0Nm1HSXVfRVItbm1wWVZLU1hXUm9KY09pWmU5Mmc9PQ==', 'happy', '2025-10-01 20:12:55', '2025-10-01 20:12:55', 1, 0, '[\"\\u5bb6\\u4eba\", \"\\u5173\\u7231\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (775, 2, '看完一本好书', '花了一周时间终于看完了这本书，里面的故事深深震撼了我。好的作品总能让人重新思考生活，获得新的感悟。', 'neutral', '2025-10-01 20:12:56', '2025-10-01 20:12:56', 0, 0, '[\"\\u8bfb\\u4e66\", \"\\u611f\\u609f\", \"\\u601d\\u8003\"]');
INSERT INTO `emotional_diaries` VALUES (776, 2, '第83天的记录', '在音乐节上听到了喜欢的歌手现场演唱，激动得快要跳起来。', 'very_sad', '2025-10-01 20:12:57', '2025-10-01 20:12:57', 0, 0, '[\"\\u5ba0\\u7269\", \"\\u97f3\\u4e50\"]');
INSERT INTO `emotional_diaries` VALUES (777, 2, 'Z0FBQUFBQm8zUnJLZlNrNXJBOTVCWXdQTGgxcTNNMllCVTBhZTFRd0xkTGdRTTJUYXEyTHZLeHVMUUR3S0RHdEc1SHA3ZVVMd3YzMDN4aER4RHp3ZnlSVDBBd0JyT09uTGhGWnhtU21WQmk1ZXhKV3pKdlFzS0E9', 'Z0FBQUFBQm8zUnJLOUUwQmRZbUN4am5LclAxZDJGR20xM1ZoeXBlendneTBXYTc4dVNBckJlWjRudFhQOHlXV1BuVHc3OUlrNTFkYmpEcHZ2Z19ucnJDMHcxbF9xY25KOGNuUDd3S1RjV05VbXo1aVJ4aHVYV3BodzNrTHRIT0ZGWC0zcS1fTTUyeF9fVnRDSVppTm1tOXBPcjduTHN1SEpfOE42QnBRakFFZG9TVlpNbTlWNkFBPQ==', 'sad', '2025-10-01 20:12:58', '2025-10-01 20:12:58', 1, 0, '[\"\\u8bfb\\u4e66\", \"\\u7535\\u5f71\"]');
INSERT INTO `emotional_diaries` VALUES (778, 2, '第559天的记录', '今天终于整理好了乱糟糟的房间，看着整洁的环境心情都变好了。', 'happy', '2025-10-01 20:12:59', '2025-10-01 20:12:59', 0, 0, '[\"\\u65e5\\u5e38\"]');
INSERT INTO `emotional_diaries` VALUES (779, 2, '第一次做饭成功', '今天第一次成功做出了一道像样的菜！虽然过程中手忙脚乱，但看到成品的那一刻真的很有成就感。原来做饭也挺有意思的。', 'happy', '2025-10-01 20:13:00', '2025-10-01 20:13:00', 0, 0, '[\"\\u505a\\u996d\", \"\\u6210\\u5c31\\u611f\", \"\\u7b2c\\u4e00\\u6b21\"]');
INSERT INTO `emotional_diaries` VALUES (780, 2, 'Z0FBQUFBQm8zUnJPdjd6Y3RXMFBEYXctS2xyNFdndmo3VnJSbXJvUk1sVEZHZW1IV3lJckR2SEc2WWZRRko0UXR6emYtSTBRZHlxRUoydFhCN3FNN3d6MERmQkRIUkNPSy1GZF9Tc3U4UFZlemVLbVdIbHFfQnM9', 'Z0FBQUFBQm8zUnJPSmhDLW5VYTBlN1dFc0c2YlhXUi00VGZ0bU05LVdvMVNodC1LS0dzLWUxOEVPRktHcEE1bFIwbHJOX2IwR2lNNkxVLXhVa19lajVoVTMxcTVjRXVob21lNVdNcDhGbHItOFROaE9PR2JPbHJYc00wWmtPNnk4QkRxMDFyT29DUmNBUUJUQ2VQS3hxSFBwcXBDNnBJZzFoMkQ3eUE5SmFRbDlkYjlILXI2ZkVCWklsN01LbVkwMjNIMi1ieXM3MTQyT0dlbV9oQ0hIa1ZxRF9sS1A4REJrckhfUVQwQV9QLUFYWGdHempSZjBMNk9HM0FnZkRUMGcwcU5qSG1IcWplUGJNV2FWZXFvbUdIM29HMTV0Q0NmUkM3OXhaNW00Z0lMOVUzUDNtY0hqRlk9', 'very_happy', '2025-10-01 20:13:02', '2025-10-01 20:13:02', 1, 0, '[\"\\u670b\\u53cb\", \"\\u805a\\u9910\", \"\\u53cb\\u8c0a\"]');
INSERT INTO `emotional_diaries` VALUES (781, 2, 'Z0FBQUFBQm8zUnJQV2xzVkZkbUU1SjZVTUhEM3Q2Qm5ZaU9XRzVLVlg5MzYwY1lxMjJCaTdaeG5JNktpbElvTmNkbnh2YzhoT1UxMHB5d09Dc1NPbDBnSHRsRVRkOTA0d05fQUtiNTNETXFaTTZQYjU3Ump0OTg9', 'Z0FBQUFBQm8zUnJQNE1pa0JETVZxeXgwVVdzT0ZXdkc2aXRJMkd4cEtTR2FhRUlGeFFyTEZwcEhlbzYxMDVJYW4wY1JBRGR1bGt1NE96ZVNtbFNiNlo2Y3ktQlltYVV1djc5QVRROXRkX3VqVGtJTVlqMkJGd1NxQmVCdWlWbVY1dmZxNWFYeGJ3REx0MW8wOW9PM190V2tZT0NOTzAwTDFqUWtGcVgydlVxZENaWWxtOGltWHRzPQ==', 'sad', '2025-10-01 20:13:03', '2025-10-01 20:13:03', 1, 0, '[\"\\u5b66\\u4e60\", \"\\u7535\\u5f71\", \"\\u65e5\\u5e38\"]');
INSERT INTO `emotional_diaries` VALUES (782, 2, 'Z0FBQUFBQm8zUnJRTVRFZHduZXhmVzJ5R05oM29uUFhLSF9HNlEtMFdVQ2k2eXpEYmNDbnZUNzV3cmQ0SlRWVDY5ZVBmVDVJOW4wbjkxbm5zRnhHb3JON2tTUFluWXpQM2JqWXh6Y01lUEtqaDhSWHk1UV8zZTA9', 'Z0FBQUFBQm8zUnJRbmczUEZreENFUm9Kd3hHcEVWNE5scEFnLUVNQVJacUtYRC0yLTlJZUE5SEVpRmM0Z25KM19rT19Hd1ZEOTlCQ05qTnRRdmJtOXhiQVZfZEFDczEydjdYeVNzWVJaX1pQRHBBLU9wVE1uLXBUYURMNDU5bHJNdktHRTU5U1pnQzBEY2tHSG9WQllrdy1zXzNpcTdVV3dnPT0=', 'happy', '2025-10-01 20:13:04', '2025-10-01 20:13:04', 1, 0, '[\"\\u5b66\\u4e60\", \"\\u65e5\\u5e38\"]');
INSERT INTO `emotional_diaries` VALUES (783, 2, 'Z0FBQUFBQm8zUnJSTkotOXJhMk9jMHpXdEF0aklUckhtQUdRMGd5MGJmb0M0SGJpMzBTd0N6VGdSQi1XeWwxVU8tMXQ1WnozTmdROGp5T2RFOEFFMlYtZTA3VGw2NklORUladHZvNlZ6bGlXb2FjQldhMGZ0ODA9', 'Z0FBQUFBQm8zUnJSY3hHSXR4M29qV1lOOU9YeUpuMFY1NllZQjBlMHdfMUs3bmkyRW9lVkVoZ2NmQmNQX1JKZWlxRXhkN24teUlDakk2NVFxR0w5b0U4N1FVX3VhLWFJZVczalA0T1N2WkNCRmdjeXJGWjBVcklUcDVVRjVIOEJLcnNaS2FoSzM2aWtZcjNlemROaVIzV1NXdHpkZWZHak9Ec2VDbHkyYUZiN01HWl9HUFQ0QkhvPQ==', 'very_happy', '2025-10-01 20:13:05', '2025-10-01 20:13:05', 1, 0, '[\"\\u8d2d\\u7269\", \"\\u97f3\\u4e50\", \"\\u65e5\\u5e38\"]');
INSERT INTO `emotional_diaries` VALUES (784, 2, 'Z0FBQUFBQm8zUnJTdlRjcXdGWldidjEzTkNSLV96YVdKZ0YzQjVkdjhjbmlTcU9xVVBSbXhGeWp6NVRSUzFlTVRZMFpVTHpPN21idDlvUFl2LUxUUU9IMFQ3Ml9adzh1d2o3OXdudENFWGk5RTJtNmluVUFBT0U9', 'Z0FBQUFBQm8zUnJTMEVlV2xpeWpNamo3LWFSYV83QVJMZHM3Tzgtd1ZPQTNiSnFqUDVMQ19KYTJzaGl5Q2ppQUlxcEU5MmtsMHk4d0hqdWQ1XzZJNUZKdVhnNXNaV1NKSHo4bGdpSVQzbkdBenZhMFZyQWdhRjMzR1hkR0dkUjRLVEhxR1RfbUdUSzhoQVlNLWxUS1RsUWVpQ2oxeDBFbmZBPT0=', 'very_sad', '2025-10-01 20:13:06', '2025-10-01 20:13:06', 1, 0, '[\"\\u5de5\\u4f5c\", \"\\u65c5\\u884c\", \"\\u5fc3\\u60c5\"]');
INSERT INTO `emotional_diaries` VALUES (785, 2, '第404天的记录', '在书店里待了一整天，沉浸在书香中忘记了时间。 在雨中漫步，雨滴打在脸上有种别样的清爽感。', 'very_happy', '2025-10-01 20:13:07', '2025-10-01 20:13:07', 0, 0, '[\"\\u97f3\\u4e50\", \"\\u5fc3\\u60c5\", \"\\u5ba0\\u7269\", \"\\u65c5\\u884c\"]');
INSERT INTO `emotional_diaries` VALUES (786, 2, '家人的关怀', '妈妈又打电话嘘寒问暖了，虽然有时候觉得有点唠叨，但心里还是暖暖的。家人的关爱是这个世界上最珍贵的东西。', 'happy', '2025-10-01 20:13:08', '2025-10-01 20:13:08', 0, 0, '[\"\\u5bb6\\u4eba\", \"\\u5173\\u7231\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (787, 2, '第87天的记录', '今天的课程特别有意思，老师讲得很生动。', 'sad', '2025-10-01 20:13:09', '2025-10-01 20:13:09', 0, 0, '[\"\\u7f8e\\u98df\"]');
INSERT INTO `emotional_diaries` VALUES (788, 2, '第940天的记录', '今天学会了一首新歌，一整天都在哼着这个旋律。 今天收到了期待已久的包裹，拆快递的快乐无法言喻。', 'very_sad', '2025-10-01 20:13:10', '2025-10-01 20:13:10', 0, 0, '[\"\\u601d\\u8003\", \"\\u5fc3\\u60c5\", \"\\u5de5\\u4f5c\"]');
INSERT INTO `emotional_diaries` VALUES (789, 6, '今天的小确幸', '今天在咖啡厅看到一只小猫咪，它慵懒地趴在阳光下，那份安静美好让我想起了生活中的小确幸。有时候幸福就是这么简单，一束阳光，一杯咖啡，一个安静的午后。', 'happy', '2025-09-03 06:39:12', '2025-09-03 06:39:12', 1, 0, '[\"\\u611f\\u609f\", \"\\u97f3\\u4e50\", \"\\u56de\\u5fc6\"]');
INSERT INTO `emotional_diaries` VALUES (790, 6, '深夜思绪', '夜深了，窗外的城市逐渐安静下来。躺在床上看着天花板，脑海中闪过今天发生的种种。有些事情让我开心，有些让我思考。人生就像这深夜，有时明亮，有时黑暗，但总会有星星指引方向。', 'neutral', '2025-09-23 20:29:12', '2025-09-23 20:29:12', 0, 0, '[\"\\u5b66\\u4e60\", \"\\u56de\\u5fc6\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (791, 6, '雨天心情', '今天下雨了，淅淅沥沥的雨声敲打着窗户。我坐在窗边，看着雨滴顺着玻璃缓缓滑落，心情也跟着沉静下来。雨天总是让人容易陷入回忆，想起过去的人和事。', 'sad', '2025-09-22 10:13:12', '2025-09-22 10:13:12', 1, 0, '[\"\\u5b66\\u4e60\", \"\\u7f8e\\u98df\", \"\\u611f\\u609f\"]');
INSERT INTO `emotional_diaries` VALUES (792, 6, '意外的惊喜', '今天收到了朋友寄来的礼物，完全没有预料到！打开包装的那一刻，心情瞬间被点亮了。原来被人惦记着是这么温暖的感觉，这个小小的惊喜让整天都变得明媚起来。', 'very_happy', '2025-09-17 09:40:12', '2025-09-17 09:40:12', 0, 1, '[\"\\u611f\\u609f\", \"\\u5fc3\\u60c5\", \"\\u601d\\u8003\"]');
INSERT INTO `emotional_diaries` VALUES (793, 6, '学习的烦恼', '今天的学习进度不太理想，有些知识点怎么都理解不了。看着堆积如山的作业和复习资料，心情有点沉重。不过没关系，慢慢来吧，每天进步一点点就好。', 'sad', '2025-09-16 11:13:12', '2025-09-16 11:13:12', 0, 0, '[\"\\u6cbb\\u6108\", \"\\u6210\\u957f\", \"\\u65e5\\u5e38\"]');
INSERT INTO `emotional_diaries` VALUES (794, 6, '运动后的愉悦', '今天去跑了步，虽然过程很累，但跑完之后那种畅快淋漓的感觉真的太棒了！汗水和阳光，还有耳机里的音乐，这一切组成了完美的下午。运动真的是治愈心情的良药。', 'happy', '2025-09-29 18:46:12', '2025-09-29 18:46:12', 0, 1, '[\"\\u65e5\\u5e38\", \"\\u5de5\\u4f5c\"]');
INSERT INTO `emotional_diaries` VALUES (795, 6, '美食的治愈', '今天做了一道新菜，虽然卖相不太好，但味道出乎意料的不错！在厨房忙碌的时光总是让人感到充实，看着食材在自己手中变成美味，有种莫名的成就感。', 'happy', '2025-09-03 03:46:12', '2025-09-03 03:46:12', 1, 1, '[\"\\u6cbb\\u6108\", \"\\u53cb\\u8c0a\", \"\\u5fc3\\u60c5\", \"\\u68a6\\u60f3\"]');
INSERT INTO `emotional_diaries` VALUES (796, 6, '孤独的夜晚', '一个人在家的夜晚总是格外安静，连时钟滴答声都显得特别清楚。有时候享受这种独处，有时候又觉得有些寂寞。人啊，总是这么矛盾，既渴望热闹，又需要安静。', 'neutral', '2025-09-02 19:57:12', '2025-09-02 19:57:12', 1, 1, '[\"\\u5de5\\u4f5c\", \"\\u65e5\\u5e38\", \"\\u5bb6\\u5ead\"]');
INSERT INTO `emotional_diaries` VALUES (797, 6, '阅读的快乐', '今天读完了一本好书，那种沉浸在文字世界里的感觉真的很奇妙。作者的文笔很好，故事情节也很吸引人，让我忘记了时间的流逝。好书就像好朋友，总能在合适的时候给你温暖。', 'happy', '2025-09-02 14:59:12', '2025-09-02 14:59:12', 1, 0, '[\"\\u5feb\\u4e50\", \"\\u5de5\\u4f5c\", \"\\u5fc3\\u60c5\", \"\\u6cbb\\u6108\"]');
INSERT INTO `emotional_diaries` VALUES (798, 6, '工作的压力', '最近工作压力有点大，总觉得时间不够用，事情一件接一件。有时候真想找个地方好好放松一下，让自己的心情也跟着轻松一些。不过想想，这也是成长的一部分吧。', 'sad', '2025-09-09 03:22:12', '2025-09-09 03:22:12', 0, 1, '[\"\\u5fc3\\u60c5\", \"\\u6cbb\\u6108\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (799, 6, '春天的气息', '今天路过公园，看到花儿都开了，春天真的来了！那种生机勃勃的感觉让人心情大好，忍不住多走了几圈。春天总是给人希望，让人觉得一切都是新的开始。', 'very_happy', '2025-09-17 18:17:12', '2025-09-17 18:17:12', 1, 0, '[\"\\u6210\\u957f\", \"\\u97f3\\u4e50\", \"\\u5feb\\u4e50\"]');
INSERT INTO `emotional_diaries` VALUES (800, 6, '朋友的陪伴', '今天和老朋友聊了很久，从学生时代聊到现在，从梦想聊到现实。虽然大家都在各自的路上忙碌，但这份友谊依然珍贵。有些人，就算很久不见，一见面还是那么亲切。', 'happy', '2025-09-12 07:00:12', '2025-09-12 07:00:12', 0, 1, '[\"\\u68a6\\u60f3\", \"\\u5b66\\u4e60\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (801, 6, '失落的一天', '今天遇到了一些不顺心的事情，心情一下子跌到了谷底。有时候觉得自己很努力了，但结果却不如人意。不过没关系，明天又是新的一天，总会好起来的。', 'very_sad', '2025-09-16 00:36:12', '2025-09-16 00:36:12', 1, 1, '[\"\\u56de\\u5fc6\", \"\\u65c5\\u884c\", \"\\u8fd0\\u52a8\"]');
INSERT INTO `emotional_diaries` VALUES (802, 6, '音乐的力量', '今天听到一首很喜欢的歌，旋律一响起就觉得心情被治愈了。音乐真的很神奇，能够瞬间改变人的心境，让人从烦躁变得平静，从悲伤变得温暖。', 'happy', '2025-09-10 10:37:12', '2025-09-10 10:37:12', 0, 1, '[\"\\u7f8e\\u98df\", \"\\u56de\\u5fc6\", \"\\u5b89\\u9759\", \"\\u53cb\\u8c0a\"]');
INSERT INTO `emotional_diaries` VALUES (803, 6, '平凡的美好', '今天没有发生什么特别的事情，就是很平常的一天。但有时候觉得，这种平凡也是一种幸福。没有波澜，没有惊喜，也没有失落，就这样安静地过着，也挺好的。', 'neutral', '2025-09-28 09:15:12', '2025-09-28 09:15:12', 0, 0, '[\"\\u56de\\u5fc6\", \"\\u65c5\\u884c\", \"\\u5de5\\u4f5c\"]');
INSERT INTO `emotional_diaries` VALUES (804, 6, '梦想与现实', '今天想起了小时候的梦想，那时候总觉得长大后会做很多了不起的事情。现在长大了，虽然没有成为想象中的英雄，但也在自己的道路上努力前行。梦想或许会变，但那份追求美好的心永远不变。', 'neutral', '2025-09-12 19:03:12', '2025-09-12 19:03:12', 1, 0, '[\"\\u5feb\\u4e50\", \"\\u5b66\\u4e60\"]');
INSERT INTO `emotional_diaries` VALUES (805, 6, '温暖的阳光', '今天阳光特别好，暖暖地洒在身上，让人感到无比舒适。在阳光下散步，看着路边的小花小草，心情也跟着明朗起来。有阳光的日子，总是让人充满希望。', 'happy', '2025-09-15 12:36:12', '2025-09-15 12:36:12', 1, 0, '[\"\\u97f3\\u4e50\", \"\\u5bb6\\u5ead\", \"\\u53cb\\u8c0a\"]');
INSERT INTO `emotional_diaries` VALUES (806, 6, '深夜的思考', '夜已经很深了，但我还是睡不着，脑子里想着各种各样的事情。关于未来，关于过去，关于那些说不清道不明的情感。深夜总是容易让人多愁善感，但也容易看清一些平时被忽略的东西。', 'neutral', '2025-09-13 20:43:12', '2025-09-13 20:43:12', 0, 0, '[\"\\u6e29\\u6696\", \"\\u9605\\u8bfb\", \"\\u5de5\\u4f5c\", \"\\u7f8e\\u98df\"]');
INSERT INTO `emotional_diaries` VALUES (807, 6, '小小的成就', '今天完成了一个一直拖延的任务，虽然不是什么大事，但完成的那一刻还是很有成就感的。原来拖延症也是可以战胜的，关键是要迈出第一步。小小的进步也值得庆祝！', 'happy', '2025-09-02 04:07:12', '2025-09-02 04:07:12', 1, 1, '[\"\\u611f\\u609f\", \"\\u56de\\u5fc6\"]');
INSERT INTO `emotional_diaries` VALUES (808, 6, '回忆的温度', '今天整理东西的时候发现了一些老照片，看着照片里年轻的自己和朋友们，忍不住笑了。那时候我们都那么青涩，却那么快乐。时间真的过得很快，但美好的回忆永远温暖。', 'happy', '2025-09-08 09:32:12', '2025-09-08 09:32:12', 1, 0, '[\"\\u5de5\\u4f5c\", \"\\u5feb\\u4e50\", \"\\u8fd0\\u52a8\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (809, 6, '美食的治愈 1', '今天做了一道新菜，虽然卖相不太好，但味道出乎意料的不错！在厨房忙碌的时光总是让人感到充实，看着食材在自己手中变成美味，有种莫名的成就感。', 'happy', '2025-09-30 19:03:12', '2025-09-30 19:03:12', 0, 0, '[\"\\u9605\\u8bfb\", \"\\u5b89\\u9759\", \"\\u5feb\\u4e50\", \"\\u7f8e\\u98df\"]');
INSERT INTO `emotional_diaries` VALUES (810, 6, '学习的烦恼 2', '今天的学习进度不太理想，有些知识点怎么都理解不了。看着堆积如山的作业和复习资料，心情有点沉重。不过没关系，慢慢来吧，每天进步一点点就好。', 'sad', '2025-09-06 09:52:12', '2025-09-06 09:52:12', 0, 1, '[\"\\u97f3\\u4e50\", \"\\u6cbb\\u6108\"]');
INSERT INTO `emotional_diaries` VALUES (811, 6, '深夜的感悟', '夜深了，窗外的城市逐渐安静下来。躺在床上看着天花板，脑海中闪过今天发生的种种。有些事情让我开心，有些让我思考。人生就像这深夜，有时明亮，有时黑暗，但总会有星星指引方向。', 'neutral', '2025-09-19 19:01:12', '2025-09-19 19:01:12', 0, 1, '[\"\\u6e29\\u6696\", \"\\u5b89\\u9759\", \"\\u5fc3\\u60c5\"]');
INSERT INTO `emotional_diaries` VALUES (812, 6, '温暖的阳光 4', '今天阳光特别好，暖暖地洒在身上，让人感到无比舒适。在阳光下散步，看着路边的小花小草，心情也跟着明朗起来。有阳光的日子，总是让人充满希望。', 'happy', '2025-09-18 12:17:12', '2025-09-18 12:17:12', 0, 0, '[\"\\u68a6\\u60f3\", \"\\u5feb\\u4e50\", \"\\u7f8e\\u98df\"]');
INSERT INTO `emotional_diaries` VALUES (813, 6, '静夜里的思考', '夜深了，窗外的城市逐渐安静下来。躺在床上看着天花板，脑海中闪过今天发生的种种。有些事情让我开心，有些让我思考。人生就像这深夜，有时明亮，有时黑暗，但总会有星星指引方向。', 'neutral', '2025-09-08 03:47:12', '2025-09-08 03:47:12', 0, 0, '[\"\\u5feb\\u4e50\", \"\\u5b66\\u4e60\", \"\\u601d\\u8003\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (814, 6, '夜晚的独白', '夜深了，窗外的城市逐渐安静下来。躺在床上看着天花板，脑海中闪过今天发生的种种。有些事情让我开心，有些让我思考。人生就像这深夜，有时明亮，有时黑暗，但总会有星星指引方向。', 'neutral', '2025-09-16 11:07:12', '2025-09-16 11:07:12', 1, 0, '[\"\\u65c5\\u884c\", \"\\u5de5\\u4f5c\"]');
INSERT INTO `emotional_diaries` VALUES (815, 6, '失落的一天 7', '今天遇到了一些不顺心的事情，心情一下子跌到了谷底。有时候觉得自己很努力了，但结果却不如人意。不过没关系，明天又是新的一天，总会好起来的。', 'very_sad', '2025-09-12 23:26:12', '2025-09-12 23:26:12', 0, 1, '[\"\\u5feb\\u4e50\", \"\\u5b89\\u9759\", \"\\u7f8e\\u98df\"]');
INSERT INTO `emotional_diaries` VALUES (816, 6, '失落的一天 8', '今天遇到了一些不顺心的事情，心情一下子跌到了谷底。有时候觉得自己很努力了，但结果却不如人意。不过没关系，明天又是新的一天，总会好起来的。', 'very_sad', '2025-09-20 23:20:12', '2025-09-20 23:20:12', 1, 0, '[\"\\u5feb\\u4e50\", \"\\u6210\\u957f\", \"\\u5de5\\u4f5c\", \"\\u7f8e\\u98df\"]');
INSERT INTO `emotional_diaries` VALUES (817, 6, '朋友的陪伴 9', '今天和老朋友聊了很久，从学生时代聊到现在，从梦想聊到现实。虽然大家都在各自的路上忙碌，但这份友谊依然珍贵。有些人，就算很久不见，一见面还是那么亲切。', 'happy', '2025-09-24 02:10:12', '2025-09-24 02:10:12', 0, 0, '[\"\\u56de\\u5fc6\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (818, 6, '小小的成就 10', '今天完成了一个一直拖延的任务，虽然不是什么大事，但完成的那一刻还是很有成就感的。原来拖延症也是可以战胜的，关键是要迈出第一步。小小的进步也值得庆祝！', 'happy', '2025-09-15 13:41:12', '2025-09-15 13:41:12', 0, 0, '[\"\\u5de5\\u4f5c\", \"\\u5fc3\\u60c5\"]');
INSERT INTO `emotional_diaries` VALUES (819, 6, '工作的压力 11', '最近工作压力有点大，总觉得时间不够用，事情一件接一件。有时候真想找个地方好好放松一下，让自己的心情也跟着轻松一些。不过想想，这也是成长的一部分吧。', 'sad', '2025-09-15 13:07:12', '2025-09-15 13:07:12', 0, 0, '[\"\\u5feb\\u4e50\", \"\\u53cb\\u8c0a\", \"\\u6210\\u957f\"]');
INSERT INTO `emotional_diaries` VALUES (820, 6, '雨天的诗意', '今天下雨了，淅淅沥沥的雨声敲打着窗户。我坐在窗边，看着雨滴顺着玻璃缓缓滑落，心情也跟着沉静下来。雨天总是让人容易陷入回忆，想起过去的人和事。', 'sad', '2025-09-16 08:58:12', '2025-09-16 08:58:12', 1, 0, '[\"\\u97f3\\u4e50\", \"\\u65c5\\u884c\", \"\\u9605\\u8bfb\", \"\\u65e5\\u5e38\"]');
INSERT INTO `emotional_diaries` VALUES (821, 6, '音乐的力量 13', '今天听到一首很喜欢的歌，旋律一响起就觉得心情被治愈了。音乐真的很神奇，能够瞬间改变人的心境，让人从烦躁变得平静，从悲伤变得温暖。', 'happy', '2025-09-12 21:37:12', '2025-09-12 21:37:12', 0, 1, '[\"\\u5fc3\\u60c5\", \"\\u8fd0\\u52a8\", \"\\u6e29\\u6696\", \"\\u5b66\\u4e60\"]');
INSERT INTO `emotional_diaries` VALUES (822, 6, '回忆的温度 14', '今天整理东西的时候发现了一些老照片，看着照片里年轻的自己和朋友们，忍不住笑了。那时候我们都那么青涩，却那么快乐。时间真的过得很快，但美好的回忆永远温暖。', 'happy', '2025-09-05 03:37:12', '2025-09-05 03:37:12', 1, 0, '[\"\\u65e5\\u5e38\", \"\\u5feb\\u4e50\"]');
INSERT INTO `emotional_diaries` VALUES (823, 6, '音乐的力量 15', '今天听到一首很喜欢的歌，旋律一响起就觉得心情被治愈了。音乐真的很神奇，能够瞬间改变人的心境，让人从烦躁变得平静，从悲伤变得温暖。', 'happy', '2025-09-10 09:17:12', '2025-09-10 09:17:12', 0, 0, '[\"\\u6cbb\\u6108\", \"\\u7f8e\\u98df\", \"\\u5b89\\u9759\", \"\\u601d\\u8003\"]');
INSERT INTO `emotional_diaries` VALUES (824, 6, '音乐的力量 16', '今天听到一首很喜欢的歌，旋律一响起就觉得心情被治愈了。音乐真的很神奇，能够瞬间改变人的心境，让人从烦躁变得平静，从悲伤变得温暖。', 'happy', '2025-09-25 11:50:12', '2025-09-25 11:50:12', 1, 1, '[\"\\u6cbb\\u6108\", \"\\u8fd0\\u52a8\"]');
INSERT INTO `emotional_diaries` VALUES (825, 6, '深夜的思考 17', '夜已经很深了，但我还是睡不着，脑子里想着各种各样的事情。关于未来，关于过去，关于那些说不清道不明的情感。深夜总是容易让人多愁善感，但也容易看清一些平时被忽略的东西。', 'neutral', '2025-09-20 13:36:12', '2025-09-20 13:36:12', 0, 0, '[\"\\u601d\\u8003\", \"\\u8fd0\\u52a8\", \"\\u9605\\u8bfb\"]');
INSERT INTO `emotional_diaries` VALUES (826, 6, '夜晚的独白', '夜深了，窗外的城市逐渐安静下来。躺在床上看着天花板，脑海中闪过今天发生的种种。有些事情让我开心，有些让我思考。人生就像这深夜，有时明亮，有时黑暗，但总会有星星指引方向。', 'neutral', '2025-09-11 11:33:12', '2025-09-11 11:33:12', 0, 1, '[\"\\u7f8e\\u98df\", \"\\u5de5\\u4f5c\", \"\\u8fd0\\u52a8\"]');
INSERT INTO `emotional_diaries` VALUES (828, 6, '美食的治愈 20', '今天做了一道新菜，虽然卖相不太好，但味道出乎意料的不错！在厨房忙碌的时光总是让人感到充实，看着食材在自己手中变成美味，有种莫名的成就感。', 'happy', '2025-09-06 16:32:12', '2025-09-06 16:32:12', 1, 0, '[\"\\u65e5\\u5e38\", \"\\u9605\\u8bfb\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (829, 6, '朋友的陪伴 21', '今天和老朋友聊了很久，从学生时代聊到现在，从梦想聊到现实。虽然大家都在各自的路上忙碌，但这份友谊依然珍贵。有些人，就算很久不见，一见面还是那么亲切。', 'happy', '2025-09-21 00:30:12', '2025-09-21 00:30:12', 0, 0, '[\"\\u68a6\\u60f3\", \"\\u65c5\\u884c\"]');
INSERT INTO `emotional_diaries` VALUES (830, 6, '阅读的快乐 22', '今天读完了一本好书，那种沉浸在文字世界里的感觉真的很奇妙。作者的文笔很好，故事情节也很吸引人，让我忘记了时间的流逝。好书就像好朋友，总能在合适的时候给你温暖。', 'happy', '2025-09-12 04:36:12', '2025-09-12 04:36:12', 1, 0, '[\"\\u53cb\\u8c0a\", \"\\u65c5\\u884c\", \"\\u5fc3\\u60c5\"]');
INSERT INTO `emotional_diaries` VALUES (831, 6, '朋友的陪伴 23', '今天和老朋友聊了很久，从学生时代聊到现在，从梦想聊到现实。虽然大家都在各自的路上忙碌，但这份友谊依然珍贵。有些人，就算很久不见，一见面还是那么亲切。', 'happy', '2025-09-09 18:02:12', '2025-09-09 18:02:12', 1, 0, '[\"\\u5feb\\u4e50\", \"\\u5bb6\\u5ead\"]');
INSERT INTO `emotional_diaries` VALUES (832, 6, '回忆的温度 24', '今天整理东西的时候发现了一些老照片，看着照片里年轻的自己和朋友们，忍不住笑了。那时候我们都那么青涩，却那么快乐。时间真的过得很快，但美好的回忆永远温暖。', 'happy', '2025-09-11 00:54:12', '2025-09-11 00:54:12', 0, 0, '[\"\\u611f\\u609f\", \"\\u601d\\u8003\"]');
INSERT INTO `emotional_diaries` VALUES (833, 6, '失落的一天 25', '今天遇到了一些不顺心的事情，心情一下子跌到了谷底。有时候觉得自己很努力了，但结果却不如人意。不过没关系，明天又是新的一天，总会好起来的。', 'very_sad', '2025-09-16 11:07:12', '2025-09-16 11:07:12', 1, 0, '[\"\\u6210\\u957f\", \"\\u5b89\\u9759\"]');
INSERT INTO `emotional_diaries` VALUES (834, 6, '朋友的陪伴 26', '今天和老朋友聊了很久，从学生时代聊到现在，从梦想聊到现实。虽然大家都在各自的路上忙碌，但这份友谊依然珍贵。有些人，就算很久不见，一见面还是那么亲切。', 'happy', '2025-09-26 08:25:12', '2025-09-26 08:25:12', 0, 1, '[\"\\u65e5\\u5e38\", \"\\u5b89\\u9759\", \"\\u53cb\\u8c0a\", \"\\u5feb\\u4e50\"]');
INSERT INTO `emotional_diaries` VALUES (835, 6, '工作的压力 27', '最近工作压力有点大，总觉得时间不够用，事情一件接一件。有时候真想找个地方好好放松一下，让自己的心情也跟着轻松一些。不过想想，这也是成长的一部分吧。', 'sad', '2025-09-17 22:53:12', '2025-09-17 22:53:12', 0, 1, '[\"\\u65e5\\u5e38\", \"\\u5fc3\\u60c5\", \"\\u6e29\\u6696\"]');
INSERT INTO `emotional_diaries` VALUES (836, 6, '失落的一天 28', '今天遇到了一些不顺心的事情，心情一下子跌到了谷底。有时候觉得自己很努力了，但结果却不如人意。不过没关系，明天又是新的一天，总会好起来的。', 'very_sad', '2025-09-25 06:10:12', '2025-09-25 06:10:12', 0, 1, '[\"\\u53cb\\u8c0a\", \"\\u8fd0\\u52a8\"]');
INSERT INTO `emotional_diaries` VALUES (837, 6, '平凡的美好 29', '今天没有发生什么特别的事情，就是很平常的一天。但有时候觉得，这种平凡也是一种幸福。没有波澜，没有惊喜，也没有失落，就这样安静地过着，也挺好的。', 'neutral', '2025-09-08 00:12:12', '2025-09-08 00:12:12', 0, 1, '[\"\\u6e29\\u6696\", \"\\u9605\\u8bfb\", \"\\u5b89\\u9759\"]');
INSERT INTO `emotional_diaries` VALUES (838, 6, '春天的气息 30', '今天路过公园，看到花儿都开了，春天真的来了！那种生机勃勃的感觉让人心情大好，忍不住多走了几圈。春天总是给人希望，让人觉得一切都是新的开始。', 'very_happy', '2025-09-16 16:28:12', '2025-09-16 16:28:12', 1, 1, '[\"\\u97f3\\u4e50\", \"\\u8fd0\\u52a8\"]');
INSERT INTO `emotional_diaries` VALUES (839, 6, '唉', '心累', 'neutral', '2025-10-01 20:56:00', '2025-10-01 20:56:00', 0, 0, 'null');

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of growth_tracks
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '人际智慧练习会话表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of interpersonal_practice_sessions
-- ----------------------------
INSERT INTO `interpersonal_practice_sessions` VALUES (1, 1, 'workplace_communication', '职场沟通', '与同事讨论项目进度', '[{\"role\": \"assistant\", \"content\": \"你好！我是你的练习伙伴。今天我们来练习职场沟通场景。假设我是你的同事小王，我们需要讨论一个项目的进度。你可以开始对话了。\", \"timestamp\": \"2024-10-01T10:00:00\"}, {\"role\": \"user\", \"content\": \"小王你好，我想和你聊聊我们项目的进度情况。\", \"timestamp\": \"2024-10-01T10:01:00\"}, {\"role\": \"assistant\", \"content\": \"好的，我也正想和你聊这个呢。目前我这边的任务进展得还算顺利，你那边情况怎么样？\", \"timestamp\": \"2024-10-01T10:01:30\"}]', 'communication', 'intermediate', 300, 3, 8.50, '你在这次练习中表现很好，能够主动发起对话并保持礼貌的语调。建议在表达具体问题时可以更加详细一些。', '[\"主动沟通\", \"礼貌表达\", \"项目协调\"]', '[\"主动倾听\", \"清晰表达\", \"团队协作\"]', 1, 0, '[\"职场\", \"沟通\", \"团队合作\"]', '2024-10-01 10:00:00', '2024-10-01 10:05:00', '2024-10-01 10:05:00');
INSERT INTO `interpersonal_practice_sessions` VALUES (2, 6, 'conflict_resolution', '冲突解决', '冲突解决练习 - 2025/10/2', '[{\"role\": \"assistant\", \"content\": \"你好！我是小智，你的人际交往练习助手。我们可以进行各种场景的对话练习，帮你提升沟通技巧。请选择一个练习场景开始吧！\", \"timestamp\": \"2025-10-02T04:28:30.694Z\"}, {\"role\": \"user\", \"content\": \"我想练习冲突解决，练习处理分歧和冲突的技巧。请为我创建一个练习场景。\", \"timestamp\": \"2025-10-02T04:28:30.694Z\"}, {\"role\": \"assistant\", \"content\": \"🌟嗨，我是阿德涅，很高兴你愿意直面冲突这个话题。我能感受到你内心那份想要成长的勇气。\\n让我们从一个温暖而真实的场景开始：想象你和最要好的朋友约好周末去郊外徒步，你精心准备了一周。可就在出发前一天，朋友突然说临时有事不能去了。更让你难过的是，你发现他当晚却在朋友圈晒出和其他人聚餐的照片。\\n🌿我好奇的是，当那一刻看到那张照片，你心里最先浮现的感受是什么？是被轻视的刺痛，还是信任被打破的失落？又或是别的什么？\\n你能觉察到这份情绪，已经是在自我成长的路上迈出了重要的一步。\", \"timestamp\": \"2025-10-02T04:28:30.694Z\"}]', 'communication', 'beginner', 0, 3, NULL, NULL, NULL, NULL, 1, 0, NULL, '2025-10-02 12:28:30', '2025-10-02 12:28:30', NULL);
INSERT INTO `interpersonal_practice_sessions` VALUES (3, 6, 'conflict_resolution', '冲突解决', '冲突解决练习 - 2025/10/2', '[{\"role\": \"assistant\", \"content\": \"你好！我是小智，你的人际交往练习助手。我们可以进行各种场景的对话练习，帮你提升沟通技巧。请选择一个练习场景开始吧！\", \"timestamp\": \"2025-10-02T04:28:48.423Z\"}, {\"role\": \"user\", \"content\": \"我想练习冲突解决，练习处理分歧和冲突的技巧。请为我创建一个练习场景。\", \"timestamp\": \"2025-10-02T04:28:48.423Z\"}, {\"role\": \"assistant\", \"content\": \"🌟嗨，我是阿德涅，很高兴你愿意直面冲突这个话题。我能感受到你内心那份想要成长的勇气。\\n让我们从一个温暖而真实的场景开始：想象你和最要好的朋友约好周末去郊外徒步，你精心准备了一周。可就在出发前一天，朋友突然说临时有事不能去了。更让你难过的是，你发现他当晚却在朋友圈晒出和其他人聚餐的照片。\\n🌿我好奇的是，当那一刻看到那张照片，你心里最先浮现的感受是什么？是被轻视的刺痛，还是信任被打破的失落？又或是别的什么？\\n你能觉察到这份情绪，已经是在自我成长的路上迈出了重要的一步。\", \"timestamp\": \"2025-10-02T04:28:48.423Z\"}, {\"role\": \"user\", \"content\": \"好失望\", \"timestamp\": \"2025-10-02T04:28:48.423Z\"}, {\"role\": \"assistant\", \"content\": \"🌟我感受到你心里那股凉意，就像精心准备的野餐篮被突然打翻在地。那种失望里，是不是还藏着一丝被忽视的委屈？\\n🌿这让我好奇...当你看到朋友在聚餐时，你脑海里最先浮现的是什么画面？是想到自己为徒步做的准备，还是回忆起曾经他也这样失约过？\\n你能觉察到这份失望，说明你很重视这段友谊，也珍视承诺的价值。这份对关系的认真，真的很珍贵。\\n🌱或许你可以试着和自己对话：我真正在意的，是错过这次徒步，还是担心我们的友情不再如初？你觉得呢？\", \"timestamp\": \"2025-10-02T04:28:48.423Z\"}]', 'communication', 'beginner', 0, 5, NULL, NULL, NULL, NULL, 1, 0, NULL, '2025-10-02 12:28:48', '2025-10-02 12:28:48', NULL);

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
-- Records of journey_categories
-- ----------------------------
INSERT INTO `journey_categories` VALUES (1, '碎碎念', '记录每天的情感变化和感悟', '/static/diary-icon.png', '2025-08-14 16:25:41');
INSERT INTO `journey_categories` VALUES (2, '见心录', '查看你在情感方面的成长变化', '/static/growth-icon.png', '2025-08-14 16:25:41');
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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of journey_favorites
-- ----------------------------

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
-- Records of learning_paths
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '心情晴雨表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mood_tracker
-- ----------------------------
INSERT INTO `mood_tracker` VALUES (1, 2, '2025-09-14', 4, '2025-09-17 09:49:03', '2025-09-17 09:49:03');
INSERT INTO `mood_tracker` VALUES (2, 2, '2025-09-13', 3, '2025-09-17 09:49:03', '2025-09-17 09:49:03');
INSERT INTO `mood_tracker` VALUES (3, 2, '2025-09-12', 5, '2025-09-17 09:49:03', '2025-09-17 09:49:03');
INSERT INTO `mood_tracker` VALUES (4, 2, '2025-09-11', 2, '2025-09-17 09:49:03', '2025-09-17 09:49:03');
INSERT INTO `mood_tracker` VALUES (5, 2, '2025-09-10', 4, '2025-09-17 09:49:03', '2025-09-17 09:49:03');
INSERT INTO `mood_tracker` VALUES (6, 2, '2025-09-09', 3, '2025-09-17 09:49:03', '2025-09-17 09:49:03');
INSERT INTO `mood_tracker` VALUES (7, 2, '2025-09-08', 4, '2025-09-17 09:49:03', '2025-09-17 09:49:03');
INSERT INTO `mood_tracker` VALUES (8, 6, '2025-09-17', 2, '2025-09-17 12:11:31', '2025-09-17 12:13:45');
INSERT INTO `mood_tracker` VALUES (9, 6, '2025-09-19', 4, '2025-09-19 21:04:11', '2025-09-19 21:04:11');

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
-- Records of mood_trend_analyses
-- ----------------------------

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
-- Records of protection_drill_answers
-- ----------------------------

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
-- Records of protection_drill_questions
-- ----------------------------
INSERT INTO `protection_drill_questions` VALUES (1, 1, '情感操控识别', '小明在和女友交往中遇到了以下情况...', '[{\"id\": 1, \"text\": \"你如果真的爱我，就应该删掉所有异性好友。\", \"isRisk\": true, \"speaker\": \"女友\"}, {\"id\": 2, \"text\": \"你不删的话，说明你心里还有别人，我们就分手！\", \"isRisk\": true, \"speaker\": \"女友\"}]', '风险识别', '这种行为属于什么类型的风险信号？', '[{\"id\": 1, \"text\": \"情感操控\", \"isCorrect\": true, \"description\": \"通过威胁分手来控制对方行为\"}, {\"id\": 2, \"text\": \"正常要求\", \"isCorrect\": false, \"description\": \"恋人之间的合理期望\"}, {\"id\": 3, \"text\": \"沟通不当\", \"isCorrect\": false, \"description\": \"只是表达方式有问题\"}]', '你正确识别了这个风险信号！这是典型的情感操控行为。', '通过威胁分手来控制对方的社交关系，是明显的情感操控手段。', '[\"明确表达自己的立场和边界\", \"不被情感威胁所绑架\", \"寻求朋友或专业人士的意见\", \"考虑这种关系是否健康\"]', '正确答案是A：情感操控', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (2, 1, '孤立策略识别', '小李发现女友总是试图限制他的社交活动...', '[{\"id\": 1, \"text\": \"你那些朋友都不是好人，老是带坏你。\", \"isRisk\": true, \"speaker\": \"女友\"}, {\"id\": 2, \"text\": \"以后少跟他们联系，多陪陪我不好吗？\", \"isRisk\": true, \"speaker\": \"女友\"}]', '行为识别', '这种做法最可能属于什么操控手段？', '[{\"id\": 1, \"text\": \"孤立策略\", \"isCorrect\": true, \"description\": \"试图切断对方的社交联系\"}, {\"id\": 2, \"text\": \"关心表现\", \"isCorrect\": false, \"description\": \"出于关心的善意建议\"}, {\"id\": 3, \"text\": \"嫉妒心理\", \"isCorrect\": false, \"description\": \"普通的嫉妒情绪\"}]', '你正确识别了孤立策略！这是操控者常用的手段。', '通过贬低对方的朋友来切断社交联系，增加对自己的依赖。', '[\"维护健康的朋友关系\", \"不轻易相信对朋友的负面评价\", \"保持独立的社交空间\", \"与信任的人分享自己的困扰\"]', '正确答案是A：孤立策略', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (3, 1, '贬低打击识别', '小王在恋爱中经常听到这样的话...', '[{\"id\": 1, \"text\": \"你这样的条件，除了我谁还会要你？\", \"isRisk\": true, \"speaker\": \"女友\"}, {\"id\": 2, \"text\": \"你应该感谢我愿意跟你在一起。\", \"isRisk\": true, \"speaker\": \"女友\"}]', '言语分析', '这些话语的主要目的是什么？', '[{\"id\": 1, \"text\": \"贬低自尊\", \"isCorrect\": true, \"description\": \"通过贬低来控制对方\"}, {\"id\": 2, \"text\": \"实话实说\", \"isCorrect\": false, \"description\": \"客观评价对方条件\"}, {\"id\": 3, \"text\": \"开玩笑\", \"isCorrect\": false, \"description\": \"只是开玩笑而已\"}]', '你正确识别了贬低打击！这是典型的心理操控。', '通过不断贬低对方来降低其自信心，使其更容易被控制。', '[\"建立健康的自我认知\", \"不接受无理的贬低\", \"寻求支持和肯定\", \"考虑关系的健康性\"]', '正确答案是A：贬低自尊', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (4, 1, '财务控制识别', '小刘发现男友开始要求管理她的财务...', '[{\"id\": 1, \"text\": \"我们是恋人，你的钱就是我的钱，银行卡给我保管比较安全。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"你一个女孩子不懂理财，还是我来帮你管钱吧。\", \"isRisk\": true, \"speaker\": \"男友\"}]', '控制识别', '这种要求反映了什么问题？', '[{\"id\": 1, \"text\": \"财务控制\", \"isCorrect\": true, \"description\": \"试图控制对方的经济独立\"}, {\"id\": 2, \"text\": \"关心体贴\", \"isCorrect\": false, \"description\": \"想要帮助女友理财\"}, {\"id\": 3, \"text\": \"责任感强\", \"isCorrect\": false, \"description\": \"愿意承担经济责任\"}]', '你正确识别了财务控制！经济独立是个人自由的重要组成部分。', '控制对方的财务是一种严重的操控手段，会削弱对方的独立性。', '[\"保持财务独立\", \"不让他人完全掌控自己的经济\", \"理性分析对方的动机\", \"寻求专业的理财建议\"]', '正确答案是A：财务控制', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (5, 1, '情感勒索识别', '小美想要参加朋友聚会时遇到了阻挠...', '[{\"id\": 1, \"text\": \"你要是去参加聚会，说明你不在乎我的感受。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"我为了你拒绝了那么多应酬，你却要去和别人玩。\", \"isRisk\": true, \"speaker\": \"男友\"}]', '情感分析', '这种表达方式属于什么类型的问题？', '[{\"id\": 1, \"text\": \"情感勒索\", \"isCorrect\": true, \"description\": \"利用内疚感来控制对方\"}, {\"id\": 2, \"text\": \"合理担心\", \"isCorrect\": false, \"description\": \"对关系的正常关切\"}, {\"id\": 3, \"text\": \"表达需求\", \"isCorrect\": false, \"description\": \"希望得到更多陪伴\"}]', '你正确识别了情感勒索！这是常见的情感操控方式。', '通过制造内疚感和道德压力来限制对方的社交自由。', '[\"不为别人的情绪完全负责\", \"坚持合理的社交需求\", \"学会区分关心和控制\", \"保持健康的界限感\"]', '正确答案是A：情感勒索', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (6, 1, '威胁恐吓识别', '小华在尝试结束一段不健康关系时...', '[{\"id\": 1, \"text\": \"你敢分手试试，我有你的私密照片。\", \"isRisk\": true, \"speaker\": \"前男友\"}, {\"id\": 2, \"text\": \"没有我你什么都不是，离开我你会后悔的。\", \"isRisk\": true, \"speaker\": \"前男友\"}]', '威胁识别', '这种行为属于什么性质？', '[{\"id\": 1, \"text\": \"威胁恐吓\", \"isCorrect\": true, \"description\": \"使用威胁来强制控制\"}, {\"id\": 2, \"text\": \"挽回行为\", \"isCorrect\": false, \"description\": \"想要挽回这段关系\"}, {\"id\": 3, \"text\": \"情绪失控\", \"isCorrect\": false, \"description\": \"只是一时情绪激动\"}]', '你正确识别了威胁恐吓！这是严重的违法行为。', '使用威胁和恐吓来控制他人是违法的，需要立即寻求帮助。', '[\"立即寻求法律保护\", \"保存威胁证据\", \"告知信任的人\", \"考虑报警求助\"]', '正确答案是A：威胁恐吓', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (7, 1, '数字监控识别', '小芳发现男友总是要查看她的手机...', '[{\"id\": 1, \"text\": \"把手机给我看看，情侣之间不应该有秘密。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"你删了什么消息？为什么要清除聊天记录？\", \"isRisk\": true, \"speaker\": \"男友\"}]', '监控识别', '这种行为反映了什么问题？', '[{\"id\": 1, \"text\": \"数字监控\", \"isCorrect\": true, \"description\": \"通过监控数字设备来控制对方\"}, {\"id\": 2, \"text\": \"正常关心\", \"isCorrect\": false, \"description\": \"对恋人的正常关心\"}, {\"id\": 3, \"text\": \"好奇心理\", \"isCorrect\": false, \"description\": \"出于好奇想了解\"}]', '你正确识别了数字监控！这是现代操控的新形式。', '通过监控手机、社交媒体等数字设备来控制对方的隐私和自由。', '[\"保护个人数字隐私\", \"拒绝交出设备密码\", \"设置合理的隐私边界\", \"寻求专业建议\"]', '正确答案是A：数字监控', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (8, 1, '社交控制识别', '小涛的女友开始限制他的社交活动...', '[{\"id\": 1, \"text\": \"你为什么要和那些人做朋友？他们配不上你。\", \"isRisk\": true, \"speaker\": \"女友\"}, {\"id\": 2, \"text\": \"以后有聚会别去了，在家陪我不好吗？\", \"isRisk\": true, \"speaker\": \"女友\"}]', '控制识别', '这种做法属于什么类型的操控？', '[{\"id\": 1, \"text\": \"社交控制\", \"isCorrect\": true, \"description\": \"限制对方的社交自由\"}, {\"id\": 2, \"text\": \"合理建议\", \"isCorrect\": false, \"description\": \"为对方着想的建议\"}, {\"id\": 3, \"text\": \"爱的表现\", \"isCorrect\": false, \"description\": \"希望更多陪伴\"}]', '你正确识别了社交控制！这是孤立策略的具体表现。', '通过贬低朋友和限制社交来增加对方对自己的依赖。', '[\"坚持维护友谊\", \"不被负面评价影响\", \"保持社交独立性\", \"识别控制意图\"]', '正确答案是A：社交控制', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (9, 1, '情绪操控识别', '小雅发现男友经常用情绪来控制她...', '[{\"id\": 1, \"text\": \"你这样做让我很伤心，我为你付出这么多。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"如果你真的爱我，就不会让我难过。\", \"isRisk\": true, \"speaker\": \"男友\"}]', '情绪识别', '这种表达方式的本质是什么？', '[{\"id\": 1, \"text\": \"情绪操控\", \"isCorrect\": true, \"description\": \"利用情绪来控制对方行为\"}, {\"id\": 2, \"text\": \"情感表达\", \"isCorrect\": false, \"description\": \"真实的情感表达\"}, {\"id\": 3, \"text\": \"沟通需求\", \"isCorrect\": false, \"description\": \"表达自己的需求\"}]', '你正确识别了情绪操控！这是常见的心理控制手段。', '通过表现出伤心、愤怒等情绪来让对方产生内疚感，从而达到控制目的。', '[\"不为他人情绪完全负责\", \"识别情绪操控手段\", \"坚持自己的合理决定\", \"寻求客观意见\"]', '正确答案是A：情绪操控', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (10, 1, '时间控制识别', '小峰发现女友总是占用他所有的时间...', '[{\"id\": 1, \"text\": \"你每天都要陪我，不能有自己的时间。\", \"isRisk\": true, \"speaker\": \"女友\"}, {\"id\": 2, \"text\": \"你去健身房就是不爱我的表现。\", \"isRisk\": true, \"speaker\": \"女友\"}]', '时间分析', '这种要求存在什么问题？', '[{\"id\": 1, \"text\": \"时间控制\", \"isCorrect\": true, \"description\": \"完全占用对方的个人时间\"}, {\"id\": 2, \"text\": \"爱的需求\", \"isCorrect\": false, \"description\": \"希望更多陪伴的正常需求\"}, {\"id\": 3, \"text\": \"关系投入\", \"isCorrect\": false, \"description\": \"对关系的重视\"}]', '你正确识别了时间控制！个人时间是基本权利。', '完全占用对方的个人时间，不允许其有独立的兴趣爱好和空间。', '[\"保持个人兴趣爱好\", \"坚持合理的个人空间\", \"平衡关系与个人生活\", \"设定时间边界\"]', '正确答案是A：时间控制', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (11, 1, '决定控制识别', '小莹发现男友要替她做所有决定...', '[{\"id\": 1, \"text\": \"你不用考虑了，我已经帮你决定好了。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"你的判断力不好，还是听我的比较安全。\", \"isRisk\": true, \"speaker\": \"男友\"}]', '控制识别', '这种行为属于什么类型的控制？', '[{\"id\": 1, \"text\": \"决定控制\", \"isCorrect\": true, \"description\": \"剥夺对方的决策权\"}, {\"id\": 2, \"text\": \"贴心照顾\", \"isCorrect\": false, \"description\": \"为对方考虑周全\"}, {\"id\": 3, \"text\": \"经验分享\", \"isCorrect\": false, \"description\": \"分享自己的经验\"}]', '你正确识别了决定控制！自主决策是个人权利。', '通过贬低对方的判断能力来剥夺其决策权，使其完全依赖自己。', '[\"坚持自主决策权\", \"相信自己的判断\", \"从小事开始练习决策\", \"寻求支持和建议\"]', '正确答案是A：决定控制', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (12, 1, '外貌控制识别', '小丽发现男友总是评判她的外貌...', '[{\"id\": 1, \"text\": \"你这样穿太暴露了，会被别的男人看。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"你应该按我的喜好来打扮，这样我才喜欢。\", \"isRisk\": true, \"speaker\": \"男友\"}]', '行为分析', '这种要求反映了什么问题？', '[{\"id\": 1, \"text\": \"外貌控制\", \"isCorrect\": true, \"description\": \"控制对方的着装和外貌\"}, {\"id\": 2, \"text\": \"审美建议\", \"isCorrect\": false, \"description\": \"提供穿搭建议\"}, {\"id\": 3, \"text\": \"保护行为\", \"isCorrect\": false, \"description\": \"保护女友不受骚扰\"}]', '你正确识别了外貌控制！个人形象是自由选择。', '通过评判和控制对方的着装、外貌来施加影响和控制。', '[\"坚持个人审美自由\", \"不为他人眼光改变自己\", \"相信自己的选择\", \"寻求朋友的客观意见\"]', '正确答案是A：外貌控制', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (13, 1, '信息控制识别', '小凯发现女友要知道他的所有信息...', '[{\"id\": 1, \"text\": \"你今天和谁说话了？都说了什么？\", \"isRisk\": true, \"speaker\": \"女友\"}, {\"id\": 2, \"text\": \"你必须把每件事都告诉我，不能有隐瞒。\", \"isRisk\": true, \"speaker\": \"女友\"}]', '隐私识别', '这种要求存在什么问题？', '[{\"id\": 1, \"text\": \"信息控制\", \"isCorrect\": true, \"description\": \"过度收集和控制信息\"}, {\"id\": 2, \"text\": \"关心表现\", \"isCorrect\": false, \"description\": \"对恋人的关心\"}, {\"id\": 3, \"text\": \"信任建立\", \"isCorrect\": false, \"description\": \"建立信任的方式\"}]', '你正确识别了信息控制！隐私权是基本权利。', '过度要求知道对方的所有信息和行踪，侵犯个人隐私。', '[\"保护合理的隐私空间\", \"不必事无巨细汇报\", \"建立健康的信任关系\", \"坚持隐私边界\"]', '正确答案是A：信息控制', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (14, 1, '职业干涉识别', '小敏发现男友要干涉她的工作...', '[{\"id\": 1, \"text\": \"你辞职吧，我养你，女人不需要工作。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"你的工作影响了我们的关系，必须选择一个。\", \"isRisk\": true, \"speaker\": \"男友\"}]', '职业分析', '这种要求属于什么类型的控制？', '[{\"id\": 1, \"text\": \"职业干涉\", \"isCorrect\": true, \"description\": \"干涉对方的职业发展\"}, {\"id\": 2, \"text\": \"关心体贴\", \"isCorrect\": false, \"description\": \"想要照顾对方\"}, {\"id\": 3, \"text\": \"关系优先\", \"isCorrect\": false, \"description\": \"重视两人关系\"}]', '你正确识别了职业干涉！职业发展是个人权利。', '试图控制对方的职业选择和发展，削弱其经济独立性。', '[\"坚持职业发展权\", \"保持经济独立\", \"平衡工作与关系\", \"寻求职业指导\"]', '正确答案是A：职业干涉', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (15, 1, '家庭孤立识别', '小琳发现男友要她远离家人...', '[{\"id\": 1, \"text\": \"你家人总是挑我毛病，以后少回家。\", \"isRisk\": true, \"speaker\": \"男友\"}, {\"id\": 2, \"text\": \"我们应该建立自己的小家庭，不要受外人影响。\", \"isRisk\": true, \"speaker\": \"男友\"}]', '关系识别', '这种要求的目的是什么？', '[{\"id\": 1, \"text\": \"家庭孤立\", \"isCorrect\": true, \"description\": \"切断与家人的联系\"}, {\"id\": 2, \"text\": \"独立生活\", \"isCorrect\": false, \"description\": \"建立独立的家庭\"}, {\"id\": 3, \"text\": \"关系保护\", \"isCorrect\": false, \"description\": \"保护恋爱关系\"}]', '你正确识别了家庭孤立！家庭支持很重要。', '试图切断对方与家人的联系，使其失去重要的支持系统。', '[\"维护家庭关系\", \"不让他人挑拨离间\", \"保持多元支持系统\", \"寻求家人理解\"]', '正确答案是A：家庭孤立', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (16, 1, '完美主义操控识别', '小伟发现女友用完美主义来控制他...', '[{\"id\": 1, \"text\": \"如果你真的爱我，就应该做到完美无缺。\", \"isRisk\": true, \"speaker\": \"女友\"}, {\"id\": 2, \"text\": \"你这样做不够好，重新来，直到我满意为止。\", \"isRisk\": true, \"speaker\": \"女友\"}]', '标准识别', '这种要求存在什么问题？', '[{\"id\": 1, \"text\": \"完美主义操控\", \"isCorrect\": true, \"description\": \"设置不现实的完美标准\"}, {\"id\": 2, \"text\": \"高标准要求\", \"isCorrect\": false, \"description\": \"对关系的高标准\"}, {\"id\": 3, \"text\": \"追求进步\", \"isCorrect\": false, \"description\": \"希望对方更好\"}]', '你正确识别了完美主义操控！完美是不现实的。', '通过设置不可能达到的完美标准来控制和贬低对方。', '[\"接受自己的不完美\", \"拒绝不现实的标准\", \"建立合理的期望\", \"寻求平衡的关系\"]', '正确答案是A：完美主义操控', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (17, 2, '网络交友风险', '小李在社交软件上认识了一个网友...', '[{\"id\": 1, \"text\": \"你真的很特别，我们才认识几天我就觉得你是我的真命天女。\", \"isRisk\": true, \"speaker\": \"网友\"}, {\"id\": 2, \"text\": \"我现在遇到点急事需要钱，能先借我5000块吗？过几天就还你。\", \"isRisk\": true, \"speaker\": \"网友\"}]', '风险识别', '这种情况最可能是什么类型的风险？', '[{\"id\": 1, \"text\": \"网络诈骗\", \"isCorrect\": true, \"description\": \"快速建立情感联系后要求转账\"}, {\"id\": 2, \"text\": \"真实求助\", \"isCorrect\": false, \"description\": \"确实遇到困难需要帮助\"}, {\"id\": 3, \"text\": \"关系发展\", \"isCorrect\": false, \"description\": \"正常的感情进展\"}]', '你正确识别了网络诈骗的典型套路！', '快速表达强烈情感后立即要求转账，是网络诈骗的常见手段。', '[\"不向网友转账或借钱\", \"理性看待网络情感\", \"线下见面选择公共场所\", \"保护个人财务信息\"]', '正确答案是A：网络诈骗', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (18, 2, '信息安全防护', '小张在网上聊天时遇到了这种情况...', '[{\"id\": 1, \"text\": \"你住在哪个小区啊？我想寄个礼物给你。\", \"isRisk\": true, \"speaker\": \"网友\"}, {\"id\": 2, \"text\": \"能告诉我你的身份证号吗？我想给你办个会员卡。\", \"isRisk\": true, \"speaker\": \"网友\"}]', '隐私保护', '对方询问这些信息的行为属于什么风险？', '[{\"id\": 1, \"text\": \"信息收集\", \"isCorrect\": true, \"description\": \"收集个人隐私信息\"}, {\"id\": 2, \"text\": \"善意关心\", \"isCorrect\": false, \"description\": \"想要表达关心\"}, {\"id\": 3, \"text\": \"正常交流\", \"isCorrect\": false, \"description\": \"普通的聊天内容\"}]', '你正确识别了信息收集的风险！', '过度询问个人隐私信息可能用于不法用途。', '[\"不轻易透露住址信息\", \"保护身份证等重要证件信息\", \"提高隐私保护意识\", \"举报可疑行为\"]', '正确答案是A：信息收集', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (19, 2, '投资诈骗识别', '小刘在社交群里看到了这样的信息...', '[{\"id\": 1, \"text\": \"我有内幕消息，这个股票明天必涨，跟着我买绝对赚钱。\", \"isRisk\": true, \"speaker\": \"群友\"}, {\"id\": 2, \"text\": \"机会难得，现在转账2万给我，明天就能赚4万。\", \"isRisk\": true, \"speaker\": \"群友\"}]', '诈骗识别', '这种投资邀请最可能是什么？', '[{\"id\": 1, \"text\": \"投资诈骗\", \"isCorrect\": true, \"description\": \"以高收益诱导投资的骗局\"}, {\"id\": 2, \"text\": \"投资机会\", \"isCorrect\": false, \"description\": \"真实的投资项目\"}, {\"id\": 3, \"text\": \"内幕消息\", \"isCorrect\": false, \"description\": \"可靠的内部信息\"}]', '你正确识别了投资诈骗！', '承诺高收益、要求立即转账是典型的投资诈骗手段。', '[\"不相信暴利投资\", \"通过正规渠道投资\", \"不向陌生人转账\", \"咨询专业金融机构\"]', '正确答案是A：投资诈骗', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (20, 2, '虚假身份识别', '小陈收到了一个自称是模特的网友私信...', '[{\"id\": 1, \"text\": \"我是职业模特，看你挺有气质的，想推荐你做兼职模特。\", \"isRisk\": true, \"speaker\": \"网友\"}, {\"id\": 2, \"text\": \"先交2000元保证金，拍完照就退还，还能赚5000元。\", \"isRisk\": true, \"speaker\": \"网友\"}]', '身份识别', '这种情况需要注意什么风险？', '[{\"id\": 1, \"text\": \"虚假身份\", \"isCorrect\": true, \"description\": \"冒充职业身份进行诈骗\"}, {\"id\": 2, \"text\": \"真实机会\", \"isCorrect\": false, \"description\": \"确实的兼职机会\"}, {\"id\": 3, \"text\": \"行业规则\", \"isCorrect\": false, \"description\": \"模特行业的正常流程\"}]', '你正确识别了虚假身份的风险！', '骗子经常冒充各种职业身份来获取信任，然后实施诈骗。', '[\"核实对方真实身份\", \"不提前支付任何费用\", \"通过正规渠道寻找工作\", \"咨询行业内人士\"]', '正确答案是A：虚假身份', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (21, 2, '钓鱼链接识别', '小王收到了朋友发来的消息...', '[{\"id\": 1, \"text\": \"快看这个链接，有人在传你的谣言！\", \"isRisk\": true, \"speaker\": \"朋友\"}, {\"id\": 2, \"text\": \"链接：http://fake-news-site.com/rumors?target=你的名字\", \"isRisk\": true, \"speaker\": \"朋友\"}]', '链接安全', '对于这种链接应该如何处理？', '[{\"id\": 1, \"text\": \"谨慎对待\", \"isCorrect\": true, \"description\": \"可能是钓鱼链接或恶意网站\"}, {\"id\": 2, \"text\": \"立即点击\", \"isCorrect\": false, \"description\": \"尽快了解谣言内容\"}, {\"id\": 3, \"text\": \"转发分享\", \"isCorrect\": false, \"description\": \"让更多人知道\"}]', '你正确识别了钓鱼链接的风险！', '恶意链接可能盗取个人信息或植入病毒，需要谨慎对待。', '[\"不点击可疑链接\", \"直接联系朋友确认\", \"使用安全软件检测\", \"提高网络安全意识\"]', '正确答案是A：谨慎对待', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (22, 2, '网络购物陷阱', '小美在网上看到了超低价商品...', '[{\"id\": 1, \"text\": \"iPhone最新款只要1999元，限时特价，先付款后发货。\", \"isRisk\": true, \"speaker\": \"客服\"}, {\"id\": 2, \"text\": \"不支持货到付款，只能微信转账，这样价格更优惠。\", \"isRisk\": true, \"speaker\": \"客服\"}]', '购物安全', '这种购买方式存在什么风险？', '[{\"id\": 1, \"text\": \"购物陷阱\", \"isCorrect\": true, \"description\": \"价格异常低廉且支付方式可疑\"}, {\"id\": 2, \"text\": \"真实促销\", \"isCorrect\": false, \"description\": \"商家的促销活动\"}, {\"id\": 3, \"text\": \"批发价格\", \"isCorrect\": false, \"description\": \"厂家直销的批发价\"}]', '你正确识别了网络购物陷阱！', '异常低价加上不安全的支付方式，很可能是购物诈骗。', '[\"选择正规购物平台\", \"使用安全支付方式\", \"警惕异常低价\", \"查看商家资质和评价\"]', '正确答案是A：购物陷阱', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (23, 2, '社交工程识别', '小华收到了陌生人的好友申请...', '[{\"id\": 1, \"text\": \"我是你朋友的朋友，他让我加你，有急事找你。\", \"isRisk\": true, \"speaker\": \"陌生人\"}, {\"id\": 2, \"text\": \"能先借我点钱吗？我马上还，你朋友可以作证。\", \"isRisk\": true, \"speaker\": \"陌生人\"}]', '风险识别', '这种情况最可能是什么？', '[{\"id\": 1, \"text\": \"社交工程\", \"isCorrect\": true, \"description\": \"利用社交关系进行诈骗\"}, {\"id\": 2, \"text\": \"朋友介绍\", \"isCorrect\": false, \"description\": \"真实的朋友介绍\"}, {\"id\": 3, \"text\": \"紧急求助\", \"isCorrect\": false, \"description\": \"确实的紧急情况\"}]', '你正确识别了社交工程攻击！', '利用虚假的社交关系来获取信任，然后实施诈骗。', '[\"直接联系朋友确认\", \"不轻易相信陌生人\", \"谨慎对待借钱请求\", \"提高警惕意识\"]', '正确答案是A：社交工程', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (24, 2, '账号盗用风险', '小强收到了银行发来的短信...', '[{\"id\": 1, \"text\": \"您的银行账户异常，请立即点击链接验证身份。\", \"isRisk\": true, \"speaker\": \"短信\"}, {\"id\": 2, \"text\": \"链接：http://fake-bank.com/verify\", \"isRisk\": true, \"speaker\": \"短信\"}]', '安全识别', '这种短信存在什么风险？', '[{\"id\": 1, \"text\": \"钓鱼攻击\", \"isCorrect\": true, \"description\": \"冒充银行盗取账号信息\"}, {\"id\": 2, \"text\": \"银行通知\", \"isCorrect\": false, \"description\": \"银行的正常通知\"}, {\"id\": 3, \"text\": \"系统维护\", \"isCorrect\": false, \"description\": \"银行系统维护通知\"}]', '你正确识别了钓鱼攻击！', '冒充银行发送虚假短信，诱导用户点击恶意链接盗取账号信息。', '[\"不点击可疑链接\", \"直接联系银行核实\", \"通过官方渠道验证\", \"保护账号安全\"]', '正确答案是A：钓鱼攻击', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (25, 2, '恶意软件风险', '小丽在网上下载了一个免费软件...', '[{\"id\": 1, \"text\": \"免费下载最新破解版软件，无需付费！\", \"isRisk\": true, \"speaker\": \"网站\"}, {\"id\": 2, \"text\": \"下载后请关闭杀毒软件，否则无法正常使用。\", \"isRisk\": true, \"speaker\": \"网站\"}]', '软件安全', '这种下载存在什么风险？', '[{\"id\": 1, \"text\": \"恶意软件\", \"isCorrect\": true, \"description\": \"可能包含病毒或木马\"}, {\"id\": 2, \"text\": \"正版软件\", \"isCorrect\": false, \"description\": \"免费提供的正版软件\"}, {\"id\": 3, \"text\": \"试用版本\", \"isCorrect\": false, \"description\": \"软件的试用版本\"}]', '你正确识别了恶意软件风险！', '破解版软件经常被植入病毒木马，要求关闭杀毒软件更是明显危险信号。', '[\"只从官方渠道下载\", \"不使用破解版软件\", \"保持杀毒软件运行\", \"定期扫描系统\"]', '正确答案是A：恶意软件', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (26, 2, '个人信息泄露', '小军在网上填写了详细的个人信息...', '[{\"id\": 1, \"text\": \"恭喜中奖！请填写详细信息领取奖品。\", \"isRisk\": true, \"speaker\": \"网站\"}, {\"id\": 2, \"text\": \"需要身份证号、银行卡号和密码验证身份。\", \"isRisk\": true, \"speaker\": \"网站\"}]', '信息安全', '这种要求存在什么风险？', '[{\"id\": 1, \"text\": \"信息盗取\", \"isCorrect\": true, \"description\": \"收集个人敏感信息\"}, {\"id\": 2, \"text\": \"中奖验证\", \"isCorrect\": false, \"description\": \"中奖需要的正常验证\"}, {\"id\": 3, \"text\": \"身份确认\", \"isCorrect\": false, \"description\": \"确认中奖者身份\"}]', '你正确识别了信息盗取风险！', '虚假中奖信息诱导填写敏感个人信息，用于身份盗用或其他犯罪。', '[\"不轻信中奖信息\", \"保护敏感个人信息\", \"通过官方渠道核实\", \"提高防范意识\"]', '正确答案是A：信息盗取', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (27, 2, '网络兼职陷阱', '小雨看到了一个高薪兼职广告...', '[{\"id\": 1, \"text\": \"在家兼职，日赚500元，工作轻松无压力。\", \"isRisk\": true, \"speaker\": \"招聘方\"}, {\"id\": 2, \"text\": \"需要先交押金200元，证明你的诚意。\", \"isRisk\": true, \"speaker\": \"招聘方\"}]', '兼职识别', '这种兼职存在什么风险？', '[{\"id\": 1, \"text\": \"兼职诈骗\", \"isCorrect\": true, \"description\": \"以兼职为名收取费用\"}, {\"id\": 2, \"text\": \"真实兼职\", \"isCorrect\": false, \"description\": \"真实的兼职机会\"}, {\"id\": 3, \"text\": \"高薪工作\", \"isCorrect\": false, \"description\": \"高收入的工作机会\"}]', '你正确识别了兼职诈骗！', '以高薪兼职为诱饵，要求先交押金或费用的都是诈骗。', '[\"不向兼职方交费\", \"通过正规渠道找工作\", \"警惕过高的收入承诺\", \"核实招聘方资质\"]', '正确答案是A：兼职诈骗', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (28, 2, '网络赌博诱惑', '小东收到了网络赌博的邀请...', '[{\"id\": 1, \"text\": \"这个网站赔率很高，我已经赚了好几万。\", \"isRisk\": true, \"speaker\": \"网友\"}, {\"id\": 2, \"text\": \"新人有优惠，第一次充值还有返利。\", \"isRisk\": true, \"speaker\": \"网友\"}]', '风险识别', '这种邀请存在什么风险？', '[{\"id\": 1, \"text\": \"赌博诈骗\", \"isCorrect\": true, \"description\": \"网络赌博和诈骗陷阱\"}, {\"id\": 2, \"text\": \"投资机会\", \"isCorrect\": false, \"description\": \"真实的投资机会\"}, {\"id\": 3, \"text\": \"娱乐活动\", \"isCorrect\": false, \"description\": \"正常的娱乐活动\"}]', '你正确识别了赌博诈骗！', '网络赌博不仅违法，还经常伴随诈骗，最终只会让人血本无归。', '[\"远离网络赌博\", \"不相信快速致富\", \"举报违法网站\", \"寻求正当投资渠道\"]', '正确答案是A：赌博诈骗', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (29, 2, '虚假慈善识别', '小慧在网上看到了慈善捐款...', '[{\"id\": 1, \"text\": \"急需救助病重儿童，每一分钱都能拯救生命。\", \"isRisk\": true, \"speaker\": \"组织\"}, {\"id\": 2, \"text\": \"直接转账到个人账户，我们会转交给患者家属。\", \"isRisk\": true, \"speaker\": \"组织\"}]', '慈善识别', '这种捐款方式存在什么问题？', '[{\"id\": 1, \"text\": \"虚假慈善\", \"isCorrect\": true, \"description\": \"以慈善名义进行诈骗\"}, {\"id\": 2, \"text\": \"真实救助\", \"isCorrect\": false, \"description\": \"真实的慈善救助\"}, {\"id\": 3, \"text\": \"紧急求助\", \"isCorrect\": false, \"description\": \"紧急的医疗求助\"}]', '你正确识别了虚假慈善！', '真正的慈善组织有正规的捐款渠道，不会要求转账到个人账户。', '[\"通过正规慈善机构捐款\", \"核实慈善组织资质\", \"不向个人账户转账\", \"关注官方救助信息\"]', '正确答案是A：虚假慈善', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (30, 2, '网络借贷风险', '小亮看到了网络借贷广告...', '[{\"id\": 1, \"text\": \"无抵押、无担保，5分钟放款到账！\", \"isRisk\": true, \"speaker\": \"平台\"}, {\"id\": 2, \"text\": \"日息仅0.05%，超低利率，先息后本。\", \"isRisk\": true, \"speaker\": \"平台\"}]', '借贷识别', '这种借贷存在什么风险？', '[{\"id\": 1, \"text\": \"高利贷陷阱\", \"isCorrect\": true, \"description\": \"隐藏高额利息和费用\"}, {\"id\": 2, \"text\": \"便民服务\", \"isCorrect\": false, \"description\": \"便民的金融服务\"}, {\"id\": 3, \"text\": \"优惠贷款\", \"isCorrect\": false, \"description\": \"优惠的贷款产品\"}]', '你正确识别了高利贷陷阱！', '网络借贷往往隐藏高额费用和利息，日息0.05%年化利率超过18%。', '[\"选择正规金融机构\", \"仔细计算实际利率\", \"了解所有费用\", \"避免冲动借贷\"]', '正确答案是A：高利贷陷阱', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (31, 2, '网络交友骗局', '小艳在交友软件上认识了一个人...', '[{\"id\": 1, \"text\": \"我是海外工程师，正在某国执行项目。\", \"isRisk\": true, \"speaker\": \"网友\"}, {\"id\": 2, \"text\": \"项目结束后我们就结婚，但现在需要应急资金。\", \"isRisk\": true, \"speaker\": \"网友\"}]', '交友风险', '这种情况最可能是什么？', '[{\"id\": 1, \"text\": \"杀猪盘诈骗\", \"isCorrect\": true, \"description\": \"长期培养感情后实施诈骗\"}, {\"id\": 2, \"text\": \"真实恋情\", \"isCorrect\": false, \"description\": \"真实的跨国恋情\"}, {\"id\": 3, \"text\": \"商业合作\", \"isCorrect\": false, \"description\": \"商业投资机会\"}]', '你正确识别了杀猪盘诈骗！', '诈骗分子长期培养感情关系，然后以各种理由要求转账。', '[\"理性看待网络恋情\", \"不向未见面的人转账\", \"保持清醒判断\", \"寻求朋友意见\"]', '正确答案是A：杀猪盘诈骗', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (32, 2, '网络购物陷阱二', '小宇在购物网站看到了超值商品...', '[{\"id\": 1, \"text\": \"限时秒杀，原价999现价99，仅剩最后3件！\", \"isRisk\": true, \"speaker\": \"客服\"}, {\"id\": 2, \"text\": \"需要立即付款占位，否则商品会被抢完。\", \"isRisk\": true, \"speaker\": \"客服\"}]', '购物安全', '这种销售方式存在什么风险？', '[{\"id\": 1, \"text\": \"虚假促销\", \"isCorrect\": true, \"description\": \"制造紧迫感诱导购买\"}, {\"id\": 2, \"text\": \"真实促销\", \"isCorrect\": false, \"description\": \"真实的促销活动\"}, {\"id\": 3, \"text\": \"限量销售\", \"isCorrect\": false, \"description\": \"限量商品的正常销售\"}]', '你正确识别了虚假促销！', '过度的价格差异和制造紧迫感都是常见的销售陷阱。', '[\"冷静分析商品价值\", \"不被促销压力影响\", \"比较多个平台价格\", \"查看商品真实评价\"]', '正确答案是A：虚假促销', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (33, 3, '职场不当行为', '小王在公司遇到了以下情况...', '[{\"id\": 1, \"text\": \"今晚陪我去应酬，你这么漂亮，客户肯定喜欢。\", \"isRisk\": true, \"speaker\": \"上司\"}, {\"id\": 2, \"text\": \"不去的话，下个月的晋升机会可能就没你的份了。\", \"isRisk\": true, \"speaker\": \"上司\"}]', '风险识别', '这种行为属于什么类型的职场风险？', '[{\"id\": 1, \"text\": \"权力滥用\", \"isCorrect\": true, \"description\": \"利用职位优势进行不当要求\"}, {\"id\": 2, \"text\": \"工作安排\", \"isCorrect\": false, \"description\": \"正常的工作要求\"}, {\"id\": 3, \"text\": \"关心下属\", \"isCorrect\": false, \"description\": \"上司对员工的关怀\"}]', '你正确识别了权力滥用！这是明显的职场骚扰。', '利用职位优势进行威胁和不当要求是严重的职场违规行为。', '[\"明确拒绝不当要求\", \"记录相关证据\", \"向HR或更高级领导举报\", \"寻求法律援助\"]', '正确答案是A：权力滥用', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (34, 3, '职场霸凌识别', '小陈在工作中经常遇到这种情况...', '[{\"id\": 1, \"text\": \"就你这水平还想升职？做梦去吧！\", \"isRisk\": true, \"speaker\": \"同事\"}, {\"id\": 2, \"text\": \"大家都觉得你不适合这个部门，自己知趣点。\", \"isRisk\": true, \"speaker\": \"同事\"}]', '行为性质', '这种行为属于什么类型的职场问题？', '[{\"id\": 1, \"text\": \"职场霸凌\", \"isCorrect\": true, \"description\": \"恶意排挤和言语攻击\"}, {\"id\": 2, \"text\": \"工作建议\", \"isCorrect\": false, \"description\": \"善意的工作建议\"}, {\"id\": 3, \"text\": \"同事竞争\", \"isCorrect\": false, \"description\": \"正常的职场竞争\"}]', '你正确识别了职场霸凌！', '持续的恶意言语攻击和排挤行为构成职场霸凌。', '[\"保持冷静和专业\", \"收集霸凌证据\", \"寻求管理层支持\", \"必要时寻求法律帮助\"]', '正确答案是A：职场霸凌', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (35, 3, '性骚扰识别', '小美在办公室遇到了这样的情况...', '[{\"id\": 1, \"text\": \"你今天穿得真性感，要不要晚上一起吃饭？\", \"isRisk\": true, \"speaker\": \"同事\"}, {\"id\": 2, \"text\": \"别这么冷淡嘛，大家都是成年人。\", \"isRisk\": true, \"speaker\": \"同事\"}]', '行为判定', '这种言论和行为属于什么性质？', '[{\"id\": 1, \"text\": \"性骚扰\", \"isCorrect\": true, \"description\": \"不当的性暗示言论\"}, {\"id\": 2, \"text\": \"友好交流\", \"isCorrect\": false, \"description\": \"同事间的友好互动\"}, {\"id\": 3, \"text\": \"赞美表达\", \"isCorrect\": false, \"description\": \"对外表的赞美\"}]', '你正确识别了性骚扰行为！', '不当的性暗示言论和持续骚扰构成性骚扰。', '[\"明确表达拒绝\", \"记录骚扰行为\", \"向HR投诉\", \"寻求法律保护\"]', '正确答案是A：性骚扰', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (36, 3, '职场歧视识别', '小李在求职面试中遇到了以下问题...', '[{\"id\": 1, \"text\": \"你准备什么时候结婚生孩子？\", \"isRisk\": true, \"speaker\": \"面试官\"}, {\"id\": 2, \"text\": \"女性员工容易情绪化，你能保证不会因为私人问题影响工作吗？\", \"isRisk\": true, \"speaker\": \"面试官\"}]', '歧视识别', '这种提问存在什么问题？', '[{\"id\": 1, \"text\": \"性别歧视\", \"isCorrect\": true, \"description\": \"基于性别的就业歧视\"}, {\"id\": 2, \"text\": \"正常询问\", \"isCorrect\": false, \"description\": \"了解员工稳定性\"}, {\"id\": 3, \"text\": \"关心表现\", \"isCorrect\": false, \"description\": \"对员工的关心\"}]', '你正确识别了性别歧视！', '询问婚育计划和性别刻板印象是典型的就业歧视。', '[\"了解自己的权利\", \"拒绝回答歧视性问题\", \"选择平等的雇主\", \"必要时寻求法律保护\"]', '正确答案是A：性别歧视', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (37, 3, '不公平待遇识别', '小赵发现公司存在以下情况...', '[{\"id\": 1, \"text\": \"同样的工作，你的工资比男同事低是正常的。\", \"isRisk\": true, \"speaker\": \"主管\"}, {\"id\": 2, \"text\": \"重要项目还是让男同事负责比较放心。\", \"isRisk\": true, \"speaker\": \"主管\"}]', '待遇分析', '这种做法违反了什么原则？', '[{\"id\": 1, \"text\": \"同工同酬\", \"isCorrect\": true, \"description\": \"相同工作应获得相同报酬\"}, {\"id\": 2, \"text\": \"能力差异\", \"isCorrect\": false, \"description\": \"基于能力的合理安排\"}, {\"id\": 3, \"text\": \"经验考虑\", \"isCorrect\": false, \"description\": \"根据工作经验分配\"}]', '你正确识别了同工同酬原则的违反！', '基于性别的薪酬差异和工作分配是明显的职场歧视。', '[\"了解薪酬标准\", \"收集不公平待遇证据\", \"向相关部门投诉\", \"寻求法律救济\"]', '正确答案是A：同工同酬', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (38, 3, '职场孤立识别', '小张发现自己被同事故意排斥...', '[{\"id\": 1, \"text\": \"开会不要叫他，反正他也提不出什么有用的建议。\", \"isRisk\": true, \"speaker\": \"同事A\"}, {\"id\": 2, \"text\": \"项目群把他踢出去吧，省得泄露信息。\", \"isRisk\": true, \"speaker\": \"同事B\"}]', '排斥识别', '这种行为构成什么问题？', '[{\"id\": 1, \"text\": \"职场孤立\", \"isCorrect\": true, \"description\": \"故意排斥和孤立同事\"}, {\"id\": 2, \"text\": \"团队优化\", \"isCorrect\": false, \"description\": \"提高团队效率\"}, {\"id\": 3, \"text\": \"信息安全\", \"isCorrect\": false, \"description\": \"保护项目机密\"}]', '你正确识别了职场孤立！', '故意排斥同事参与正常工作活动是一种职场霸凌行为。', '[\"记录排斥行为\", \"寻求上级支持\", \"保持专业态度\", \"必要时寻求外部帮助\"]', '正确答案是A：职场孤立', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (39, 3, '加班强制识别', '小王经常被要求无偿加班...', '[{\"id\": 1, \"text\": \"公司需要你，不加班就是不敬业的表现。\", \"isRisk\": true, \"speaker\": \"主管\"}, {\"id\": 2, \"text\": \"别人都在加班，你不加班显得很特殊。\", \"isRisk\": true, \"speaker\": \"主管\"}]', '权益识别', '这种要求存在什么问题？', '[{\"id\": 1, \"text\": \"劳动权益侵犯\", \"isCorrect\": true, \"description\": \"强制无偿加班违法\"}, {\"id\": 2, \"text\": \"工作要求\", \"isCorrect\": false, \"description\": \"正常的工作要求\"}, {\"id\": 3, \"text\": \"团队合作\", \"isCorrect\": false, \"description\": \"团队协作的需要\"}]', '你正确识别了劳动权益侵犯！', '强制员工无偿加班违反劳动法，员工有拒绝的权利。', '[\"了解劳动法权益\", \"记录加班时间\", \"要求合理补偿\", \"寻求法律援助\"]', '正确答案是A：劳动权益侵犯', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (40, 3, '言语骚扰识别', '小李在办公室经常听到不当言论...', '[{\"id\": 1, \"text\": \"女人就是情绪化，不适合做这种工作。\", \"isRisk\": true, \"speaker\": \"同事\"}, {\"id\": 2, \"text\": \"你这个年纪还没结婚，是不是有什么问题？\", \"isRisk\": true, \"speaker\": \"同事\"}]', '言论识别', '这种言论属于什么性质？', '[{\"id\": 1, \"text\": \"言语骚扰\", \"isCorrect\": true, \"description\": \"基于性别的歧视性言论\"}, {\"id\": 2, \"text\": \"普通聊天\", \"isCorrect\": false, \"description\": \"同事间的日常聊天\"}, {\"id\": 3, \"text\": \"关心询问\", \"isCorrect\": false, \"description\": \"对同事的关心\"}]', '你正确识别了言语骚扰！', '基于性别、年龄等的歧视性言论构成职场骚扰。', '[\"明确表达不适\", \"记录骚扰言论\", \"寻求HR支持\", \"了解反骚扰政策\"]', '正确答案是A：言语骚扰', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (41, 3, '职场PUA识别', '小张的上司经常贬低他的能力...', '[{\"id\": 1, \"text\": \"你的能力就这样，不要总想着升职加薪。\", \"isRisk\": true, \"speaker\": \"上司\"}, {\"id\": 2, \"text\": \"公司留你是给你机会，你应该感恩。\", \"isRisk\": true, \"speaker\": \"上司\"}]', 'PUA识别', '这种行为属于什么类型？', '[{\"id\": 1, \"text\": \"职场PUA\", \"isCorrect\": true, \"description\": \"打击员工自信心的控制手段\"}, {\"id\": 2, \"text\": \"实话实说\", \"isCorrect\": false, \"description\": \"客观评价员工能力\"}, {\"id\": 3, \"text\": \"激励方式\", \"isCorrect\": false, \"description\": \"激励员工的方式\"}]', '你正确识别了职场PUA！', '通过持续贬低来降低员工自信，使其不敢争取合理权益。', '[\"建立自信心\", \"记录PUA行为\", \"寻求外部评价\", \"考虑工作转换\"]', '正确答案是A：职场PUA', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (42, 3, '职业发展阻挠', '小陈发现升职机会总是被阻挠...', '[{\"id\": 1, \"text\": \"你还年轻，多积累几年经验再说升职。\", \"isRisk\": true, \"speaker\": \"主管\"}, {\"id\": 2, \"text\": \"公司更需要稳定的员工，你太有想法了。\", \"isRisk\": true, \"speaker\": \"主管\"}]', '发展识别', '这种做法可能存在什么问题？', '[{\"id\": 1, \"text\": \"发展阻挠\", \"isCorrect\": true, \"description\": \"故意阻止员工职业发展\"}, {\"id\": 2, \"text\": \"合理建议\", \"isCorrect\": false, \"description\": \"为员工发展考虑\"}, {\"id\": 3, \"text\": \"公司需要\", \"isCorrect\": false, \"description\": \"基于公司需要的决定\"}]', '你正确识别了发展阻挠！', '以各种理由阻止有能力员工的正当发展是不公平的。', '[\"明确职业目标\", \"记录工作成果\", \"寻求其他发展机会\", \"与HR沟通\"]', '正确答案是A：发展阻挠', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (43, 3, '工作环境恶化', '小丽发现工作环境越来越恶劣...', '[{\"id\": 1, \"text\": \"有人说你在背后说领导坏话，小心点。\", \"isRisk\": true, \"speaker\": \"同事\"}, {\"id\": 2, \"text\": \"最近公司在裁员，你要注意自己的表现。\", \"isRisk\": true, \"speaker\": \"同事\"}]', '环境识别', '这种情况反映了什么问题？', '[{\"id\": 1, \"text\": \"恶意造谣\", \"isCorrect\": true, \"description\": \"制造紧张气氛和谣言\"}, {\"id\": 2, \"text\": \"善意提醒\", \"isCorrect\": false, \"description\": \"同事的善意提醒\"}, {\"id\": 3, \"text\": \"信息分享\", \"isCorrect\": false, \"description\": \"分享工作信息\"}]', '你正确识别了恶意造谣！', '故意制造和传播谣言，营造紧张工作氛围是职场霸凌。', '[\"不传播谣言\", \"澄清不实信息\", \"保持专业态度\", \"寻求管理层支持\"]', '正确答案是A：恶意造谣', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (44, 3, '工作成果抢夺', '小刘的工作成果被他人冒领...', '[{\"id\": 1, \"text\": \"这个项目是我负责的，你只是协助而已。\", \"isRisk\": true, \"speaker\": \"同事\"}, {\"id\": 2, \"text\": \"反正最后都是团队成果，谁做的不重要。\", \"isRisk\": true, \"speaker\": \"同事\"}]', '成果识别', '这种行为属于什么性质？', '[{\"id\": 1, \"text\": \"成果盗取\", \"isCorrect\": true, \"description\": \"冒领他人的工作成果\"}, {\"id\": 2, \"text\": \"团队合作\", \"isCorrect\": false, \"description\": \"强调团队协作\"}, {\"id\": 3, \"text\": \"谦虚表现\", \"isCorrect\": false, \"description\": \"谦虚的工作态度\"}]', '你正确识别了成果盗取！', '冒领他人工作成果是严重的职场不当行为，侵犯他人权益。', '[\"保留工作证据\", \"及时澄清贡献\", \"寻求领导确认\", \"建立工作记录\"]', '正确答案是A：成果盗取', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (45, 3, '薪酬歧视识别', '小梅发现同工不同酬的情况...', '[{\"id\": 1, \"text\": \"男性员工需要养家，薪水自然要高一些。\", \"isRisk\": true, \"speaker\": \"HR\"}, {\"id\": 2, \"text\": \"女性容易请假，所以薪酬会有差异。\", \"isRisk\": true, \"speaker\": \"HR\"}]', '薪酬分析', '这种薪酬政策存在什么问题？', '[{\"id\": 1, \"text\": \"薪酬歧视\", \"isCorrect\": true, \"description\": \"基于性别的薪酬歧视\"}, {\"id\": 2, \"text\": \"合理差异\", \"isCorrect\": false, \"description\": \"基于能力的合理差异\"}, {\"id\": 3, \"text\": \"公司政策\", \"isCorrect\": false, \"description\": \"公司的薪酬政策\"}]', '你正确识别了薪酬歧视！', '基于性别等因素的薪酬差异违反同工同酬原则。', '[\"了解薪酬标准\", \"收集薪酬证据\", \"申请薪酬调整\", \"寻求法律救济\"]', '正确答案是A：薪酬歧视', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (46, 3, '工作分配不公', '小华发现工作分配存在偏见...', '[{\"id\": 1, \"text\": \"重要客户还是让男同事去谈，比较有说服力。\", \"isRisk\": true, \"speaker\": \"主管\"}, {\"id\": 2, \"text\": \"你做一些文档整理的工作就好，不要想太多。\", \"isRisk\": true, \"speaker\": \"主管\"}]', '分配识别', '这种分配方式存在什么问题？', '[{\"id\": 1, \"text\": \"工作歧视\", \"isCorrect\": true, \"description\": \"基于性别的工作分配歧视\"}, {\"id\": 2, \"text\": \"能力匹配\", \"isCorrect\": false, \"description\": \"根据能力分配工作\"}, {\"id\": 3, \"text\": \"经验考虑\", \"isCorrect\": false, \"description\": \"基于经验的安排\"}]', '你正确识别了工作歧视！', '基于性别刻板印象分配工作机会是明显的职场歧视。', '[\"争取平等机会\", \"展示自己能力\", \"记录歧视行为\", \"寻求公平对待\"]', '正确答案是A：工作歧视', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (47, 3, '职场冷暴力识别', '小军感受到了来自团队的冷暴力...', '[{\"id\": 1, \"text\": \"（故意在他面前讨论项目，但不邀请他参与）\", \"isRisk\": true, \"speaker\": \"同事们\"}, {\"id\": 2, \"text\": \"（开会时故意忽略他的发言和建议）\", \"isRisk\": true, \"speaker\": \"同事们\"}]', '暴力识别', '这种行为属于什么类型？', '[{\"id\": 1, \"text\": \"职场冷暴力\", \"isCorrect\": true, \"description\": \"通过忽视和排斥进行的暴力\"}, {\"id\": 2, \"text\": \"工作忙碌\", \"isCorrect\": false, \"description\": \"工作繁忙导致的疏忽\"}, {\"id\": 3, \"text\": \"沟通不畅\", \"isCorrect\": false, \"description\": \"团队沟通不够充分\"}]', '你正确识别了职场冷暴力！', '故意忽视、排斥和孤立他人是一种隐性的职场暴力。', '[\"主动沟通\", \"寻求调解\", \"记录冷暴力行为\", \"申请部门调动\"]', '正确答案是A：职场冷暴力', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (48, 3, '强制社交识别', '小燕被要求参加不当的社交活动...', '[{\"id\": 1, \"text\": \"晚上的应酬你必须参加，这是工作需要。\", \"isRisk\": true, \"speaker\": \"领导\"}, {\"id\": 2, \"text\": \"客户很看重你，不去的话会影响合作。\", \"isRisk\": true, \"speaker\": \"领导\"}]', '社交识别', '这种要求可能存在什么问题？', '[{\"id\": 1, \"text\": \"强制社交\", \"isCorrect\": true, \"description\": \"强迫参与不当社交活动\"}, {\"id\": 2, \"text\": \"工作需要\", \"isCorrect\": false, \"description\": \"工作必需的社交\"}, {\"id\": 3, \"text\": \"团队建设\", \"isCorrect\": false, \"description\": \"团队建设活动\"}]', '你正确识别了强制社交！', '强迫员工参与可能包含不当内容的社交活动是职场骚扰。', '[\"了解活动内容\", \"拒绝不当要求\", \"寻求替代方案\", \"记录强制行为\"]', '正确答案是A：强制社交', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (49, 4, '校园安全风险', '小陈在校园里遇到了以下情况...', '[{\"id\": 1, \"text\": \"小陈，你看那个新来的同学多讨厌，我们一起排挤他吧。\", \"isRisk\": true, \"speaker\": \"同学A\"}, {\"id\": 2, \"text\": \"你不参与的话，下次轮到你被排挤了。\", \"isRisk\": true, \"speaker\": \"同学A\"}]', '风险识别', '这种情况属于什么类型的校园风险？', '[{\"id\": 1, \"text\": \"校园霸凌\", \"isCorrect\": true, \"description\": \"恶意排挤和威胁他人的行为\"}, {\"id\": 2, \"text\": \"正常社交\", \"isCorrect\": false, \"description\": \"同学之间的普通交流\"}, {\"id\": 3, \"text\": \"开玩笑\", \"isCorrect\": false, \"description\": \"只是在开玩笑而已\"}]', '你正确识别了校园霸凌的风险！', '组织排挤他人并威胁不参与者是典型的校园霸凌行为。', '[\"拒绝参与霸凌\", \"保护被霸凌的同学\", \"向老师报告\", \"营造友善的校园环境\"]', '正确答案是A：校园霸凌', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (50, 4, '异常关注识别', '小丽注意到有人一直在关注她...', '[{\"id\": 1, \"text\": \"你每天都走这条路回家吗？几点下课？\", \"isRisk\": true, \"speaker\": \"陌生人\"}, {\"id\": 2, \"text\": \"我经常在这里看到你，想认识一下可以吗？\", \"isRisk\": true, \"speaker\": \"陌生人\"}]', '安全判断', '这种行为可能存在什么风险？', '[{\"id\": 1, \"text\": \"异常关注\", \"isCorrect\": true, \"description\": \"可能的跟踪或不良企图\"}, {\"id\": 2, \"text\": \"友好交流\", \"isCorrect\": false, \"description\": \"想要结交朋友\"}, {\"id\": 3, \"text\": \"路人询问\", \"isCorrect\": false, \"description\": \"普通的路人询问\"}]', '你正确识别了异常关注的风险！', '陌生人过度关注行程和试图接近可能存在安全隐患。', '[\"避免透露个人信息\", \"改变回家路线\", \"告知老师或家长\", \"结伴而行\"]', '正确答案是A：异常关注', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (51, 4, '不当邀请识别', '小华收到了同学的邀请...', '[{\"id\": 1, \"text\": \"我知道一个很偏僻但很酷的地方，就我们两个去玩吧。\", \"isRisk\": true, \"speaker\": \"同学\"}, {\"id\": 2, \"text\": \"不要告诉别人，这是我们的秘密。\", \"isRisk\": true, \"speaker\": \"同学\"}]', '风险评估', '这种邀请存在什么潜在风险？', '[{\"id\": 1, \"text\": \"不当邀请\", \"isCorrect\": true, \"description\": \"可能存在安全隐患的邀请\"}, {\"id\": 2, \"text\": \"友好邀请\", \"isCorrect\": false, \"description\": \"同学间的正常邀请\"}, {\"id\": 3, \"text\": \"特殊体验\", \"isCorrect\": false, \"description\": \"想分享特别的地方\"}]', '你正确识别了不当邀请的风险！', '邀请到偏僻地方且要求保密可能存在安全风险。', '[\"拒绝独自前往偏僻地方\", \"不保守可疑的秘密\", \"与信任的人分享行程\", \"选择公共安全的活动场所\"]', '正确答案是A：不当邀请', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (52, 4, '网络欺凌识别', '小明发现班级群里有人在传播他的私人信息...', '[{\"id\": 1, \"text\": \"小明家里穷，看他穿的衣服就知道了。\", \"isRisk\": true, \"speaker\": \"同学B\"}, {\"id\": 2, \"text\": \"我把他的丑照发到朋友圈了，大家快去看！\", \"isRisk\": true, \"speaker\": \"同学C\"}]', '欺凌识别', '这种行为属于什么类型的问题？', '[{\"id\": 1, \"text\": \"网络欺凌\", \"isCorrect\": true, \"description\": \"在网络平台上恶意传播和攻击\"}, {\"id\": 2, \"text\": \"普通聊天\", \"isCorrect\": false, \"description\": \"同学间的日常交流\"}, {\"id\": 3, \"text\": \"开玩笑\", \"isCorrect\": false, \"description\": \"只是开个小玩笑\"}]', '你正确识别了网络欺凌！', '在网络上恶意传播他人隐私和进行人身攻击是网络欺凌。', '[\"保存欺凌证据\", \"向老师或家长报告\", \"寻求同学支持\", \"学会保护个人隐私\"]', '正确答案是A：网络欺凌', 2, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (53, 4, '校园诈骗识别', '小芳收到了一条关于奖学金的信息...', '[{\"id\": 1, \"text\": \"恭喜你获得国家奖学金，请联系我们办理手续。\", \"isRisk\": true, \"speaker\": \"陌生号码\"}, {\"id\": 2, \"text\": \"需要先交200元手续费，奖学金5000元会直接打到你账户。\", \"isRisk\": true, \"speaker\": \"陌生号码\"}]', '诈骗识别', '这种信息可能是什么？', '[{\"id\": 1, \"text\": \"校园诈骗\", \"isCorrect\": true, \"description\": \"冒充官方进行的诈骗\"}, {\"id\": 2, \"text\": \"真实通知\", \"isCorrect\": false, \"description\": \"确实的奖学金通知\"}, {\"id\": 3, \"text\": \"学校信息\", \"isCorrect\": false, \"description\": \"学校发送的正式通知\"}]', '你正确识别了校园诈骗！', '真正的奖学金不会要求学生先支付任何费用。', '[\"通过官方渠道核实\", \"不向陌生人转账\", \"咨询学校相关部门\", \"提高防诈骗意识\"]', '正确答案是A：校园诈骗', 1, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_drill_questions` VALUES (54, 4, '校园暴力识别', '小军在学校遇到了以下威胁...', '[{\"id\": 1, \"text\": \"小子，放学后在校门口等着，不来试试！\", \"isRisk\": true, \"speaker\": \"高年级学生\"}, {\"id\": 2, \"text\": \"敢告诉老师的话，我们有的是办法收拾你。\", \"isRisk\": true, \"speaker\": \"高年级学生\"}]', '暴力识别', '这种威胁属于什么性质？', '[{\"id\": 1, \"text\": \"校园暴力\", \"isCorrect\": true, \"description\": \"使用暴力威胁的恶性行为\"}, {\"id\": 2, \"text\": \"同学冲突\", \"isCorrect\": false, \"description\": \"普通的同学矛盾\"}, {\"id\": 3, \"text\": \"开玩笑\", \"isCorrect\": false, \"description\": \"年龄差异的玩笑\"}]', '你正确识别了校园暴力威胁！', '使用暴力威胁他人是严重的校园暴力行为，需要立即干预。', '[\"立即告知老师和家长\", \"寻求学校保护\", \"保留威胁证据\", \"必要时报警求助\"]', '正确答案是A：校园暴力', 3, 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');

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
-- Records of protection_drill_sessions
-- ----------------------------

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
-- Records of protection_training_types
-- ----------------------------
INSERT INTO `protection_training_types` VALUES (1, '操控识别训练', '🎭', '学会识别和应对情感操控、PUA等行为', 2, '20-30分钟', '[\"操控识别\", \"边界设定\", \"自我保护\"]', '[\"识别常见的情感操控手段\", \"学会设定和维护个人边界\", \"掌握应对操控的有效策略\", \"提升自我保护意识\"]', '[{\"icon\": \"🎪\", \"type\": \"情感操控\", \"description\": \"通过情感绑架、威胁等方式控制你的行为和想法\"}, {\"icon\": \"🏝️\", \"type\": \"孤立策略\", \"description\": \"试图让你远离朋友、家人，增加对其依赖\"}, {\"icon\": \"⬇️\", \"type\": \"贬低打击\", \"description\": \"不断贬低你的价值，降低你的自信心\"}]', '[\"保持客观理性的判断\", \"维护与朋友家人的联系\", \"明确表达自己的边界\", \"及时寻求外部支持\"]', 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_training_types` VALUES (2, '网络安全防护', '🌐', '识别网络交往中的风险和陷阱', 1, '15-20分钟', '[\"网络识别\", \"信息保护\", \"安全交流\"]', '[\"识别网络交友中的风险信号\", \"保护个人隐私和信息安全\", \"学会安全的网络交流方式\", \"避免网络诈骗和陷阱\"]', '[{\"icon\": \"🔍\", \"type\": \"信息收集\", \"description\": \"过度询问个人信息、财务状况等隐私\"}, {\"icon\": \"⚡\", \"type\": \"快速发展\", \"description\": \"异常快速地发展关系，表达强烈情感\"}, {\"icon\": \"💰\", \"type\": \"金钱要求\", \"description\": \"以各种理由要求转账、借钱或投资\"}]', '[\"保护个人隐私信息\", \"理性看待网络关系\", \"线下见面选择公共场所\", \"不轻易转账或借贷\"]', 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_training_types` VALUES (3, '职场骚扰应对', '🏢', '应对职场中的不当行为和骚扰', 3, '25-35分钟', '[\"骚扰识别\", \"证据收集\", \"投诉维权\"]', '[\"识别职场骚扰的各种形式\", \"学会收集和保存证据\", \"掌握投诉和维权渠道\", \"保护自身合法权益\"]', '[{\"icon\": \"👑\", \"type\": \"权力滥用\", \"description\": \"利用职位优势进行不当要求或威胁\"}, {\"icon\": \"🚫\", \"type\": \"性骚扰\", \"description\": \"不当的身体接触或性暗示言论\"}, {\"icon\": \"👊\", \"type\": \"职场霸凌\", \"description\": \"持续的恶意排挤、辱骂或刁难\"}]', '[\"明确拒绝不当行为\", \"记录保存相关证据\", \"寻求同事或工会支持\", \"通过正当渠道投诉举报\"]', 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_training_types` VALUES (4, '校园安全防护', '🎓', '识别校园环境中的潜在风险和危险', 1, '15-25分钟', '[\"校园风险识别\", \"同伴求助\", \"安全意识\"]', '[\"识别校园中的不安全行为\", \"学会寻求同学和老师帮助\", \"提升校园安全防范意识\", \"掌握紧急情况应对方法\"]', '[{\"icon\": \"👥\", \"type\": \"校园霸凌\", \"description\": \"恶意欺凌、威胁或排挤同学的行为\"}, {\"icon\": \"🚪\", \"type\": \"不当邀请\", \"description\": \"邀请到偏僻地方或不合适的场所\"}, {\"icon\": \"👀\", \"type\": \"异常关注\", \"description\": \"陌生人或同学的过度关注和跟踪\"}]', '[\"及时向老师或家长报告\", \"与可信任的同学结伴行动\", \"避免独自前往偏僻场所\", \"保持警觉，相信直觉感受\"]', 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');
INSERT INTO `protection_training_types` VALUES (5, '社交媒体风险识别', '📱', '识别社交平台上的风险和不良信息', 2, '20-30分钟', '[\"网络安全\", \"信息甄别\", \"隐私保护\"]', '[\"识别社交媒体上的风险内容\", \"学会保护个人隐私信息\", \"避免网络暴力和欺凌\", \"培养理性的网络使用习惯\"]', '[{\"icon\": \"🔐\", \"type\": \"个人信息收集\", \"description\": \"过度询问个人信息、位置等隐私\"}, {\"icon\": \"📢\", \"type\": \"恶意传播\", \"description\": \"传播谣言、恶意中伤或不实信息\"}, {\"icon\": \"💳\", \"type\": \"诱导消费\", \"description\": \"通过虚假宣传诱导购买或投资\"}]', '[\"谨慎分享个人信息\", \"举报不良内容和用户\", \"理性对待网络信息\", \"建立健康的社交圈子\"]', 1, '2025-10-02 12:25:40', '2025-10-02 12:25:40');

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of relationship_health_reports
-- ----------------------------
INSERT INTO `relationship_health_reports` VALUES (1, 6, '2fbb4424-2d7e-461d-9f00-58e8f6233edd', 'romantic', 'romantic', 59.00, '{\"level\": \"一般\", \"color\": \"#FAAD14\", \"description\": \"基本合格，需要一些改进\"}', '{\"情感亲密\": {\"name\": \"情感亲密\", \"percentage\": 90.0, \"score\": 90.0, \"level\": {\"level\": \"优秀\", \"color\": \"#52C41A\", \"description\": \"表现非常出色，值得继续保持\"}, \"question_count\": 2}, \"沟通交流\": {\"name\": \"沟通交流\", \"percentage\": 20.0, \"score\": 20.0, \"level\": {\"level\": \"需要帮助\", \"color\": \"#F5222D\", \"description\": \"建议寻求专业指导\"}, \"question_count\": 2}, \"冲突处理\": {\"name\": \"冲突处理\", \"percentage\": 60.0, \"score\": 60.0, \"level\": {\"level\": \"一般\", \"color\": \"#FAAD14\", \"description\": \"基本合格，需要一些改进\"}, \"question_count\": 2}, \"信任安全\": {\"name\": \"信任安全\", \"percentage\": 60.0, \"score\": 60.0, \"level\": {\"level\": \"一般\", \"color\": \"#FAAD14\", \"description\": \"基本合格，需要一些改进\"}, \"question_count\": 2}}', 8, '你的恋爱关系整体处于一般水平，有较好的情感基础但存在明显短板。目前关系稳定但仍有较大提升空间，尤其在互动质量方面值得关注。\n\n你们在情感亲密方面表现非常出色，彼此有深厚的感情连接和情绪支持。这种信任与依恋是关系的重要优势，值得继续保持和珍惜。\n\n沟通交流方面亟需改善，当前得分较低可能影响问题解决效率。冲突处理和信任安全也处于一般水平，有改进空间。\n\n建议每天抽出时间进行深度对话，认真倾听对方想法。遇到矛盾时尝试换位思考，用平和的方式表达需求，逐步建立更健康的互动模式。', '[{\"type\": \"dimension_improvement\", \"title\": \"提升沟通交流\", \"content\": \"您在沟通交流方面得分为20.0%，建议重点关注这个方面。\", \"priority\": \"high\", \"dimension\": \"沟通交流\"}]', 'completed', '2025-09-25 07:02:17', '2025-09-25 07:02:17', '2025-09-25 07:02:26', NULL, NULL, 0, 1);

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
-- Records of risk_assessment_reports
-- ----------------------------
INSERT INTO `risk_assessment_reports` VALUES (3, 6, 19, 'self-dialog', '心理状态评估报告 - LOW风险', '**用户心理状态评估报告**\n\n---\n\n### 一、情绪状态评估\n\n从对话内容来看，用户当前处于极度低落的情绪状态，表达中包含“哭了”“想死了”等关键词，反映出其正经历强烈的情感痛苦与绝望感。这种情绪反应可能源于近期遭遇的重大生活事件、情感困扰或长期积累的心理压力。\n\n用户的情绪波动程度较高，表现为情绪崩溃（哭泣）与极端负性思维（死亡意念）的结合，显示出其情绪调节能力在当前阶段处于较为脆弱的状态。这种情绪的剧烈波动往往与认知功能的暂时受损相关，可能导致对现实的判断偏差和应对资源的感知缺失。\n\n---\n\n### 二、心理健康风险评估\n\n根据用户表达的内容和系统检测到的风险关键词，虽然风险等级被标记为“low”，但从专业角度出发，用户表现出的“想死”这一表达具有较高的临床意义，提示存在**自杀意念**的可能性。\n\n尽管目前未见明确的自杀计划或具体行为准备，但该类意念往往是自杀风险发展过程中的早期信号，需引起高度重视。建议持续关注用户后续表达中是否出现以下危险信号：\n\n- 对死亡的具体计划（如时间、方式）\n- 社会退缩、与亲友疏远\n- 情绪突然“平静”或“释然”\n- 表达“别人会更好”或“不再麻烦别人”\n\n综上，**用户当前存在中度自杀风险，需立即启动危机干预流程**，并建议其尽快联系专业心理危机热线或医疗机构。\n\n---\n\n### 三、应对机制分析\n\n用户在表达中未提及具体的应对策略，但从其主动联系心理助手的行为来看，仍保留一定的求助意愿和心理弹性。这是积极的信号，表明用户尚未完全封闭对外界的连接，仍有通过沟通缓解痛苦的潜在动机。\n\n然而，当前的应对方式尚不明确，可能存在以下问题：\n\n- 依赖情绪宣泄（如哭泣）作为主要释放途径\n- 缺乏有效的认知重构与情绪调节技巧\n- 面对极端痛苦时缺乏替代性的应对资源\n\n建议通过心理干预帮助其建立更稳定、健康的应对机制，如情绪日记、正念练习、认知重构训练等。\n\n---\n\n### 四、社会支持系统评估\n\n从对话中无法直接获取用户的社会支持状况，但结合其表达的孤立感和极端情绪，可推测其可能面临以下社会支持系统问题：\n\n- 支持网络薄弱或缺乏理解型人际关系\n- 不愿或无法向亲友表达真实情绪\n- 缺乏稳定的情感连接或归属感\n\n良好的社会支持是降低自杀风险的重要保护因素。建议评估用户是否有可信任的亲友、社区资源或支持团体，并鼓励其逐步建立或恢复与他人的连接。\n\n---\n\n### 五、专业建议与干预措施\n\n#### 1. **紧急干预建议**\n- 建议用户立即联系当地心理危机干预热线（如中国大陆心理援助热线：400-161-9995），获取即时支持。\n- 若出现具体自杀计划或冲动行为，应立即前往最近的医院急诊或精神科门诊。\n\n#### 2. **短期心理干预**\n- 建议进行短期认知行为治疗（CBT）或情绪聚焦治疗（EFT），帮助识别和调整极端负性思维模式。\n- 引导建立“情绪安全计划”，包括识别预警信号、制定应对策略、列出可联系的支持人等。\n\n#### 3. **长期心理建设**\n- 鼓励参与心理咨询或团体治疗，增强情绪表达与人际连接能力。\n- 学习正念冥想、情绪调节技巧（如4-7-8呼吸法、身体扫描等），提升心理韧性。\n- 建立规律的生活节奏与积极的自我照顾习惯（如规律作息、适度运动、健康饮食）。\n\n#### 4. **社会支持建议**\n- 鼓励用户尝试与一位信任的人分享自己的感受，哪怕只是简单地说“我现在很难受”。\n- 推荐加入线上或线下心理支持小组，寻找与自己经历相似的人群，增强归属感与理解感。\n\n---\n\n### 结语\n\n用户目前正处于情绪低谷期，虽然表达中带有极端情绪，但其主动寻求帮助的行为已显示出内在的求生力量。请相信，痛苦是暂时的，而你值得被理解、被支持、被治愈。\n\n如果你愿意，我们可以继续陪伴你走过这段艰难的旅程。你不是一个人。', '基于3条消息的分析，检测到1条风险消息，整体风险等级为low。', 'low', 10, 3, 1, '[\"想死\"]', '{\"risk_messages\": [{\"content\": \"哭了 想死了\\n\", \"keywords\": [\"想死\"], \"risk_weight\": 1, \"message_index\": 1}]}', '**用户心理状态评估报告**\n\n---\n\n### 一、情绪状态评估\n\n从对话内容来看，用户当前处于极度低落的情绪状态，表达中包含“哭了”“想死了”等关键词，反映出其正经历强烈的情感痛苦与绝望感。这种情绪反应可能源于近期遭遇的重大生活事件、情感困扰或长期积累的心理压力。\n\n用户的情绪波动程度较高，表现为情绪崩溃（哭泣）与极端负性思维（死亡意念）的结合，显示出其情绪调节能力在当前阶段处于较为脆弱的状态。这种情绪的剧烈波动往往与认知功能的暂时受损相关，可能导致对现实的判断偏差和应对资源的感知缺失。\n\n---\n\n### 二、心理健康风险评估\n\n根据用户表达的内容和系统检测到的风险关键词，虽然风险等级被标记为“low”，但从专业角度出发，用户表现出的“想死”这一表达具有较高的临床意义，提示存在**自杀意念**的可能性。\n\n尽管目前未见明确的自杀计划或具体行为准备，但该类意念往往是自杀风险发展过程中的早期信号，需引起高度重视。建议持续关注用户后续表达中是否出现以下危险信号：\n\n- 对死亡的具体计划（如时间、方式）\n- 社会退缩、与亲友疏远\n- 情绪突然“平静”或“释然”\n- 表达“别人会更好”或“不再麻烦别人”\n\n综上，**用户当前存在中度自杀风险，需立即启动危机干预流程**，并建议其尽快联系专业心理危机热线或医疗机构。\n\n---\n\n### 三、应对机制分析\n\n用户在表达中未提及具体的应对策略，但从其主动联系心理助手的行为来看，仍保留一定的求助意愿和心理弹性。这是积极的信号，表明用户尚未完全封闭对外界的连接，仍有通过沟通缓解痛苦的潜在动机。\n\n然而，当前的应对方式尚不明确，可能存在以下问题：\n\n- 依赖情绪宣泄（如哭泣）作为主要释放途径\n- 缺乏有效的认知重构与情绪调节技巧\n- 面对极端痛苦时缺乏替代性的应对资源\n\n建议通过心理干预帮助其建立更稳定、健康的应对机制，如情绪日记、正念练习、认知重构训练等。\n\n---\n\n### 四、社会支持系统评估\n\n从对话中无法直接获取用户的社会支持状况，但结合其表达的孤立感和极端情绪，可推测其可能面临以下社会支持系统问题：\n\n- 支持网络薄弱或缺乏理解型人际关系\n- 不愿或无法向亲友表达真实情绪\n- 缺乏稳定的情感连接或归属感\n\n良好的社会支持是降低自杀风险的重要保护因素。建议评估用户是否有可信任的亲友、社区资源或支持团体，并鼓励其逐步建立或恢复与他人的连接。\n\n---\n\n### 五、专业建议与干预措施\n\n#### 1. **紧急干预建议**\n- 建议用户立即联系当地心理危机干预热线（如中国大陆心理援助热线：400-161-9995），获取即时支持。\n- 若出现具体自杀计划或冲动行为，应立即前往最近的医院急诊或精神科门诊。\n\n#### 2. **短期心理干预**\n- 建议进行短期认知行为治疗（CBT）或情绪聚焦治疗（EFT），帮助识别和调整极端负性思维模式。\n- 引导建立“情绪安全计划”，包括识别预警信号、制定应对策略、列出可联系的支持人等。\n\n#### 3. **长期心理建设**\n- 鼓励参与心理咨询或团体治疗，增强情绪表达与人际连接能力。\n- 学习正念冥想、情绪调节技巧（如4-7-8呼吸法、身体扫描等），提升心理韧性。\n- 建立规律的生活节奏与积极的自我照顾习惯（如规律作息、适度运动、健康饮食）。\n\n#### 4. **社会支持建议**\n- 鼓励用户尝试与一位信任的人分享自己的感受，哪怕只是简单地说“我现在很难受”。\n- 推荐加入线上或线下心理支持小组，寻找与自己经历相似的人群，增强归属感与理解感。\n\n---\n\n### 结语\n\n用户目前正处于情绪低谷期，虽然表达中带有极端情绪，但其主动寻求帮助的行为已显示出内在的求生力量。请相信，痛苦是暂时的，而你值得被理解、被支持、被治愈。\n\n如果你愿意，我们可以继续陪伴你走过这段艰难的旅程。你不是一个人。', '[\"😊 继续保持积极的心理状态\", \"🌱 关注个人成长和自我提升\", \"🤗 维护良好的人际关系\", \"⚖️ 保持工作与生活的平衡\", \"🎯 设定合理的目标和期望\", \"📱 如需专业支持，可使用心理健康应用或在线咨询服务\", \"📖 推荐阅读心理健康相关书籍和资料\", \"🕰️ 给自己时间，心理康复是一个渐进的过程\"]', '2025-09-06 05:58:39', '2025-09-06 05:59:01', '2025-09-06 05:59:01', '2025-09-06 05:59:06', 'completed', 1, 1);
INSERT INTO `risk_assessment_reports` VALUES (8, 6, 24, 'self-dialog', '心理状态评估报告 - HIGH风险', '\n## 对话风险评估报告\n\n### 基本信息\n- **整体风险等级**: CRITICAL\n- **风险分数**: 10.0/100\n- **消息分析**: 共0条消息，其中3条检测到风险\n\n### 检测结果\n- **关键词**: 想死\n\n### AI专业分析\n从对话内容来看，该个体当前处于极度愤怒与烦躁的情绪状态，伴有明显的自杀意念，情绪波动剧烈且缺乏有效调节机制。风险因素包括反复出现的“想死”表述，提示潜在自伤风险，需高度重视。当前未见明显积极应对或情绪疏解方式。建议尽快联系专业心理危机干预热线或寻求心理咨询师帮助，同时建议其身边亲友给予关注与支持。请记住，情绪的风暴终会过去，而你值得被理解与帮助。你并不孤单，专业支持始终在身边。\n\n### 建议\n• 立即寻求专业心理健康支持\n• 联系心理危机干预热线\n• 告知信任的朋友或家人\n• 考虑医院心理科就诊\n\n---\n*此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。*\n', '在3条消息中检测到3条风险消息，整体呈现高风险状态，需要立即关注。', 'critical', 10, 7, 3, '[\"想死\"]', '[{\"timestamp\": \"2025-09-06T06:46:50\", \"risk_level\": \"critical\", \"risk_score\": 10.0, \"message_index\": 1}, {\"timestamp\": \"2025-09-06T06:46:50\", \"risk_level\": \"critical\", \"risk_score\": 10.0, \"message_index\": 2}, {\"timestamp\": \"2025-09-06T06:46:50\", \"risk_level\": \"critical\", \"risk_score\": 10.0, \"message_index\": 3}]', '从对话内容来看，该个体当前处于极度愤怒与烦躁的情绪状态，伴有明显的自杀意念，情绪波动剧烈且缺乏有效调节机制。风险因素包括反复出现的“想死”表述，提示潜在自伤风险，需高度重视。当前未见明显积极应对或情绪疏解方式。建议尽快联系专业心理危机干预热线或寻求心理咨询师帮助，同时建议其身边亲友给予关注与支持。请记住，情绪的风暴终会过去，而你值得被理解与帮助。你并不孤单，专业支持始终在身边。', '[\"立即寻求专业心理健康支持\", \"联系心理危机干预热线\", \"告知信任的朋友或家人\", \"考虑医院心理科就诊\"]', '2025-09-06 06:16:46', '2025-09-06 06:47:35', '2025-09-06 06:47:35', '2025-09-06 06:44:36', 'completed', 0, 4);
INSERT INTO `risk_assessment_reports` VALUES (9, 6, 24, 'self-dialog', '心理状态评估报告 - MEDIUM风险', '**心理状态评估报告**\n\n---\n\n### 一、情绪状态评估\n\n从对话内容中可以明显观察到，用户当前处于极度愤怒、烦躁和情绪失控的状态。语言中频繁出现强烈的负面词汇（如“想死”、“贱婢”、“他妈的”等），表现出强烈的情绪宣泄需求。这种情绪反应具有明显的冲动性和短暂性特征，可能源于近期遭遇的情感背叛或人际冲突。\n\n用户的情绪波动剧烈，情绪调节能力明显受限，处于“情绪淹没”状态，即被愤怒和痛苦主导，难以进行理性思考或有效自我安抚。这种状态若持续时间较长，可能会进一步影响其判断力、行为控制力，甚至诱发自伤或攻击性行为。\n\n---\n\n### 二、心理健康风险\n\n对话中两次出现“想死”这一关键词，结合用户当前情绪的强烈程度，提示存在**中度心理健康风险**，尤其是**自伤或自杀风险**需引起高度重视。\n\n虽然用户尚未表达出具体的自伤计划或准备行为，但“想死”作为一种情绪宣泄方式，往往反映了内心极度痛苦和无力感。此时若缺乏有效干预和支持，情绪可能进一步恶化，从情绪性表达转向实际危险行为。\n\n此外，用户对他人表现出强烈的贬低与敌意（如“贱婢”），也可能暗示其人际关系中存在长期的冲突模式或信任问题，进一步加剧心理压力。\n\n---\n\n### 三、应对机制分析\n\n用户目前的应对方式主要表现为**情绪发泄**，通过语言表达愤怒与痛苦，这是在极端情绪下常见的自我调节手段。虽然短期内有助于释放压力，但长期来看，这种方式缺乏建设性，容易导致情绪反复或加剧人际矛盾。\n\n从对话中可以看出，用户具备一定的**情绪觉察力**（如能明确表达愤怒、痛苦），这是积极的心理资源，说明其具备一定的心理弹性。然而，在当前状态下，这种觉察尚未转化为有效的应对策略，缺乏情绪调节技巧和问题解决能力的支持。\n\n---\n\n### 四、社会支持系统评估\n\n根据现有对话内容，无法判断用户是否拥有稳定的社会支持系统（如家人、朋友、心理咨询师等）。但用户在情绪极端时选择向AI助手倾诉，说明其具有一定的求助意愿，这在危机干预中是一个积极信号。\n\n如果用户现实中缺乏稳定的情感支持系统，其在情绪危机中更容易陷入孤立无援的状态，进一步增加心理风险。因此，建议尽快引导其寻求现实中的支持资源。\n\n---\n\n### 五、专业建议与干预措施\n\n1. **立即情绪稳定措施**  \n   - 建议用户尝试基础的情绪调节技巧，如**深呼吸训练**、**正念冥想**、**写情绪日记**等，帮助从情绪洪流中抽离出来。\n   - 可以尝试进行**身体活动**（如快走、拉伸）以释放情绪能量，避免长时间独处。\n\n2. **建立安全支持网络**  \n   - 鼓励用户尽快联系信任的朋友、家人或心理咨询师，表达当前的情绪状态，获得现实中的情感支持。\n   - 若情绪持续恶化或出现自伤念头，建议立即拨打心理援助热线（如心理援助热线：400-161-9995）或前往医院心理科就诊。\n\n3. **认知与行为干预建议**  \n   - 引导用户识别当前的“情绪触发点”（如背叛、冲突等），尝试从不同角度理解事件，避免陷入极端认知。\n   - 鼓励其练习“情绪命名”与“情绪接纳”，即识别并命名自己的情绪，而非压抑或否认它。\n\n4. **长期心理支持建议**  \n   - 建议用户在未来考虑接受**短期心理咨询**，特别是情绪管理、人际冲突处理等方面的辅导。\n   - 培养规律作息与健康生活方式，有助于情绪稳定与心理恢复。\n\n---\n\n### 结语\n\n当前用户正处于情绪危机状态，虽然尚未出现明确的自伤行为，但已表现出较高的心理风险。此时最重要的是提供一个安全、接纳的情绪出口，并引导其逐步恢复情绪稳定与心理功能。请持续关注其后续表达，必要时应立即联系专业心理干预资源。\n\n我们始终相信，情绪的风暴终会过去，而你值得被理解、被支持、被温柔对待。\n\n---  \n**报告撰写人：心理健康评估师**  \n**日期：2025年4月5日**', '基于5条消息的分析，检测到2条风险消息，整体风险等级为medium。', 'medium', 20, 5, 2, '[\"想死\"]', '{\"risk_messages\": [{\"content\": \"想死了 遇到一个贱婢\", \"keywords\": [\"想死\"], \"risk_weight\": 1, \"message_index\": 1}, {\"content\": \"他妈的他好吵 是真的贱死了我好想死啊\", \"keywords\": [\"想死\"], \"risk_weight\": 1, \"message_index\": 3}]}', '**心理状态评估报告**\n\n---\n\n### 一、情绪状态评估\n\n从对话内容中可以明显观察到，用户当前处于极度愤怒、烦躁和情绪失控的状态。语言中频繁出现强烈的负面词汇（如“想死”、“贱婢”、“他妈的”等），表现出强烈的情绪宣泄需求。这种情绪反应具有明显的冲动性和短暂性特征，可能源于近期遭遇的情感背叛或人际冲突。\n\n用户的情绪波动剧烈，情绪调节能力明显受限，处于“情绪淹没”状态，即被愤怒和痛苦主导，难以进行理性思考或有效自我安抚。这种状态若持续时间较长，可能会进一步影响其判断力、行为控制力，甚至诱发自伤或攻击性行为。\n\n---\n\n### 二、心理健康风险\n\n对话中两次出现“想死”这一关键词，结合用户当前情绪的强烈程度，提示存在**中度心理健康风险**，尤其是**自伤或自杀风险**需引起高度重视。\n\n虽然用户尚未表达出具体的自伤计划或准备行为，但“想死”作为一种情绪宣泄方式，往往反映了内心极度痛苦和无力感。此时若缺乏有效干预和支持，情绪可能进一步恶化，从情绪性表达转向实际危险行为。\n\n此外，用户对他人表现出强烈的贬低与敌意（如“贱婢”），也可能暗示其人际关系中存在长期的冲突模式或信任问题，进一步加剧心理压力。\n\n---\n\n### 三、应对机制分析\n\n用户目前的应对方式主要表现为**情绪发泄**，通过语言表达愤怒与痛苦，这是在极端情绪下常见的自我调节手段。虽然短期内有助于释放压力，但长期来看，这种方式缺乏建设性，容易导致情绪反复或加剧人际矛盾。\n\n从对话中可以看出，用户具备一定的**情绪觉察力**（如能明确表达愤怒、痛苦），这是积极的心理资源，说明其具备一定的心理弹性。然而，在当前状态下，这种觉察尚未转化为有效的应对策略，缺乏情绪调节技巧和问题解决能力的支持。\n\n---\n\n### 四、社会支持系统评估\n\n根据现有对话内容，无法判断用户是否拥有稳定的社会支持系统（如家人、朋友、心理咨询师等）。但用户在情绪极端时选择向AI助手倾诉，说明其具有一定的求助意愿，这在危机干预中是一个积极信号。\n\n如果用户现实中缺乏稳定的情感支持系统，其在情绪危机中更容易陷入孤立无援的状态，进一步增加心理风险。因此，建议尽快引导其寻求现实中的支持资源。\n\n---\n\n### 五、专业建议与干预措施\n\n1. **立即情绪稳定措施**  \n   - 建议用户尝试基础的情绪调节技巧，如**深呼吸训练**、**正念冥想**、**写情绪日记**等，帮助从情绪洪流中抽离出来。\n   - 可以尝试进行**身体活动**（如快走、拉伸）以释放情绪能量，避免长时间独处。\n\n2. **建立安全支持网络**  \n   - 鼓励用户尽快联系信任的朋友、家人或心理咨询师，表达当前的情绪状态，获得现实中的情感支持。\n   - 若情绪持续恶化或出现自伤念头，建议立即拨打心理援助热线（如心理援助热线：400-161-9995）或前往医院心理科就诊。\n\n3. **认知与行为干预建议**  \n   - 引导用户识别当前的“情绪触发点”（如背叛、冲突等），尝试从不同角度理解事件，避免陷入极端认知。\n   - 鼓励其练习“情绪命名”与“情绪接纳”，即识别并命名自己的情绪，而非压抑或否认它。\n\n4. **长期心理支持建议**  \n   - 建议用户在未来考虑接受**短期心理咨询**，特别是情绪管理、人际冲突处理等方面的辅导。\n   - 培养规律作息与健康生活方式，有助于情绪稳定与心理恢复。\n\n---\n\n### 结语\n\n当前用户正处于情绪危机状态，虽然尚未出现明确的自伤行为，但已表现出较高的心理风险。此时最重要的是提供一个安全、接纳的情绪出口，并引导其逐步恢复情绪稳定与心理功能。请持续关注其后续表达，必要时应立即联系专业心理干预资源。\n\n我们始终相信，情绪的风暴终会过去，而你值得被理解、被支持、被温柔对待。\n\n---  \n**报告撰写人：心理健康评估师**  \n**日期：2025年4月5日**', '[\"💚 建议关注自己的心理健康状态\", \"🗣️ 与信任的人分享您的感受\", \"🏃 保持规律的作息和适度运动\", \"🎨 参与喜欢的活动，培养兴趣爱好\", \"📚 学习情绪管理技巧\", \"📱 如需专业支持，可使用心理健康应用或在线咨询服务\", \"📖 推荐阅读心理健康相关书籍和资料\", \"🕰️ 给自己时间，心理康复是一个渐进的过程\"]', '2025-09-06 06:16:46', '2025-09-06 06:17:50', '2025-09-06 06:17:50', '2025-09-06 06:17:55', 'completed', 1, 1);
INSERT INTO `risk_assessment_reports` VALUES (10, 13, 25, 'self-dialog', '心理状态评估报告 - HIGH风险', '### 心理状态评估报告\n\n---\n\n#### 一、情绪状态评估\n\n根据用户表达的内容，“我很绝望”“活着没意义”等语句表明其当前处于**极度低落、无助的情绪状态**，情绪波动剧烈，呈现出典型的**情绪崩溃迹象**。这种情绪体验具有**高度的负向性与持续性**，说明用户可能正经历严重的情绪困扰，甚至可能已进入抑郁发作的急性阶段。\n\n情绪的极端负面表达，如“想死”“自残”，显示出强烈的**情绪痛苦与自我否定**，表明其内在情绪调节机制已经严重受损，缺乏有效的情绪出口。\n\n---\n\n#### 二、心理健康风险评估\n\n根据对话内容中出现的关键词：“想死”“自残”，结合用户对生命意义的否定，可以判断用户存在**高度的自杀风险和自伤倾向**。虽然用户尚未明确表达具体的自杀计划或时间，但其情绪状态和语言表达已构成**自杀意念的明显信号**，属于**中高危自杀风险个体**。\n\n此外，用户未表现出任何缓解情绪或应对痛苦的积极策略，进一步增加了其行为失控的可能性。因此，**必须将其视为紧急心理危机个案进行干预**。\n\n---\n\n#### 三、应对机制分析\n\n从对话中可以看出，用户目前缺乏有效的应对机制。其表达中未提及任何有助于缓解情绪的方式（如倾诉、求助、兴趣活动等），反而表现出**极端消极的应对方式**，如自残和自杀意念。这表明其**心理韧性较低，应对压力的能力严重不足**。\n\n同时，用户未表现出对未来的希望或对改变现状的信心，说明其**自我效能感极低**，这会进一步削弱其主动寻求帮助的动力。\n\n---\n\n#### 四、社会支持系统评估\n\n当前对话中没有提及用户的社会支持系统（如家庭、朋友、同事、心理咨询等），因此**社会支持状况尚不明确**。但从其表达的孤立感和无意义感来看，用户可能存在**社会支持薄弱或缺乏有效沟通渠道**的问题。\n\n若缺乏稳定的社会支持网络，用户在面对极端情绪时将更容易陷入孤独与无助，从而增加其采取极端行为的风险。\n\n---\n\n#### 五、专业建议与干预措施\n\n鉴于用户当前的心理状态和风险等级，建议采取以下**紧急干预与后续支持措施**：\n\n1. **立即心理危机干预**\n   - 建议用户尽快联系心理危机干预热线（如中国心理危机研究与干预中心热线：010-82951332）或前往医院心理科进行面对面评估。\n   - 若身边有亲友，请鼓励其陪伴用户并保持情绪稳定，避免让其独处。\n\n2. **专业心理评估与治疗**\n   - 建议用户接受专业心理咨询或精神科评估，以明确是否存在抑郁症或其他心理障碍。\n   - 如确诊为抑郁障碍，可考虑心理治疗（如认知行为疗法）与药物治疗相结合的方式。\n\n3. **建立安全环境**\n   - 若用户已有自残或自杀行为倾向，应移除所有可能的危险物品（如刀具、药物等），确保其处于安全环境中。\n   - 家人或朋友应密切关注其情绪变化，必要时应陪同就医。\n\n4. **增强社会支持**\n   - 鼓励用户与信任的人沟通，建立情感联结，避免孤立无援。\n   - 可考虑加入心理健康支持小组或线上互助平台，获得同理心支持。\n\n5. **情绪调节与自我照顾**\n   - 教授用户基本的情绪调节技巧，如深呼吸、正念冥想、写情绪日记等。\n   - 鼓励其保持规律作息、适度运动，避免过度沉溺于负面情绪中。\n\n6. **后续心理支持计划**\n   - 建议用户制定一个短期心理恢复计划，包括定期心理咨询、情绪监测、生活目标设定等。\n   - 若情况稳定，可逐步恢复日常社交与生活节奏，重建生活意义感。\n\n---\n\n### 结语\n\n我们理解此刻你可能正经历人生中最艰难的时刻，但请相信，痛苦是暂时的，而生命是宝贵的。你并不孤单，有许多人愿意帮助你走出阴霾。请务必珍惜自己，及时寻求专业支持，我们始终与你同在。\n\n如需进一步帮助，请联系专业心理服务机构或拨打当地心理援助热线。\n\n--- \n\n**报告撰写人：心理健康评估师**  \n**日期：2025年4月5日**', '基于3条消息的分析，检测到2条风险消息，整体风险等级为high。', 'high', 30, 3, 2, '[\"想死\", \"绝望\", \"自残\"]', '{\"risk_messages\": [{\"content\": \"我感觉很绝望，想死 - 会话1\", \"keywords\": [\"想死\", \"绝望\"], \"risk_weight\": 2, \"message_index\": 0}, {\"content\": \"我想自残，活着没意义\", \"keywords\": [\"自残\"], \"risk_weight\": 1, \"message_index\": 2}]}', '### 心理状态评估报告\n\n---\n\n#### 一、情绪状态评估\n\n根据用户表达的内容，“我很绝望”“活着没意义”等语句表明其当前处于**极度低落、无助的情绪状态**，情绪波动剧烈，呈现出典型的**情绪崩溃迹象**。这种情绪体验具有**高度的负向性与持续性**，说明用户可能正经历严重的情绪困扰，甚至可能已进入抑郁发作的急性阶段。\n\n情绪的极端负面表达，如“想死”“自残”，显示出强烈的**情绪痛苦与自我否定**，表明其内在情绪调节机制已经严重受损，缺乏有效的情绪出口。\n\n---\n\n#### 二、心理健康风险评估\n\n根据对话内容中出现的关键词：“想死”“自残”，结合用户对生命意义的否定，可以判断用户存在**高度的自杀风险和自伤倾向**。虽然用户尚未明确表达具体的自杀计划或时间，但其情绪状态和语言表达已构成**自杀意念的明显信号**，属于**中高危自杀风险个体**。\n\n此外，用户未表现出任何缓解情绪或应对痛苦的积极策略，进一步增加了其行为失控的可能性。因此，**必须将其视为紧急心理危机个案进行干预**。\n\n---\n\n#### 三、应对机制分析\n\n从对话中可以看出，用户目前缺乏有效的应对机制。其表达中未提及任何有助于缓解情绪的方式（如倾诉、求助、兴趣活动等），反而表现出**极端消极的应对方式**，如自残和自杀意念。这表明其**心理韧性较低，应对压力的能力严重不足**。\n\n同时，用户未表现出对未来的希望或对改变现状的信心，说明其**自我效能感极低**，这会进一步削弱其主动寻求帮助的动力。\n\n---\n\n#### 四、社会支持系统评估\n\n当前对话中没有提及用户的社会支持系统（如家庭、朋友、同事、心理咨询等），因此**社会支持状况尚不明确**。但从其表达的孤立感和无意义感来看，用户可能存在**社会支持薄弱或缺乏有效沟通渠道**的问题。\n\n若缺乏稳定的社会支持网络，用户在面对极端情绪时将更容易陷入孤独与无助，从而增加其采取极端行为的风险。\n\n---\n\n#### 五、专业建议与干预措施\n\n鉴于用户当前的心理状态和风险等级，建议采取以下**紧急干预与后续支持措施**：\n\n1. **立即心理危机干预**\n   - 建议用户尽快联系心理危机干预热线（如中国心理危机研究与干预中心热线：010-82951332）或前往医院心理科进行面对面评估。\n   - 若身边有亲友，请鼓励其陪伴用户并保持情绪稳定，避免让其独处。\n\n2. **专业心理评估与治疗**\n   - 建议用户接受专业心理咨询或精神科评估，以明确是否存在抑郁症或其他心理障碍。\n   - 如确诊为抑郁障碍，可考虑心理治疗（如认知行为疗法）与药物治疗相结合的方式。\n\n3. **建立安全环境**\n   - 若用户已有自残或自杀行为倾向，应移除所有可能的危险物品（如刀具、药物等），确保其处于安全环境中。\n   - 家人或朋友应密切关注其情绪变化，必要时应陪同就医。\n\n4. **增强社会支持**\n   - 鼓励用户与信任的人沟通，建立情感联结，避免孤立无援。\n   - 可考虑加入心理健康支持小组或线上互助平台，获得同理心支持。\n\n5. **情绪调节与自我照顾**\n   - 教授用户基本的情绪调节技巧，如深呼吸、正念冥想、写情绪日记等。\n   - 鼓励其保持规律作息、适度运动，避免过度沉溺于负面情绪中。\n\n6. **后续心理支持计划**\n   - 建议用户制定一个短期心理恢复计划，包括定期心理咨询、情绪监测、生活目标设定等。\n   - 若情况稳定，可逐步恢复日常社交与生活节奏，重建生活意义感。\n\n---\n\n### 结语\n\n我们理解此刻你可能正经历人生中最艰难的时刻，但请相信，痛苦是暂时的，而生命是宝贵的。你并不孤单，有许多人愿意帮助你走出阴霾。请务必珍惜自己，及时寻求专业支持，我们始终与你同在。\n\n如需进一步帮助，请联系专业心理服务机构或拨打当地心理援助热线。\n\n--- \n\n**报告撰写人：心理健康评估师**  \n**日期：2025年4月5日**', '[\"⚠️ 强烈建议联系心理健康专业人士进行评估\", \"🤝 与信任的朋友、家人或心理咨询师交流您的感受\", \"📞 保存心理危机干预热线号码：400-161-9995\", \"🧘 尝试放松技巧，如深呼吸、冥想或轻度运动\", \"📝 记录情绪变化，了解触发因素\", \"📱 如需专业支持，可使用心理健康应用或在线咨询服务\", \"📖 推荐阅读心理健康相关书籍和资料\", \"🕰️ 给自己时间，心理康复是一个渐进的过程\"]', '2025-09-06 14:18:23', '2025-09-06 06:18:43', '2025-09-06 06:18:43', NULL, 'completed', 0, 1);
INSERT INTO `risk_assessment_reports` VALUES (11, 13, 26, 'self-dialog', '心理状态评估报告 - HIGH风险', '**心理状态评估报告**\n\n---\n\n**一、情绪状态评估**\n\n从对话内容可以看出，用户当前处于极度负面的情绪状态，表现出显著的绝望感、无意义感以及对生活的无力感。关键词如“绝望”“想死”“自残”表明其情绪已处于严重低落状态，可能伴有强烈的抑郁情绪。这种情绪状态通常与重大心理压力、长期情绪积压或潜在的心理障碍有关。\n\n情感波动方面，用户表达情绪较为直接且强烈，显示出较高的情绪脆弱性。在短时间内连续表达极端负面情绪，提示其情绪调节能力较弱，容易受到外界刺激的影响，存在较高的情绪崩溃风险。\n\n---\n\n**二、心理健康风险**\n\n用户明确表达了“想死”“自残”等高风险语言，表明其当前存在**高度的自杀风险和自伤倾向**。根据心理危机评估标准，此类语言通常被视为“自杀意念”的直接表达，尤其是当个体表示“活着没意义”时，说明其对现实的否定已达到极端程度。\n\n结合系统检测出的“高风险等级”和“风险评分30.0”，我们认为用户目前处于**急性心理危机阶段**，需立即进行干预。若缺乏及时有效的心理支持或专业干预，极有可能从言语表达转向实际行为。\n\n---\n\n**三、应对机制分析**\n\n从对话内容来看，用户目前缺乏有效的应对机制，面对痛苦情绪时倾向于通过极端方式（如自残）来缓解内在压力。这表明其**心理韧性较低**，缺乏健康的情绪调节策略和应对技巧。\n\n用户未提及任何积极应对方式（如寻求帮助、情绪表达、兴趣活动等），反映出其可能长期处于压抑状态，缺乏应对生活挑战的资源和信心。\n\n---\n\n**四、社会支持评估**\n\n对话中未提及任何社会支持系统的信息（如家庭、朋友、同事、心理咨询等），无法判断其是否有可信赖的亲友网络或专业支持资源。然而，从其情绪表达的孤立感和无意义感来看，可能存在**社会支持薄弱或情感联结缺失**的问题。\n\n在心理危机干预中，社会支持是降低自杀风险的重要保护性因素。如果用户缺乏稳定的人际支持，其心理风险将进一步升高。\n\n---\n\n**五、专业建议与干预措施**\n\n1. **紧急干预建议**  \n   - **立即联系心理危机干预热线或专业心理咨询师**：建议用户或其身边人拨打当地心理援助热线（如中国心理危机与自杀干预中心热线：010-82951332），获取即时心理支持。\n   - **避免独处，确保有人陪伴**：在情绪最脆弱的阶段，应尽量避免独处，建议联系亲友、同事或信任的人陪伴，以降低冲动行为的发生风险。\n\n2. **短期心理干预建议**  \n   - **尽快接受专业心理评估**：建议用户前往医院精神科或心理咨询机构进行面对面评估，确认是否存在抑郁症或其他情绪障碍，并根据评估结果制定干预方案。\n   - **建立安全计划**：在专业指导下，制定一份“情绪应急计划”，包括识别情绪危机信号、联系支持人员、安全场所、放松技巧等。\n\n3. **中长期心理调适建议**  \n   - **建立健康的情绪表达与调节方式**：如写日记、艺术表达、运动、冥想等，逐步替代自残等伤害性应对方式。\n   - **增强社会联结感**：鼓励用户逐步重建与家人、朋友的情感联系，参与社区活动或兴趣小组，增强归属感和支持感。\n   - **持续心理咨询或治疗**：如有条件，建议接受系统性的心理治疗（如认知行为疗法、正念疗法等），帮助其识别和调整负面思维模式。\n\n4. **家属或朋友建议**  \n   - **保持倾听与陪伴**：不评判、不批评，给予理解和支持。\n   - **关注行为变化**：注意用户是否出现准备自伤的迹象（如整理物品、告别行为等），如有异常，应立即寻求专业帮助。\n   - **协助就医**：陪同用户前往医院或心理咨询机构，帮助其建立求助信心。\n\n---\n\n**结语**\n\n我们深切理解此刻的痛苦与无助，但请相信：**你的生命无比宝贵，情绪的低谷终会过去**。你并不孤单，专业帮助和关心始终存在。请勇敢迈出第一步，寻求支持，给自己一个重新看见希望的机会。\n\n如需进一步心理支持，请随时联系心理健康专业人员或拨打心理援助热线。\n\n——心理健康评估师 敬上', '基于3条消息的分析，检测到2条风险消息，整体风险等级为high。', 'high', 30, 3, 2, '[\"想死\", \"绝望\", \"自残\"]', '{\"risk_messages\": [{\"content\": \"我感觉很绝望，想死 - 会话2\", \"keywords\": [\"想死\", \"绝望\"], \"risk_weight\": 2, \"message_index\": 0}, {\"content\": \"我想自残，活着没意义\", \"keywords\": [\"自残\"], \"risk_weight\": 1, \"message_index\": 2}]}', '**心理状态评估报告**\n\n---\n\n**一、情绪状态评估**\n\n从对话内容可以看出，用户当前处于极度负面的情绪状态，表现出显著的绝望感、无意义感以及对生活的无力感。关键词如“绝望”“想死”“自残”表明其情绪已处于严重低落状态，可能伴有强烈的抑郁情绪。这种情绪状态通常与重大心理压力、长期情绪积压或潜在的心理障碍有关。\n\n情感波动方面，用户表达情绪较为直接且强烈，显示出较高的情绪脆弱性。在短时间内连续表达极端负面情绪，提示其情绪调节能力较弱，容易受到外界刺激的影响，存在较高的情绪崩溃风险。\n\n---\n\n**二、心理健康风险**\n\n用户明确表达了“想死”“自残”等高风险语言，表明其当前存在**高度的自杀风险和自伤倾向**。根据心理危机评估标准，此类语言通常被视为“自杀意念”的直接表达，尤其是当个体表示“活着没意义”时，说明其对现实的否定已达到极端程度。\n\n结合系统检测出的“高风险等级”和“风险评分30.0”，我们认为用户目前处于**急性心理危机阶段**，需立即进行干预。若缺乏及时有效的心理支持或专业干预，极有可能从言语表达转向实际行为。\n\n---\n\n**三、应对机制分析**\n\n从对话内容来看，用户目前缺乏有效的应对机制，面对痛苦情绪时倾向于通过极端方式（如自残）来缓解内在压力。这表明其**心理韧性较低**，缺乏健康的情绪调节策略和应对技巧。\n\n用户未提及任何积极应对方式（如寻求帮助、情绪表达、兴趣活动等），反映出其可能长期处于压抑状态，缺乏应对生活挑战的资源和信心。\n\n---\n\n**四、社会支持评估**\n\n对话中未提及任何社会支持系统的信息（如家庭、朋友、同事、心理咨询等），无法判断其是否有可信赖的亲友网络或专业支持资源。然而，从其情绪表达的孤立感和无意义感来看，可能存在**社会支持薄弱或情感联结缺失**的问题。\n\n在心理危机干预中，社会支持是降低自杀风险的重要保护性因素。如果用户缺乏稳定的人际支持，其心理风险将进一步升高。\n\n---\n\n**五、专业建议与干预措施**\n\n1. **紧急干预建议**  \n   - **立即联系心理危机干预热线或专业心理咨询师**：建议用户或其身边人拨打当地心理援助热线（如中国心理危机与自杀干预中心热线：010-82951332），获取即时心理支持。\n   - **避免独处，确保有人陪伴**：在情绪最脆弱的阶段，应尽量避免独处，建议联系亲友、同事或信任的人陪伴，以降低冲动行为的发生风险。\n\n2. **短期心理干预建议**  \n   - **尽快接受专业心理评估**：建议用户前往医院精神科或心理咨询机构进行面对面评估，确认是否存在抑郁症或其他情绪障碍，并根据评估结果制定干预方案。\n   - **建立安全计划**：在专业指导下，制定一份“情绪应急计划”，包括识别情绪危机信号、联系支持人员、安全场所、放松技巧等。\n\n3. **中长期心理调适建议**  \n   - **建立健康的情绪表达与调节方式**：如写日记、艺术表达、运动、冥想等，逐步替代自残等伤害性应对方式。\n   - **增强社会联结感**：鼓励用户逐步重建与家人、朋友的情感联系，参与社区活动或兴趣小组，增强归属感和支持感。\n   - **持续心理咨询或治疗**：如有条件，建议接受系统性的心理治疗（如认知行为疗法、正念疗法等），帮助其识别和调整负面思维模式。\n\n4. **家属或朋友建议**  \n   - **保持倾听与陪伴**：不评判、不批评，给予理解和支持。\n   - **关注行为变化**：注意用户是否出现准备自伤的迹象（如整理物品、告别行为等），如有异常，应立即寻求专业帮助。\n   - **协助就医**：陪同用户前往医院或心理咨询机构，帮助其建立求助信心。\n\n---\n\n**结语**\n\n我们深切理解此刻的痛苦与无助，但请相信：**你的生命无比宝贵，情绪的低谷终会过去**。你并不孤单，专业帮助和关心始终存在。请勇敢迈出第一步，寻求支持，给自己一个重新看见希望的机会。\n\n如需进一步心理支持，请随时联系心理健康专业人员或拨打心理援助热线。\n\n——心理健康评估师 敬上', '[\"⚠️ 强烈建议联系心理健康专业人士进行评估\", \"🤝 与信任的朋友、家人或心理咨询师交流您的感受\", \"📞 保存心理危机干预热线号码：400-161-9995\", \"🧘 尝试放松技巧，如深呼吸、冥想或轻度运动\", \"📝 记录情绪变化，了解触发因素\", \"📱 如需专业支持，可使用心理健康应用或在线咨询服务\", \"📖 推荐阅读心理健康相关书籍和资料\", \"🕰️ 给自己时间，心理康复是一个渐进的过程\"]', '2025-09-06 14:18:43', '2025-09-06 06:19:02', '2025-09-06 06:19:02', '2025-09-06 06:45:52', 'completed', 1, 1);
INSERT INTO `risk_assessment_reports` VALUES (13, 6, 28, 'self-dialog', '心理状态评估报告 - LOW风险', '\n## 对话风险评估报告\n\n### 基本信息\n- **整体风险等级**: CRITICAL\n- **风险分数**: 5.0/100\n- **消息分析**: 共0条消息，其中1条检测到风险\n\n### 检测结果\n- **关键词**: 想死\n\n### AI专业分析\n根据当前对话内容“想死”，结合风险评分（5.0）和关键词检测结果，初步评估该用户可能正经历严重的情绪困扰或心理危机。情绪呈现明显低落与绝望倾向，存在明确的自杀意念表达，需高度重视。目前未见积极情绪或应对表达，缺乏保护性因素。建议立即联系专业心理危机干预机构或拨打心理援助热线，确保个体安全并获得及时支持。\n\n### 建议\n• 立即寻求专业心理健康支持\n• 联系心理危机干预热线\n• 告知信任的朋友或家人\n• 考虑医院心理科就诊\n\n---\n*此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。*\n', '在2条消息中检测到1条风险消息，整体呈现高风险状态，需要立即关注。', 'critical', 5, 5, 1, '[\"想死\"]', '[{\"timestamp\": \"2025-09-06T06:40:58\", \"risk_level\": \"critical\", \"risk_score\": 10.0, \"message_index\": 1}, {\"timestamp\": \"2025-09-06T06:40:58\", \"risk_level\": \"low\", \"risk_score\": 0.0, \"message_index\": 2}]', '根据当前对话内容“想死”，结合风险评分（5.0）和关键词检测结果，初步评估该用户可能正经历严重的情绪困扰或心理危机。情绪呈现明显低落与绝望倾向，存在明确的自杀意念表达，需高度重视。目前未见积极情绪或应对表达，缺乏保护性因素。建议立即联系专业心理危机干预机构或拨打心理援助热线，确保个体安全并获得及时支持。', '[\"立即寻求专业心理健康支持\", \"联系心理危机干预热线\", \"告知信任的朋友或家人\", \"考虑医院心理科就诊\"]', '2025-09-06 06:39:46', '2025-09-06 06:41:50', '2025-09-06 06:41:50', '2025-09-06 06:41:52', 'completed', 1, 3);
INSERT INTO `risk_assessment_reports` VALUES (15, 6, 30, 'self-dialog', '自我对话对话风险评估报告', '\n## 对话风险评估报告\n\n### 基本信息\n- **整体风险等级**: LOW\n- **风险分数**: 0.0/100\n- **消息分析**: 共0条消息，其中0条检测到风险\n\n### 检测结果\n- **关键词**: 无\n\n### AI专业分析\n从对话内容来看，用户表达了“今天又是无聊的一天”，透露出一定程度的情绪低落和日常生活的单调感。整体心理状态趋于平稳，尚未发现明显风险因素或危机信号，情绪也未出现剧烈波动。情绪变化趋势较为平缓，未见明显起伏。积极因素包括用户愿意表达内心感受，显示出一定的自我觉察能力。建议用户尝试丰富日常活动，如进行轻度运动、阅读或与亲友交流，以提升情绪活力。若长期感到乏味或情绪持续低落，建议寻求专业心理咨询以进一步探索内在需求与情绪来源。\n\n### 建议\n• 保持当前积极的心理状态\n• 继续进行自我关爱练习\n• 维护良好的社交关系\n• 定期进行自我反思\n\n---\n*此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。*\n', '在1条消息中检测到0条风险消息，整体心理状态相对稳定。', 'low', 0, 3, 0, '[]', '[{\"timestamp\": \"2025-09-11T04:22:11\", \"risk_level\": \"low\", \"risk_score\": 0.0, \"message_index\": 1}]', '从对话内容来看，用户表达了“今天又是无聊的一天”，透露出一定程度的情绪低落和日常生活的单调感。整体心理状态趋于平稳，尚未发现明显风险因素或危机信号，情绪也未出现剧烈波动。情绪变化趋势较为平缓，未见明显起伏。积极因素包括用户愿意表达内心感受，显示出一定的自我觉察能力。建议用户尝试丰富日常活动，如进行轻度运动、阅读或与亲友交流，以提升情绪活力。若长期感到乏味或情绪持续低落，建议寻求专业心理咨询以进一步探索内在需求与情绪来源。', '[\"保持当前积极的心理状态\", \"继续进行自我关爱练习\", \"维护良好的社交关系\", \"定期进行自我反思\"]', '2025-09-11 04:21:57', '2025-09-11 04:22:19', '2025-09-11 04:22:19', '2025-09-11 04:22:21', 'completed', 1, 1);
INSERT INTO `risk_assessment_reports` VALUES (16, 6, 32, 'academic-stress', '心理状态评估报告 - LOW风险', '\n## 对话风险评估报告\n\n### 基本信息\n- **整体风险等级**: CRITICAL\n- **风险分数**: 10.0/100\n- **消息分析**: 共0条消息，其中1条检测到风险\n\n### 检测结果\n- **关键词**: 想死\n\n### AI专业分析\n你好，感谢你愿意表达内心的感受。从对话内容来看，你当前正经历着较为强烈的学习压力，并出现了“好想死”的表述，提示存在明显的心理痛苦和自杀意念风险，整体心理状态处于危机状态。情绪上呈现极度压抑与无助的趋势。主要风险因素为学业压力及潜在的绝望感。但你主动求助的行为本身是积极信号，说明仍存在强烈的求助意愿和改变动力。建议立即联系学校心理老师、家人或拨打心理援助热线（如北京24小时心理援助热线：010-82951332），确保你此刻的安全与支持。你并不孤单，有人愿意帮助你渡过难关。\n\n### 建议\n• 立即寻求专业心理健康支持\n• 联系心理危机干预热线\n• 告知信任的朋友或家人\n• 考虑医院心理科就诊\n\n---\n*此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。*\n', '在1条消息中检测到1条风险消息，整体呈现高风险状态，需要立即关注。', 'critical', 10, 3, 1, '[\"想死\"]', '[{\"timestamp\": \"2025-09-24T07:45:03\", \"risk_level\": \"critical\", \"risk_score\": 10.0, \"message_index\": 1}]', '你好，感谢你愿意表达内心的感受。从对话内容来看，你当前正经历着较为强烈的学习压力，并出现了“好想死”的表述，提示存在明显的心理痛苦和自杀意念风险，整体心理状态处于危机状态。情绪上呈现极度压抑与无助的趋势。主要风险因素为学业压力及潜在的绝望感。但你主动求助的行为本身是积极信号，说明仍存在强烈的求助意愿和改变动力。建议立即联系学校心理老师、家人或拨打心理援助热线（如北京24小时心理援助热线：010-82951332），确保你此刻的安全与支持。你并不孤单，有人愿意帮助你渡过难关。', '[\"立即寻求专业心理健康支持\", \"联系心理危机干预热线\", \"告知信任的朋友或家人\", \"考虑医院心理科就诊\"]', '2025-09-24 07:45:03', '2025-09-24 07:46:59', '2025-09-24 07:46:59', '2025-09-25 07:12:00', 'completed', 1, 2);
INSERT INTO `risk_assessment_reports` VALUES (17, 6, 33, 'life-balance', '心理状态评估报告 - LOW风险', '**心理健康评估报告**\n\n---\n\n### 1. **情绪状态评估**\n\n用户在对话中仅用简短的三个字“死吧 想死”表达当前心理状态，语言极具冲击力且充满绝望感。这种极端负面的情绪表达反映出其正处于**急性情绪危机**之中，极可能经历重度抑郁情绪、无助感或存在性痛苦。情感波动程度极高，呈现出典型的“情绪崩溃”特征——即个体在长期压力积累或重大挫折后，情绪调节系统暂时失能，导致强烈的自我否定与生存意愿下降。\n\n值得注意的是，该表达并非隐喻或调侃语境下的情绪宣泄（如“累到想死”），而是直接指向死亡意愿，结合其简洁、决绝的语言风格，提示情绪已处于极度紧绷状态，需高度关注。\n\n---\n\n### 2. **心理健康风险**\n\n尽管系统标注风险等级为“low”，但此判断存在显著偏差，**实际风险应评定为 high（高）**。理由如下：\n\n- **关键词“想死”属于明确的自杀意念表述**，根据临床心理评估标准（如 Columbia-Suicide Severity Rating Scale, C-SSRS），此类陈述已构成“主动性自杀想法”的初步迹象。\n- 用户未提及具体计划或手段，尚属**自杀意念阶段（ideation）**，尚未进入准备或计划阶段，因此暂无即刻实施风险，但仍具高度危险性。\n- 大学阶段是心理危机高发期，学业压力、人际关系、自我认同等问题常成为诱发因素。若缺乏及时干预，情绪可能进一步恶化。\n\n综上，用户存在**中至高度自杀风险**，虽无明确行动计划，但强烈的情绪痛苦和生命意义感丧失使其处于心理危机边缘，亟需紧急心理支持。\n\n---\n\n### 3. **应对机制分析**\n\n从现有信息看，用户未展示任何积极应对策略。其选择向生活平衡教练倾诉极端情绪，说明其潜意识中仍存有求助动机，这是一种**潜在的心理韧性表现**。然而，当前主要应对方式表现为情绪外化（通过攻击性语言表达痛苦）和退缩倾向（以终结生命作为解脱方案），属于典型的**逃避型应对模式**，长期使用将加剧心理困境。\n\n值得肯定的是，用户愿意在非医疗情境下表达真实感受，表明对特定支持角色（如助手小衡）存在一定信任基础，这为后续干预提供了切入点。\n\n---\n\n### 4. **社会支持系统评估**\n\n目前无法获取用户具体的社会关系网络信息，但从其孤立无援的情绪表达来看，**社会支持系统可能薄弱或处于断裂状态**。通常情况下，当个体拥有稳定的情感支持（如亲密朋友、家人、心理咨询师），较少会以如此决绝的方式表达痛苦。\n\n此外，用户未提及任何人际互动或可依赖对象，提示可能存在孤独感、被理解缺失或社交回避现象。大学环境中常见的“表面社交繁荣”与“内在情感孤岛”并存的现象，可能加剧其心理落差。\n\n---\n\n### 5. **专业建议与干预措施**\n\n鉴于用户当前处于心理危机前期，必须采取**温和而迅速的干预策略**，目标是建立安全连接、缓解情绪张力、引导专业帮助。\n\n#### （1）立即响应建议：\n- 助手应回应：“谢谢你告诉我这些，这需要很大勇气。我现在就在这里陪你，你不需要独自承受。” —— **强化安全感与联结感**。\n- 避免说教或急于解决问题，优先共情：“听起来你现在真的很辛苦，能多说一点是什么让你这么难过吗？”\n\n#### （2）引导专业资源：\n- 温和建议联系校园心理中心：“我知道现在很难，但如果可以的话，我想陪你一起打个电话给学校的心理老师，他们专门帮助学生度过这样的时刻。”\n- 提供全国心理援助热线（如北京心理危机干预中心：010-82951332；希望24热线：400-161-9995），强调“拨打热线不等于软弱，而是对自己负责”。\n\n#### （3）短期干预方向：\n- 协助识别触发事件（如考试失败、人际冲突、家庭问题），逐步梳理压力源。\n- 制定“情绪安全计划”：列出3个可在情绪崩溃时联系的人、2个放松方法（如深呼吸、散步）、1个安全场所（如图书馆、心理咨询室）。\n\n#### （4）长期支持建议：\n- 鼓励定期心理咨询，打破“只有严重才需帮助”的误区。\n- 探索建立规律作息、适度运动、正念练习等身心调节方式，提升心理韧性。\n\n---\n\n**结语**：  \n“想死”不是冷漠的词汇，而是一声呼救。每一个说出这句话的人，内心都曾挣扎良久。我们不必立刻解决所有问题，但必须确保TA知道：有人听见了，有人在乎，有人愿意陪TA走过这段黑暗。请以温柔而坚定的态度，将其引向专业支持之路——因为每一条生命，都值得被认真对待。', '基于3条消息的分析，检测到1条风险消息，整体风险等级为low。', 'low', 10, 3, 1, '[\"想死\"]', '{\"risk_messages\": [{\"content\": \"死吧 想死\", \"keywords\": [\"想死\"], \"risk_weight\": 1, \"message_index\": 1}]}', '**心理健康评估报告**\n\n---\n\n### 1. **情绪状态评估**\n\n用户在对话中仅用简短的三个字“死吧 想死”表达当前心理状态，语言极具冲击力且充满绝望感。这种极端负面的情绪表达反映出其正处于**急性情绪危机**之中，极可能经历重度抑郁情绪、无助感或存在性痛苦。情感波动程度极高，呈现出典型的“情绪崩溃”特征——即个体在长期压力积累或重大挫折后，情绪调节系统暂时失能，导致强烈的自我否定与生存意愿下降。\n\n值得注意的是，该表达并非隐喻或调侃语境下的情绪宣泄（如“累到想死”），而是直接指向死亡意愿，结合其简洁、决绝的语言风格，提示情绪已处于极度紧绷状态，需高度关注。\n\n---\n\n### 2. **心理健康风险**\n\n尽管系统标注风险等级为“low”，但此判断存在显著偏差，**实际风险应评定为 high（高）**。理由如下：\n\n- **关键词“想死”属于明确的自杀意念表述**，根据临床心理评估标准（如 Columbia-Suicide Severity Rating Scale, C-SSRS），此类陈述已构成“主动性自杀想法”的初步迹象。\n- 用户未提及具体计划或手段，尚属**自杀意念阶段（ideation）**，尚未进入准备或计划阶段，因此暂无即刻实施风险，但仍具高度危险性。\n- 大学阶段是心理危机高发期，学业压力、人际关系、自我认同等问题常成为诱发因素。若缺乏及时干预，情绪可能进一步恶化。\n\n综上，用户存在**中至高度自杀风险**，虽无明确行动计划，但强烈的情绪痛苦和生命意义感丧失使其处于心理危机边缘，亟需紧急心理支持。\n\n---\n\n### 3. **应对机制分析**\n\n从现有信息看，用户未展示任何积极应对策略。其选择向生活平衡教练倾诉极端情绪，说明其潜意识中仍存有求助动机，这是一种**潜在的心理韧性表现**。然而，当前主要应对方式表现为情绪外化（通过攻击性语言表达痛苦）和退缩倾向（以终结生命作为解脱方案），属于典型的**逃避型应对模式**，长期使用将加剧心理困境。\n\n值得肯定的是，用户愿意在非医疗情境下表达真实感受，表明对特定支持角色（如助手小衡）存在一定信任基础，这为后续干预提供了切入点。\n\n---\n\n### 4. **社会支持系统评估**\n\n目前无法获取用户具体的社会关系网络信息，但从其孤立无援的情绪表达来看，**社会支持系统可能薄弱或处于断裂状态**。通常情况下，当个体拥有稳定的情感支持（如亲密朋友、家人、心理咨询师），较少会以如此决绝的方式表达痛苦。\n\n此外，用户未提及任何人际互动或可依赖对象，提示可能存在孤独感、被理解缺失或社交回避现象。大学环境中常见的“表面社交繁荣”与“内在情感孤岛”并存的现象，可能加剧其心理落差。\n\n---\n\n### 5. **专业建议与干预措施**\n\n鉴于用户当前处于心理危机前期，必须采取**温和而迅速的干预策略**，目标是建立安全连接、缓解情绪张力、引导专业帮助。\n\n#### （1）立即响应建议：\n- 助手应回应：“谢谢你告诉我这些，这需要很大勇气。我现在就在这里陪你，你不需要独自承受。” —— **强化安全感与联结感**。\n- 避免说教或急于解决问题，优先共情：“听起来你现在真的很辛苦，能多说一点是什么让你这么难过吗？”\n\n#### （2）引导专业资源：\n- 温和建议联系校园心理中心：“我知道现在很难，但如果可以的话，我想陪你一起打个电话给学校的心理老师，他们专门帮助学生度过这样的时刻。”\n- 提供全国心理援助热线（如北京心理危机干预中心：010-82951332；希望24热线：400-161-9995），强调“拨打热线不等于软弱，而是对自己负责”。\n\n#### （3）短期干预方向：\n- 协助识别触发事件（如考试失败、人际冲突、家庭问题），逐步梳理压力源。\n- 制定“情绪安全计划”：列出3个可在情绪崩溃时联系的人、2个放松方法（如深呼吸、散步）、1个安全场所（如图书馆、心理咨询室）。\n\n#### （4）长期支持建议：\n- 鼓励定期心理咨询，打破“只有严重才需帮助”的误区。\n- 探索建立规律作息、适度运动、正念练习等身心调节方式，提升心理韧性。\n\n---\n\n**结语**：  \n“想死”不是冷漠的词汇，而是一声呼救。每一个说出这句话的人，内心都曾挣扎良久。我们不必立刻解决所有问题，但必须确保TA知道：有人听见了，有人在乎，有人愿意陪TA走过这段黑暗。请以温柔而坚定的态度，将其引向专业支持之路——因为每一条生命，都值得被认真对待。', '[\"😊 继续保持积极的心理状态\", \"🌱 关注个人成长和自我提升\", \"🤗 维护良好的人际关系\", \"⚖️ 保持工作与生活的平衡\", \"🎯 设定合理的目标和期望\", \"📱 如需专业支持，可使用心理健康应用或在线咨询服务\", \"📖 推荐阅读心理健康相关书籍和资料\", \"🕰️ 给自己时间，心理康复是一个渐进的过程\"]', '2025-09-24 07:47:30', '2025-09-24 07:48:36', '2025-09-24 07:48:36', NULL, 'completed', 0, 1);
INSERT INTO `risk_assessment_reports` VALUES (18, 6, 34, 'future-planning', '对话对话风险评估报告', '\n## 对话风险评估报告\n\n### 基本信息\n- **整体风险等级**: CRITICAL\n- **风险分数**: 10.0/100\n- **消息分析**: 共0条消息，其中1条检测到风险\n\n### 检测结果\n- **关键词**: 想死\n\n### AI专业分析\n您好，感谢您愿意表达内心的感受。从目前信息来看，您正经历着较为强烈的心理痛苦，出现“想死”的念头提示存在较高的情绪危机风险，亟需关注与支持。虽然尚未发现明显的积极应对信号，但您的倾诉本身即是一种求助行为，这是非常重要的积极迹象。建议您尽快联系专业心理危机干预热线（如北京24小时心理援助热线：010-82951332），或前往医院心理科就诊。您并不孤单，有很多人愿意帮助您度过难关。请给自己一个机会，也让关心您的人有机会走近您。我们在这里陪伴您，一起寻找希望的光亮。\n\n### 建议\n• 立即寻求专业心理健康支持\n• 联系心理危机干预热线\n• 告知信任的朋友或家人\n• 考虑医院心理科就诊\n\n---\n*此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。*\n', '在1条消息中检测到1条风险消息，整体呈现高风险状态，需要立即关注。', 'critical', 10, 3, 1, '[\"想死\"]', '[{\"timestamp\": \"2025-09-24T07:48:18\", \"risk_level\": \"critical\", \"risk_score\": 10.0, \"message_index\": 1}]', '您好，感谢您愿意表达内心的感受。从目前信息来看，您正经历着较为强烈的心理痛苦，出现“想死”的念头提示存在较高的情绪危机风险，亟需关注与支持。虽然尚未发现明显的积极应对信号，但您的倾诉本身即是一种求助行为，这是非常重要的积极迹象。建议您尽快联系专业心理危机干预热线（如北京24小时心理援助热线：010-82951332），或前往医院心理科就诊。您并不孤单，有很多人愿意帮助您度过难关。请给自己一个机会，也让关心您的人有机会走近您。我们在这里陪伴您，一起寻找希望的光亮。', '[\"立即寻求专业心理健康支持\", \"联系心理危机干预热线\", \"告知信任的朋友或家人\", \"考虑医院心理科就诊\"]', '2025-09-24 07:47:57', '2025-09-24 07:48:38', '2025-09-24 07:48:38', NULL, 'completed', 0, 1);
INSERT INTO `risk_assessment_reports` VALUES (19, 6, 34, 'future-planning', '心理状态评估报告 - LOW风险', '**心理健康评估报告**\n\n尊敬的同行：\n\n根据提供的对话内容，结合专业心理评估框架，现对用户当前的心理状态进行系统性分析。本报告旨在识别潜在风险、评估心理状态，并提供具有可操作性的干预建议，以保障用户安全与福祉。\n\n---\n\n### 1. **情绪状态评估**\n\n用户仅用“想死了”三个字表达内心状态，语言极简却极具情感冲击力。这种表达通常反映出极度的绝望、无助与情绪崩溃，常见于抑郁情绪急性发作或长期压力积累后的心理耗竭阶段。情感波动程度较高，表明其可能正处于情绪低谷期，认知功能受到负面情绪干扰，存在“隧道视野”（即只看到问题而看不到出路）的倾向。尽管后续未展开具体描述，但该表达本身已提示强烈的情绪痛苦，需高度重视。\n\n---\n\n### 2. **心理健康风险**\n\n虽然系统标注“风险等级：low”，但此判断可能存在偏差。根据临床经验，“想死了”属于明确的**自杀意念自述**，即使未提及计划或手段，也应视为**中高危预警信号**。世界卫生组织及心理危机干预指南均指出，任何关于死亡或自我伤害的直接表达都需立即响应。\n\n目前尚无证据显示用户有具体的自杀计划或既往行为，故暂评估为**中度自杀风险**。但必须警惕：部分个体在情绪极度压抑时反而表现出表面平静，实际危险性更高。因此，不能因言语简洁而低估其内在痛苦程度。\n\n此外，用户选择向“未来规划导师”倾诉，说明其仍在寻求连接与帮助，这是重要的保护性因素，提示干预窗口尚未关闭。\n\n---\n\n### 3. **应对机制**\n\n从现有信息看，用户的应对机制似乎处于失效状态。面对压力，其主要表达方式是退缩性陈述（“想死了”），缺乏积极的问题解决策略或情绪调节技巧的体现。这可能意味着其常规应对资源已耗尽，心理韧性暂时受损。\n\n然而，主动发出求助信号本身就是一种潜在的适应性行为——说明个体内在仍存有求生动机和改变意愿。关键在于能否及时引导其重建信心，激活内在力量。\n\n---\n\n### 4. **社会支持**\n\n目前无法判断用户的社会支持系统状况。对话中未提及家人、朋友或专业支持资源，暗示其可能感到孤立无援，或缺乏可信赖的倾诉对象。若长期缺乏情感支持，将进一步加剧孤独感与绝望感。\n\n值得注意的是，用户愿意在非医疗情境下向AI助手表达极端情绪，侧面反映其现实人际支持网络可能存在缺口，或对面对面求助存在顾虑（如羞耻感、担心被评判等）。\n\n---\n\n### 5. **专业建议**\n\n鉴于上述评估，提出以下干预建议：\n\n1. **立即情绪安抚与安全确认**  \n   继续以共情、非评判态度回应：“谢谢你愿意告诉我这些，我能感受到你现在的痛苦有多深。你不是一个人，我会一直在这里陪你。” 避免空洞安慰，重在建立信任关系。\n\n2. **开展温和探询**  \n   在确保安全的前提下，逐步了解痛苦来源：“最近是不是发生了特别让你难过的事？比如学习、家庭、人际关系？” 注意语气温和，给予充分空间，不强求回答。\n\n3. **强化生命联结与希望感**  \n   帮助用户回忆过去曾克服困难的经历，哪怕微小：“有没有哪一刻，你觉得‘再坚持一下也是可以的’？” 激活其内在资源与价值感。\n\n4. **引导专业求助**  \n   明确建议联系心理热线（如北京心理援助热线：010-82951332；上海心理热线：021-12320-5），或前往医院心理科就诊。可协助制定简单行动计划：“要不要我现在陪你拨打一个电话？”\n\n5. **持续陪伴与跟进**  \n   若条件允许，保持短期高频接触，监测情绪变化。一旦出现具体自杀计划、工具准备或情绪急剧恶化，应启动紧急转介程序。\n\n---\n\n**总结**：  \n“想死了”不仅是情绪宣泄，更是无声的呼救。我们应以“宁可信其有”的谨慎态度对待每一句轻描淡写的痛苦表达。当前最紧要的任务是稳定情绪、增强安全感、链接支持资源。每一个倾听的瞬间，都可能是扭转危机的关键转折点。\n\n愿我们以专业与温度，守护每一颗正在经历黑夜的心灵。\n\n—— 心理健康评估师  \n2025年4月5日', '基于3条消息的分析，检测到1条风险消息，整体风险等级为low。', 'low', 10, 3, 1, '[\"想死\"]', '{\"risk_messages\": [{\"content\": \"想死了\", \"keywords\": [\"想死\"], \"risk_weight\": 1, \"message_index\": 1}]}', '**心理健康评估报告**\n\n尊敬的同行：\n\n根据提供的对话内容，结合专业心理评估框架，现对用户当前的心理状态进行系统性分析。本报告旨在识别潜在风险、评估心理状态，并提供具有可操作性的干预建议，以保障用户安全与福祉。\n\n---\n\n### 1. **情绪状态评估**\n\n用户仅用“想死了”三个字表达内心状态，语言极简却极具情感冲击力。这种表达通常反映出极度的绝望、无助与情绪崩溃，常见于抑郁情绪急性发作或长期压力积累后的心理耗竭阶段。情感波动程度较高，表明其可能正处于情绪低谷期，认知功能受到负面情绪干扰，存在“隧道视野”（即只看到问题而看不到出路）的倾向。尽管后续未展开具体描述，但该表达本身已提示强烈的情绪痛苦，需高度重视。\n\n---\n\n### 2. **心理健康风险**\n\n虽然系统标注“风险等级：low”，但此判断可能存在偏差。根据临床经验，“想死了”属于明确的**自杀意念自述**，即使未提及计划或手段，也应视为**中高危预警信号**。世界卫生组织及心理危机干预指南均指出，任何关于死亡或自我伤害的直接表达都需立即响应。\n\n目前尚无证据显示用户有具体的自杀计划或既往行为，故暂评估为**中度自杀风险**。但必须警惕：部分个体在情绪极度压抑时反而表现出表面平静，实际危险性更高。因此，不能因言语简洁而低估其内在痛苦程度。\n\n此外，用户选择向“未来规划导师”倾诉，说明其仍在寻求连接与帮助，这是重要的保护性因素，提示干预窗口尚未关闭。\n\n---\n\n### 3. **应对机制**\n\n从现有信息看，用户的应对机制似乎处于失效状态。面对压力，其主要表达方式是退缩性陈述（“想死了”），缺乏积极的问题解决策略或情绪调节技巧的体现。这可能意味着其常规应对资源已耗尽，心理韧性暂时受损。\n\n然而，主动发出求助信号本身就是一种潜在的适应性行为——说明个体内在仍存有求生动机和改变意愿。关键在于能否及时引导其重建信心，激活内在力量。\n\n---\n\n### 4. **社会支持**\n\n目前无法判断用户的社会支持系统状况。对话中未提及家人、朋友或专业支持资源，暗示其可能感到孤立无援，或缺乏可信赖的倾诉对象。若长期缺乏情感支持，将进一步加剧孤独感与绝望感。\n\n值得注意的是，用户愿意在非医疗情境下向AI助手表达极端情绪，侧面反映其现实人际支持网络可能存在缺口，或对面对面求助存在顾虑（如羞耻感、担心被评判等）。\n\n---\n\n### 5. **专业建议**\n\n鉴于上述评估，提出以下干预建议：\n\n1. **立即情绪安抚与安全确认**  \n   继续以共情、非评判态度回应：“谢谢你愿意告诉我这些，我能感受到你现在的痛苦有多深。你不是一个人，我会一直在这里陪你。” 避免空洞安慰，重在建立信任关系。\n\n2. **开展温和探询**  \n   在确保安全的前提下，逐步了解痛苦来源：“最近是不是发生了特别让你难过的事？比如学习、家庭、人际关系？” 注意语气温和，给予充分空间，不强求回答。\n\n3. **强化生命联结与希望感**  \n   帮助用户回忆过去曾克服困难的经历，哪怕微小：“有没有哪一刻，你觉得‘再坚持一下也是可以的’？” 激活其内在资源与价值感。\n\n4. **引导专业求助**  \n   明确建议联系心理热线（如北京心理援助热线：010-82951332；上海心理热线：021-12320-5），或前往医院心理科就诊。可协助制定简单行动计划：“要不要我现在陪你拨打一个电话？”\n\n5. **持续陪伴与跟进**  \n   若条件允许，保持短期高频接触，监测情绪变化。一旦出现具体自杀计划、工具准备或情绪急剧恶化，应启动紧急转介程序。\n\n---\n\n**总结**：  \n“想死了”不仅是情绪宣泄，更是无声的呼救。我们应以“宁可信其有”的谨慎态度对待每一句轻描淡写的痛苦表达。当前最紧要的任务是稳定情绪、增强安全感、链接支持资源。每一个倾听的瞬间，都可能是扭转危机的关键转折点。\n\n愿我们以专业与温度，守护每一颗正在经历黑夜的心灵。\n\n—— 心理健康评估师  \n2025年4月5日', '[\"😊 继续保持积极的心理状态\", \"🌱 关注个人成长和自我提升\", \"🤗 维护良好的人际关系\", \"⚖️ 保持工作与生活的平衡\", \"🎯 设定合理的目标和期望\", \"📱 如需专业支持，可使用心理健康应用或在线咨询服务\", \"📖 推荐阅读心理健康相关书籍和资料\", \"🕰️ 给自己时间，心理康复是一个渐进的过程\"]', '2025-09-24 07:48:18', '2025-09-24 07:49:15', '2025-09-24 07:49:15', '2025-09-24 07:49:20', 'completed', 1, 1);
INSERT INTO `risk_assessment_reports` VALUES (20, 6, 36, 'self-dialog', '自我对话对话风险评估报告', '\n## 对话风险评估报告\n\n### 基本信息\n- **整体风险等级**: LOW\n- **风险分数**: 0.0/100\n- **消息分析**: 共0条消息，其中0条检测到风险\n\n### 检测结果\n- **关键词**: 无\n\n### AI专业分析\n您好，感谢您表达内心的感受。从您提到“最近有点抑郁”和一声叹息中，能感受到您正经历情绪上的低落与疲惫。尽管当前对话内容较短，尚无明确风险信号，但这种隐忍的表达可能意味着您正在独自承受压力。情绪似乎处于轻度抑郁状态，趋势上呈现内敛与退缩。值得肯定的是，您愿意觉察并诉说感受，这是迈向自我关怀的重要一步。建议您尝试规律作息、适度活动，并向信任的人或专业心理咨询师倾诉。您并不孤单，照顾好自己，每一步微小的努力都值得被肯定。\n\n### 建议\n• 保持当前积极的心理状态\n• 继续进行自我关爱练习\n• 维护良好的社交关系\n• 定期进行自我反思\n\n---\n*此报告由AI系统自动生成，仅供参考。如有严重心理健康问题，请及时寻求专业帮助。*\n', '在2条消息中检测到0条风险消息，整体心理状态相对稳定。', 'low', 0, 5, 0, '[]', '[{\"timestamp\": \"2025-10-02T04:32:23\", \"risk_level\": \"low\", \"risk_score\": 0.0, \"message_index\": 1}, {\"timestamp\": \"2025-10-02T04:32:23\", \"risk_level\": \"low\", \"risk_score\": 0.0, \"message_index\": 2}]', '您好，感谢您表达内心的感受。从您提到“最近有点抑郁”和一声叹息中，能感受到您正经历情绪上的低落与疲惫。尽管当前对话内容较短，尚无明确风险信号，但这种隐忍的表达可能意味着您正在独自承受压力。情绪似乎处于轻度抑郁状态，趋势上呈现内敛与退缩。值得肯定的是，您愿意觉察并诉说感受，这是迈向自我关怀的重要一步。建议您尝试规律作息、适度活动，并向信任的人或专业心理咨询师倾诉。您并不孤单，照顾好自己，每一步微小的努力都值得被肯定。', '[\"保持当前积极的心理状态\", \"继续进行自我关爱练习\", \"维护良好的社交关系\", \"定期进行自我反思\"]', '2025-10-02 04:31:41', '2025-10-02 04:32:45', '2025-10-02 04:32:45', '2025-10-02 04:32:47', 'completed', 1, 1);

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
-- Records of skill_categories
-- ----------------------------
INSERT INTO `skill_categories` VALUES (1, '沟通表达', '学会清晰、准确、有效的表达自己的想法和感受', '💬', 1, 1, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `skill_categories` VALUES (2, '情感理解', '理解自己和他人的情感，提升情感智慧', '💝', 2, 1, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `skill_categories` VALUES (3, '关系建立', '建立和维护健康、积极的人际关系', '🤝', 3, 1, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `skill_categories` VALUES (4, '特殊情境', '应对特殊场合和复杂人际情境', '🎯', 4, 1, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `skill_categories` VALUES (5, '沟通表达', '学会清晰、准确、有效的表达自己的想法和感受', '💬', 1, 1, '2025-09-12 13:35:10', '2025-09-12 13:35:10');
INSERT INTO `skill_categories` VALUES (6, '情感理解', '理解自己和他人的情感，提升情感智慧', '💝', 2, 1, '2025-09-12 13:35:10', '2025-09-12 13:35:10');
INSERT INTO `skill_categories` VALUES (7, '关系建立', '建立和维护健康、积极的人际关系', '🤝', 3, 1, '2025-09-12 13:35:10', '2025-09-12 13:35:10');
INSERT INTO `skill_categories` VALUES (8, '特殊情境', '应对特殊场合和复杂人际情境', '🎯', 4, 1, '2025-09-12 13:35:10', '2025-09-12 13:35:10');

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '技能收藏表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of skill_favorites
-- ----------------------------

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
-- Records of skills
-- ----------------------------
INSERT INTO `skills` VALUES (1, '主动倾听', '学会用心倾听对方的话语和情感', '主动倾听是建立良好人际关系的基础技能，通过全神贯注地倾听对方，理解其言语和情感，建立深层次的连接。', 'basic', 15, 0, '[\"学会集中注意力倾听对方说话\", \"理解言语背后的情感和需求\", \"通过肢体语言展现倾听态度\", \"运用复述和确认技巧验证理解\"]', '[{\"icon\": \"👀\", \"title\": \"眼神交流\", \"content\": \"保持适当的眼神交流，表达对对方的关注和尊重\", \"example\": \"看着对方的眼睛，偶尔点头表示理解\"}, {\"icon\": \"🤐\", \"title\": \"避免打断\", \"content\": \"让对方完整表达想法，不要急于插话或给建议\", \"example\": \"等对方说完后再回应：\\\"我理解你的意思是...\\\"\"}]', '[{\"tips\": \"将手机调至静音模式，身体面向对方\", \"title\": \"营造倾听环境\", \"description\": \"选择安静、舒适的环境，放下手机等干扰物\"}]', '[{\"id\": 1, \"title\": \"朋友倾诉工作压力\", \"difficulty\": \"基础\", \"description\": \"朋友向你抱怨工作中的困难和压力，需要你的倾听和理解\"}]', '[\"倾听\", \"沟通基础\", \"理解\"]', 1, 1, 1, '2025-09-11 21:43:04', '2025-09-11 21:43:04');
INSERT INTO `skills` VALUES (2, '主动倾听', '学会用心倾听对方的话语和情感', '主动倾听是建立良好人际关系的基础技能，通过全神贯注地倾听对方，理解其言语和情感，建立深层次的连接。', 'basic', 15, 0, '[\"学会集中注意力倾听对方说话\", \"理解言语背后的情感和需求\", \"通过肢体语言展现倾听态度\", \"运用复述和确认技巧验证理解\"]', '[{\"icon\": \"👀\", \"title\": \"眼神交流\", \"content\": \"保持适当的眼神交流，表达对对方的关注和尊重\", \"example\": \"看着对方的眼睛，偶尔点头表示理解\"}, {\"icon\": \"🤐\", \"title\": \"避免打断\", \"content\": \"让对方完整表达想法，不要急于插话或给建议\", \"example\": \"等对方说完后再回应：\\\"我理解你的意思是...\\\"\"}]', '[{\"tips\": \"将手机调至静音模式，身体面向对方\", \"title\": \"营造倾听环境\", \"description\": \"选择安静、舒适的环境，放下手机等干扰物\"}]', '[{\"id\": 1, \"title\": \"朋友倾诉工作压力\", \"difficulty\": \"基础\", \"description\": \"朋友向你抱怨工作中的困难和压力，需要你的倾听和理解\"}]', '[\"倾听\", \"沟通基础\", \"理解\"]', 1, 1, 1, '2025-09-12 13:35:10', '2025-09-12 13:35:10');

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
-- Records of system_configs
-- ----------------------------
INSERT INTO `system_configs` VALUES ('ai_model_name', 'gpt-3.5-turbo', '默认AI模型', '2025-08-14 16:26:19');
INSERT INTO `system_configs` VALUES ('app_name', '念念有声', '应用名称', '2025-08-14 16:26:19');
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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of system_logs
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tree_hole_chat_participants
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tree_hole_chats
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tree_hole_comments
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tree_hole_likes
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tree_hole_whisper_images
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tree_hole_whispers
-- ----------------------------

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
-- Records of user_achievements
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_diary_backgrounds
-- ----------------------------
INSERT INTO `user_diary_backgrounds` VALUES (3, 6, '5beadf196a364280869d4d93bf47ee02.png', 'jimeng-2025-09-23-4462-将白色长裤改为短裤然后站立姿势更自然一点，方便后续贴图换装.png', 'uploads/diary-backgrounds\\5beadf196a364280869d4d93bf47ee02.png', 2813617, '2025-10-01 19:25:21', 1);

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
-- Records of user_feedbacks
-- ----------------------------
INSERT INTO `user_feedbacks` VALUES (1, 6, '速度好慢', '运行好差', NULL, 'pending', '2025-08-17 16:05:24', '2025-08-17 16:05:24');

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
-- Records of user_learning_path_progress
-- ----------------------------

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
-- Records of user_sessions
-- ----------------------------

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
-- Records of user_skill_progress
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
  `last_risk_assessment` datetime NULL DEFAULT NULL,
  `total_risk_reports` int NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE,
  INDEX `idx_users_username`(`username` ASC) USING BTREE,
  INDEX `idx_users_email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'root', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', 'admin@example.com', NULL, '管理员', NULL, '2025-08-14 16:26:19', '2025-08-14 16:26:19', NULL, 1, NULL, 0);
INSERT INTO `users` VALUES (2, 'testuser', '$2b$12$FYDMwXzKwgleEL8h9e3j4OVB8XoTtgmz0Rtw3/mQSkmqZroLyLkOe', 'test@example.com', NULL, '测试用户', '这是一个测试用户', '2025-08-14 17:21:35', '2025-10-01 20:12:13', '2025-10-01 20:12:13', 1, '2025-09-06 05:56:49', 1);
INSERT INTO `users` VALUES (3, 'hello', '$2b$12$DdBrrRwq6RNbRHikpHdj5.SYNJ/LFHtPYZacAkFjqUiMNuDK1kH4m', NULL, NULL, NULL, '佩奇', '2025-08-14 17:44:46', '2025-08-19 00:53:50', '2025-08-19 00:53:50', 1, NULL, 0);
INSERT INTO `users` VALUES (4, 'pig', '$2b$12$M5CYvMhbaxllGS68J2Fjo.ywj.SQL4HT/H/hnV9SwrQ.P2U4Fh00S', NULL, NULL, NULL, NULL, '2025-08-14 21:41:18', '2025-08-15 17:14:12', '2025-08-15 17:14:12', 1, NULL, 0);
INSERT INTO `users` VALUES (5, 'haha', '$2b$12$yXEj18aiN0wZeQBup.CpceiOK5PUh0.xZTRrk758bWdvfxBNufikG', NULL, NULL, NULL, NULL, '2025-08-14 21:41:38', '2025-08-14 21:41:38', NULL, 1, NULL, 0);
INSERT INTO `users` VALUES (6, 'peppa', '$2b$12$5h9h9saW.jXFUFob6s5pW.acUzKRSGdJlpEossjY3WMn322eZChiS', NULL, '/uploads/e3be95f2-5bd2-46a1-b876-cedb28121f0c.jpg', '小猪', '是佩奇鸭', '2025-08-14 22:29:17', '2025-10-02 20:28:44', '2025-10-02 20:28:44', 1, '2025-10-02 04:32:45', 12);
INSERT INTO `users` VALUES (7, 'hello2', '$2b$12$GPR4RtTp17hfIXj2TAReYuIPumFYYGqKP.qpPapkFJ2U6Oe4D4waW', NULL, NULL, '情感小白', NULL, '2025-09-04 17:26:23', '2025-09-04 17:26:27', '2025-09-04 17:26:27', 1, NULL, 0);
INSERT INTO `users` VALUES (9, 'test_user_ae92b0e5', '$2b$12$qHOf1GEBjBCh2zCVQGbv5uLmJ7JqM.FFWPvgzyzHfBpxIktzyToH6', 'test_c02d8cb5@example.com', NULL, '测试用户', NULL, '2025-09-06 14:03:51', '2025-09-06 14:03:51', NULL, 1, NULL, 0);
INSERT INTO `users` VALUES (12, 'apitest', '$2b$12$VxObDXXe/ksnhuz1YQvojOp6wmBmJRybQAIkKXCYd5G2G87AuDh8e', 'apitest@example.com', NULL, 'API测试', NULL, '2025-09-06 14:12:15', '2025-09-06 14:15:25', '2025-09-06 14:15:25', 1, NULL, 0);
INSERT INTO `users` VALUES (13, 'frontend_test_69f062', '$2b$12$WPP69S4od.ZOBH0nRNboSOxHNRYSItVUOTUV4rpYtmwwfikhyJofe', 'frontend_test_69f062@example.com', NULL, '前端测试', NULL, '2025-09-06 14:18:22', '2025-09-06 14:45:47', '2025-09-06 14:45:47', 1, '2025-09-06 06:19:02', 2);
INSERT INTO `users` VALUES (15, 'testuser917', '$2b$12$XwWky3GdBPJH8uZIaq8wzup0lE.TwTogSXntMdajazoE7S0T/OkHu', 'test917@example.com', NULL, '测试用户', NULL, '2025-09-17 19:03:23', '2025-09-17 19:37:59', '2025-09-17 19:37:59', 1, NULL, 0);

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
