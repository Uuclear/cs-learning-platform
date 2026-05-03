#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：数据获取策略模拟

这个脚本模拟了Next.js中的不同数据获取策略：
- getStaticProps (SSG)
- getServerSideProps (SSR)
- getStaticPaths + ISR (增量静态再生)
"""

import time
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class DataFetchingSimulator:
    """数据获取策略模拟器"""

    def __init__(self):
        self.cache = {}
        self.last_build_time = None
        self.revalidation_count = 0

    def simulate_api_call(self, endpoint: str, delay_ms: int = 100) -> Dict:
        """
        模拟API调用

        Args:
            endpoint: API端点
            delay_ms: 模拟网络延迟（毫秒）

        Returns:
            API响应数据
        """
        print(f"  📡 调用API: {endpoint}")
        time.sleep(delay_ms / 1000)

        # 模拟不同的API响应
        if "posts" in endpoint:
            return {
                "id": random.randint(1, 1000),
                "title": f"文章标题 {random.randint(1, 100)}",
                "content": "这是文章内容...",
                "author": f"作者{random.randint(1, 10)}",
                "published_at": datetime.now().isoformat(),
                "views": random.randint(0, 10000)
            }
        elif "users" in endpoint:
            return {
                "id": random.randint(1, 100),
                "name": f"用户{random.randint(1, 100)}",
                "email": f"user{random.randint(1, 100)}@example.com",
                "role": random.choice(["admin", "user", "guest"])
            }
        else:
            return {"data": "模拟数据"}

    def get_static_props(self, page_context: Dict) -> Tuple[Dict, float]:
        """
        模拟getStaticProps - 在构建时获取数据（SSG）

        Args:
            page_context: 页面上下文

        Returns:
            (props数据, 执行时间)
        """
        start_time = time.time()
        print("🔄 执行 getStaticProps...")

        # 模拟在构建时获取数据
        posts_data = self.simulate_api_call("/api/posts", delay_ms=200)
        user_data = self.simulate_api_call("/api/users", delay_ms=150)

        props = {
            "posts": [posts_data],
            "user": user_data,
            "buildTime": datetime.now().isoformat(),
            "pageContext": page_context
        }

        execution_time = time.time() - start_time
        print(f"✅ getStaticProps 完成，耗时: {execution_time:.3f}秒")
        return props, execution_time

    def get_server_side_props(self, page_context: Dict) -> Tuple[Dict, float]:
        """
        模拟getServerSideProps - 在每次请求时获取数据（SSR）

        Args:
            page_context: 页面上下文（包含请求信息）

        Returns:
            (props数据, 执行时间)
        """
        start_time = time.time()
        print("🔄 执行 getServerSideProps...")

        # 模拟在每次请求时获取最新数据
        posts_data = self.simulate_api_call("/api/posts/latest", delay_ms=100)
        user_data = self.simulate_api_call("/api/users/current", delay_ms=80)

        # 可以访问请求头、cookies等
        request_info = {
            "ip": page_context.get("ip", "127.0.0.1"),
            "userAgent": page_context.get("userAgent", "模拟浏览器"),
            "timestamp": datetime.now().isoformat()
        }

        props = {
            "posts": [posts_data],
            "user": user_data,
            "requestInfo": request_info,
            "serverRenderTime": datetime.now().isoformat()
        }

        execution_time = time.time() - start_time
        print(f"✅ getServerSideProps 完成，耗时: {execution_time:.3f}秒")
        return props, execution_time

    def get_static_paths(self) -> Tuple[List[Dict], float]:
        """
        模拟getStaticPaths - 获取所有静态路径

        Returns:
            (路径列表, 执行时间)
        """
        start_time = time.time()
        print("🔄 执行 getStaticPaths...")

        # 模拟获取所有可能的静态路径
        paths = []
        for i in range(1, 6):  # 模拟5个博客文章
            paths.append({
                "params": {"slug": f"post-{i}"},
                "locale": "zh-CN"
            })

        execution_time = time.time() - start_time
        print(f"✅ getStaticPaths 完成，生成 {len(paths)} 个路径，耗时: {execution_time:.3f}秒")
        return paths, execution_time

    def incremental_static_regeneration(self, page_params: Dict, revalidate_seconds: int = 60) -> Tuple[Dict, bool, float]:
        """
        模拟增量静态再生（ISR）

        Args:
            page_params: 页面参数
            revalidate_seconds: 重新验证间隔（秒）

        Returns:
            (props数据, 是否从缓存获取, 执行时间)
        """
        start_time = time.time()
        slug = page_params.get("slug", "default")

        # 检查缓存是否有效
        cache_key = f"page_{slug}"
        current_time = datetime.now()

        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            time_diff = (current_time - cached_time).total_seconds()

            if time_diff < revalidate_seconds:
                print(f"📦 从缓存返回页面 {slug} (缓存年龄: {time_diff:.1f}秒)")
                execution_time = time.time() - start_time
                return cached_data, True, execution_time

        print(f"🔄 重新生成页面 {slug} (缓存过期或不存在)")

        # 获取新数据
        post_data = self.simulate_api_call(f"/api/posts/{slug}", delay_ms=120)
        related_posts = [self.simulate_api_call("/api/posts/related", delay_ms=80)]

        props = {
            "post": post_data,
            "relatedPosts": related_posts,
            "generatedAt": current_time.isoformat(),
            "revalidate": revalidate_seconds
        }

        # 更新缓存
        self.cache[cache_key] = (props, current_time)
        self.revalidation_count += 1

        execution_time = time.time() - start_time
        print(f"✅ 页面 {slug} 重新生成完成，耗时: {execution_time:.3f}秒")
        return props, False, execution_time


def compare_data_fetching_strategies():
    """比较不同的数据获取策略"""
    print("=" * 70)
    print("Next.js 数据获取策略对比模拟")
    print("=" * 70)

    simulator = DataFetchingSimulator()

    # 测试场景1: 静态站点生成 (SSG)
    print("\n🚀 场景1: 静态站点生成 (getStaticProps)")
    print("-" * 50)
    ssg_context = {"params": {"slug": "welcome"}}
    ssg_props, ssg_time = simulator.get_static_props(ssg_context)

    # 测试场景2: 服务器端渲染 (SSR)
    print("\n⚡ 场景2: 服务器端渲染 (getServerSideProps)")
    print("-" * 50)
    ssr_context = {
        "ip": "192.168.1.100",
        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }
    ssr_props, ssr_time = simulator.get_server_side_props(ssr_context)

    # 测试场景3: 增量静态再生 (ISR)
    print("\n🔄 场景3: 增量静态再生 (ISR)")
    print("-" * 50)

    # 第一次访问（缓存未命中）
    isr_params = {"slug": "blog-post-1"}
    isr_props1, from_cache1, isr_time1 = simulator.incremental_static_regeneration(isr_params, revalidate_seconds=30)

    # 立即再次访问（应该从缓存获取）
    time.sleep(1)
    isr_props2, from_cache2, isr_time2 = simulator.incremental_static_regeneration(isr_params, revalidate_seconds=30)

    # 等待超过revalidate时间后访问
    print(f"\n⏳ 等待35秒（超过revalidate时间30秒）...")
    time.sleep(35)
    isr_props3, from_cache3, isr_time3 = simulator.incremental_static_regeneration(isr_params, revalidate_seconds=30)

    # 性能对比总结
    print("\n📊 性能对比总结:")
    print(f"  • SSG (getStaticProps): {ssg_time:.3f}秒 (构建时执行，服务时为0)")
    print(f"  • SSR (getServerSideProps): {ssr_time:.3f}秒 (每次请求都执行)")
    print(f"  • ISR 第一次: {isr_time1:.3f}秒 (缓存未命中)")
    print(f"  • ISR 第二次: {isr_time2:.3f}秒 (缓存命中)")
    print(f"  • ISR 35秒后: {isr_time3:.3f}秒 (缓存过期，重新生成)")
    print(f"  • ISR 重新验证次数: {simulator.revalidation_count}")

    print("\n💡 使用建议:")
    print("  • SSG: 适合内容不经常变化的页面（如文档、博客）")
    print("  • SSR: 适合需要实时数据或个性化内容的页面（如仪表板、用户资料）")
    print("  • ISR: 适合内容偶尔更新但需要高性能的页面（如新闻、产品目录）")


if __name__ == "__main__":
    compare_data_fetching_strategies()