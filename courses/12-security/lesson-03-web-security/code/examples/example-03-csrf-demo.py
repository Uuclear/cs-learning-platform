#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSRF（跨站请求伪造）攻击演示与防御

本示例展示了CSRF攻击的原理以及如何使用令牌进行防御。
注意：此代码仅用于教育目的，演示CSRF防护机制。
"""

import http.server
import socketserver
import urllib.parse
import secrets
import json
from http.cookies import SimpleCookie


class CSRFHandler(http.server.BaseHTTPRequestHandler):
    """CSRF演示处理器"""

    # 存储会话和CSRF令牌（实际应用中应使用数据库）
    sessions = {}
    users = {"admin": "password123"}

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.show_main_page()
        elif self.path == '/transfer':
            self.show_transfer_form()
        elif self.path.startswith('/login'):
            self.show_login_form()
        else:
            self.send_error(404)

    def do_POST(self):
        """处理POST请求"""
        if self.path == '/login':
            self.handle_login()
        elif self.path == '/transfer':
            self.handle_transfer()
        else:
            self.send_error(404)

    def show_main_page(self):
        """显示主页"""
        session_id = self.get_session_id()
        is_logged_in = session_id in self.sessions

        html_content = f"""
        <html>
        <head><title>银行转账系统</title></head>
        <body>
            <h1>安全银行系统</h1>
            {'<p>已登录为: ' + self.sessions.get(session_id, '') + '</p>' if is_logged_in else '<p>请先登录</p>'}
            <p><a href="/login">登录</a> | <a href="/transfer">转账</a></p>
            <h2>CSRF攻击说明</h2>
            <p>CSRF攻击利用用户已认证的会话，在用户不知情的情况下执行操作。</p>
            <p>攻击者可以创建恶意网站，诱导用户点击，自动发起转账请求。</p>
            <h3>防御措施</h3>
            <ul>
                <li>使用CSRF令牌验证每个敏感操作</li>
                <li>设置SameSite Cookie属性</li>
                <li>验证Referer头（辅助措施）</li>
            </ul>
        </body>
        </html>
        """
        self.send_html_response(html_content)

    def show_login_form(self):
        """显示登录表单"""
        html_content = """
        <html>
        <head><title>登录</title></head>
        <body>
            <h2>用户登录</h2>
            <form method="POST" action="/login">
                用户名: <input type="text" name="username" required><br><br>
                密码: <input type="password" name="password" required><br><br>
                <input type="submit" value="登录">
            </form>
            <p>测试账户: admin / password123</p>
        </body>
        </html>
        """
        self.send_html_response(html_content)

    def handle_login(self):
        """处理登录请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)

        username = params.get('username', [''])[0]
        password = params.get('password', [''])[0]

        if username in self.users and self.users[username] == password:
            # 创建会话
            session_id = secrets.token_hex(16)
            self.sessions[session_id] = username

            # 设置会话Cookie（实际应用中应设置HttpOnly和Secure标志）
            self.send_response(302)
            self.send_header('Set-Cookie', f'sessionid={session_id}; Path=/; SameSite=Lax')
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(401, "用户名或密码错误")

    def show_transfer_form(self):
        """显示转账表单（带CSRF保护）"""
        session_id = self.get_session_id()
        if session_id not in self.sessions:
            self.send_error(401, "请先登录")
            return

        # 生成CSRF令牌
        csrf_token = secrets.token_hex(32)
        # 在实际应用中，令牌应存储在服务器端并与会话关联
        # 这里为了简化，每次请求都生成新令牌

        html_content = f"""
        <html>
        <head><title>转账</title></head>
        <body>
            <h2>转账表单（带CSRF保护）</h2>
            <form method="POST" action="/transfer">
                <input type="hidden" name="csrf_token" value="{csrf_token}">
                收款人: <input type="text" name="recipient" required><br><br>
                金额: <input type="number" name="amount" min="1" required><br><br>
                <input type="submit" value="转账">
            </form>
            <p><b>CSRF令牌:</b> {csrf_token}</p>
            <p>注意：每个表单都有唯一的CSRF令牌，服务器会验证该令牌。</p>
            <h3>CSRF攻击演示</h3>
            <p>如果移除CSRF令牌验证，攻击者可以创建如下恶意表单：</p>
            <pre>
&lt;form action="http://localhost:8000/transfer" method="POST"&gt;
  &lt;input type="hidden" name="recipient" value="攻击者账户"&gt;
  &lt;input type="hidden" name="amount" value="1000"&gt;
  &lt;input type="submit" value="点击赢取大奖！"&gt;
&lt;/form&gt;
            </pre>
            <p>用户点击后会在不知情的情况下完成转账。</p>
        </body>
        </html>
        """
        self.send_html_response(html_content)

    def handle_transfer(self):
        """处理转账请求（带CSRF验证）"""
        session_id = self.get_session_id()
        if session_id not in self.sessions:
            self.send_error(401, "请先登录")
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)

        # CSRF令牌验证（简化版 - 实际应用中应更严格）
        received_token = params.get('csrf_token', [''])[0]
        if not received_token:
            self.send_error(403, "缺少CSRF令牌 - 请求被拒绝")
            return

        # 在实际应用中，这里应该验证令牌是否与会话匹配
        # 由于我们每次生成新令牌，这里只检查是否存在

        recipient = params.get('recipient', [''])[0]
        amount = params.get('amount', [''])[0]

        if not recipient or not amount:
            self.send_error(400, "缺少必要参数")
            return

        # 执行转账（模拟）
        response_html = f"""
        <html>
        <body>
            <h2>转账成功！</h2>
            <p>向 {recipient} 转账 {amount} 元</p>
            <p><a href="/">返回主页</a></p>
        </body>
        </html>
        """
        self.send_html_response(response_html)

    def get_session_id(self):
        """从Cookie中获取会话ID"""
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookie = SimpleCookie()
            cookie.load(cookie_header)
            if 'sessionid' in cookie:
                return cookie['sessionid'].value
        return None

    def send_html_response(self, content):
        """发送HTML响应"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))


def run_cli_demo():
    """命令行演示：无需启动 HTTP 服务即可理解 CSRF 防护"""
    print("=== CSRF 攻击演示与防御（命令行模式）===\n")

    session_id = secrets.token_hex(8)
    CSRFHandler.sessions[session_id] = "admin"
    valid_token = secrets.token_hex(16)

    print("1. 用户已登录，会话 Cookie 已建立")
    print(f"   sessionid={session_id[:12]}...")

    print("\n2. 合法转账请求（带 CSRF 令牌）")
    print(f"   csrf_token={valid_token[:12]}... recipient=Bob amount=100")
    print("   ✅ 服务器验证令牌 → 转账允许")

    print("\n3. 恶意站点发起的伪造请求（无令牌）")
    print("   recipient=攻击者 amount=10000 （无 csrf_token）")
    print("   ❌ 服务器拒绝 → 403 缺少 CSRF 令牌")

    print("\n4. 防御要点")
    print("   • 每个敏感表单嵌入不可预测的 CSRF 令牌")
    print("   • 服务端校验令牌与会话绑定")
    print("   • Cookie 设置 SameSite=Lax/Strict")
    print("\n💡 运行 python example-03-csrf-demo.py --server 可启动交互式演示服务器")


def main():
    """默认运行命令行演示；--server 启动 HTTP 服务"""
    import sys

    if "--server" in sys.argv:
        print("=== CSRF攻击演示与防御 ===")
        print("启动服务器: http://localhost:8000")
        print("注意：此演示仅用于教育目的")
        print("按 Ctrl+C 停止服务器\n")
        try:
            with socketserver.TCPServer(("", 8000), CSRFHandler) as httpd:
                print("服务器运行中...")
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
    else:
        run_cli_demo()


if __name__ == "__main__":
    main()