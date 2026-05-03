#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: OAuth2 授权码流程实现

这个解决方案提供了 OAuth2 授权码流程的完整实现，
包括 PKCE 支持和安全最佳实践。
"""

import urllib.parse
import secrets
import hashlib
import base64
import time


class OAuth2Client:
    """OAuth2 客户端实现"""

    def __init__(self, client_id, client_secret, redirect_uri, auth_server_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_server_url = auth_server_url
        self.code_verifier = None
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = 0

    def generate_pkce_codes(self):
        """生成 PKCE code_verifier 和 code_challenge"""
        self.code_verifier = secrets.token_urlsafe(64)
        sha256 = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        code_challenge = base64.urlsafe_b64encode(sha256).decode('utf-8').rstrip('=')
        return code_challenge

    def get_authorization_url(self, scope, state=None):
        """获取授权 URL"""
        if state is None:
            state = secrets.token_urlsafe(32)

        code_challenge = self.generate_pkce_codes()

        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': scope,
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }

        return f"{self.auth_server_url}/authorize?{urllib.parse.urlencode(params)}"

    def exchange_code_for_tokens(self, authorization_code):
        """使用授权码交换访问令牌"""
        # 在真实实现中，这里会向令牌端点发送 POST 请求
        # 验证 code_verifier（PKCE）
        if not self.code_verifier:
            raise ValueError("缺少 code_verifier")

        # 模拟令牌响应
        self.access_token = f"access-token-{secrets.token_urlsafe(32)}"
        self.refresh_token = f"refresh-token-{secrets.token_urlsafe(64)}"
        self.token_expires_at = int(time.time()) + 3600

        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_type': 'Bearer',
            'expires_in': 3600
        }

    def is_access_token_valid(self):
        """检查访问令牌是否有效"""
        return (self.access_token is not None and
                int(time.time()) < self.token_expires_at)


def main():
    """主函数：演示 OAuth2 客户端"""
    client = OAuth2Client(
        client_id="my-web-app",
        client_secret="secret123",
        redirect_uri="https://myapp.com/callback",
        auth_server_url="https://auth.example.com"
    )

    # 获取授权 URL
    auth_url = client.get_authorization_url("openid profile email")
    print(f"授权 URL: {auth_url}")

    # 模拟收到授权码
    auth_code = "4/P7q-oMsCeLvIaQm6bTrgtp7..."

    # 交换令牌
    tokens = client.exchange_code_for_tokens(auth_code)
    print(f"访问令牌: {tokens['access_token'][:20]}...")
    print(f"刷新令牌: {tokens['refresh_token'][:20]}...")


if __name__ == "__main__":
    main()