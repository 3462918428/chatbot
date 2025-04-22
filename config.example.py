# config.example.py
# 这是一个示例配置文件，请复制为config.py并填入你的实际信息

# 恋爱开始日期，格式：YYYY-MM-DD
START_DATE = "YYYY-MM-DD"

# 目标城市
CITY = "你的城市"

# 和风天气 API Key
# 请前往 https://dev.qweather.com/ 注册获取你的API密钥
WEATHER_API_KEY = "你的和风天气API密钥"

# 微信公众号开发者凭证
# 在微信公众平台 -> 开发 -> 基本配置 中获取
APP_ID = "你的微信公众号AppID"
APP_SECRET = "你的微信公众号AppSecret"

# 微信模板消息 ID
# 在微信公众平台 -> 功能 -> 模板消息 中申请，审核通过后获得
TEMPLATE_ID = "你的微信模板消息ID"

# 接收消息的用户（女朋友）的微信 OpenID
# 需要用户关注你的公众号，并在公众号后台 -> 用户管理 中查看其 OpenID
USER_ID = "接收消息的微信用户OpenID"

# 生日配置（阳历和农历）
BIRTHDAY_SOLAR = "MM-DD"  # 阳历生日：月-日
BIRTHDAY_LUNAR = "MM-DD"  # 农历生日：月-日 