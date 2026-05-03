#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：安全的Web应用程序示例

实现一个简单的Web应用，包含适当的输入验证和输出编码。
使用Python内置的http.server模块构建。
"""

import http.server
import socketserver
import urllib.parse
import html
import re
import json


class SecureWebAppHandler(http.server.BaseHTTPRequestHandler):
    """安全的Web应用处理器"""

    def do_GET(self):
        """处理GET请求"""
        if self.path == '/':
            self.show_homepage()
        elif self.path.startswith('/search'):
            self.handle_search()
        else:
            self.send_error(404)

    def do_POST(self):
        """处理POST请求"""
        if self.path == '/submit':
            self.handle_form_submission()
        else:
            self.send_error(404)

    def show_homepage(self):
        """显示主页（包含搜索表单和提交表单）"""
        html_content = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>安全Web应用示例</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .form-group { margin: 20px 0; }
                input[type="text"], input[type="email"], textarea {
                    width: 300px; padding: 8px; border: 1px solid #ddd;
                }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; }
            </style>
        </head>
        <body>
            <h1>安全Web应用示例</h1>

            <h2>安全搜索</h2>
            <form method="GET" action="/search">
                <div class="form-group">
                    <label>搜索关键词:</label><br>
                    <input type="text" name="q" placeholder="输入搜索词" required>
                </div>
                <button type="submit">搜索</button>
            </form>

            <h2>安全表单提交</h2>
            <form method="POST" action="/submit">
                <div class="form-group">
                    <label>姓名:</label><br>
                    <input type="text" name="name" placeholder="请输入姓名" required>
                </div>
                <div class="form-group">
                    <label>邮箱:</label><br>
                    <input type="email" name="email" placeholder="请输入邮箱" required>
                </div>
                <div class="form-group">
                    <label>评论:</label><br>
                    <textarea name="comment" rows="4" placeholder="请输入评论"></textarea>
                </div>
                <button type="submit">提交</button>
            </form>

            <h2>安全特性说明</h2>
            <ul>
                <li><strong>输入验证</strong>: 对所有用户输入进行格式和内容验证</li>
                <li><strong>输出编码</strong>: 在HTML上下文中对输出进行HTML实体编码</li>
                <li><strong>内容类型</strong>: 正确设置Content-Type头</li>
                <li><strong>错误处理</strong>: 不暴露敏感的错误信息</li>
            </ul>
        </body>
        </html>
        """
        self.send_html_response(html_content)

    def handle_search(self):
        """处理搜索请求（带输入验证和输出编码）"""
        # 解析查询参数
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        search_term = params.get('q', [''])[0]

        # 输入验证
        if not search_term:
            self.send_error(400, "搜索词不能为空")
            return

        if len(search_term) > 100:
            self.send_error(400, "搜索词长度不能超过100个字符")
            return

        # 验证搜索词只包含允许的字符（防止特殊字符注入）
        if not re.match(r'^[a-zA-Z0-9一-鿿\s\-_]+$', search_term):
            self.send_error(400, "搜索词包含不允许的字符")
            return

        # 安全的输出编码
        safe_search_term = html.escape(search_term, quote=True)

        # 模拟搜索结果
        results = [
            f"结果1: 关于 '{safe_search_term}' 的相关信息",
            f"结果2: '{safe_search_term}' 的详细说明",
            f"结果3: 相关链接到 '{safe_search_term}'"
        ]

        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>搜索结果</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .result {{ margin: 20px 0; padding: 10px; border-left: 3px solid #007bff; }}
            </style>
        </head>
        <body>
            <h1>搜索结果: {safe_search_term}</h1>
            {''.join(f'<div class="result">{result}</div>' for result in results)}
            <p><a href="/">返回主页</a></p>
        </body>
        </html>
        """
        self.send_html_response(html_content)

    def handle_form_submission(self):
        """处理表单提交（带完整输入验证）"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)

        name = params.get('name', [''])[0]
        email = params.get('email', [''])[0]
        comment = params.get('comment', [''])[0]

        # 输入验证
        errors = []

        # 姓名验证
        if not name or len(name.strip()) == 0:
            errors.append("姓名不能为空")
        elif len(name) > 50:
            errors.append("姓名长度不能超过50个字符")
        elif not re.match(r'^[一-鿿\w\s\-]+$', name):
            errors.append("姓名包含不允许的字符")

        # 邮箱验证
        if not email or len(email.strip()) == 0:
            errors.append("邮箱不能为空")
        elif len(email) > 100:
            errors.append("邮箱长度不能超过100个字符")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("邮箱格式不正确")

        # 评论验证
        if comment and len(comment) > 500:
            errors.append("评论长度不能超过500个字符")

        if errors:
            error_html = "<br>".join(errors)
            self.send_error(400, f"输入验证失败: {error_html}")
            return

        # 安全的输出编码
        safe_name = html.escape(name.strip(), quote=True)
        safe_email = html.escape(email.strip(), quote=True)
        safe_comment = html.escape(comment.strip(), quote=True) if comment else ""

        # 成功响应
        html_content = f"""
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <title>提交成功</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .success {{ background: #d4edda; padding: 20px; border: 1px solid #c3e6cb; }}
            </style>
        </head>
        <body>
            <div class="success">
                <h2>提交成功！</h2>
                <p><strong>姓名:</strong> {safe_name}</p>
                <p><strong>邮箱:</strong> {safe_email}</p>
                {'<p><strong>评论:</strong> ' + safe_comment + '</p>' if safe_comment else ''}
            </div>
            <p><a href="/">返回主页</a></p>
        </body>
        </html>
        """
        self.send_html_response(html_content)

    def send_html_response(self, content):
        """发送HTML响应（带安全头）"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        # 添加安全相关的HTTP头
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'DENY')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))


def main():
    """主函数 - 启动安全Web应用"""
    print("=== 安全Web应用示例 ===")
    print("启动服务器: http://localhost:8080")
    print("功能特点:")
    print("- 输入验证（格式、长度、字符集）")
    print("- 输出编码（HTML实体编码）")
    print("- 安全HTTP头")
    print("- 适当的错误处理")
    print("按 Ctrl+C 停止服务器\n")

    try:
        with socketserver.TCPServer(("", 8080), SecureWebAppHandler) as httpd:
            print("服务器运行中...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")


if __name__ == "__main__":
    main()