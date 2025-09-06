#!/usr/bin/env python3
"""
测试会话报告API
"""
import requests

def test_session_report_api():
    """测试会话报告API"""
    
    print("============================================================")
    print("🔍 测试会话报告API")
    print("============================================================")
    
    base_url = "http://localhost:8000"
    
    try:
        # 使用之前创建的用户登录
        login_data = {
            "username": "frontend_test_69f062",
            "password": "test123"
        }
        
        login_response = requests.post(f"{base_url}/auth/login", json=login_data)
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"✅ 登录成功")
            
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # 先获取报告列表，找到一个有效的session_id
            list_response = requests.get(
                f"{base_url}/risk-assessment/reports-history?page=1&page_size=10",
                headers=headers
            )
            
            if list_response.status_code == 200:
                reports = list_response.json()
                print(f"✅ 获取到 {len(reports)} 个报告")
                
                if reports:
                    # 测试第一个报告对应的会话
                    session_id = reports[0]['session_id']
                    print(f"\n🔍 测试会话 {session_id} 的报告...")
                    
                    session_response = requests.get(
                        f"{base_url}/risk-assessment/session/{session_id}/report",
                        headers=headers
                    )
                    
                    print(f"状态码: {session_response.status_code}")
                    
                    if session_response.status_code == 200:
                        session_report = session_response.json()
                        print(f"✅ 会话报告获取成功")
                        print(f"   报告ID: {session_report['report_id']} (类型: {type(session_report['report_id'])})")
                        print(f"   会话ID: {session_report['session_id']} (类型: {type(session_report['session_id'])})")
                        print(f"   标题: {session_report['report_title']}")
                        print(f"   风险等级: {session_report['overall_risk_level']}")
                        
                        print(f"\n📱 前端应该获取到的数据结构:")
                        print(f"   report.report_id = {session_report['report_id']}")
                        print(f"   跳转URL: /pages/risk-report/report-detail?reportId={session_report['report_id']}")
                        
                    else:
                        print(f"❌ 获取会话报告失败: {session_response.text}")
                else:
                    print("❌ 没有可用的报告进行测试")
            else:
                print(f"❌ 获取报告列表失败: {list_response.text}")
        else:
            print(f"❌ 登录失败: {login_response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_session_report_api()
    if success:
        print("\n" + "="*60)
        print("🎉 会话报告API测试完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
