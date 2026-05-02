#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: 个人主页构建
这个脚本生成并提供一个完整的个人主页，包含HTML、CSS和JavaScript。
用户可以通过运行此脚本并在浏览器中访问 http://localhost:8080 来查看效果。
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time

def generate_personal_homepage():
    """生成个人主页的完整HTML内容"""
    html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>张小明 - 个人主页</title>
    <style>
        /* CSS重置和基础样式 */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f9f9f9;
        }

        /* 头部样式 */
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            text-align: center;
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .avatar {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 4px solid rgba(255,255,255,0.3);
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            color: white;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .tagline {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }

        .social-links {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
        }

        .social-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .social-link:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }

        /* 主要内容区域 */
        main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 20px;
        }

        section {
            margin-bottom: 3rem;
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        h2 {
            color: #2c3e50;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #3498db;
        }

        /* 关于我部分 */
        .about-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            align-items: center;
        }

        .about-text p {
            margin-bottom: 1rem;
        }

        .interests {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .interest-tag {
            background: #e3f2fd;
            color: #1976d2;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.9rem;
        }

        /* 技能部分 */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }

        .skill-category {
            border-left: 4px solid #3498db;
            padding-left: 1rem;
        }

        .skill-category h3 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }

        .skill-item {
            margin-bottom: 0.75rem;
        }

        .skill-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.25rem;
        }

        .skill-bar {
            height: 8px;
            background-color: #ecf0f1;
            border-radius: 4px;
            overflow: hidden;
        }

        .skill-progress {
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            border-radius: 4px;
        }

        /* 项目作品集 */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .project-card {
            border: 1px solid #eee;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }

        .project-image {
            height: 180px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
        }

        .project-content {
            padding: 1.5rem;
        }

        .project-content h3 {
            margin-bottom: 0.5rem;
            color: #2c3e50;
        }

        .project-content p {
            color: #666;
            margin-bottom: 1rem;
            font-size: 0.95rem;
        }

        .project-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }

        .project-tag {
            background: #f8f9fa;
            color: #6c757d;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
        }

        /* 联系表单 */
        .contact-form {
            max-width: 600px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
            color: #2c3e50;
        }

        input,
        textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-family: inherit;
            font-size: 1rem;
        }

        input:focus,
        textarea:focus {
            outline: none;
            border-color: #3498db;
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
        }

        textarea {
            min-height: 150px;
            resize: vertical;
        }

        .submit-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 5px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
        }

        /* 页脚 */
        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 2rem;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }

        .copyright {
            opacity: 0.8;
            margin-top: 1rem;
        }

        /* 响应式设计 */
        @media (max-width: 768px) {
            .about-content {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 2rem;
            }

            .avatar {
                width: 120px;
                height: 120px;
                font-size: 48px;
            }

            main {
                padding: 1.5rem 15px;
            }

            section {
                padding: 1.5rem;
            }
        }

        @media (max-width: 480px) {
            .social-links {
                gap: 0.5rem;
            }

            .social-link {
                width: 35px;
                height: 35px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>
<body>
    <!-- 头部 -->
    <header>
        <div class="header-content">
            <div class="avatar">👤</div>
            <h1>张小明</h1>
            <p class="tagline">前端开发者 | 用户体验爱好者 | 持续学习者</p>
            <div class="social-links">
                <a href="#" class="social-link" title="GitHub">GH</a>
                <a href="#" class="social-link" title="LinkedIn">LI</a>
                <a href="#" class="social-link" title="Twitter">TW</a>
                <a href="#" class="social-link" title="Email">📧</a>
            </div>
        </div>
    </header>

    <!-- 主要内容 -->
    <main>
        <!-- 关于我 -->
        <section id="about">
            <h2>关于我</h2>
            <div class="about-content">
                <div class="about-text">
                    <p>你好！我是张小明，一名热爱前端开发的工程师。我专注于创造美观、高效且用户友好的Web应用。</p>
                    <p>我相信技术应该服务于人，而不是相反。因此，我始终将用户体验放在首位，努力让复杂的功能变得简单直观。</p>
                    <p>在业余时间，我喜欢探索新的Web技术、参与开源项目，并分享我的学习心得。</p>

                    <div class="interests">
                        <span class="interest-tag">前端开发</span>
                        <span class="interest-tag">用户体验设计</span>
                        <span class="interest-tag">开源贡献</span>
                        <span class="interest-tag">技术写作</span>
                        <span class="interest-tag">摄影</span>
                        <span class="interest-tag">旅行</span>
                    </div>
                </div>
                <div class="about-stats">
                    <h3>快速统计</h3>
                    <ul style="list-style: none;">
                        <li style="margin: 10px 0;"><strong>3+</strong> 年前端开发经验</li>
                        <li style="margin: 10px 0;"><strong>15+</strong> 开源项目贡献</li>
                        <li style="margin: 10px 0;"><strong>50+</strong> 技术博客文章</li>
                        <li style="margin: 10px 0;"><strong>100%</strong> 用户满意度</li>
                    </ul>
                </div>
            </div>
        </section>

        <!-- 技能 -->
        <section id="skills">
            <h2>我的技能</h2>
            <div class="skills-grid">
                <div class="skill-category">
                    <h3>前端技术</h3>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>HTML5 & CSS3</span>
                            <span>95%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 95%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>JavaScript (ES6+)</span>
                            <span>90%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 90%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>React & Vue</span>
                            <span>85%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 85%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>TypeScript</span>
                            <span>80%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 80%"></div>
                        </div>
                    </div>
                </div>

                <div class="skill-category">
                    <h3>工具与框架</h3>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>Webpack & Vite</span>
                            <span>85%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 85%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>Tailwind CSS</span>
                            <span>90%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 90%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>Git & GitHub</span>
                            <span>95%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 95%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>Jest & Testing Library</span>
                            <span>75%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 75%"></div>
                        </div>
                    </div>
                </div>

                <div class="skill-category">
                    <h3>软技能</h3>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>问题解决</span>
                            <span>95%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 95%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>团队协作</span>
                            <span>90%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 90%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>沟通能力</span>
                            <span>85%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 85%"></div>
                        </div>
                    </div>
                    <div class="skill-item">
                        <div class="skill-header">
                            <span>持续学习</span>
                            <span>100%</span>
                        </div>
                        <div class="skill-bar">
                            <div class="skill-progress" style="width: 100%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 项目作品集 -->
        <section id="projects">
            <h2>项目作品集</h2>
            <div class="projects-grid">
                <div class="project-card">
                    <div class="project-image">📊</div>
                    <div class="project-content">
                        <h3>数据可视化仪表板</h3>
                        <p>一个基于React和D3.js的数据可视化平台，支持实时数据展示和交互式图表。</p>
                        <div class="project-tags">
                            <span class="project-tag">React</span>
                            <span class="project-tag">D3.js</span>
                            <span class="project-tag">TypeScript</span>
                            <span class="project-tag">REST API</span>
                        </div>
                        <a href="#" style="color: #3498db; text-decoration: none; font-weight: bold;">查看详情 →</a>
                    </div>
                </div>

                <div class="project-card">
                    <div class="project-image">🛒</div>
                    <div class="project-content">
                        <h3>电商平台前端</h3>
                        <p>完整的电商网站前端，包含产品展示、购物车、订单管理和用户认证功能。</p>
                        <div class="project-tags">
                            <span class="project-tag">Vue.js</span>
                            <span class="project-tag">Vuex</span>
                            <span class="project-tag">SCSS</span>
                            <span class="project-tag">Axios</span>
                        </div>
                        <a href="#" style="color: #3498db; text-decoration: none; font-weight: bold;">查看详情 →</a>
                    </div>
                </div>

                <div class="project-card">
                    <div class="project-image">📱</div>
                    <div class="project-content">
                        <h3>移动优先博客系统</h3>
                        <p>响应式博客平台，专为移动设备优化，支持Markdown编辑和SEO友好URL。</p>
                        <div class="project-tags">
                            <span class="project-tag">Next.js</span>
                            <span class="project-tag">Tailwind CSS</span>
                            <span class="project-tag">Markdown</span>
                            <span class="project-tag">Vercel</span>
                        </div>
                        <a href="#" style="color: #3498db; text-decoration: none; font-weight: bold;">查看详情 →</a>
                    </div>
                </div>
            </div>
        </section>

        <!-- 联系我 -->
        <section id="contact">
            <h2>联系我</h2>
            <form class="contact-form" id="contactForm">
                <div class="form-group">
                    <label for="name">姓名</label>
                    <input type="text" id="name" name="name" required placeholder="请输入您的姓名">
                </div>
                <div class="form-group">
                    <label for="email">邮箱</label>
                    <input type="email" id="email" name="email" required placeholder="请输入您的邮箱">
                </div>
                <div class="form-group">
                    <label for="message">消息</label>
                    <textarea id="message" name="message" required placeholder="请输入您的消息"></textarea>
                </div>
                <button type="submit" class="submit-btn">发送消息</button>
            </form>
        </section>
    </main>

    <!-- 页脚 -->
    <footer>
        <div class="footer-content">
            <h3>张小明 - 前端开发者</h3>
            <p>创造美好的数字体验</p>
            <div class="copyright">
                &copy; 2026 张小明. 保留所有权利.
            </div>
        </div>
    </footer>

    <script>
        // 表单提交处理
        document.getElementById('contactForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;

            // 简单的表单验证
            if (!name || !email || !message) {
                alert('请填写所有字段！');
                return;
            }

            // 模拟表单提交（实际项目中会发送到服务器）
            alert(`感谢您的消息，${name}！我们会尽快回复您。`);

            // 重置表单
            this.reset();
        });

        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // 返回顶部按钮（动态创建）
        const backToTop = document.createElement('button');
        backToTop.textContent = '↑';
        backToTop.style.position = 'fixed';
        backToTop.style.bottom = '20px';
        backToTop.style.right = '20px';
        backToTop.style.padding = '10px';
        backToTop.style.backgroundColor = '#3498db';
        backToTop.style.color = 'white';
        backToTop.style.border = 'none';
        backToTop.style.borderRadius = '50%';
        backToTop.style.cursor = 'pointer';
        backToTop.style.display = 'none';
        backToTop.style.zIndex = '1000';
        document.body.appendChild(backToTop);

        // 监听滚动显示/隐藏返回顶部按钮
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTop.style.display = 'block';
            } else {
                backToTop.style.display = 'none';
            }
        });

        // 返回顶部功能
        backToTop.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        console.log('个人主页已加载完成！');
    </script>
</body>
</html>"""
    return html_content

def save_html_file(content, filename="personal-homepage.html"):
    """将HTML内容保存到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 已生成个人主页文件: {filename}")

def start_server(port=8080):
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
    print("🚀 开始构建个人主页...")

    # 生成HTML内容
    html_content = generate_personal_homepage()

    # 保存HTML文件
    save_html_file(html_content)

    # 启动服务器（在新线程中）
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # 等待服务器启动
    time.sleep(1)

    # 自动打开浏览器（可选）
    try:
        webbrowser.open(f"http://localhost:8080")
    except:
        print("💡 请手动在浏览器中打开: http://localhost:8080")

    # 保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 个人主页程序已退出")

if __name__ == "__main__":
    main()