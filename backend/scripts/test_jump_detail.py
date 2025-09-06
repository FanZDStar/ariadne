#!/usr/bin/env python3
"""
测试报告详情API
"""
import requests

def test_report_detail_with_known_report():
    """使用已知的报告ID测试详情API"""
    
    print("============================================================")
    print("🔍 测试报告详情API (使用已知报告)")
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
            
            # 先获取报告列表，找到一个有效的report_id
            list_response = requests.get(
                f"{base_url}/risk-assessment/reports-history?page=1&page_size=10",
                headers=headers
            )
            
            if list_response.status_code == 200:
                reports = list_response.json()
                print(f"✅ 获取到 {len(reports)} 个报告")
                
                if reports:
                    # 测试第一个报告的详情
                    report_id = reports[0]['report_id']
                    print(f"\n🔍 测试报告 {report_id} 的详情...")
                    
                    detail_response = requests.get(
                        f"{base_url}/risk-assessment/reports/{report_id}",
                        headers=headers
                    )
                    
                    print(f"状态码: {detail_response.status_code}")
                    
                    if detail_response.status_code == 200:
                        detail = detail_response.json()
                        print(f"✅ 报告详情获取成功")
                        print(f"   报告ID: {detail['report_id']}")
                        print(f"   标题: {detail['report_title']}")
                        print(f"   风险等级: {detail['overall_risk_level']}")
                        print(f"   风险分数: {detail['overall_risk_score']}")
                        print(f"   AI分析长度: {len(detail.get('ai_analysis', ''))}")
                        
                        print(f"\n📱 前端跳转URL应该是:")
                        print(f"   /pages/risk-report/report-detail?reportId={report_id}")
                        
                    else:
                        print(f"❌ 获取详情失败: {detail_response.text}")
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
    success = test_report_detail_with_known_report()
    if success:
        print("\n" + "="*60)
        print("🎉 报告详情API测试完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
