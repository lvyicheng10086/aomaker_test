import requests
from aomaker.fixture import BaseLogin
from tools.handle_rsa.get_pwd_encrypt import get_encrypted_password
from aomaker.storage import cache
pwd = get_encrypted_password('Aa@1234567>')


class Login(BaseLogin):

    def access_code(self) -> dict:
        data = {
            "method": "GET",
            "url": f"{self.sso_url}/sso/platform/user/access_code?type=login",
            "headers": {"Content-Type": "application/json, text/plain, */*"},
    
        }

        resp_access_code = requests.request(**data)
        return resp_access_code.json()


    def login(self) -> dict:
        data = {
            "method": "POST",
            "url": f"{self.sso_url}/sso/platform/login",
            "headers": {"Content-Type": "application/json"},
            "json": {
                "spCode": "122210",
                            "username": "PJY",
                            "password": pwd,
                            "imageVerifyCode": "",
                            "verifyCode": "",
                            "options": {
                                "accType": None
                            },
                            "grant_type": "account_config_pwd",
                            "accessCode": self.access_code()['data']['accessCode'],
                            "deviceId": "de1fbc605cd8055039835df7a9184400",
                            "terminalType": "pc",
                            "clientId": "123456789",
                            "identityId": "230512142514063911",
                            "siteId": "230907181448002716"
}
        }
        resp_login = requests.request(**data).json()
        return resp_login
    def set_cache_token(self, resp_login:dict) -> None:
        """
        缓存 token 并确保更新成功
        """
        token = resp_login['data']['token']
        # 先尝试删除旧的 token
        try:
            cache.delete('token')
        except Exception:
            pass
        # 设置新的 token
        cache.set('token', token)
        # 验证是否设置成功
        cached_token = cache.get('token')
        if cached_token != token:
            raise ValueError(f"Token 缓存验证失败: 期望 {token}, 实际 {cached_token}")

    def make_headers(self, resp_login:dict) -> dict:
        """
        设置请求头，优先使用缓存中的 token
        """
        # 优先从缓存获取 token
        token = cache.get('token')
        if not token:
            # 如果缓存中没有，使用响应中的 token
            token = resp_login['data']['token']
            # 同时更新缓存
            self.set_cache_token(resp_login)
        
        headers = {'token': token}
        return headers

    def __call__(self, *args, **kwargs):
        """
        初始化 token 和请求头
        """
        resp_login = self.login()
        # 先设置缓存
        self.set_cache_token(resp_login)
        # 再获取 headers
        headers = self.make_headers(resp_login)
        return headers


if __name__ == '__main__':
    login = Login()
    # 使用 __call__ 方法一次性完成所有操作
    headers = login()
    
    # 验证 token 一致性
    cached_token = cache.get('token')
    response_token = headers['token']
    print(f"Cached token: {cached_token}")
    print(f"Header token: {response_token}")
    assert cached_token == response_token, "Token 不一致！"


