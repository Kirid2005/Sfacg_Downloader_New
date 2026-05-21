from api import ApiClient
from config import get_config, save_config

def ensure_login(client: ApiClient) -> bool:
    """
    确保已登录，若未登录则尝试使用配置文件中的 cookie 或账号密码登录
    返回 True 表示登录有效
    """
    config = get_config()
    cookie = config.get("cookie", "")
    
    # 如果配置中有 cookie，先尝试使用
    if cookie:
        client.set_cookie(cookie)
        if client.check_login():
            print("已登录（使用配置文件中的 cookie）")
            return True
        else:
            print("配置文件中的 cookie 已失效，将尝试重新登录")
    
    # cookie 无效或不存在，尝试使用配置中的账号密码自动登录
    username = config.get("user", "")
    password = config.get("pass", "")
    
    if username and password:
        print(f"尝试使用配置文件中的账号 {username} 自动登录...")
        new_cookie = client.login(username, password)
        if new_cookie:
            client.set_cookie(new_cookie)
            # 更新配置文件中的 cookie
            config["cookie"] = new_cookie
            save_config(config)
            print("登录成功，cookie 已更新到配置文件")
            return True
        else:
            print("自动登录失败，现在是未登录状态")
            return False
    else:
        print("未配置账号密码，请在config.conf中配置，现在是未登录状态")
        return False