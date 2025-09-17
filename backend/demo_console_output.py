"""
模拟技能练习的控制台输出效果演示
"""

def demo_console_output():
    """演示控制台输出的效果"""
    
    # 模拟技能练习数据
    skill_id = 29
    user_response = "我今天考试考砸了，感觉很失望"
    scenario_context = "期末考试成绩不理想，心情低落"
    is_first_message = True
    chat_history = []
    
    skill = {
        "id": "disappointment_handling",
        "title": "失望处理",
        "content": "学会健康地表达和处理失望情绪，避免消极影响人际关系。",
        "tags": ["情感表达", "失望", "处理技巧"]
    }
    
    # 演示控制台输出
    print("\n" + "="*80)
    print("🎯 【技能练习会话开始】")
    print("="*80)
    print(f"📋 技能ID: {skill_id}")
    print(f"👤 用户说: {user_response}")
    print(f"🎬 场景背景: {scenario_context}")
    print(f"🔄 是否首次对话: {is_first_message}")
    print(f"📚 历史对话数量: {len(chat_history) if chat_history else 0}")
    
    print(f"✅ 技能信息:")
    print(f"   📖 技能名称: {skill.get('title', 'Unknown')}")
    print(f"   📝 技能描述: {skill.get('content', 'N/A')}")
    print(f"   🏷️ 技能标签: {', '.join(skill.get('tags', []))}")
    
    # 模拟提示词构建
    roleplay_prompt = f"""
你现在要与用户进行"{skill['title']}"技能的情景练习。请你完全进入角色扮演模式。

练习场景：{scenario_context}

重要指示：
1. 你要扮演场景中的相关角色（如：朋友、恋人、室友、同学等）
2. 完全代入角色，用第一人称与用户对话
3. 不要进行分析或指导，只要自然地对话
4. 根据场景情况合理回应用户
5. 保持角色的情感状态和个性特点
6. 以自然、友善的方式与用户对话

用户刚说：{user_response}

请作为场景中的角色自然回应，不要说教或分析。
"""
    
    print(f"\n🤖 【AI提示词构建完成】")
    print(f"🎭 对话类型: {'首次对话' if is_first_message else '继续对话'}")
    
    print(f"\n📜 【完整AI提示词】")
    print("-" * 80)
    print(roleplay_prompt)
    print("-" * 80)
    
    print(f"🚀 正在调用AI服务...")
    
    # 模拟AI回复
    ai_response = """看你脸色不太好，是不是刚出成绩了？来，坐下聊聊。

我也刚考完试，感觉这次题目出得特别偏，很多人都没发挥好。你先别太难过，具体哪里不太理想啊？

我记得你平时学习挺认真的，一次考试不代表什么。而且说不定比你想象的要好呢？"""
    
    print(f"✅ AI服务响应成功")
    print(f"📝 AI回复内容: {ai_response}")
    print(f"📏 回复长度: {len(ai_response)} 字符")
    
    print(f"\n🎉 【练习结果】")
    print(f"✨ 最终AI回复: {ai_response}")
    print(f"🔄 对话是否继续: True")
    print(f"📊 练习是否完成: False")
    print("="*80)
    print("🎯 【技能练习会话结束】")
    print("="*80 + "\n")

if __name__ == "__main__":
    print("🎭 【控制台输出效果演示】")
    print("以下是您在进行技能练习时，后端控制台会显示的详细信息：\n")
    demo_console_output()
    
    print("\n📌 【说明】")
    print("✅ 已为您的技能练习系统添加了详细的控制台打印信息")
    print("📊 现在您可以在后端控制台看到：")
    print("   🎯 每次技能练习的完整信息")
    print("   👤 用户输入的内容")
    print("   📖 正在练习的技能详情") 
    print("   📜 发送给AI的完整提示词")
    print("   🤖 AI服务的调用过程和响应")
    print("   ✨ 最终返回给用户的结果")
    print("\n🚀 开始进行技能练习，即可在后端控制台看到这些详细信息！")
