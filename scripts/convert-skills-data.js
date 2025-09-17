const fs = require('fs');
const path = require('path');

// 读取前端skillsData.js文件
const skillsDataPath = path.join(__dirname, '../frontend/src/data/skillsData.js');
const outputPath = path.join(__dirname, '../shared/skills-database.json');

// 确保输出目录存在
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

console.log('🔄 开始转换skillsData.js到JSON格式...');

try {
    // 读取skillsData.js文件内容
    let content = fs.readFileSync(skillsDataPath, 'utf8');

    // 移除export语句和注释
    content = content.replace(/export\s+default\s+/, '');
    content = content.replace(/\/\/.*$/gm, ''); // 移除单行注释
    content = content.replace(/\/\*[\s\S]*?\*\//g, ''); // 移除多行注释

    // 使用eval来解析JavaScript对象（注意：这在生产环境中不推荐，这里仅用于数据转换）
    const skillsData = eval(`(${content})`);

    // 转换数据结构，添加后端需要的字段
    const convertedData = {
        metadata: {
            version: "1.0.0",
            lastUpdated: new Date().toISOString(),
            totalSkills: Object.keys(skillsData).length,
            source: "frontend/skillsData.js"
        },
        categories: {
            communication: { name: "沟通交流", skills: [] },
            emotional_expression: { name: "情感表达", skills: [] },
            relationship_building: { name: "关系建立", skills: [] },
            special_scenarios: { name: "特殊场景", skills: [] }
        },
        skills: {}
    };

    // ID到后端字符串ID的映射
    const idMapping = {
        // 沟通交流 (1-25)
        1: "listen_actively", 2: "express_clearly", 3: "topic_transition", 4: "conflict_resolution", 5: "empathy_building",
        6: "boundary_setting", 7: "small_talk", 8: "deep_conversation", 9: "feedback_giving", 10: "feedback_receiving",
        11: "apology_skills", 12: "appreciation_expression", 13: "question_asking", 14: "story_telling", 15: "humor_usage",
        16: "emotional_regulation", 17: "trust_building", 18: "cultural_sensitivity", 19: "digital_communication", 20: "group_discussion",
        21: "presentation_skills", 22: "negotiation_basics", 23: "persuasion_ethics", 24: "active_listening_advanced", 25: "nonverbal_communication",

        // 情感表达 (26-38)
        26: "feeling_sharing", 27: "comfort_providing", 28: "celebration_sharing", 29: "disappointment_handling", 30: "anger_management",
        31: "sadness_expression", 32: "joy_sharing", 33: "fear_discussion", 34: "surprise_reaction", 35: "emotional_validation",
        36: "emotional_boundaries", 37: "vulnerability_sharing", 38: "emotional_support",

        // 关系建立 (39-51)
        39: "friendship_building", 40: "romantic_expression", 41: "family_communication", 42: "colleague_interaction", 43: "mentor_relationship",
        44: "network_building", 45: "intimacy_development", 46: "trust_repair", 47: "relationship_maintenance", 48: "social_integration",
        49: "community_participation", 50: "leadership_development", 51: "team_collaboration",

        // 特殊场景 (52-65)
        52: "crisis_support", 53: "grief_support", 54: "celebration_participation", 55: "conflict_mediation", 56: "public_speaking",
        57: "job_interview", 58: "customer_service", 59: "teaching_communication", 60: "healthcare_communication", 61: "legal_communication",
        62: "cross_cultural", 63: "intergenerational", 64: "disability_inclusion", 65: "crisis_intervention"
    };

    // 转换每个技能
    Object.entries(skillsData).forEach(([skillId, skillData]) => {
        const numericId = parseInt(skillId);
        const backendId = idMapping[numericId] || `skill_${numericId}`;

        // 转换技能数据为后端格式
        const convertedSkill = {
            id: backendId,
            numeric_id: numericId,
            title: skillData.name,
            content: skillData.description,
            difficulty: skillData.estimatedTime <= 20 ? "basic" : skillData.estimatedTime <= 35 ? "intermediate" : "advanced",
            tags: skillData.tags || [],
            scenarios: skillData.practiceScenarios?.map(scenario => scenario.situation) || [],
            category: skillData.category,
            // 保留前端的完整数据
            frontend_data: skillData
        };

        // 添加到对应分类
        const category = skillData.category;
        if (convertedData.categories[category]) {
            convertedData.categories[category].skills.push(convertedSkill);
        }

        // 添加到技能字典
        convertedData.skills[backendId] = convertedSkill;
        convertedData.skills[numericId] = convertedSkill; // 也支持数字ID查找
    });

    // 写入JSON文件
    fs.writeFileSync(outputPath, JSON.stringify(convertedData, null, 2), 'utf8');

    console.log('✅ 转换完成！');
    console.log(`📁 输出文件: ${outputPath}`);
    console.log(`📊 转换了 ${Object.keys(skillsData).length} 个技能`);
    console.log(`📂 包含 ${Object.keys(convertedData.categories).length} 个分类`);

} catch (error) {
    console.error('❌ 转换过程中出现错误:', error);
    process.exit(1);
}
