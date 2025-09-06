#!/usr/bin/env python3
"""
测试风险评估API端点 - HTTP测试
"""
import requests
import json

def test_risk_assessment_api():
    """测试风险评估API HTTP端点"""
    
    print("============================================================")
    print("🌐 风险评估API HTTP测试")
    print("============================================================")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. 测试统计端点（不需要认证）
        print("📊 测试统计端点...")
        response = requests.get(f"{base_url}/risk-assessment/statistics")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"   统计数据: {response.json()}")
        else:
            print(f"   错误: {response.text}")
        
        # 2. 测试报告历史端点（需要认证）
        print("\n📋 测试报告历史端点...")
        
        # 先尝试登录获取token
        print("🔐 尝试登录...")
        login_data = {
            "username": "peppa", 
            "password": "123456"  # 尝试常见密码
        }
        
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        print(f"   登录状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"   获取到token: {access_token[:20]}...")
            
            # 使用token访问报告历史
            headers = {"Authorization": f"Bearer {access_token}"}
            reports_response = requests.get(f"{base_url}/risk-assessment/reports-history", headers=headers)
            print(f"   报告历史状态码: {reports_response.status_code}")
            
            if reports_response.status_code == 200:
                reports = reports_response.json()
                print(f"   找到 {len(reports)} 个报告")
                for report in reports:
                    print(f"     - 报告ID: {report.get('report_id')}, 标题: {report.get('report_title')}")
            else:
                print(f"   错误: {reports_response.text}")
        else:
            print(f"   登录失败: {login_response.text}")
            # 尝试不带认证直接访问
            print("\n🔓 尝试不带认证访问...")
            reports_response = requests.get(f"{base_url}/risk-assessment/reports-history")
            print(f"   状态码: {reports_response.status_code}")
            print(f"   响应: {reports_response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_risk_assessment_api()
    if success:
        print("\n" + "="*60)
        print("🎉 HTTP API测试完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
