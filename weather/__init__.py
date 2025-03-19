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
    return "抱歉，天气预警功能暂未实现。"

if __name__ == "__main__":
    mcp.run(transport='stdio')
