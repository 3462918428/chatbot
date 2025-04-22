# 微信每日消息推送

这是一个基于微信公众号的每日消息推送服务，可以向指定用户发送包含天气、恋爱天数、生日倒计时和课程表等信息的模板消息。

## 功能

- 每日自动推送微信模板消息
- 显示天气信息（使用和风天气API）
- 计算恋爱天数
- 显示生日倒计时（支持阳历和农历）
- 显示每日课程表

## 安装与配置

### 本地运行

1. 克隆仓库：
   ```
   git clone https://github.com/你的用户名/wechat-daily-message.git
   cd wechat-daily-message
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 编辑 `.env` 文件，填入你的实际信息

4. 运行程序：
   ```
   python main.py
   ```

### 部署到GitHub Actions

1. Fork本仓库

2. 在GitHub仓库设置中添加Secrets：
   - 进入仓库 -> Settings -> Secrets and variables -> Actions
   - 添加以下Secrets：
     - START_DATE: 恋爱开始日期，格式 YYYY-MM-DD
     - CITY: 目标城市
     - WEATHER_API_KEY: 和风天气API密钥
     - APP_ID: 微信公众号AppID
     - APP_SECRET: 微信公众号AppSecret
     - TEMPLATE_ID: 微信模板消息ID
     - USER_ID: 接收消息的微信用户OpenID
     - BIRTHDAY_SOLAR: 阳历生日（月-日）
     - BIRTHDAY_LUNAR: 农历生日（月-日）

3. 启用GitHub Actions：
   - 进入仓库 -> Actions，确保工作流已启用
   - 工作流将按照设定的时间表自动运行（默认每天北京时间6:30）
   - 你也可以手动触发工作流

## 自定义

### 修改发送时间

编辑`.github/workflows/daily_message.yml`文件中的cron表达式：
```yaml
on:
  schedule:
    # UTC时间，需要换算成北京时间（UTC+8）
    - cron: '30 22 * * *' # 每天UTC 22:30（北京时间6:30）
```

### 修改课程表

编辑`schedule.py`文件，根据实际情况修改课程安排。

## 微信公众号配置

1. 注册微信公众号（订阅号或服务号）
2. 开启开发者模式并获取AppID和AppSecret
3. 申请模板消息并获取模板ID
4. 获取用户的OpenID

## 注意事项

- 确保微信公众号有模板消息的权限
- 确保用户已关注你的公众号
- 模板消息的格式必须与代码中的数据结构匹配

## 许可证

MIT 