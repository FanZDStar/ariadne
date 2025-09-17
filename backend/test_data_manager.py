import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试数据管理器
from app.core.skills_data import skills_manager

def test_skills_manager():
    """测试技能数据管理器"""
    
    print("🧪 测试技能数据管理器...")
    
    # 检查数据是否加载
    if skills_manager.skills_data:
        metadata = skills_manager.get_metadata()
        print(f"📊 元数据: {metadata}")
        
        categories = skills_manager.get_categories()
        print(f"📂 分类数量: {len(categories)}")
        
        for cat_id, cat_data in categories.items():
            skill_count = len(cat_data.get("skills", []))
            print(f"  - {cat_data.get('name', cat_id)}: {skill_count} 个技能")
        
        # 测试技能查找
        skill_1 = skills_manager.get_skill_by_id(1)
        if skill_1:
            print(f"✅ 技能1: {skill_1.get('title', 'N/A')}")
        else:
            print("❌ 找不到技能1")
            
        skill_29 = skills_manager.get_skill_by_id(29)
        if skill_29:
            print(f"✅ 技能29: {skill_29.get('title', 'N/A')}")
        else:
            print("❌ 找不到技能29")
            
    else:
        print("❌ 技能数据未加载")
        
    # 检查JSON文件是否存在
    from pathlib import Path
    current_dir = Path(__file__).parent
    json_path = current_dir.parent / "shared" / "skills-database.json"
    
    print(f"📁 JSON文件路径: {json_path}")
    print(f"📁 文件存在: {json_path.exists()}")
    
    if json_path.exists():
        import json
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 JSON文件包含 {len(data.get('skills', {}))} 个技能条目")
        print(f"📂 JSON文件包含 {len(data.get('categories', {}))} 个分类")

if __name__ == "__main__":
    test_skills_manager()
