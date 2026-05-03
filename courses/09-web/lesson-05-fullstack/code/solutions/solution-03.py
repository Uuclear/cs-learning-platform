#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：优化的数据获取策略

这个解决方案展示了如何在实际应用中优化数据获取，
包括缓存策略、并行请求、错误处理和性能监控。
"""

import time
import random
import asyncio
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from functools import wraps


class OptimizedDataFetcher:
    """优化的数据获取器"""

    def __init__(self):
        self.cache = {}
        self.cache_stats = {'hits': 0, 'misses': 0}
        self.request_stats = {'total': 0, 'errors': 0}

    def cache_with_ttl(self, ttl_seconds: int = 300):
        """带TTL的缓存装饰器"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # 创建缓存键
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
                current_time = time.time()

                # 检查缓存
                if cache_key in self.cache:
                    cached_data, expiry_time = self.cache[cache_key]
                    if current_time < expiry_time:
                        self.cache_stats['hits'] += 1
                        return cached_data

                self.cache_stats['misses'] += 1

                # 执行函数
                try:
                    result = await func(*args, **kwargs)
                    # 缓存结果
                    self.cache[cache_key] = (result, current_time + ttl_seconds)
                    return result
                except Exception as e:
                    self.request_stats['errors'] += 1
                    raise e
                finally:
                    self.request_stats['total'] += 1

            return wrapper
        return decorator

    async def fetch_api_data(self, endpoint: str, delay_range: Tuple[float, float] = (0.1, 0.3)) -> Dict:
        """模拟API数据获取"""
        print(f"  📡 请求 {endpoint}")
        delay = random.uniform(*delay_range)
        await asyncio.sleep(delay)

        # 模拟偶尔的错误
        if random.random() < 0.05:  # 5% 错误率
            raise Exception(f"API错误: {endpoint}")

        if "posts" in endpoint:
            return {
                "id": random.randint(1, 1000),
                "title": f"文章 {random.randint(1, 100)}",
                "content": "文章内容...",
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
            return {"data": "模拟数据", "timestamp": datetime.now().isoformat()}

    async def get_static_props_optimized(self, page_context: Dict) -> Dict:
        """优化的getStaticProps实现"""
        # Apply caching manually instead of using decorator
        cache_key = f"get_static_props_optimized:{hash(str(page_context))}"
        current_time = time.time()

        if cache_key in self.cache:
            cached_data, expiry_time = self.cache[cache_key]
            if current_time < expiry_time:
                self.cache_stats['hits'] += 1
                return cached_data

        self.cache_stats['misses'] += 1
        print("🔄 执行优化的 getStaticProps...")

        # 并行获取多个数据源
        posts_task = self.fetch_api_data("/api/posts")
        users_task = self.fetch_api_data("/api/users")
        config_task = self.fetch_api_data("/api/config")

        try:
            posts, users, config = await asyncio.gather(posts_task, users_task, config_task)

            result = {
                "posts": [posts],
                "users": [users],
                "config": config,
                "buildTime": datetime.now().isoformat(),
                "pageContext": page_context
            }

            # 缓存结果 (60秒TTL)
            self.cache[cache_key] = (result, current_time + 60)
            return result
        except Exception as e:
            self.request_stats['errors'] += 1
            raise e
        finally:
            self.request_stats['total'] += 1

    async def get_server_side_props_optimized(self, page_context: Dict) -> Dict:
        """优化的getServerSideProps实现"""
        # Apply caching manually instead of using decorator
        cache_key = f"get_server_side_props_optimized:{hash(str(page_context))}"
        current_time = time.time()

        if cache_key in self.cache:
            cached_data, expiry_time = self.cache[cache_key]
            if current_time < expiry_time:
                self.cache_stats['hits'] += 1
                return cached_data

        self.cache_stats['misses'] += 1
        print("🔄 执行优化的 getServerSideProps...")

        # 根据用户上下文个性化数据获取
        user_id = page_context.get("user", {}).get("id")
        try:
            if user_id:
                user_profile_task = self.fetch_api_data(f"/api/users/{user_id}")
                user_posts_task = self.fetch_api_data(f"/api/posts?user={user_id}")
                featured_posts_task = self.fetch_api_data("/api/posts/featured")

                user_profile, user_posts, featured_posts = await asyncio.gather(
                    user_profile_task, user_posts_task, featured_posts_task
                )
            else:
                # 匿名用户获取通用数据
                featured_posts_task = self.fetch_api_data("/api/posts/featured")
                popular_posts_task = self.fetch_api_data("/api/posts/popular")
                featured_posts, popular_posts = await asyncio.gather(
                    featured_posts_task, popular_posts_task
                )
                user_profile = None
                user_posts = []

            result = {
                "userProfile": user_profile,
                "userPosts": user_posts,
                "featuredPosts": [featured_posts],
                "popularPosts": [popular_posts] if not user_id else [],
                "serverRenderTime": datetime.now().isoformat(),
                "requestContext": page_context
            }

            # 缓存结果 (10秒TTL)
            self.cache[cache_key] = (result, current_time + 10)
            return result
        except Exception as e:
            self.request_stats['errors'] += 1
            raise e
        finally:
            self.request_stats['total'] += 1

    async def incremental_static_regeneration_optimized(self, slug: str, revalidate: int = 60) -> Dict:
        """优化的增量静态再生"""
        cache_key = f"isr_page_{slug}"
        current_time = time.time()

        # 检查后台更新
        if cache_key in self.cache:
            cached_data, last_update = self.cache[cache_key]
            if current_time - last_update < revalidate:
                # 返回缓存数据，同时在后台检查是否需要更新
                asyncio.create_task(self._background_revalidate(slug, revalidate))
                return cached_data

        # 需要重新生成
        return await self._regenerate_page(slug, revalidate)

    async def _background_revalidate(self, slug: str, revalidate: int):
        """后台重新验证"""
        await asyncio.sleep(revalidate - 5)  # 提前5秒开始重新验证
        try:
            new_data = await self._regenerate_page(slug, revalidate)
            print(f"✅ 后台重新验证完成: {slug}")
        except Exception as e:
            print(f"❌ 后台重新验证失败: {slug}, 错误: {e}")

    async def _regenerate_page(self, slug: str, revalidate: int) -> Dict:
        """重新生成页面"""
        print(f"🔄 重新生成页面: {slug}")

        post_task = self.fetch_api_data(f"/api/posts/{slug}")
        related_task = self.fetch_api_data(f"/api/posts/{slug}/related")
        comments_task = self.fetch_api_data(f"/api/posts/{slug}/comments")

        post, related, comments = await asyncio.gather(post_task, related_task, comments_task)

        data = {
            "post": post,
            "relatedPosts": [related],
            "comments": [comments],
            "generatedAt": datetime.now().isoformat(),
            "revalidate": revalidate
        }

        # 更新缓存
        self.cache[f"isr_page_{slug}"] = (data, time.time())
        return data

    def get_performance_metrics(self) -> Dict:
        """获取性能指标"""
        total_requests = self.request_stats['total']
        cache_hits = self.cache_stats['hits']
        cache_misses = self.cache_stats['misses']

        return {
            "totalRequests": total_requests,
            "cacheHits": cache_hits,
            "cacheMisses": cache_misses,
            "cacheHitRate": cache_hits / (cache_hits + cache_misses) if (cache_hits + cache_misses) > 0 else 0,
            "errorRate": self.request_stats['errors'] / total_requests if total_requests > 0 else 0,
            "cacheSize": len(self.cache)
        }


async def demonstrate_optimized_data_fetching():
    """演示优化的数据获取"""
    print("=" * 70)
    print("优化的数据获取策略演示")
    print("=" * 70)

    fetcher = OptimizedDataFetcher()

    # 测试1: 优化的SSG
    print("\n🚀 测试1: 优化的静态站点生成 (getStaticProps)")
    print("-" * 50)
    ssg_start = time.time()
    ssg_data = await fetcher.get_static_props_optimized({"params": {"slug": "welcome"}})
    ssg_time = time.time() - ssg_start
    print(f"✅ SSG完成，耗时: {ssg_time:.3f}秒")

    # 测试2: 优化的SSR（有用户上下文）
    print("\n⚡ 测试2: 优化的服务器端渲染 (getServerSideProps)")
    print("-" * 50)
    ssr_start = time.time()
    ssr_data = await fetcher.get_server_side_props_optimized({
        "user": {"id": 123, "name": "张三"},
        "ip": "192.168.1.100"
    })
    ssr_time = time.time() - ssr_start
    print(f"✅ SSR完成，耗时: {ssr_time:.3f}秒")

    # 测试3: ISR性能测试
    print("\n🔄 测试3: 增量静态再生性能")
    print("-" * 50)

    # 第一次访问
    isr_start1 = time.time()
    isr_data1 = await fetcher.incremental_static_regeneration_optimized("blog-post-1", revalidate=30)
    isr_time1 = time.time() - isr_start1
    print(f"✅ ISR第一次: {isr_time1:.3f}秒")

    # 立即再次访问（应该使用缓存）
    isr_start2 = time.time()
    isr_data2 = await fetcher.incremental_static_regeneration_optimized("blog-post-1", revalidate=30)
    isr_time2 = time.time() - isr_start2
    print(f"✅ ISR第二次: {isr_time2:.3f}秒")

    # 显示性能指标
    metrics = fetcher.get_performance_metrics()
    print(f"\n📊 性能指标:")
    print(f"  • 总请求数: {metrics['totalRequests']}")
    print(f"  • 缓存命中率: {metrics['cacheHitRate']:.2%}")
    print(f"  • 缓存大小: {metrics['cacheSize']}")
    print(f"  • 错误率: {metrics['errorRate']:.2%}")

    print(f"\n💡 优化要点:")
    print(f"  • 使用缓存减少重复API调用")
    print(f"  • 并行请求提高数据获取效率")
    print(f"  • 后台重新验证保证数据新鲜度")
    print(f"  • 错误处理和监控确保可靠性")


if __name__ == "__main__":
    asyncio.run(demonstrate_optimized_data_fetching())