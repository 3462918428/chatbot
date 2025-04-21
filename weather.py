# weather.py
import requests
import json

def get_city_location_id(city_name, api_key):
    """获取城市的Location ID"""
    lookup_url = f"https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={api_key}"
    try:
        response = requests.get(lookup_url)
        response.raise_for_status()
        data = response.json()
        if data.get('code') == '200' and data.get('location'):
            return data['location'][0]['id']
        else:
            print(f"获取城市 Location ID 失败: {data.get('code')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求城市 Location ID API 时发生错误: {e}")
        return None
    except Exception as e:
        print(f"处理城市 Location ID 数据时发生未知错误: {e}")
        return None

def get_weather(city, api_key):
    """获取指定城市的天气信息"""
    location_id = get_city_location_id(city, api_key)
    if not location_id:
        return None

    url = f"https://devapi.qweather.com/v7/weather/now?location={location_id}&key={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('code') != '200':
            print(f"获取天气数据失败: {data.get('code')}")
            return None

        weather_data = data.get('now', {})
        weather_desc = weather_data.get('text', '未知')
        temp = weather_data.get('temp', 'N/A')
        feelsLike = weather_data.get('feelsLike', 'N/A')

        # 获取生活指数
        indices_url = f"https://devapi.qweather.com/v7/indices/1d?type=3,9&location={location_id}&key={api_key}"
        indices_response = requests.get(indices_url)
        indices_data = indices_response.json()

        tips = "今天也要元气满满哦！"
        if indices_data.get('code') == '200':
            for index in indices_data.get('daily', []):
                if index.get('type') == '3':  # 穿衣指数
                    tips = index.get('text', tips)

        return {
            'weather': weather_desc,
            'temp': temp,
            'feels_like': feelsLike,
            'tips': tips
        }

    except requests.exceptions.RequestException as e:
        print(f"请求天气 API 时发生错误: {e}")
        return None
    except json.JSONDecodeError:
        print("解析天气 API 响应失败")
        return None
    except Exception as e:
        print(f"处理天气数据时发生未知错误: {e}")
        return None