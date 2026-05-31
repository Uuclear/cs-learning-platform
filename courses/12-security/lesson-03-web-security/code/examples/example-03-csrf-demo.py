#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSRF（跨站请求伪造）攻击演示与防御

本示例用控制台模拟说明 CSRF 原理与令牌防御，无需启动 HTTP 服务。
教育用途：理解为何敏感操作必须校验 CSRF Token。
"""

import secrets
import urllib.parse


class CSRFDefenseDemo:
    """CSRF 防护机制演示（内存会话）"""

    def __init__(self):
        self.sessions: dict[str, str] = {}
        self.csrf_tokens: dict[str, str] = {}
        self.users = {"admin": "password123"}

    def login(self, username: str, password: str) -> str | None:
        if self.users.get(username) == password:
            session_id = secrets.token_hex(8)
            self.sessions[session_id] = username
            return session_id
        return None

    def issue_csrf_token(self, session_id: str) -> str:
        token = secrets.token_hex(16)
        self.csrf_tokens[session_id] = token
        return token

    def transfer_unsafe(self, session_id: str, recipient: str, amount: int) -> tuple[bool, str]:
        """无 CSRF 校验的转账（漏洞版本，仅用于对比演示）"""
        if session_id not in self.sessions:
            return False, "未登录"
        user = self.sessions[session_id]
        return True, f"用户 {user} 向 {recipient} 转账 {amount} 元成功（未校验 CSRF）"

    def transfer(self, session_id: str, csrf_token: str, recipient: str, amount: int) -> tuple[bool, str]:
        if session_id not in self.sessions:
            return False, "未登录"
        expected = self.csrf_tokens.get(session_id)
        if not expected or csrf_token != expected:
            return False, "CSRF 令牌无效 — 请求被拒绝"
        user = self.sessions[session_id]
        return True, f"用户 {user} 向 {recipient} 转账 {amount} 元成功"


def demo_without_csrf_token():
    """模拟无 CSRF 防护时，恶意站点可伪造 POST"""
    print("【场景 A】无 CSRF 令牌校验")
    demo = CSRFDefenseDemo()
    session = demo.login("admin", "password123")
    cookie = f"sessionid={session}"
    print(f"  用户已登录，Cookie: {cookie}")

    forged_body = urllib.parse.urlencode({"recipient": "attacker", "amount": "1000"})
    print("  恶意站点伪造 POST:", forged_body)
    ok, msg = demo.transfer_unsafe(session, "attacker", 1000)
    print(f"  结果: {msg} (允许={ok})\n")


def demo_with_csrf_token():
    """有 CSRF 令牌时，伪造请求无法通过"""
    print("【场景 B】启用 CSRF 令牌")
    demo = CSRFDefenseDemo()
    session = demo.login("admin", "password123")
    token = demo.issue_csrf_token(session)
    print(f"  合法表单携带令牌: {token[:16]}...")

    ok, msg = demo.transfer(session, token, "bob", 100)
    print(f"  合法请求: {msg}")

    ok, msg = demo.transfer(session, "", "attacker", 1000)
    print(f"  伪造请求（无令牌）: {msg}\n")


def demo_samesite_cookie():
    """说明 SameSite Cookie 的辅助作用"""
    print("【场景 C】SameSite Cookie 辅助防御")
    print("  Set-Cookie: sessionid=...; HttpOnly; Secure; SameSite=Lax")
    print("  跨站 POST 通常不会携带 Cookie，可降低 CSRF 风险（需配合令牌）\n")


def main():
    print("=== CSRF 攻击演示与防御 ===\n")
    demo_without_csrf_token()
    demo_with_csrf_token()
    demo_samesite_cookie()
    print("✅ 演示完成。生产环境请使用框架内置 CSRF 中间件（如 Django/Flask-WTF）。")


if __name__ == "__main__":
    main()
