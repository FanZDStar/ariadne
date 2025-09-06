#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试心理评估报告中的会话标题功能
"""

import asyncio
import requests
import json
from datetime import datetime

# API配置
BASE_URL = "http://localhost:8000"
TEST_USER_EMAIL = "frontend_test_69f062@test.com"
TEST_USER_PASSWORD = "securePassword123"

def test_login():
    """登录获取token"""
    print("=== 测试用户登录 ===")
    
    login_data = {
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/login", 
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"登录状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        token = result.get("access_token")
        print(f"✅ 登录成功，获取到token: {token[:30]}...")
        return token
    else:
        print(f"❌ 登录失败: {response.text}")
        return None

def test_reports_history_with_session_title(token):
    """测试报告历史API是否包含会话标题"""
    print("\n=== 测试报告历史（包含会话标题）===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/risk-assessment/reports-history", headers=headers)
    print(f"获取报告历史状态码: {response.status_code}")
    
    if response.status_code == 200:
        reports = response.json()
        print(f"✅ 获取到 {len(reports)} 个报告")
        
        for i, report in enumerate(reports[:3]):  # 只显示前3个
            print(f"\n报告 {i+1}:")
            print(f"  - 报告ID: {report.get('report_id')}")
            print(f"  - 会话ID: {report.get('session_id')}")
            print(f"  - 会话标题: {report.get('session_title', '未找到标题')}")
            print(f"  - 风险等级: {report.get('overall_risk_level')}")
            print(f"  - 生成时间: {report.get('report_generated_time')}")
        
        # 检查是否包含session_title字段
        if reports and 'session_title' in reports[0]:
            print("✅ 报告历史API成功包含会话标题字段")
            return reports[0]  # 返回第一个报告用于详情测试
        else:
            print("❌ 报告历史API缺少会话标题字段")
            return None
    else:
        print(f"❌ 获取报告历史失败: {response.text}")
        return None

def test_report_detail_with_session_title(token, report_id):
    """测试报告详情API是否包含会话标题"""
    print(f"\n=== 测试报告详情（包含会话标题）===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/risk-assessment/report/{report_id}", headers=headers)
    print(f"获取报告详情状态码: {response.status_code}")
    
    if response.status_code == 200:
        report = response.json()
        print(f"✅ 获取报告详情成功")
        print(f"  - 报告ID: {report.get('report_id')}")
        print(f"  - 会话ID: {report.get('session_id')}")
        print(f"  - 会话标题: {report.get('session_title', '未找到标题')}")
        print(f"  - 报告标题: {report.get('report_title')}")
        print(f"  - 风险等级: {report.get('overall_risk_level')}")
        
        # 检查是否包含session_title字段
        if 'session_title' in report:
            print("✅ 报告详情API成功包含会话标题字段")
            return True
        else:
            print("❌ 报告详情API缺少会话标题字段")
            return False
    else:
        print(f"❌ 获取报告详情失败: {response.text}")
        return False

def main():
    """主测试函数"""
    print("开始测试心理评估报告的会话标题功能...")
    
    # 1. 登录获取token
    token = test_login()
    if not token:
        print("❌ 无法获取访问令牌，测试终止")
        return
    
    # 2. 测试报告历史API
    first_report = test_reports_history_with_session_title(token)
    if not first_report:
        print("❌ 报告历史API测试失败")
        return
    
    # 3. 测试报告详情API
    report_id = first_report.get('report_id')
    if report_id:
        success = test_report_detail_with_session_title(token, report_id)
        if success:
            print("\n🎉 所有测试通过！会话标题功能已成功集成")
        else:
            print("\n❌ 报告详情API测试失败")
    else:
        print("❌ 无法获取报告ID进行详情测试")

if __name__ == "__main__":
    main()
