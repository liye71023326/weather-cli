from typing import Any
import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
WEATHER_API_BASE = "https://wttr.in"
USER_AGENT = "weather-app/1.0"

# 默认位置（北京）
DEFAULT_LATITUDE = 39.9042
DEFAULT_LONGITUDE = 116.4074
DEFAULT_CITY = "Beijing"

# 添加区域代码到城市映射
REGION_MAPPING = {
    "CN-11": ("北京", 39.9042, 116.4074),
    "CN-31": ("上海", 31.2304, 121.4737),
    "CN-44": ("广州", 23.1291, 113.2644),
    "CN-51": ("成都", 30.5728, 104.0668),
    "CN-42": ("武汉", 30.5928, 114.3055),
    "CN-61": ("西安", 34.3416, 108.9398),
    "CN-33": ("杭州", 30.2741, 120.1551),
}

async def make_weather_request(url: str, params: dict[str, Any]) -> str | None:
    """Make a request to the wttr.in API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

@mcp.tool()
async def get_forecast(latitude: float = DEFAULT_LATITUDE, longitude: float = DEFAULT_LONGITUDE) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location (default: Beijing)
        longitude: Longitude of the location (default: Beijing)
    """
    # 构建位置字符串
    location = f"{latitude},{longitude}"
    
    # 获取天气信息
    params = {
        "format": "%l:+%c+%t+%h+%w+%p+%m\n",  # 自定义输出格式
        "lang": "zh",  # 使用中文
        "m": "",      # 使用公制单位
    }
    
    weather_data = await make_weather_request(f"{WEATHER_API_BASE}/{location}", params)
    if not weather_data:
        return "无法获取该位置的天气预报"

    # 获取详细天气信息
    detailed_params = {
        "format": "j1",  # JSON 格式
        "lang": "zh",
        "m": "",
    }
    
    detailed_data = await make_weather_request(f"{WEATHER_API_BASE}/{location}", detailed_params)
    if not detailed_data:
        return weather_data

    try:
        import json
        data = json.loads(detailed_data)
        current = data["current_condition"][0]
        area_name = data.get('nearest_area', [{}])[0].get('areaName', [{}])[0].get('value', DEFAULT_CITY)
        
        return f"""
位置：{area_name}
当前天气：{current.get('lang_zh', [{}])[0].get('value', '未知')}
温度：{current.get('temp_C', 'N/A')}°C
体感温度：{current.get('FeelsLikeC', 'N/A')}°C
相对湿度：{current.get('humidity', 'N/A')}%
气压：{current.get('pressure', 'N/A')}hPa
风向：{current.get('winddir16Point', 'N/A')}
风速：{current.get('windspeedKmph', 'N/A')}km/h
能见度：{current.get('visibility', 'N/A')}km
降水量：{current.get('precipMM', 'N/A')}mm
云量：{current.get('cloudcover', 'N/A')}%
"""
    except Exception as e:
        return weather_data

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a region.

    Args:
        state: Region code (e.g. CN-11 for Beijing)
    """
    if state not in REGION_MAPPING:
        return f"错误：不支持的区域代码 {state}。支持的区域代码包括：{', '.join(REGION_MAPPING.keys())}"
    
    city_name, lat, lon = REGION_MAPPING[state]
    
    # 获取天气预警信息
    params = {
        "format": "j1",  # JSON 格式
        "lang": "zh",    # 中文
    }
    
    weather_data = await make_weather_request(f"{WEATHER_API_BASE}/{lat},{lon}", params)
    if not weather_data:
        return f"无法获取 {city_name} 的天气预警信息"

    try:
        import json
        data = json.loads(weather_data)
        
        # 提取天气预警信息
        weather_desc = data["current_condition"][0]["lang_zh"][0]["value"]
        weather_alerts = []
        
        # 检查极端天气条件
        current = data["current_condition"][0]
        temp = float(current["temp_C"])
        humidity = float(current["humidity"])
        wind_speed = float(current["windspeedKmph"])
        precip = float(current["precipMM"])
        
        # 添加天气预警
        if temp >= 35:
            weather_alerts.append("高温预警：当前温度超过35°C，请注意防暑降温")
        elif temp <= 0:
            weather_alerts.append("低温预警：当前温度低于0°C，请注意防寒保暖")
            
        if humidity >= 85:
            weather_alerts.append("湿度预警：当前湿度较高，请注意防潮")
            
        if wind_speed >= 39:
            weather_alerts.append("大风预警：当前风速较大，请注意防风")
            
        if precip >= 50:
            weather_alerts.append("暴雨预警：当前降水量较大，请注意防涝")
            
        # 整理返回信息
        result = f"""
{city_name}天气预警信息：
当前天气：{weather_desc}
温度：{temp}°C
相对湿度：{humidity}%
风速：{wind_speed}km/h
降水量：{precip}mm

预警信息："""
        
        if weather_alerts:
            for alert in weather_alerts:
                result += f"\n- {alert}"
        else:
            result += "\n当前无特别预警信息"
            
        return result
        
    except Exception as e:
        return f"解析 {city_name} 的天气预警信息时出错：{str(e)}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
