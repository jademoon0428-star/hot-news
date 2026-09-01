<<<<<<< HEAD
import requests
import json

# ====== 免费天气 API（不需要注册，直接用） ======
def get_weather(city):
    """查询城市实时天气"""
    # 使用 wttr.in 免费天气服务
    url = f"https://wttr.in/{city}?format=%l:+%c+%t+%w+%h&lang=zh"
    
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            print("=" * 45)
            print(f"🌤️  {resp.text}")
            print("=" * 45)
        else:
            print("❌ 查询失败，请检查城市名是否正确")
    except Exception as e:
        print(f"❌ 网络错误: {e}")
        print("请检查网络连接")


# ====== 第二种方式：用和风天气（需要注册获取 Key） ======
def get_weather_qweather(city, api_key):
    """使用和风天气 API 查询（更详细）"""
    # 第一步：城市名转城市ID
    geo_url = "https://geoapi.qweather.com/v2/city/lookup"
    geo_params = {"location": city, "key": api_key}
    
    try:
        geo_resp = requests.get(geo_url, params=geo_params)
        geo_data = geo_resp.json()
        
        if geo_data.get("code") != "200":
            print("❌ 城市名有误，请检查输入")
            return
        
        city_id = geo_data["location"][0]["id"]
        city_name = geo_data["location"][0]["name"]
        city_adm = geo_data["location"][0]["adm1"]
        
        # 第二步：查询天气
        weather_url = "https://devapi.qweather.com/v7/weather/now"
        weather_params = {"location": city_id, "key": api_key}
        
        weather_resp = requests.get(weather_url, params=weather_params)
        weather_data = weather_resp.json()
        
        if weather_data.get("code") != "200":
            print("❌ 天气查询失败")
            return
        
        now = weather_data["now"]
        print("=" * 45)
        print(f"📍 {city_name}, {city_adm}")
        print(f"🌡️  温度: {now['temp']}°C (体感 {now['feelsLike']}°C)")
        print(f"🌤️  天气: {now['text']}")
        print(f"💧 湿度: {now['humidity']}%")
        print(f"💨 风向: {now['windDir']} {now['windSpeed']}km/h")
        print("=" * 45)
        
    except Exception as e:
        print(f"❌ 出错: {e}")


# ====== 主程序 ======
if __name__ == "__main__":
    print("🌤️  天气查询工具")
    print("输入 'exit' 退出")
    print("-" * 45)
    
    while True:
        city = input("请输入城市名: ").strip()
        if city.lower() == "exit":
            print("再见！")
            break
        if not city:
            print("❌ 城市名不能为空")
            continue
        
        # 使用免费版（不需要 Key）
        get_weather(city)
=======
import requests
import json

# ====== 免费天气 API（不需要注册，直接用） ======
def get_weather(city):
    """查询城市实时天气"""
    # 使用 wttr.in 免费天气服务
    url = f"https://wttr.in/{city}?format=%l:+%c+%t+%w+%h&lang=zh"
    
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            print("=" * 45)
            print(f"🌤️  {resp.text}")
            print("=" * 45)
        else:
            print("❌ 查询失败，请检查城市名是否正确")
    except Exception as e:
        print(f"❌ 网络错误: {e}")
        print("请检查网络连接")


# ====== 第二种方式：用和风天气（需要注册获取 Key） ======
def get_weather_qweather(city, api_key):
    """使用和风天气 API 查询（更详细）"""
    # 第一步：城市名转城市ID
    geo_url = "https://geoapi.qweather.com/v2/city/lookup"
    geo_params = {"location": city, "key": api_key}
    
    try:
        geo_resp = requests.get(geo_url, params=geo_params)
        geo_data = geo_resp.json()
        
        if geo_data.get("code") != "200":
            print("❌ 城市名有误，请检查输入")
            return
        
        city_id = geo_data["location"][0]["id"]
        city_name = geo_data["location"][0]["name"]
        city_adm = geo_data["location"][0]["adm1"]
        
        # 第二步：查询天气
        weather_url = "https://devapi.qweather.com/v7/weather/now"
        weather_params = {"location": city_id, "key": api_key}
        
        weather_resp = requests.get(weather_url, params=weather_params)
        weather_data = weather_resp.json()
        
        if weather_data.get("code") != "200":
            print("❌ 天气查询失败")
            return
        
        now = weather_data["now"]
        print("=" * 45)
        print(f"📍 {city_name}, {city_adm}")
        print(f"🌡️  温度: {now['temp']}°C (体感 {now['feelsLike']}°C)")
        print(f"🌤️  天气: {now['text']}")
        print(f"💧 湿度: {now['humidity']}%")
        print(f"💨 风向: {now['windDir']} {now['windSpeed']}km/h")
        print("=" * 45)
        
    except Exception as e:
        print(f"❌ 出错: {e}")


# ====== 主程序 ======
if __name__ == "__main__":
    print("🌤️  天气查询工具")
    print("输入 'exit' 退出")
    print("-" * 45)
    
    while True:
        city = input("请输入城市名: ").strip()
        if city.lower() == "exit":
            print("再见！")
            break
        if not city:
            print("❌ 城市名不能为空")
            continue
        
        # 使用免费版（不需要 Key）
        get_weather(city)
>>>>>>> 64ba21b9fe987e2166e7406f7d105dda93aa4f42
        print()