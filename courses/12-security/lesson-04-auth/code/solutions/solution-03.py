#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: 令牌验证和刷新实现

这个解决方案提供了完整的令牌管理实现，
包括自动刷新、令牌轮换和安全验证。
"""

import time
import secrets


class SecureTokenManager:
    """安全令牌管理器"""

    def __init__(self, client_id, client_secret, token_endpoint):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = 0
        self.refresh_token_used = False

    def store_tokens(self, access_token, refresh_token, expires_in):
        """安全存储令牌"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = int(time.time()) + expires_in
        self.refresh_token_used = False

    def is_access_token_valid(self):
        """检查访问令牌是否有效（提前 60 秒刷新）"""
        return (self.access_token is not None and
                not self.refresh_token_used and
                int(time.time()) < (self.token_expires_at - 60))

    def refresh_tokens(self):
        """刷新令牌（实现令牌轮换）"""
        if self.refresh_token_used:
            raise ValueError("刷新令牌已被使用，无法再次使用")

        if not self.refresh_token:
            raise ValueError("没有可用的刷新令牌")

        # 标记当前刷新令牌为已使用
        self.refresh_token_used = True

        # 在真实场景中，向令牌端点发送刷新请求
        new_access_token = f"new-access-{secrets.token_urlsafe(32)}"
        new_refresh_token = f"new-refresh-{secrets.token_urlsafe(64)}"

        # 存储新令牌
        self.store_tokens(new_access_token, new_refresh_token, expires_in=3600)

        return new_access_token

    def get_access_token(self):
        """获取有效的访问令牌"""
        if self.is_access_token_valid():
            return self.access_token
        else:
            return self.refresh_tokens()


def main():
    """主函数：演示安全令牌管理"""
    token_manager = SecureTokenManager(
        "my-client-id",
        "my-client-secret",
        "https://auth.example.com/token"
    )

    # 初始令牌
    token_manager.store_tokens(
        "initial-access-token",
        "initial-refresh-token",
        expires_in=5
    )

    print("初始访问令牌:", token_manager.get_access_token())

    # 等待过期
    time.sleep(6)

    # 自动刷新
    print("刷新后的访问令牌:", token_manager.get_access_token())


if __name__ == "__main__":
    main()