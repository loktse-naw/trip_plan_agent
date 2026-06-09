#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高德API验证脚本
测试高德Web服务API是否可以正常使用
"""

import os
import requests
import json
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


def test_amap_api():
    """测试高德地图API"""

    # 获取API密钥
    api_key = os.getenv('AMAP_API_KEY')

    if not api_key:
        print("❌ 错误：未找到AMAP_API_KEY配置")
        print("请确保.env文件中包含: AMAP_API_KEY=你的密钥")
        return False

    print(f"🔑 使用API密钥: {api_key[:10]}...{api_key[-4:]}")
    print("\n" + "=" * 50)

    # 测试1: 地理编码（将地址转换为坐标）
    print("\n📝 测试1: 地理编码 - '北京市朝阳区'")
    geo_url = "https://restapi.amap.com/v3/geocode/geo"
    geo_params = {
        "key": api_key,
        "address": "北京市朝阳区",
        "output": "JSON"
    }

    try:
        response = requests.get(geo_url, params=geo_params, timeout=10)
        data = response.json()

        if data.get('status') == '1':
            print(f"✅ 地理编码成功!")
            if data.get('geocodes'):
                location = data['geocodes'][0]['location']
                print(f"   坐标: {location}")
                print(f"   完整地址: {data['geocodes'][0]['formatted_address']}")
        else:
            print(f"❌ 地理编码失败: {data.get('info', '未知错误')}")
            print(f"   返回信息: {json.dumps(data, ensure_ascii=False, indent=2)}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return False

    print("\n" + "=" * 50)

    # 测试2: POI搜索（搜索美食）
    print("\n📝 测试2: POI搜索 - '北戴河美食'")
    poi_url = "https://restapi.amap.com/v3/place/text"
    poi_params = {
        "key": api_key,
        "keywords": "美食",
        "city": "北戴河",
        "citylimit": "true",
        "offset": 5,
        "output": "JSON"
    }

    try:
        response = requests.get(poi_url, params=poi_params, timeout=10)
        data = response.json()

        if data.get('status') == '1':
            print(f"✅ POI搜索成功!")
            count = data.get('count', 0)
            print(f"   找到 {count} 个结果")

            pois = data.get('pois', [])
            if pois:
                print(f"\n   前3个搜索结果:")
                for i, poi in enumerate(pois[:3], 1):
                    name = poi.get('name', '未知')
                    address = poi.get('address', '未知地址')
                    print(f"   {i}. {name}")
                    print(f"      地址: {address}")
            else:
                print("   未找到相关POI")
        else:
            print(f"❌ POI搜索失败: {data.get('info', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return False

    print("\n" + "=" * 50)

    # 测试3: 逆地理编码（将坐标转换为地址）
    print("\n📝 测试3: 逆地理编码 - 使用天安门坐标 (116.397128,39.916527)")
    regeo_url = "https://restapi.amap.com/v3/geocode/regeo"
    regeo_params = {
        "key": api_key,
        "location": "116.397128,39.916527",
        "output": "JSON"
    }

    try:
        response = requests.get(regeo_url, params=regeo_params, timeout=10)
        data = response.json()

        if data.get('status') == '1':
            print(f"✅ 逆地理编码成功!")
            if data.get('regeocode'):
                address = data['regeocode'].get('formatted_address', '未知')
                print(f"   地址: {address}")
        else:
            print(f"❌ 逆地理编码失败: {data.get('info', '未知错误')}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return False

    print("\n" + "=" * 50)
    print("\n🎉 所有测试通过！高德API配置正确，可以正常使用。")
    return True


def check_api_key_type():
    """检查API密钥类型"""
    api_key = os.getenv('AMAP_API_KEY')

    if not api_key:
        return

    print("\n" + "=" * 50)
    print("\n🔍 检测API密钥类型...")

    # 尝试调用需要Web服务权限的API
    test_url = "https://restapi.amap.com/v3/ip"
    params = {
        "key": api_key,
        "output": "JSON"
    }

    try:
        response = requests.get(test_url, params=params, timeout=10)
        data = response.json()

        if data.get('status') == '1':
            print("✅ 当前密钥类型: Web服务 (可用于后端)")
            if data.get('city'):
                print(f"   测试结果: 获取到城市 {data.get('city')}")
        elif data.get('info') == 'INVALID_USER_KEY':
            print("❌ 密钥无效")
            print("   建议: 请检查密钥是否正确，或重新生成")
        elif 'USERKEY_PLAT_NOMATCH' in str(data.get('info', '')):
            print("⚠️  密钥类型不匹配!")
            print("   当前密钥可能是 'Web端 JS API' 类型")
            print("   后端需要使用 'Web服务' 类型")
            print("   请在控制台创建新的 'Web服务' 类型密钥")
        else:
            print(f"⚠️  无法确定密钥类型: {data.get('info', '未知错误')}")
    except Exception as e:
        print(f"❌ 检测失败: {str(e)}")


if __name__ == "__main__":
    print("🚀 开始测试高德地图API配置")
    print("=" * 50)

    # 检查环境变量
    load_dotenv()
    print(f"\n📁 加载配置文件: {os.path.exists('.env')}")

    # 检测密钥类型
    check_api_key_type()

    print("\n")

    # 运行功能测试
    success = test_amap_api()

    if not success:
        print("\n💡 解决建议:")
        print("1. 确保.env文件中AMAP_API_KEY配置正确")
        print("2. 确保使用的是'Web服务'类型的API密钥")
        print("3. 检查网络连接是否正常")
        print("4. 登录 https://lbs.amap.com/ 查看密钥状态")

    print("\n" + "=" * 50)