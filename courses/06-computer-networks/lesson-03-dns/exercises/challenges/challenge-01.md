# 编程挑战 1：DNS 缓存优化

## 背景
在实际的 DNS 系统中，缓存是提高性能的关键。但简单的 TTL 机制有时不够灵活。

## 任务
实现一个智能 DNS 缓存系统，要求：

1. 支持基本的 get/set 操作和 TTL 过期
2. 实现 LRU（最近最少使用）淘汰策略，当缓存达到容量限制时自动清理
3. 支持动态调整 TTL：频繁访问的记录可以适当延长 TTL，不常访问的记录缩短 TTL

## 要求
- 使用 Python 3.10+
- 缓存容量限制为 100 条记录
- 初始 TTL 为 300 秒（5 分钟）
- 频繁访问的定义：1 分钟内访问超过 3 次
- 不常访问的定义：10 分钟内只访问 1 次

## 提示
- 可以使用 collections.OrderedDict 来实现 LRU
- 需要记录每个记录的访问历史
- 考虑线程安全问题（可选）

## 测试用例
```python
cache = SmartDNSCache(capacity=3)
cache.set("google.com", "142.250.185.206")
cache.set("baidu.com", "220.181.38.148") 
cache.set("github.com", "140.82.114.4")
cache.set("example.com", "93.184.216.34")  # 应该触发 LRU 淘汰

# 验证 google.com 是否被正确淘汰（因为最久未使用）
assert cache.get("google.com") is None
```