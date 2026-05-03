#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：缓存策略模拟器

这个脚本比较不同的HTTP缓存策略对命中率的影响，
包括no-cache、max-age、stale-while-revalidate等策略。
"""

import random
from collections import defaultdict
from datetime import datetime, timedelta


class CacheSimulator:
    """缓存模拟器类"""

    def __init__(self, cache_capacity=100):
        """
        初始化缓存模拟器

        :param cache_capacity: 缓存容量（条目数）
        """
        self.cache_capacity = cache_capacity
        self.cache = {}  # {resource_id: {'content': content, 'timestamp': timestamp, 'ttl': ttl}}
        self.stats = defaultdict(int)  # 统计信息

    def simulate_no_cache(self, requests):
        """
        模拟no-cache策略：每次请求都去源服务器

        :param requests: 请求列表 [(resource_id, timestamp), ...]
        :return: 命中率
        """
        hits = 0
        total = len(requests)

        for resource_id, timestamp in requests:
            # no-cache策略总是miss，需要重新验证
            self.stats['no_cache_requests'] += 1
            # 模拟条件请求（If-Modified-Since等）
            self.stats['conditional_requests'] += 1

        return 0.0  # 命中率总是0%

    def simulate_max_age(self, requests, max_age_seconds):
        """
        模拟max-age缓存策略

        :param requests: 请求列表 [(resource_id, timestamp), ...]
        :param max_age_seconds: 最大年龄（秒）
        :return: 命中率
        """
        hits = 0
        total = len(requests)
        cache = {}

        for resource_id, timestamp in requests:
            current_time = timestamp

            if resource_id in cache:
                cached_time, cached_content = cache[resource_id]
                age = (current_time - cached_time).total_seconds()

                if age <= max_age_seconds:
                    # 缓存命中
                    hits += 1
                    self.stats['max_age_hits'] += 1
                else:
                    # 缓存过期，需要重新获取
                    cache[resource_id] = (current_time, f"content_{resource_id}")
                    self.stats['max_age_misses'] += 1
            else:
                # 缓存未命中
                cache[resource_id] = (current_time, f"content_{resource_id}")
                self.stats['max_age_misses'] += 1

            # 维护缓存大小
            if len(cache) > self.cache_capacity:
                # 简单的LRU：移除最早的条目
                oldest_key = min(cache.keys(), key=lambda k: cache[k][0])
                del cache[oldest_key]

        return hits / total if total > 0 else 0.0

    def simulate_stale_while_revalidate(self, requests, max_age_seconds, stale_while_seconds):
        """
        模拟stale-while-revalidate缓存策略

        :param requests: 请求列表 [(resource_id, timestamp), ...]
        :param max_age_seconds: 最大年龄（秒）
        :param stale_while_seconds: 允许使用过期内容的时间（秒）
        :return: 命中率（包括新鲜和过期但可用的）
        """
        hits = 0
        total = len(requests)
        cache = {}

        for resource_id, timestamp in requests:
            current_time = timestamp

            if resource_id in cache:
                cached_time, cached_content = cache[resource_id]
                age = (current_time - cached_time).total_seconds()
                total_valid_time = max_age_seconds + stale_while_seconds

                if age <= total_valid_time:
                    # 可以使用缓存（新鲜或过期但在stale-while窗口内）
                    hits += 1
                    self.stats['swr_hits'] += 1

                    # 如果在stale-while窗口内，后台重新验证
                    if age > max_age_seconds:
                        self.stats['swr_background_refresh'] += 1
                else:
                    # 完全过期，需要重新获取
                    cache[resource_id] = (current_time, f"content_{resource_id}")
                    self.stats['swr_misses'] += 1
            else:
                # 缓存未命中
                cache[resource_id] = (current_time, f"content_{resource_id}")
                self.stats['swr_misses'] += 1

            # 维护缓存大小
            if len(cache) > self.cache_capacity:
                oldest_key = min(cache.keys(), key=lambda k: cache[k][0])
                del cache[oldest_key]

        return hits / total if total > 0 else 0.0

    def generate_requests(self, num_requests=1000, time_span_hours=24, popular_ratio=0.3):
        """
        生成模拟请求数据

        :param num_requests: 请求总数
        :param time_span_hours: 时间跨度（小时）
        :param popular_ratio: 热门资源比例
        :return: 请求列表 [(resource_id, timestamp), ...]
        """
        requests = []
        start_time = datetime.now()

        # 创建热门和普通资源
        num_popular = int(20 * popular_ratio)
        num_regular = 80

        for i in range(num_requests):
            # 随机选择时间点
            time_offset = random.uniform(0, time_span_hours * 3600)
            request_time = start_time + timedelta(seconds=time_offset)

            # 80%概率请求热门资源，20%请求普通资源
            if random.random() < 0.8 and num_popular > 0:
                resource_id = f"popular_{random.randint(1, num_popular)}"
            else:
                resource_id = f"regular_{random.randint(1, num_regular)}"

            requests.append((resource_id, request_time))

        # 按时间排序
        requests.sort(key=lambda x: x[1])
        return requests


def main():
    """主函数：运行缓存策略比较"""
    print("=== HTTP缓存策略模拟器 ===\n")

    # 创建模拟器
    simulator = CacheSimulator(cache_capacity=50)

    # 生成测试请求
    print("正在生成测试请求...")
    requests = simulator.generate_requests(num_requests=1000, time_span_hours=24)
    print(f"生成了 {len(requests)} 个请求\n")

    # 测试不同策略
    strategies = [
        ("no-cache", lambda: simulator.simulate_no_cache(requests)),
        ("max-age=300 (5分钟)", lambda: simulator.simulate_max_age(requests, 300)),
        ("max-age=3600 (1小时)", lambda: simulator.simulate_max_age(requests, 3600)),
        ("stale-while-revalidate (max-age=300, swr=60)",
         lambda: simulator.simulate_stale_while_revalidate(requests, 300, 60)),
        ("stale-while-revalidate (max-age=3600, swr=300)",
         lambda: simulator.simulate_stale_while_revalidate(requests, 3600, 300))
    ]

    results = []
    for name, strategy_func in strategies:
        hit_rate = strategy_func()
        results.append((name, hit_rate))
        print(f"{name:40} 命中率: {hit_rate:.2%}")

    print("\n=== 缓存策略分析 ===")
    print("1. no-cache: 每次都需要重新验证，但保证内容最新")
    print("2. max-age: 简单有效，但过期后会有延迟")
    print("3. stale-while-revalidate: 最佳用户体验，后台刷新保证内容新鲜")

    print("\n=== 推荐策略 ===")
    best_strategy = max(results, key=lambda x: x[1])
    print(f"最佳策略: {best_strategy[0]} (命中率: {best_strategy[1]:.2%})")

    if "stale-while-revalidate" in best_strategy[0]:
        print("✅ 推荐使用stale-while-revalidate策略获得最佳性能和用户体验")


if __name__ == "__main__":
    main()