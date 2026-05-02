#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: HTML + CSS 基础演示
这个脚本生成一个简单的HTML页面，展示HTML结构和CSS样式的结合使用。
用户可以通过运行此脚本并在浏览器中访问 http://localhost:8000 来查看效果。
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time

def generate_html_content():
    """生成包含HTML结构和CSS样式的完整HTML内容"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>前端基础示例 - HTML + CSS</title>
    <style>
        /* 页面基础样式 */
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }

        /* 容器样式 */
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        /* 标题样式 */
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }

        /* 个人卡片样式 */
        .profile-card {
            display: flex;
            align-items: center;
            gap: 20px;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fafafa;
        }

        .avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(45deg, #3498db, #9b59b6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 24px;
        }

        .profile-info h2 {
            margin: 0 0 5px 0;
            color: #2c3e50;
        }

        .profile-info p {
            margin: 0;
            color: #7f8c8d;
        }

        /* 技能条样式 */
        .skills {
            margin-top: 20px;
        }

        .skill-item {
            margin-bottom: 10px;
        }

        .skill-name {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            font-weight: bold;
        }

        .skill-bar {
            height: 10px;
            background-color: #ecf0f1;
            border-radius: 5px;
            overflow: hidden;
        }

        .skill-progress {
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            border-radius: 5px;
        }

        /* 响应式设计 */
        @media (max-width: 600px) {
            .profile-card {
                flex-direction: column;
                text-align: center;
            }

            .container {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 前端基础示例</h1>

        <!-- 个人卡片 -->
        <div class="profile-card">
            <div class="avatar">👤</div>
            <div class="profile-info">
                <h2>张小明</h2>
                <p>前端开发者 | 热爱创造美好的用户体验</p>
            </div>
        </div>

        <!-- 技能展示 -->
        <div class="skills">
            <h3>我的技能</h3>
            <div class="skill-item">
                <div class="skill-name">
                    <span>HTML5</span>
                    <span>95%</span>
                </div>
                <div class="skill-bar">
                    <div class="skill-progress" style="width: 95%"></div>
                </div>
            </div>
            <div class="skill-item">
                <div class="skill-name">
                    <span>CSS3</span>
                    <span>90%</span>
                </div>
                <div class="skill-bar">
                    <div class="skill-progress" style="width: 90%"></div>
                </div>
            </div>
            <div class="skill-item">
                <div class="skill-name">
                    <span>JavaScript</span>
                    <span>85%</span>
                </div>
                <div class="skill-bar">
                    <div class="skill-progress" style="width: 85%"></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    return html_content

def save_html_file(content, filename="index.html"):
    """将HTML内容保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已生成HTML文件: {filename}")

def start_server(port=8000):
    """启动HTTP服务器"""
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 服务器已启动，请在浏览器中访问: http://localhost:{port}")
        print("按 Ctrl+C 停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")
            httpd.shutdown()

def main():
    """主函数"""
    print("🚀 开始生成前端基础示例...")

    # 生成HTML内容
    html_content = generate_html_content()

    # 保存HTML文件
    save_html_file(html_content)

    # 启动服务器（在新线程中）
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 等待服务器启动
    time.sleep(1)

    # 自动打开浏览器（可选）
    try:
        webbrowser.open(f"http://localhost:8000")
    except:
        print("💡 请手动在浏览器中打开: http://localhost:8000")

    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 示例程序已退出")

if __name__ == "__main__":
    main()