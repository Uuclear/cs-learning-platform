#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：SSR vs SSG 渲染模拟
模拟服务器端渲染（SSR）和静态站点生成（SSG）的差异和性能对比
"""

import time
import random
from datetime import datetime

class SSRRenderer:
    """服务器端渲染模拟器"""

    def __init__(self):
        self.cache = {}
        self.render_count = 0

    def render_page(self, page_id, user_data=None):
        """
        模拟SSR页面渲染
        :param page_id: 页面ID
        :param user_data: 用户数据（个性化内容）
        :return: 渲染后的HTML内容
        """
        self.render_count += 1

        # 模拟从数据库获取数据的时间
        fetch_time = random.uniform(0.05, 0.2)
        time.sleep(fetch_time)

        # 模拟数据处理时间
        process_time = random.uniform(0.02, 0.1)
        time.sleep(process_time)

        # 生成个性化HTML
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SSR 页面 - {page_id}</title>
</head>
<body>
    <h1>欢迎访问 {page_id}</h1>
    <p>服务器渲染时间: {timestamp}</p>
    <p>用户数据: {user_data if user_data else '未提供'}</p>
    <p>这是通过服务器端渲染(SSR)生成的内容</p>
</body>
</html>
        """
        return html.strip()

class SSGRenderer:
    """静态站点生成模拟器"""

    def __init__(self):
        self.build_cache = {}
        self.build_time = None
        self.build_count = 0

    def build_site(self, pages):
        """
        模拟SSG构建过程（在构建时生成所有页面）
        :param pages: 要构建的页面列表
        """
        self.build_count += 1
        print(f"开始构建静态站点，共 {len(pages)} 个页面...")

        # 模拟构建时间
        build_start = time.time()
        time.sleep(random.uniform(0.5, 1.5))

        for page_id in pages:
            # 模拟从CMS或数据库获取数据
            fetch_time = random.uniform(0.03, 0.1)
            time.sleep(fetch_time)

            # 生成静态HTML
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>SSG 页面 - {page_id}</title>
</head>
<body>
    <h1>欢迎访问 {page_id}</h1>
    <p>构建时间: {timestamp}</p>
    <p>这是通过静态站点生成(SSG)预构建的内容</p>
    <p>注意：此内容在构建时已固定，无法个性化</p>
</body>
</html>
            """
            self.build_cache[page_id] = html.strip()

        self.build_time = time.time() - build_start
        print(f"静态站点构建完成，耗时 {self.build_time:.2f} 秒")

    def serve_page(self, page_id):
        """
        模拟SSG服务页面（直接返回预构建的HTML）
        :param page_id: 页面ID
        :return: 预构建的HTML内容
        """
        if page_id in self.build_cache:
            # 模拟CDN分发的极快速度
            time.sleep(random.uniform(0.001, 0.01))
            return self.build_cache[page_id]
        else:
            return "<h1>404 - 页面未找到</h1>"

def compare_rendering_strategies():
    """比较SSR和SSG的性能差异"""
    print("=" * 60)
    print("SSR vs SSG 渲染策略性能对比")
    print("=" * 60)

    # 测试页面
    test_pages = ["首页", "关于我们", "产品", "博客", "联系"]
    user_data = {"name": "张三", "role": "VIP用户"}

    # 测试SSR
    print("\n🚀 测试服务器端渲染 (SSR):")
    ssr = SSRRenderer()
    ssr_start = time.time()

    for page in test_pages:
        html = ssr.render_page(page, user_data)
        print(f"  ✓ 渲染 {page}: {len(html)} 字符")

    ssr_total = time.time() - ssr_start
    print(f"  SSR 总耗时: {ssr_total:.3f} 秒")
    print(f"  SSR 渲染次数: {ssr.render_count}")

    # 测试SSG
    print("\n⚡ 测试静态站点生成 (SSG):")
    ssg = SSGRenderer()

    # 构建阶段
    build_start = time.time()
    ssg.build_site(test_pages)
    build_time = ssg.build_time

    # 服务阶段（模拟多个用户访问）
    serve_start = time.time()
    for page in test_pages:
        html = ssg.serve_page(page)
        print(f"  ✓ 服务 {page}: {len(html)} 字符")

    serve_time = time.time() - serve_start
    total_ssg_time = build_time + serve_time

    print(f"  SSG 构建耗时: {build_time:.3f} 秒")
    print(f"  SSG 服务耗时: {serve_time:.3f} 秒")
    print(f"  SSG 总耗时: {total_ssg_time:.3f} 秒")
    print(f"  SSG 构建次数: {ssg.build_count}")

    # 性能对比总结
    print("\n📊 性能对比总结:")
    print(f"  • SSR: 每次请求都重新渲染，支持个性化但较慢")
    print(f"  • SSG: 构建时生成，服务时极快但内容固定")
    print(f"  • 对于 {len(test_pages)} 个页面:")
    print(f"    - SSR 总时间: {ssr_total:.3f}s")
    print(f"    - SSG 总时间: {total_ssg_time:.3f}s ({build_time:.3f}s 构建 + {serve_time:.3f}s 服务)")

    if ssr_total > total_ssg_time:
        print("  💡 结论: 对于静态内容，SSG更高效")
    else:
        print("  💡 结论: 对于高度个性化内容，SSR可能更适合")

if __name__ == "__main__":
    compare_rendering_strategies()