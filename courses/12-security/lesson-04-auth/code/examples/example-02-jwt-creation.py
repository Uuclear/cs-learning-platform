#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: JWT (JSON Web Token) 创建、签名和验证

这个示例演示了 JWT 的基本结构和操作：
1. JWT 的三个部分：头部(Header)、载荷(Payload)、签名(Signature)
2. 使用 HMAC-SHA256 算法进行签名
3. 验证 JWT 的签名和过期时间
"""

import json
import base64
import hashlib
import hmac
import time


def base64url_encode(data):
    """Base64 URL 安全编码（移除 padding）"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    encoded = base64.urlsafe_b64encode(data).decode('utf-8')
    return encoded.rstrip('=')


def base64url_decode(encoded_str):
    """Base64 URL 安全解码（添加必要的 padding）"""
    # 添加必要的 padding
    padding = '=' * (4 - (len(encoded_str) % 4))
    encoded_str += padding
    return base64.urlsafe_b64decode(encoded_str)


def create_jwt_header(algorithm="HS256"):
    """创建 JWT 头部"""
    header = {
        "alg": algorithm,  # 签名算法
        "typ": "JWT"       # 令牌类型
    }
    return header


def create_jwt_payload(subject, issuer, audience, expiration_minutes=30):
    """创建 JWT 载荷（claims）"""
    current_time = int(time.time())
    payload = {
        "sub": subject,           # 主题（通常是用户ID）
        "iss": issuer,            # 签发者
        "aud": audience,          # 受众
        "iat": current_time,      # 签发时间
        "exp": current_time + (expiration_minutes * 60),  # 过期时间
        "name": "张三",           # 用户名
        "email": "zhangsan@example.com"  # 邮箱
    }
    return payload


def sign_jwt(header, payload, secret_key):
    """使用 HMAC-SHA256 签名 JWT"""
    # 编码头部和载荷
    header_b64 = base64url_encode(json.dumps(header, separators=(',', ':')))
    payload_b64 = base64url_encode(json.dumps(payload, separators=(',', ':')))

    # 创建签名输入
    signing_input = f"{header_b64}.{payload_b64}"

    # 计算 HMAC-SHA256 签名
    signature = hmac.new(
        secret_key.encode('utf-8'),
        signing_input.encode('utf-8'),
        hashlib.sha256
    ).digest()

    # 编码签名
    signature_b64 = base64url_encode(signature)

    # 组合完整的 JWT
    jwt_token = f"{signing_input}.{signature_b64}"
    return jwt_token


def verify_jwt(jwt_token, secret_key, expected_issuer=None, expected_audience=None):
    """验证 JWT 的签名和声明"""
    try:
        # 分割 JWT 的三个部分
        parts = jwt_token.split('.')
        if len(parts) != 3:
            raise ValueError("JWT 格式无效")

        header_b64, payload_b64, signature_b64 = parts

        # 重新计算签名
        signing_input = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(
            secret_key.encode('utf-8'),
            signing_input.encode('utf-8'),
            hashlib.sha256
        ).digest()
        expected_signature_b64 = base64url_encode(expected_signature)

        # 验证签名
        if signature_b64 != expected_signature_b64:
            raise ValueError("JWT 签名验证失败")

        # 解码头部和载荷
        header = json.loads(base64url_decode(header_b64))
        payload = json.loads(base64url_decode(payload_b64))

        # 验证过期时间
        current_time = int(time.time())
        if 'exp' in payload and payload['exp'] < current_time:
            raise ValueError("JWT 已过期")

        # 验证签发者
        if expected_issuer and payload.get('iss') != expected_issuer:
            raise ValueError(f"JWT 签发者不匹配: 期望 {expected_issuer}, 实际 {payload.get('iss')}")

        # 验证受众
        if expected_audience and payload.get('aud') != expected_audience:
            raise ValueError(f"JWT 受众不匹配: 期望 {expected_audience}, 实际 {payload.get('aud')}")

        return {
            'valid': True,
            'header': header,
            'payload': payload
        }

    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def main():
    """主函数：演示 JWT 的创建和验证"""
    print("=== JWT 创建和验证演示 ===\n")

    # 配置
    SECRET_KEY = "my-super-secret-key-for-jwt-signing"
    SUBJECT = "user123"
    ISSUER = "auth-server.example.com"
    AUDIENCE = "my-web-app"

    # 1. 创建 JWT
    print("1. 创建 JWT...")
    header = create_jwt_header("HS256")
    payload = create_jwt_payload(SUBJECT, ISSUER, AUDIENCE, expiration_minutes=5)

    jwt_token = sign_jwt(header, payload, SECRET_KEY)
    print(f"生成的 JWT: {jwt_token}")
    print(f"JWT 长度: {len(jwt_token)} 字符\n")

    # 2. 验证 JWT
    print("2. 验证 JWT...")
    result = verify_jwt(jwt_token, SECRET_KEY, ISSUER, AUDIENCE)

    if result['valid']:
        print("✅ JWT 验证成功！")
        print(f"主题: {result['payload']['sub']}")
        print(f"用户名: {result['payload']['name']}")
        print(f"邮箱: {result['payload']['email']}")
        print(f"签发时间: {result['payload']['iat']}")
        print(f"过期时间: {result['payload']['exp']}")
    else:
        print(f"❌ JWT 验证失败: {result['error']}")

    # 3. 演示无效 JWT（错误密钥）
    print("\n3. 使用错误密钥验证 JWT...")
    invalid_result = verify_jwt(jwt_token, "wrong-secret-key", ISSUER, AUDIENCE)
    if not invalid_result['valid']:
        print(f"✅ 正确检测到无效 JWT: {invalid_result['error']}")

    # 4. 演示过期 JWT
    print("\n4. 创建立即过期的 JWT...")
    expired_payload = create_jwt_payload(SUBJECT, ISSUER, AUDIENCE, expiration_minutes=-1)
    expired_jwt = sign_jwt(header, expired_payload, SECRET_KEY)
    expired_result = verify_jwt(expired_jwt, SECRET_KEY, ISSUER, AUDIENCE)
    if not expired_result['valid']:
        print(f"✅ 正确检测到过期 JWT: {expired_result['error']}")


if __name__ == "__main__":
    main()