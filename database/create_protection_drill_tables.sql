-- 创建防护技能训练相关表

-- 防护训练类型表
CREATE TABLE protection_training_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL COMMENT '训练类型标题',
    icon VARCHAR(10) NOT NULL COMMENT '图标emoji',
    description TEXT NOT NULL COMMENT '描述',
    level INT NOT NULL DEFAULT 1 COMMENT '难度等级 1-入门 2-进阶 3-高级',
    duration VARCHAR(20) NOT NULL COMMENT '预计用时',
    skills JSON NOT NULL COMMENT '训练技能列表',
    objectives JSON NOT NULL COMMENT '训练目标列表', 
    risk_signals JSON NOT NULL COMMENT '风险信号列表',
    strategies JSON NOT NULL COMMENT '保护策略列表',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 防护训练题目表
CREATE TABLE protection_drill_questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    training_type_id INT NOT NULL COMMENT '关联训练类型ID',
    title VARCHAR(200) NOT NULL COMMENT '题目标题',
    description TEXT NOT NULL COMMENT '场景描述',
    dialogue JSON NOT NULL COMMENT '对话内容',
    question_title VARCHAR(100) NOT NULL COMMENT '问题标题',
    question_text TEXT NOT NULL COMMENT '问题内容',
    options JSON NOT NULL COMMENT '选项列表',
    correct_analysis TEXT NOT NULL COMMENT '正确答案分析',
    risk_explanation TEXT NOT NULL COMMENT '风险解释',
    protection_advice JSON NOT NULL COMMENT '防护建议',
    better_choice TEXT COMMENT '更好的选择提示',
    difficulty INT DEFAULT 1 COMMENT '题目难度 1-简单 2-中等 3-困难',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (training_type_id) REFERENCES protection_training_types(id)
);

-- 防护训练会话表
CREATE TABLE protection_drill_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(100) UNIQUE NOT NULL COMMENT '会话唯一标识',
    user_id INT COMMENT '用户ID（可选）',
    training_type_id INT NOT NULL COMMENT '训练类型ID',
    total_questions INT NOT NULL COMMENT '总题目数',
    correct_count INT DEFAULT 0 COMMENT '正确答题数',
    current_question INT DEFAULT 0 COMMENT '当前题目索引',
    status ENUM('active', 'completed', 'paused') DEFAULT 'active' COMMENT '会话状态',
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
    end_time TIMESTAMP NULL COMMENT '结束时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (training_type_id) REFERENCES protection_training_types(id)
);

-- 防护训练答题记录表
CREATE TABLE protection_drill_answers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(100) NOT NULL COMMENT '会话ID',
    question_id INT NOT NULL COMMENT '题目ID',
    selected_option INT NOT NULL COMMENT '选择的选项ID',
    is_correct BOOLEAN NOT NULL COMMENT '是否正确',
    answer_time INT COMMENT '答题用时（秒）',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES protection_drill_questions(id)
);

-- 创建索引优化查询性能
CREATE INDEX idx_protection_questions_type ON protection_drill_questions(training_type_id);
CREATE INDEX idx_protection_sessions_user ON protection_drill_sessions(user_id);
CREATE INDEX idx_protection_answers_session ON protection_drill_answers(session_id);
