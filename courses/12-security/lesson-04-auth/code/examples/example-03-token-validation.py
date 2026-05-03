#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: 令牌验证、过期处理和刷新

这个示例演示了实际应用中的令牌管理：
1. 验证访问令牌的有效性
2. 处理令牌过期的情况
3. 使用刷新令牌获取新的访问令牌
4. 刷新令牌轮换（安全最佳实践）
"""

import json
import time
import secrets


class TokenManager:
    """令牌管理器类"""

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = 0

    def store_tokens(self, access_token, refresh_token, expires_in):
        """存储令牌信息"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires_at = int(time.time()) + expires_in
        print(f"✅ 令牌已存储，访问令牌将在 {expires_in} 秒后过期")

    def is_access_token_valid(self):
        """检查访问令牌是否仍然有效"""
        current_time = int(time.time())
        # 提前 60 秒认为令牌即将过期，需要刷新
        return self.access_token is not None and current_time < (self.token_expires_at - 60)

    def refresh_access_token(self):
        """使用刷新令牌获取新的访问令牌"""
        if not self.refresh_token:
            raise ValueError("没有可用的刷新令牌")

        print("🔄 正在刷新访问令牌...")

        # 在真实场景中，这里会向授权服务器发送刷新令牌请求
        # 模拟网络延迟
        time.sleep(0.1)

        # 验证刷新令牌（在真实场景中由授权服务器完成）
        if not self._validate_refresh_token(self.refresh_token):
            raise ValueError("刷新令牌无效或已过期")

        # 生成新的令牌对（刷新令牌轮换）
        new_access_token = f"new-access-token-{secrets.token_urlsafe(16)}"
        new_refresh_token = f"new-refresh-token-{secrets.token_urlsafe(32)}"

        # 存储新令牌
        self.store_tokens(new_access_token, new_refresh_token, expires_in=3600)

        # 安全最佳实践：立即废弃旧的刷新令牌
        old_refresh_token = self.refresh_token
        self.refresh_token = new_refresh_token
        print(f"🔒 旧刷新令牌已废弃: {old_refresh_token[:20]}...")
        print(f"🆕 新刷新令牌: {new_refresh_token[:20]}...")

        return new_access_token

    def _validate_refresh_token(self, refresh_token):
        """模拟验证刷新令牌（在真实场景中由授权服务器完成）"""
        # 这里应该查询数据库或缓存来验证刷新令牌
        # 简化实现：假设所有非空令牌都是有效的
        return bool(refresh_token)

    def get_valid_access_token(self):
        """获取有效的访问令牌（自动处理刷新）"""
        if self.is_access_token_valid():
            print("✅ 使用现有的有效访问令牌")
            return self.access_token
        else:
            print("⚠️ 访问令牌已过期或即将过期")
            return self.refresh_access_token()

    def call_protected_api(self, token):
        """模拟调用受保护的 API"""
        print(f"📡 使用访问令牌调用 API: {token[:20]}...")
        # 在真实场景中，这里会发送带有 Authorization 头的 HTTP 请求
        time.sleep(0.05)
        return {"status": "success", "data": "敏感数据已返回"}


def simulate_api_call_with_token_management():
    """模拟完整的 API 调用流程，包含令牌管理"""
    print("=== 令牌验证和刷新演示 ===\n")

    # 初始化令牌管理器
    token_manager = TokenManager("my-client-id", "my-client-secret")

    # 模拟初始登录后获得的令牌
    initial_access_token = "initial-access-token-abc123"
    initial_refresh_token = "initial-refresh-token-def456"
    token_manager.store_tokens(initial_access_token, initial_refresh_token, expires_in=5)

    # 第一次 API 调用（令牌有效）
    print("1. 第一次 API 调用:")
    valid_token = token_manager.get_valid_access_token()
    response = token_manager.call_protected_api(valid_token)
    print(f"响应: {response}\n")

    # 等待令牌过期
    print("2. 等待访问令牌过期...")
    time.sleep(6)  # 等待超过 5 秒的过期时间

    # 第二次 API 调用（需要刷新令牌）
    print("3. 第二次 API 调用（令牌已过期）:")
    valid_token = token_manager.get_valid_access_token()
    response = token_manager.call_protected_api(valid_token)
    print(f"响应: {response}\n")

    # 第三次 API 调用（使用新的有效令牌）
    print("4. 第三次 API 调用（使用刷新后的令牌）:")
    valid_token = token_manager.get_valid_access_token()
    response = token_manager.call_protected_api(valid_token)
    print(f"响应: {response}")


def demonstrate_common_validation_scenarios():
    """演示常见的令牌验证场景"""
    print("\n=== 常见令牌验证场景 ===\n")

    scenarios = [
        ("有效令牌", True, True),
        ("过期令牌", False, True),
        ("无效签名", True, False),
        ("缺少令牌", False, False)
    ]

    for scenario_name, has_token, is_valid in scenarios:
        print(f"场景: {scenario_name}")
        if has_token:
            if is_valid:
                print("✅ 验证通过 - 允许访问")
            else:
                print("❌ 验证失败 - 返回 401 Unauthorized")
        else:
            print("❌ 缺少令牌 - 返回 401 Unauthorized")
        print()


def main():
    """主函数"""
    simulate_api_call_with_token_management()
    demonstrate_common_validation_scenarios()


if __name__ == "__main__":
    main()