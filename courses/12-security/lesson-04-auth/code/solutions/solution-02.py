#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: JWT 完整实现

这个解决方案提供了 JWT 的完整实现，
包括创建、签名、验证和错误处理。
"""

import json
import base64
import hashlib
import hmac
import time


class JWT:
    """JWT 实现类"""

    @staticmethod
    def base64url_encode(data):
        """Base64 URL 安全编码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

    @staticmethod
    def base64url_decode(encoded_str):
        """Base64 URL 安全解码"""
        padding = '=' * (4 - (len(encoded_str) % 4))
        return base64.urlsafe_b64decode(encoded_str + padding)

    @classmethod
    def encode(cls, payload, secret_key, algorithm="HS256"):
        """编码 JWT"""
        header = {"alg": algorithm, "typ": "JWT"}

        header_b64 = cls.base64url_encode(json.dumps(header, separators=(',', ':')))
        payload_b64 = cls.base64url_encode(json.dumps(payload, separators=(',', ':')))

        signing_input = f"{header_b64}.{payload_b64}"

        signature = hmac.new(
            secret_key.encode('utf-8'),
            signing_input.encode('utf-8'),
            hashlib.sha256
        ).digest()

        signature_b64 = cls.base64url_encode(signature)

        return f"{signing_input}.{signature_b64}"

    @classmethod
    def decode(cls, jwt_token, secret_key, verify=True):
        """解码 JWT"""
        parts = jwt_token.split('.')
        if len(parts) != 3:
            raise ValueError("无效的 JWT 格式")

        header_b64, payload_b64, signature_b64 = parts

        if verify:
            # 验证签名
            signing_input = f"{header_b64}.{payload_b64}"
            expected_signature = hmac.new(
                secret_key.encode('utf-8'),
                signing_input.encode('utf-8'),
                hashlib.sha256
            ).digest()
            expected_signature_b64 = cls.base64url_encode(expected_signature)

            if signature_b64 != expected_signature_b64:
                raise ValueError("JWT 签名验证失败")

        header = json.loads(cls.base64url_decode(header_b64))
        payload = json.loads(cls.base64url_decode(payload_b64))

        # 验证过期时间
        if 'exp' in payload and payload['exp'] < int(time.time()):
            raise ValueError("JWT 已过期")

        return {'header': header, 'payload': payload}


def main():
    """主函数：演示 JWT 解决方案"""
    secret = "my-secret-key"
    payload = {
        "sub": "user123",
        "name": "张三",
        "email": "zhangsan@example.com",
        "iat": int(time.time()),
        "exp": int(time.time()) + 300  # 5 分钟后过期
    }

    # 创建 JWT
    token = JWT.encode(payload, secret)
    print(f"JWT: {token}")

    # 验证 JWT
    try:
        decoded = JWT.decode(token, secret)
        print(f"解码成功: {decoded['payload']['name']}")
    except ValueError as e:
        print(f"验证失败: {e}")


if __name__ == "__main__":
    main()