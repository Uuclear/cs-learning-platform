#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XSS（跨站脚本）攻击演示与防御

本示例展示了XSS攻击的不同类型以及如何通过输出编码进行防御。
注意：此代码仅用于教育目的，演示如何正确处理用户输入以防止XSS。
"""

import html
import re
from urllib.parse import unquote


def demonstrate_xss_attacks():
    """演示不同类型的XSS攻击向量"""
    print("=== XSS攻击向量演示 ===\n")

    # 存储型XSS示例（模拟数据库存储的恶意内容）
    stored_xss = '<script>alert("存储型XSS攻击！")</script>'

    # 反射型XSS示例（模拟URL参数中的恶意内容）
    reflected_xss = '<img src="x" onerror="alert(\'反射型XSS攻击！\')">'

    # DOM型XSS示例（模拟JavaScript中不安全的操作）
    dom_xss = 'javascript:alert("DOM型XSS攻击！")'

    print("常见的XSS攻击向量:")
    print(f"1. 存储型: {stored_xss}")
    print(f"2. 反射型: {reflected_xss}")
    print(f"3. DOM型: {dom_xss}\n")


def unsafe_output(user_input):
    """
    不安全的输出方式 - 直接将用户输入插入HTML

    这会导致XSS攻击，因为浏览器会执行嵌入的脚本
    """
    # 危险！直接将用户输入插入HTML模板
    html_template = f"""
    <html>
    <body>
        <h1>欢迎, {user_input}!</h1>
        <p>这是不安全的输出方式。</p>
    </body>
    </html>
    """
    return html_template


def safe_output_html(user_input):
    """
    安全的HTML输出 - 使用HTML实体编码

    将特殊字符转换为HTML实体，防止脚本执行
    """
    # 安全！对用户输入进行HTML编码
    safe_input = html.escape(user_input, quote=True)
    html_template = f"""
    <html>
    <body>
        <h1>欢迎, {safe_input}!</h1>
        <p>这是安全的HTML输出方式。</p>
    </body>
    </html>
    """
    return html_template


def safe_output_javascript(user_input):
    """
    安全的JavaScript输出 - 使用JSON编码和DOM操作

    当需要在JavaScript上下文中输出数据时使用安全的DOM操作
    """
    import json
    # 安全！使用JSON编码处理用户输入，并使用createElement等安全方法
    safe_input = json.dumps(user_input)
    js_template = f"""
    <html>
    <body>
        <div id="welcome"></div>
        <p>这是安全的JavaScript输出方式。</p>
        <script>
            var username = {safe_input};
            var welcomeDiv = document.getElementById('welcome');
            var heading = document.createElement('h1');
            heading.textContent = '欢迎, ' + username + '!';
            welcomeDiv.appendChild(heading);
        </script>
    </body>
    </html>
    """
    return js_template


def content_security_policy_demo():
    """演示内容安全策略(CSP)的使用"""
    print("=== 内容安全策略(CSP)演示 ===")
    csp_headers = [
        "Content-Security-Policy: default-src 'self'",
        "Content-Security-Policy: script-src 'self' 'unsafe-inline'",
        "Content-Security-Policy: style-src 'self' 'unsafe-inline'",
        "Content-Security-Policy: img-src 'self' data: https://*"
    ]

    print("CSP可以限制页面加载的资源类型:")
    for header in csp_headers:
        print(f"- {header}")
    print()


def main():
    """主函数 - 演示XSS攻击与防御"""
    demonstrate_xss_attacks()

    # 测试恶意输入
    malicious_input = '<script>alert("XSS攻击成功！")</script>'

    print("=== XSS防御演示 ===\n")

    print("1. 不安全的输出 (危险！):")
    unsafe_html = unsafe_output(malicious_input)
    print("生成的HTML包含可执行脚本:")
    print(unsafe_html[:100] + "...")

    print("\n2. 安全的HTML输出:")
    safe_html = safe_output_html(malicious_input)
    print("生成的HTML已编码，脚本不会执行:")
    print(safe_html[:100] + "...")

    print("\n3. 安全的JavaScript输出:")
    safe_js = safe_output_javascript(malicious_input)
    print("生成的JavaScript使用安全的DOM操作:")
    print(safe_js[:150] + "...")

    print("\n4. 额外防护 - 内容安全策略:")
    content_security_policy_demo()

    # 演示其他编码方式
    print("=== 其他安全编码技术 ===")
    print("除了HTML编码，还需要根据上下文选择合适的编码:")
    print("- HTML属性值: html.escape() + 引号包围")
    print("- URL参数: urllib.parse.quote()")
    print("- CSS: 避免直接插入用户输入到CSS中")
    print("- JavaScript: json.dumps() 或专用JS编码库\n")


if __name__ == "__main__":
    main()