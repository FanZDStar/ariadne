#!/usr/bin/env python3
"""
测试新的报告详情API
"""
import requests

def test_report_detail_api():
    """测试报告详情API"""
    
    print("============================================================")
    print("🔍 测试报告详情API")
    print("============================================================")
    
    base_url = "http://localhost:8000"
    
    # 使用之前创建的测试用户
    username = "frontend_test_69f062"
    password = "test123"
    
    try:
        # 1. 登录
        print("🔑 登录...")
        login_data = {"username": username, "password": password}
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ 登录失败: {login_response.text}")
            return False
            
        access_token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        print("✅ 登录成功")
        
        # 2. 获取报告列表
        print("\n📋 获取报告列表...")
        list_response = requests.get(
            f"{base_url}/risk-assessment/reports-history?page=1&page_size=10",
            headers=headers
        )
        
        if list_response.status_code != 200:
            print(f"❌ 获取报告列表失败: {list_response.text}")
            return False
            
        reports = list_response.json()
        print(f"✅ 获取到 {len(reports)} 个报告")
        
        if not reports:
            print("❌ 没有报告可测试")
            return False
        
        # 3. 测试获取第一个报告的详情
        report_id = reports[0]["report_id"]
        print(f"\n🔍 获取报告 {report_id} 的详情...")
        
        detail_response = requests.get(
            f"{base_url}/risk-assessment/reports/{report_id}",
            headers=headers
        )
        
        print(f"状态码: {detail_response.status_code}")
        
        if detail_response.status_code == 200:
            report_detail = detail_response.json()
            print("✅ 报告详情获取成功")
            print(f"   报告ID: {report_detail['report_id']}")
            print(f"   标题: {report_detail['report_title']}")
            print(f"   风险等级: {report_detail['overall_risk_level']}")
            print(f"   风险分数: {report_detail['overall_risk_score']}")
        else:
            print(f"❌ 获取报告详情失败: {detail_response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_report_detail_api()
    if success:
        print("\n" + "="*60)
        print("🎉 报告详情API测试成功！")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
