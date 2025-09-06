#!/usr/bin/env python3
"""
直接测试HTTP请求以获取详细错误信息
"""
import requests
import json

def test_api_endpoint():
    """测试API端点"""
    
    print("============================================================")
    print("🌐 直接HTTP请求测试")
    print("============================================================")
    
    base_url = "http://localhost:8000"
    
    try:
        # 1. 先测试统计端点看是否有认证问题
        print("📊 测试统计端点...")
        try:
            response = requests.get(f"{base_url}/risk-assessment/statistics", timeout=5)
            print(f"   状态码: {response.status_code}")
            print(f"   响应头: {dict(response.headers)}")
            if response.status_code != 200:
                print(f"   错误响应: {response.text}")
        except Exception as e:
            print(f"   请求异常: {e}")
        
        # 2. 测试reports-history端点
        print("\n📋 测试报告历史端点...")
        try:
            url = f"{base_url}/risk-assessment/reports-history?page=1&page_size=10"
            print(f"   请求URL: {url}")
            
            response = requests.get(url, timeout=5)
            print(f"   状态码: {response.status_code}")
            print(f"   响应头: {dict(response.headers)}")
            
            if response.status_code == 500:
                print(f"   500错误详情: {response.text}")
            elif response.status_code == 401:
                print("   需要认证，这是正常的")
            else:
                print(f"   响应内容: {response.text[:500]}")
                
        except Exception as e:
            print(f"   请求异常: {e}")
        
        # 3. 测试不带参数的请求
        print("\n📋 测试不带参数的报告历史端点...")
        try:
            url = f"{base_url}/risk-assessment/reports-history"
            print(f"   请求URL: {url}")
            
            response = requests.get(url, timeout=5)
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 500:
                print(f"   500错误详情: {response.text}")
            elif response.status_code == 401:
                print("   需要认证，这是正常的")
            else:
                print(f"   响应内容: {response.text[:500]}")
                
        except Exception as e:
            print(f"   请求异常: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_endpoint()
    if success:
        print("\n" + "="*60)
        print("🎉 HTTP请求测试完成")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("💥 测试失败！请检查错误信息")
        print("="*60)
