#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：SSR vs SSG 渲染策略优化

这个解决方案展示了如何在实际应用中结合SSR和SSG的优势，
使用混合渲染策略来获得最佳的性能和用户体验。
"""

import time
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class HybridRenderer:
    """混合渲染器 - 结合SSR和SSG的优势"""

    def __init__(self):
        self.ssg_cache = {}
        self.ssr_count = 0
        self.ssg_build_time = None

    def build_static_pages(self, static_pages: List[str]) -> float:
        """构建静态页面（SSG）"""
        start_time = time.time()
        print(f"🏗️  构建 {len(static_pages)} 个静态页面...")

        for page_id in static_pages:
            # 模拟静态内容生成
            content = self._generate_static_content(page_id)
            self.ssg_cache[page_id] = content

        self.ssg_build_time = time.time() - start_time
        print(f"✅ 静态页面构建完成，耗时: {self.ssg_build_time:.3f}秒")
        return self.ssg_build_time

    def _generate_static_content(self, page_id: str) -> str:
        """生成静态内容"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
<!DOCTYPE html>
<html>
<head><title>{page_id} - 静态内容</title></head>
<body>
    <h1>{page_id}</h1>
    <p>这是预构建的静态内容</p>
    <p>构建时间: {timestamp}</p>
</body>
</html>
        """.strip()

    def render_dynamic_page(self, page_id: str, user_context: Optional[Dict] = None) -> Tuple[str, float]:
        """渲染动态页面（SSR）"""
        self.ssr_count += 1
        start_time = time.time()

        # 模拟动态数据获取
        dynamic_data = self._fetch_dynamic_data(page_id, user_context)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
<!DOCTYPE html>
<html>
<head><title>{page_id} - 动态内容</title></head>
<body>
    <h1>{page_id}</h1>
    <p>这是服务器端渲染的动态内容</p>
    <p>渲染时间: {timestamp}</p>
    <p>用户上下文: {user_context or '无'}</p>
    <p>动态数据: {dynamic_data}</p>
</body>
</html>
        """.strip()

        render_time = time.time() - start_time
        return html, render_time

    def _fetch_dynamic_data(self, page_id: str, user_context: Optional[Dict]) -> Dict:
        """模拟动态数据获取"""
        time.sleep(random.uniform(0.05, 0.15))  # 模拟API调用延迟

        return {
            "page_views": random.randint(100, 10000),
            "last_updated": datetime.now().isoformat(),
            "personalized": bool(user_context)
        }

    def serve_page(self, page_id: str, is_static: bool = True, user_context: Optional[Dict] = None) -> Tuple[str, float, str]:
        """
        智能页面服务

        Args:
            page_id: 页面ID
            is_static: 是否为静态页面
            user_context: 用户上下文（用于个性化）

        Returns:
            (HTML内容, 服务时间, 渲染类型)
        """
        start_time = time.time()

        if is_static and page_id in self.ssg_cache:
            # 使用SSG缓存
            html = self.ssg_cache[page_id]
            serve_time = time.time() - start_time
            return html, serve_time, "SSG"
        else:
            # 使用SSR
            html, render_time = self.render_dynamic_page(page_id, user_context)
            total_time = time.time() - start_time
            return html, total_time, "SSR"


def demonstrate_hybrid_rendering():
    """演示混合渲染策略"""
    print("=" * 60)
    print("混合渲染策略演示 (SSG + SSR)")
    print("=" * 60)

    renderer = HybridRenderer()

    # 构建静态页面
    static_pages = ["首页", "关于我们", "产品介绍", "文档"]
    renderer.build_static_pages(static_pages)

    # 测试页面服务
    test_scenarios = [
        ("首页", True, None),           # 静态页面，无用户上下文
        ("用户仪表板", False, {"user_id": 123, "role": "admin"}),  # 动态页面，有用户上下文
        ("产品详情", True, None),       # 静态页面
        ("个性化推荐", False, {"preferences": ["tech", "books"]}), # 动态页面
    ]

    print(f"\n🎯 测试混合渲染:")
    total_ssg_time = 0
    total_ssr_time = 0
    ssg_requests = 0
    ssr_requests = 0

    for page_id, is_static, user_context in test_scenarios:
        html, serve_time, render_type = renderer.serve_page(page_id, is_static, user_context)

        if render_type == "SSG":
            total_ssg_time += serve_time
            ssg_requests += 1
        else:
            total_ssr_time += serve_time
            ssr_requests += 1

        print(f"  ✓ {page_id}: {render_type} ({serve_time*1000:.2f}ms)")

    print(f"\n📊 性能统计:")
    print(f"  • SSG请求: {ssg_requests} 次，平均 {(total_ssg_time/ssg_requests)*1000:.2f}ms")
    print(f"  • SSR请求: {ssr_requests} 次，平均 {(total_ssr_time/ssr_requests)*1000:.2f}ms")
    print(f"  • SSG构建时间: {renderer.ssg_build_time:.3f}秒")
    print(f"  • SSR总渲染次数: {renderer.ssr_count}")

    print(f"\n💡 最佳实践:")
    print(f"  • 将不经常变化的内容使用SSG预构建")
    print(f"  • 将需要个性化或实时数据的内容使用SSR")
    print(f"  • 结合两者可以获得最佳的性能和用户体验")


if __name__ == "__main__":
    demonstrate_hybrid_rendering()