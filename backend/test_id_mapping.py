import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 模拟ID映射功能测试
ID_MAPPING = {
    1: "listen_actively", 2: "express_clearly", 3: "topic_transition"
}

def test_id_mapping():
    """测试ID映射功能"""
    
    # 测试数字ID
    skill_id = 1
    if isinstance(skill_id, int) or (isinstance(skill_id, str) and skill_id.isdigit()):
        mapped_id = ID_MAPPING.get(int(skill_id), str(skill_id))
        print(f"数字ID {skill_id} 映射为: {mapped_id}")
    
    # 测试字符串数字ID
    skill_id = "2"
    if isinstance(skill_id, int) or (isinstance(skill_id, str) and skill_id.isdigit()):
        mapped_id = ID_MAPPING.get(int(skill_id), str(skill_id))
        print(f"字符串数字ID '{skill_id}' 映射为: {mapped_id}")
    
    # 测试已经是字符串ID的情况
    skill_id = "listen_actively"
    if isinstance(skill_id, int) or (isinstance(skill_id, str) and skill_id.isdigit()):
        mapped_id = ID_MAPPING.get(int(skill_id), str(skill_id))
        print(f"字符串ID '{skill_id}' 映射为: {mapped_id}")
    else:
        print(f"字符串ID '{skill_id}' 不需要映射")
    
    # 测试不存在的ID
    skill_id = 999
    if isinstance(skill_id, int) or (isinstance(skill_id, str) and skill_id.isdigit()):
        mapped_id = ID_MAPPING.get(int(skill_id), str(skill_id))
        print(f"不存在的ID {skill_id} 映射为: {mapped_id}")

if __name__ == "__main__":
    test_id_mapping()
