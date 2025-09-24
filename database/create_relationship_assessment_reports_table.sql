-- 创建关系健康评估报告表
-- file: ariadne/database/create_relationship_assessment_reports_table.sql

CREATE TABLE relationship_health_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    
    -- 评估基本信息
    relationship_type VARCHAR(50) NOT NULL,
    relationship_name VARCHAR(100) NOT NULL,
    
    -- 评估结果
    total_score DECIMAL(5,2) NOT NULL,
    total_level TEXT NOT NULL,  -- JSON格式存储等级信息
    dimension_scores TEXT NOT NULL,  -- JSON格式存储各维度得分
    questions_answered INT NOT NULL DEFAULT 0,
    
    -- AI分析结果
    ai_analysis TEXT,
    recommendations TEXT,  -- JSON格式存储建议列表
    
    -- 状态管理
    status VARCHAR(20) NOT NULL DEFAULT 'processing',
    
    -- 时间戳
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ai_started_at DATETIME,
    ai_completed_at DATETIME,
    last_viewed_at DATETIME,
    
    -- 错误处理
    error_message TEXT,
    retry_count INT NOT NULL DEFAULT 0,
    
    -- 版本控制
    version INT NOT NULL DEFAULT 1,
    
    -- 外键约束
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_user_id (user_id),
    INDEX idx_session_token (session_token),
    INDEX idx_relationship_type (relationship_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

