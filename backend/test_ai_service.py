#!/usr/bin/env python3
"""
AI服务测试脚本
用于测试AI服务是否正常工作
"""

import asyncio
import sys
import os

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.ai_service import AIService
from app.core.config import settings

async def test_ai_service():
    """测试AI服务"""
    print("开始测试AI服务...")
    
    # 检查配置
    print(f"AI API URL: {settings.ai_api_url}")
    print(f"AI Model: {settings.ai_model}")
    print(f"AI API Key配置: {'已配置' if settings.ai_api_key else '未配置'}")
    
    # 创建AI服务实例
    ai_service = AIService()
    
    # 测试消息
    test_messages = [
        {"role": "user", "content": "你好，我想练习一下沟通技巧，能给我一些建议吗？"}
    ]
    
    print("\n发送测试消息到AI服务...")
    try:
        response = await ai_service.get_response(test_messages, "social-skills")
        print(f"AI响应: {response}")
        
        # 检查是否是默认响应
        if "AI服务" in response or "配置错误" in response or "不可用" in response:
            print("❌ AI服务返回错误消息，可能配置有问题")
        else:
            print("✅ AI服务正常响应")
            
    except Exception as e:
        print(f"❌ AI服务测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_ai_service())
