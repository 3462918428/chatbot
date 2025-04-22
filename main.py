# main.py
import os
import datetime
import config  # 导入config模块，但稍后会优先使用环境变量
from date_utils import get_days_until
from weather import get_weather
from wechat import get_access_token, send_template_message
from schedule import Schedule

# 从环境变量或配置文件获取配置
START_DATE = os.getenv("START_DATE", config.START_DATE)
CITY = os.getenv("CITY", config.CITY)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", config.WEATHER_API_KEY)
APP_ID = os.getenv("APP_ID", config.APP_ID)
APP_SECRET = os.getenv("APP_SECRET", config.APP_SECRET)
TEMPLATE_ID = os.getenv("TEMPLATE_ID", config.TEMPLATE_ID)
# 用户ID可以是单个值或逗号分隔的列表
USER_IDS = os.getenv("USER_ID", config.USER_ID).split(',')
BIRTHDAY_SOLAR = os.getenv("BIRTHDAY_SOLAR", config.BIRTHDAY_SOLAR)
BIRTHDAY_LUNAR = os.getenv("BIRTHDAY_LUNAR", config.BIRTHDAY_LUNAR)

def calculate_days_together(start_date_str):
    """计算恋爱天数"""
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    today = datetime.date.today()
    delta = today - start_date
    return delta.days

def main():
    # 输出当前使用的配置
    print(f"[配置信息] 当前使用的模板ID: {TEMPLATE_ID}")
    print(f"[配置信息] 当前目标城市: {CITY}")
    print(f"[配置信息] 用户数量: {len(USER_IDS)}")
    
    # 计算恋爱天数
    # 计算纪念日
    start_date = datetime.datetime.strptime(START_DATE, "%Y-%m-%d").date()
    today = datetime.date.today()
    days_together = (today - start_date).days

    # 计算生日倒计时
    solar_month, solar_day = map(int, BIRTHDAY_SOLAR.split('-'))
    lunar_month, lunar_day = map(int, BIRTHDAY_LUNAR.split('-'))
    days_until_solar = get_days_until(solar_month, solar_day)
    days_until_lunar = get_days_until(lunar_month, lunar_day, is_lunar=True)

    # 获取天气信息
    weather_data = get_weather(CITY, WEATHER_API_KEY)
    if not weather_data:
        print("获取天气信息失败")
        return

    # 获取当天课程信息
    schedule = Schedule()
    today_schedule = schedule.get_today_schedule()
    courses = '今日课程：' + (', '.join(today_schedule) if today_schedule else '无课程安排')

    # 调试输出课程信息
    print(f'[调试] 当天课程表数据: {today_schedule}')
    print(f'[调试] 格式化后的课程信息: {courses}')

    # 准备模板消息数据的基本结构（不包含用户ID）
    data_template = {
        "template_id": TEMPLATE_ID,
        "url": "http://weixin.qq.com/download",
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
            "birthday_solar": {
                "value": f"{days_until_solar}天",
                "color": "#FF69B4"
            },
            "birthday_lunar": {
                "value": f"{days_until_lunar}天",
                "color": "#BA55D3"
            },
            "tips": {
                "value": weather_data.get('tips', '今天也要开心呀！') + "\n\n" + courses,
                "color": "#16A085"
            }
        }
    }

    # 获取微信 Access Token
    try:
        access_token = get_access_token(APP_ID, APP_SECRET)
        if not access_token:
            print("获取 Access Token 失败")
            return
    except Exception as e:
        print(f"获取 Access Token 时发生错误: {e}")
        return

    # 对每个用户发送消息
    success_count = 0
    for user_id in USER_IDS:
        user_id = user_id.strip()  # 去除可能的空格
        if not user_id:
            continue  # 跳过空用户ID
            
        print(f"[调试] 准备向用户 {user_id} 发送消息")
        
        # 为当前用户准备数据
        data = data_template.copy()
        data["touser"] = user_id
        
        # 发送模板消息
        try:
            print(f"[调试] 准备发送消息，使用的模板ID: {data['template_id']}")
            success = send_template_message(access_token, data)
            if success:
                print(f"向用户 {user_id} 的模板消息发送成功")
                success_count += 1
            else:
                print(f"向用户 {user_id} 的模板消息发送失败")
        except Exception as e:
            print(f"向用户 {user_id} 发送模板消息时发生错误: {e}")
    
    print(f"消息发送完成，成功: {success_count}/{len(USER_IDS)}")

if __name__ == "__main__":
    # 尝试加载.env文件中的环境变量（如果存在）
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("成功加载.env文件")
    except ImportError:
        print(".env文件加载失败，请确保安装了python-dotenv或环境变量已设置")

    # 校验必要的配置是否存在
    required_configs = {
        "START_DATE": START_DATE,
        "CITY": CITY,
        "WEATHER_API_KEY": WEATHER_API_KEY,
        "APP_ID": APP_ID,
        "APP_SECRET": APP_SECRET,
        "TEMPLATE_ID": TEMPLATE_ID,
        "USER_ID": USER_IDS
    }

    missing_configs = [key for key, value in required_configs.items() if not value]

    if missing_configs:
        print(f"错误：缺少必要的配置信息: {', '.join(missing_configs)}")
        print("请检查环境变量、.env文件或config.py文件。")
    else:
        main()