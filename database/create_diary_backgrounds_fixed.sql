-- 修正版：日记背景图片表创建脚本
-- 适用于MySQL数据库，外键引用users表的user_id列

-- 如果表已存在，先删除（可选，小心使用）
-- DROP TABLE IF EXISTS diary_backgrounds;

-- 创建日记背景图片表
CREATE TABLE IF NOT EXISTS diary_backgrounds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL COMMENT '用户ID，关联users表',
    filename VARCHAR(255) NOT NULL COMMENT '存储的文件名',
    original_filename VARCHAR(255) NOT NULL COMMENT '原始文件名',
    file_path VARCHAR(500) NOT NULL COMMENT '文件完整路径',
    file_size INT NOT NULL COMMENT '文件大小（字节）',
    mime_type VARCHAR(100) NOT NULL COMMENT 'MIME类型',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活（软删除标记）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 外键约束，引用users表的user_id列
    CONSTRAINT fk_diary_backgrounds_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_diary_backgrounds_user_id (user_id),
    INDEX idx_diary_backgrounds_active (user_id, is_active),
    INDEX idx_diary_backgrounds_created (created_at)
    
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户日记背景图片表';

-- 验证表创建结果
SELECT 'Table created successfully' AS status;
DESCRIBE diary_backgrounds;
SHOW INDEX FROM diary_backgrounds;