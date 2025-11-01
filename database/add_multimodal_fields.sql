-- 为 chat_messages 表添加多模态支持字段
-- 文件: database/add_multimodal_fields.sql

ALTER TABLE `chat_messages`
ADD COLUMN `msg_type` ENUM('text', 'img', 'multimodal') NOT NULL DEFAULT 'text' AFTER `role`,
ADD COLUMN `img_urls` JSON AFTER `content`;

-- 添加索引以提高查询效率
CREATE INDEX `idx_chat_messages_type` ON `chat_messages` (`msg_type`);

-- 查看修改后的表结构
-- SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT 
-- FROM INFORMATION_SCHEMA.COLUMNS 
-- WHERE TABLE_SCHEMA = 'ariadne' AND TABLE_NAME = 'chat_messages';
