import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class SkillsDataManager:
    """技能数据管理器 - 统一前后端数据源"""
    
    def __init__(self):
        self.skills_data = None
        self.load_skills_data()
    
    def load_skills_data(self):
        """从共享JSON文件加载技能数据"""
        try:
            # 找到共享数据文件路径 - 修正路径计算
            current_dir = Path(__file__).parent
            # 从 backend/app/core 向上到项目根目录，然后到 shared
            json_path = current_dir.parent.parent.parent / "shared" / "skills-database.json"
            
            if not json_path.exists():
                raise FileNotFoundError(f"技能数据文件不存在: {json_path}")
            
            with open(json_path, 'r', encoding='utf-8') as f:
                self.skills_data = json.load(f)
            
            print(f"✅ 成功加载技能数据: {self.skills_data['metadata']['totalSkills']} 个技能")
            
        except Exception as e:
            print(f"❌ 加载技能数据失败: {e}")
            # 使用空数据作为后备
            self.skills_data = {
                "metadata": {"totalSkills": 0},
                "categories": {},
                "skills": {},
                "id_mapping": {}
            }
    
    def get_skill_by_id(self, skill_id: Any) -> Optional[Dict]:
        """根据ID获取技能数据（支持数字ID和字符串ID）"""
        if not self.skills_data:
            return None
        
        # 直接查找
        skill = self.skills_data["skills"].get(str(skill_id))
        if skill:
            return skill
        
        # 如果是数字ID，尝试映射
        if isinstance(skill_id, (int, str)) and str(skill_id).isdigit():
            numeric_id = int(skill_id)
            backend_id = self.skills_data["id_mapping"].get(numeric_id)
            if backend_id:
                return self.skills_data["skills"].get(backend_id)
        
        return None
    
    def get_categories(self) -> Dict:
        """获取所有技能分类"""
        if not self.skills_data:
            return {}
        return self.skills_data.get("categories", {})
    
    def get_all_skills(self) -> Dict:
        """获取所有技能数据"""
        if not self.skills_data:
            return {}
        return self.skills_data.get("skills", {})
    
    def get_skills_by_category(self, category: str) -> list:
        """获取指定分类的技能列表"""
        if not self.skills_data:
            return []
        
        category_data = self.skills_data["categories"].get(category, {})
        return category_data.get("skills", [])
    
    def get_metadata(self) -> Dict:
        """获取数据元信息"""
        if not self.skills_data:
            return {}
        return self.skills_data.get("metadata", {})

# 创建全局实例
skills_manager = SkillsDataManager()

# 为了向后兼容，提供原来的数据结构
def get_legacy_database() -> Dict:
    """获取兼容原SOCIAL_SKILLS_DATABASE格式的数据"""
    if not skills_manager.skills_data:
        return {}
    
    legacy_db = {}
    for category_id, category_data in skills_manager.get_categories().items():
        legacy_db[category_id] = {
            "name": category_data["name"],
            "skills": category_data["skills"]
        }
    
    return legacy_db
