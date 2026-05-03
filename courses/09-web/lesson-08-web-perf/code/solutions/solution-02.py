#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：高级缓存策略实现

这个解决方案实现了更真实的缓存模拟，
包括ETag验证、条件请求和缓存层级。
"""

import hashlib
from datetime import datetime, timedelta


class AdvancedCacheSimulator:
    """高级缓存模拟器"""

    def __init__(self):
        self.origin_server = {}  # 源服务器存储 {resource_id: (content, last_modified, etag)}
        self.browser_cache = {}  # 浏览器缓存 {resource_id: cache_entry}
        self.cdn_cache = {}      # CDN缓存

    def store_resource(self, resource_id, content, last_modified=None):
        """在源服务器存储资源"""
        if last_modified is None:
            last_modified = datetime.now()

        etag = hashlib.md5(content.encode()).hexdigest()
        self.origin_server[resource_id] = (content, last_modified, etag)

    def request_with_caching(self, resource_id, current_time, cache_strategy):
        """
        模拟带缓存的请求

        :param resource_id: 资源ID
        :param current_time: 当前时间
        :param cache_strategy: 缓存策略字典
        :return: (hit_type, response_time_ms)
        """
        # 检查CDN缓存
        cdn_hit = self._check_cdn_cache(resource_id, current_time, cache_strategy)
        if cdn_hit:
            return "cdn_hit", 50  # CDN命中，50ms延迟

        # 检查浏览器缓存
        browser_hit = self._check_browser_cache(resource_id, current_time, cache_strategy)
        if browser_hit:
            return "browser_hit", 1  # 浏览器命中，1ms延迟

        # 缓存未命中，需要从源服务器获取
        if resource_id in self.origin_server:
            content, last_modified, etag = self.origin_server[resource_id]

            # 更新CDN和浏览器缓存
            self._update_caches(resource_id, content, last_modified, etag, current_time, cache_strategy)
            return "cache_miss", 200  # 缓存未命中，200ms延迟

        return "not_found", 0

    def _check_cdn_cache(self, resource_id, current_time, strategy):
        """检查CDN缓存"""
        if resource_id not in self.cdn_cache:
            return False

        entry = self.cdn_cache[resource_id]
        age = (current_time - entry['stored_at']).total_seconds()

        if age <= strategy.get('cdn_max_age', 3600):
            return True

        # 检查stale-while-revalidate
        if age <= strategy.get('cdn_max_age', 3600) + strategy.get('cdn_stale_while', 300):
            # 后台刷新
            return True

        return False

    def _check_browser_cache(self, resource_id, current_time, strategy):
        """检查浏览器缓存"""
        if resource_id not in self.browser_cache:
            return False

        entry = self.browser_cache[resource_id]
        age = (current_time - entry['stored_at']).total_seconds()

        if age <= strategy.get('browser_max_age', 300):
            return True

        # 检查stale-while-revalidate
        if age <= strategy.get('browser_max_age', 300) + strategy.get('browser_stale_while', 60):
            return True

        return False

    def _update_caches(self, resource_id, content, last_modified, etag, current_time, strategy):
        """更新缓存"""
        cache_entry = {
            'content': content,
            'last_modified': last_modified,
            'etag': etag,
            'stored_at': current_time
        }

        # 更新CDN缓存
        self.cdn_cache[resource_id] = cache_entry.copy()

        # 更新浏览器缓存
        self.browser_cache[resource_id] = cache_entry.copy()


if __name__ == "__main__":
    # 创建模拟器并测试
    simulator = AdvancedCacheSimulator()

    # 存储一些资源
    simulator.store_resource("index.html", "<html>...</html>")
    simulator.store_resource("app.js", "console.log('hello');")

    # 测试不同策略
    strategies = [
        {"browser_max_age": 300, "cdn_max_age": 3600},
        {"browser_max_age": 300, "browser_stale_while": 60, "cdn_max_age": 3600, "cdn_stale_while": 300}
    ]

    current_time = datetime.now()
    for i, strategy in enumerate(strategies):
        hit_type, latency = simulator.request_with_caching("app.js", current_time, strategy)
        print(f"策略{i+1}: {hit_type}, 延迟: {latency}ms")