# wechat.py
import requests
import json

def get_access_token(app_id, app_secret):
    """获取微信公众号全局唯一后台接口调用凭据（access_token）"""
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        print(f"[调试] 正在获取access_token，AppID: {app_id[:5]}...")
        response = requests.get(url)
        response.raise_for_status() # 检查请求是否成功
        data = response.json()
        if 'access_token' in data:
            print(f"获取 Access Token 成功: {data['access_token'][:10]}...，有效期 {data.get('expires_in')} 秒")
            return data['access_token']
        else:
            print(f"获取 Access Token 失败: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求 Access Token API 时发生错误: {e}")
        return None
    except json.JSONDecodeError:
        print("解析 Access Token API 响应失败")
        return None
    except Exception as e:
        print(f"获取 Access Token 时发生未知错误: {e}")
        return None

def send_template_message(access_token, data):
    """发送微信模板消息"""
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    headers = {'Content-Type': 'application/json'}
    try:
        print(f"[调试] 准备发送模板消息，模板ID: {data['template_id']}")
        print(f"[调试] 发送的数据: {json.dumps(data, ensure_ascii=False)}")
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        result = response.json()
        
        print(f"[调试] 微信API返回结果: {result}")
        
        if result.get('errcode') == 0:
            print("模板消息 API 调用成功")
            return True
        else:
            print(f"发送模板消息失败: {result}")
            # 常见错误：
            # 40001: access_token 无效或过期，需要重新获取
            # 40037: template_id 不正确
            # 41028: form_id 不正确，或者过期
            # 41029: form_id 已被使用
            # 41030: page 不正确
            # 45009: 接口调用超过限额
            # 47001: data 格式不正确
            return False
    except requests.exceptions.RequestException as e:
        print(f"请求发送模板消息 API 时发生错误: {e}")
        return False
    except json.JSONDecodeError:
        print("解析发送模板消息 API 响应失败")
        return False
    except Exception as e:
        print(f"发送模板消息时发生未知错误: {e}")
        return False