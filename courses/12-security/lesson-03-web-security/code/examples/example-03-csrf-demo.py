#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSRF（跨站请求伪造）攻击演示与防御

本示例以控制台模拟方式展示 CSRF 攻击原理及令牌防御机制。
注意：此代码仅用于教育目的，演示 CSRF 防护机制。
"""

import secrets
import urllib.parse


class BankSession:
    """模拟银行会话与 CSRF 令牌存储"""

    def __init__(self):
        self.sessions = {}
        self.csrf_tokens = {}
        self.users = {"admin": "password123"}

    def login(self, username: str, password: str) -> str | None:
        if self.users.get(username) != password:
            return None
        session_id = secrets.token_hex(8)
        self.sessions[session_id] = username
        return session_id

    def issue_csrf_token(self, session_id: str) -> str:
        token = secrets.token_hex(16)
        self.csrf_tokens[session_id] = token
        return token

    def transfer(
        self,
        session_id: str,
        recipient: str,
        amount: int,
        csrf_token: str | None = None,
        require_csrf: bool = True,
    ) -> tuple[bool, str]:
        if session_id not in self.sessions:
            return False, "未登录，转账被拒绝"

        if require_csrf:
            expected = self.csrf_tokens.get(session_id)
            if not csrf_token or csrf_token != expected:
                return False, "CSRF 令牌无效，转账被拒绝"

        user = self.sessions[session_id]
        return True, f"用户 {user} 向 {recipient} 转账 {amount} 元成功"


def simulate_malicious_form_post() -> dict[str, str]:
    """模拟攻击者在恶意页面发起的自动 POST 请求"""
    return {
        "recipient": "攻击者账户",
        "amount": "1000",
    }


def main():
    print("=== CSRF 攻击演示与防御 ===\n")

    bank = BankSession()
    session_id = bank.login("admin", "password123")
    print(f"1. 用户登录成功，会话 ID: {session_id[:8]}...")

    # 场景 A：无 CSRF 防护 —— 攻击者伪造请求可成功
    print("\n--- 场景 A：无 CSRF 令牌验证（易受攻击）---")
    forged = simulate_malicious_form_post()
    ok, msg = bank.transfer(
        session_id,
        forged["recipient"],
        int(forged["amount"]),
        csrf_token=None,
        require_csrf=False,
    )
    print(f"   恶意站点自动提交: {urllib.parse.urlencode(forged)}")
    print(f"   结果: {msg} {'⚠️' if ok else ''}")

    # 场景 B：有 CSRF 防护 —— 伪造请求缺少有效令牌
    print("\n--- 场景 B：启用 CSRF 令牌验证（推荐）---")
    token = bank.issue_csrf_token(session_id)
    print(f"   合法表单获得令牌: {token[:16]}...")

    ok, msg = bank.transfer(
        session_id,
        forged["recipient"],
        int(forged["amount"]),
        csrf_token=None,
        require_csrf=True,
    )
    print(f"   攻击者伪造请求（无令牌）: {msg}")

    ok, msg = bank.transfer(
        session_id,
        "alice",
        100,
        csrf_token=token,
        require_csrf=True,
    )
    print(f"   用户正常提交（带令牌）: {msg}")

    print("\n防御要点:")
    print("  • 每个敏感表单附带一次性 CSRF 令牌")
    print("  • 服务端校验令牌与会话绑定")
    print("  • Cookie 设置 SameSite=Lax/Strict 作为辅助措施")


if __name__ == "__main__":
    main()
