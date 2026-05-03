#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：安全头中间件

为Python HTTP服务器实现安全头中间件，包括CSP、HSTS、X-Frame-Options等。
"""

import http.server
import socketserver
from functools import wraps


def security_headers_middleware(handler_class):
    """
    安全头中间件装饰器

    为HTTP响应添加各种安全相关的HTTP头
    """
    class SecureHandler(handler_class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def end_headers(self):
            """在发送头之前添加安全头"""
            # 内容安全策略 (CSP)
            # 限制页面可以加载的资源，防止XSS攻击
            self.send_header(
                'Content-Security-Policy',
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline'; "
                "style-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                "img-src 'self' data: https:; "
                "font-src 'self' https:; "
                "connect-src 'self'; "
                "frame-ancestors 'none';"
            )

            # HTTP严格传输安全 (HSTS)
            # 强制浏览器使用HTTPS（在生产环境中应启用）
            # self.send_header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')

            # X-Frame-Options
            # 防止点击劫持攻击
            self.send_header('X-Frame-Options', 'DENY')

            # X-Content-Type-Options
            # 防止MIME类型嗅探
            self.send_header('X-Content-Type-Options', 'nosniff')

            # Referrer-Policy
            # 控制referrer信息的发送
            self.send_header('Referrer-Policy', 'no-referrer-when-downgrade')

            # Permissions-Policy (以前称为Feature-Policy)
            # 控制浏览器功能的使用
            self.send_header('Permissions-Policy', 'geolocation=(), microphone=(), camera=()')

            # 调用父类的end_headers方法
            super().end_headers()

    return SecureHandler


class BasicWebHandler(http.server.SimpleHTTPRequestHandler):
    """基础Web处理器"""

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.show_homepage()
        else:
            super().do_GET()

    def show_homepage(self):
        """显示主页"""
        html_content = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>安全头中间件演示</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                .security-feature { margin: 20px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #007bff; }
                code { background: #f1f1f1; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>安全头中间件演示</h1>

            <p>本页面通过安全头中间件自动添加了以下安全HTTP头：</p>

            <div class="security-feature">
                <h3>🛡️ Content-Security-Policy (CSP)</h3>
                <p>限制页面可以加载的资源类型，有效防止XSS攻击。</p>
                <code>Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; ...</code>
            </div>

            <div class="security-feature">
                <h3>🔒 X-Frame-Options</h3>
                <p>防止点击劫持攻击，禁止页面被嵌入到iframe中。</p>
                <code>X-Frame-Options: DENY</code>
            </div>

            <div class="security-feature">
                <h3>🛡️ X-Content-Type-Options</h3>
                <p>防止浏览器进行MIME类型嗅探，强制使用声明的内容类型。</p>
                <code>X-Content-Type-Options: nosniff</code>
            </div>

            <div class="security-feature">
                <h3>🌐 Referrer-Policy</h3>
                <p>控制referrer信息的发送，保护用户隐私。</p>
                <code>Referrer-Policy: no-referrer-when-downgrade</code>
            </div>

            <div class="security-feature">
                <h3>⚙️ Permissions-Policy</h3>
                <p>控制浏览器功能的使用，如地理位置、摄像头、麦克风等。</p>
                <code>Permissions-Policy: geolocation=(), microphone=(), camera=()</code>
            </div>

            <h2>如何使用此中间件</h2>
            <p>只需将你的处理器类传递给 <code>security_headers_middleware</code> 装饰器：</p>
            <pre><code>
# 基础处理器
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 你的处理逻辑

# 应用安全头中间件
SecureHandler = security_headers_middleware(MyHandler)

# 使用安全处理器
with socketserver.TCPServer(("", 8000), SecureHandler) as httpd:
    httpd.serve_forever()
            </code></pre>

            <p><strong>注意</strong>：在生产环境中，还应该启用HSTS并配置适当的CSP策略。</p>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))


def main():
    """主函数 - 启动带安全头的Web服务器"""
    print("=== 安全头中间件演示 ===")
    print("启动服务器: http://localhost:8000")
    print("功能特点:")
    print("- 自动添加CSP、X-Frame-Options等安全头")
    print("- 防止XSS、点击劫持、MIME嗅探等攻击")
    print("- 可轻松集成到现有HTTP处理器中")
    print("按 Ctrl+C 停止服务器\n")

    # 应用安全头中间件
    SecureHandler = security_headers_middleware(BasicWebHandler)

    try:
        with socketserver.TCPServer(("", 8000), SecureHandler) as httpd:
            print("服务器运行中...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")


if __name__ == "__main__":
    main()