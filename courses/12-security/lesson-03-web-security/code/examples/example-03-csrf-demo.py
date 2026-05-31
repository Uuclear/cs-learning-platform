#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSRF（跨站请求伪造）攻击演示与防御

本示例用控制台模拟展示 CSRF 攻击原理及 CSRF 令牌防御。
注意：此代码仅用于教育目的。
"""

import secrets
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class BankSession:
    """模拟银行会话与 CSRF 令牌存储"""

    sessions: Dict[str, str] = field(default_factory=dict)
    csrf_tokens: Dict[str, str] = field(default_factory=dict)
    users: Dict[str, str] = field(
        default_factory=lambda: {"admin": "password123"}
    )

    def login(self, username: str, password: str) -> Optional[str]:
        if self.users.get(username) != password:
            return None
        session_id = secrets.token_hex(8)
        self.sessions[session_id] = username
        return session_id

    def issue_csrf_token(self, session_id: str) -> str:
        token = secrets.token_hex(16)
        self.csrf_tokens[session_id] = token
        return token

    def validate_csrf(self, session_id: str, token: str) -> bool:
        return self.csrf_tokens.get(session_id) == token and bool(token)


def transfer(
    bank: BankSession,
    session_id: str,
    recipient: str,
    amount: int,
    csrf_token: Optional[str] = None,
    require_csrf: bool = True,
) -> str:
    """执行转账；require_csrf=False 时模拟无防护接口"""
    if session_id not in bank.sessions:
        return "❌ 未登录，转账失败"

    if require_csrf:
        if not csrf_token or not bank.validate_csrf(session_id, csrf_token):
            return "❌ CSRF 令牌无效，请求被拒绝"

    user = bank.sessions[session_id]
    return f"✅ {user} 向 {recipient} 转账 {amount} 元成功"


def demo_csrf_attack_and_defense():
    """演示：无令牌可被伪造请求；有令牌则拒绝非法请求"""
    print("=== CSRF 攻击演示与防御 ===\n")

    bank = BankSession()
    session_id = bank.login("admin", "password123")
    print(f"1. 用户 admin 已登录，会话 ID: {session_id[:8]}...")

    # 无 CSRF 防护：攻击者诱导用户浏览器自动提交表单即可成功
    print("\n2. 【无防护】攻击者伪造转账请求（用户已登录，无令牌校验）")
    attack_result = transfer(
        bank,
        session_id,
        recipient="攻击者账户",
        amount=1000,
        require_csrf=False,
    )
    print(f"   结果: {attack_result}")

    # 有 CSRF 防护：合法请求需携带服务端下发的令牌
    print("\n3. 【有防护】合法用户携带 CSRF 令牌转账")
    token = bank.issue_csrf_token(session_id)
    legit_result = transfer(
        bank,
        session_id,
        recipient="alice",
        amount=100,
        csrf_token=token,
        require_csrf=True,
    )
    print(f"   令牌: {token[:16]}...")
    print(f"   结果: {legit_result}")

    print("\n4. 【有防护】攻击者无法猜测令牌，伪造请求被拒绝")
    fake_result = transfer(
        bank,
        session_id,
        recipient="攻击者账户",
        amount=5000,
        csrf_token="fake-token-12345",
        require_csrf=True,
    )
    print(f"   结果: {fake_result}")

    print("\n💡 防御要点:")
    print("   • 敏感操作使用 POST + 不可预测的 CSRF 令牌")
    print("   • Cookie 设置 SameSite=Lax/Strict")
    print("   • 关键操作可要求二次确认（验证码、密码）")


if __name__ == "__main__":
    demo_csrf_attack_and_defense()
