-- 创建人际练习会话表，参考chat_sessions表结构
CREATE TABLE interpersonal_practice_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    session_title VARCHAR(255) DEFAULT '人际练习对话',
    practice_scenario VARCHAR(100) COMMENT '练习场景：self_introduction, small_talk, conflict_resolution等',
    practice_scenario_name VARCHAR(100) COMMENT '场景中文名称',
    scenario_description TEXT COMMENT '场景描述',
    messages JSON NOT NULL COMMENT '对话消息内容',
    total_messages INT DEFAULT 0 COMMENT '消息总数',
    user_messages_count INT DEFAULT 0 COMMENT '用户消息数量',
    ai_messages_count INT DEFAULT 0 COMMENT 'AI消息数量',
    practice_start_time DATETIME COMMENT '练习开始时间',
    practice_end_time DATETIME COMMENT '练习结束时间',
    practice_duration INT DEFAULT 0 COMMENT '练习时长(秒)',
    practice_quality_score DECIMAL(3,1) COMMENT '练习质量评分(0.0-10.0)',
    skills_practiced JSON COMMENT '练习的技能点',
    user_reflection TEXT COMMENT '用户练习反思',
    ai_feedback TEXT COMMENT 'AI反馈和建议',
    status ENUM('in_progress', 'completed', 'saved') DEFAULT 'saved',
    is_favorite BOOLEAN DEFAULT FALSE COMMENT '是否收藏',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_user_id (user_id),
    INDEX idx_practice_scenario (practice_scenario),
    INDEX idx_created_at (created_at),
    INDEX idx_status (status),
    
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='人际练习对话会话表';
