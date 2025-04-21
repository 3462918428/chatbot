# main.py
import os
import datetime
from config import START_DATE, CITY, WEATHER_API_KEY, APP_ID, APP_SECRET, TEMPLATE_ID, USER_ID
from weather import get_weather
from wechat import get_access_token, send_template_message
from schedule import Schedule

def calculate_days_together(start_date_str):
    """计算恋爱天数"""
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    today = datetime.date.today()
    delta = today - start_date
    return delta.days

def main():
    # 计算恋爱天数
    days_together = calculate_days_together(START_DATE)

    # 获取天气信息
    weather_data = get_weather(CITY, WEATHER_API_KEY)
    if not weather_data:
        print("获取天气信息失败")
        return

    # 获取微信 Access Token
    try:
        access_token = get_access_token(APP_ID, APP_SECRET)
        if not access_token:
            print("获取 Access Token 失败")
            return
    except Exception as e:
        print(f"获取 Access Token 时发生错误: {e}")
        return

    # 获取当天课程信息
    schedule = Schedule()
    today_schedule = schedule.get_today_schedule()
    courses = ', '.join(today_schedule) if today_schedule else '无课程安排'

    # 准备模板消息数据
    data = {
        "touser": USER_ID,
        "template_id": TEMPLATE_ID,
        "url": "http://weixin.qq.com/download",  # 点击模板消息后跳转的链接，可不填
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": datetime.date.today().strftime("%Y年%m月%d日"),
                "color": "#4A90E2"
            },
            "days": {
                "value": str(days_together),
                "color": "#E64C3C"
            },
            "city": {
                "value": CITY,
                "color": "#8E44AD"
            },
            "weather": {
                "value": weather_data.get('weather', 'N/A'),
                "color": "#2ECC71"
            },
            "temp": {
                "value": str(weather_data.get('temp', 'N/A')) + "°C",
                "color": "#F39C12"
            },
            "feels_like": {
                "value": str(weather_data.get('feels_like', 'N/A')) + "°C",
                "color": "#D35400"
            },
            "courses": {
                "value": courses if courses else "今天没有课程安排哦~",
                "color": "#3498DB"
            },
            "tips": {
                "value": weather_data.get('tips', '今天也要开心呀！'),
                "color": "#16A085"
            }
        }
    }

    # 发送模板消息
    try:
        success = send_template_message(access_token, data)
        if success:
            print("模板消息发送成功")
        else:
            print("模板消息发送失败")
    except Exception as e:
        print(f"发送模板消息时发生错误: {e}")

if __name__ == "__main__":
    # 从 GitHub Actions 的环境变量中读取配置信息
    # 本地测试时，可以取消注释下一行，并确保 config.py 中有默认值或使用 .env 文件
    # from dotenv import load_dotenv
    # load_dotenv()

    # 优先从环境变量获取配置，如果环境变量没有，则使用 config.py 中的默认值
    start_date = os.getenv("START_DATE", START_DATE)
    city = os.getenv("CITY", CITY)
    weather_api_key = os.getenv("WEATHER_API_KEY", WEATHER_API_KEY)
    app_id = os.getenv("APP_ID", APP_ID)
    app_secret = os.getenv("APP_SECRET", APP_SECRET)
    template_id = os.getenv("TEMPLATE_ID", TEMPLATE_ID)
    user_id = os.getenv("USER_ID", USER_ID)

    # 更新配置变量，以便后续函数使用最新的值
    START_DATE = start_date
    CITY = city
    WEATHER_API_KEY = weather_api_key
    APP_ID = app_id
    APP_SECRET = app_secret
    TEMPLATE_ID = template_id
    USER_ID = user_id

    # 校验必要的配置是否存在
    required_configs = {
        "START_DATE": START_DATE,
        "CITY": CITY,
        "WEATHER_API_KEY": WEATHER_API_KEY,
        "APP_ID": APP_ID,
        "APP_SECRET": APP_SECRET,
        "TEMPLATE_ID": TEMPLATE_ID,
        "USER_ID": USER_ID
    }

    missing_configs = [key for key, value in required_configs.items() if not value]

    if missing_configs:
        print(f"错误：缺少必要的配置信息: {', '.join(missing_configs)}")
        print("请检查环境变量或 config.py 文件。")
    else:
        main()