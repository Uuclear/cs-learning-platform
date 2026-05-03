#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: OAuth2 授权码流程模拟

这个示例演示了 OAuth2 授权码流程的基本步骤：
1. 用户被重定向到授权服务器
2. 用户登录并授权
3. 授权服务器返回授权码
4. 客户端使用授权码交换访问令牌
5. 使用访问令牌访问受保护的资源
"""

import urllib.parse
import secrets
import hashlib
import base64


def generate_code_verifier():
    """生成 PKCE code_verifier (随机字符串)"""
    return secrets.token_urlsafe(64)


def generate_code_challenge(code_verifier):
    """根据 code_verifier 生成 code_challenge (SHA256 + base64url)"""
    sha256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    # 移除 padding 并替换字符以符合 base64url 标准
    code_challenge = base64.urlsafe_b64encode(sha256).decode('utf-8').rstrip('=')
    return code_challenge


def simulate_authorization_request(client_id, redirect_uri, scope, state, code_challenge=None):
    """模拟向授权服务器发起授权请求"""
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
        'state': state
    }

    if code_challenge:
        params['code_challenge'] = code_challenge
        params['code_challenge_method'] = 'S256'

    auth_url = f"https://auth.example.com/authorize?{urllib.parse.urlencode(params)}"
    print(f"授权请求 URL: {auth_url}")
    return auth_url


def simulate_token_request(client_id, client_secret, code, redirect_uri, code_verifier=None):
    """模拟使用授权码换取访问令牌"""
    # 在真实场景中，这里会向令牌端点发送 POST 请求
    print(f"\n使用授权码 {code} 换取访问令牌...")

    # 模拟验证过程
    if code_verifier:
        print("验证 PKCE code_verifier...")
        # 这里应该验证 code_verifier 与之前存储的匹配

    # 返回模拟的访问令牌
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # 简化的 JWT
    refresh_token = "def50200a1b2c3d4e5f6..."  # 简化的刷新令牌

    print(f"获取到访问令牌: {access_token[:20]}...")
    print(f"获取到刷新令牌: {refresh_token[:20]}...")

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': 3600
    }


def main():
    """主函数：演示完整的 OAuth2 授权码流程"""
    print("=== OAuth2 授权码流程演示 ===\n")

    # 客户端配置
    CLIENT_ID = "my-web-app"
    CLIENT_SECRET = "secret123"
    REDIRECT_URI = "https://myapp.com/callback"
    SCOPE = "openid profile email"

    # 1. 生成状态参数（防止 CSRF）
    state = secrets.token_urlsafe(32)
    print(f"生成状态参数: {state[:20]}...")

    # 2. PKCE - 生成 code_verifier 和 code_challenge
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    print(f"生成 code_verifier: {code_verifier[:20]}...")
    print(f"生成 code_challenge: {code_challenge[:20]}...\n")

    # 3. 发起授权请求
    simulate_authorization_request(
        client_id=CLIENT_ID,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        state=state,
        code_challenge=code_challenge
    )

    # 4. 模拟用户授权后收到授权码
    authorization_code = "4/P7q-oMsCeLvIaQm6bTrgtp7..."
    print(f"\n模拟收到授权码: {authorization_code[:20]}...")

    # 5. 使用授权码换取访问令牌
    tokens = simulate_token_request(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=authorization_code,
        redirect_uri=REDIRECT_URI,
        code_verifier=code_verifier
    )

    print("\n=== 流程完成 ===")
    print("现在可以使用访问令牌调用受保护的 API 了！")


if __name__ == "__main__":
    main()