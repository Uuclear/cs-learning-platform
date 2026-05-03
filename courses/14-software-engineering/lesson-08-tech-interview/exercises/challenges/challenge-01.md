# 挑战1：实现LRU缓存

## 背景
LRU（Least Recently Used）缓存是一种常用的缓存淘汰策略，在系统设计面试中经常出现。当缓存容量达到上限时，需要淘汰最近最少使用的数据。

## 要求
实现一个LRU缓存类，支持以下操作：
- `LRUCache(capacity: int)` - 初始化LRU缓存，指定容量
- `get(key: int) -> int` - 获取键对应的值，如果键不存在返回-1
- `put(key: int, value: int)` - 设置键值对，如果键已存在则更新值，如果容量已满则淘汰最近最少使用的键

## 约束条件
- 时间复杂度要求：`get`和`put`操作都必须是O(1)
- 空间复杂度：O(capacity)
- 键值对都是整数类型

## 提示
- 需要结合哈希表（快速查找）和双向链表（维护使用顺序）
- 哈希表存储键到链表节点的映射
- 双向链表头部是最新的，尾部是最久未使用的

## 测试用例
```python
# 示例用法
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))    # 返回 1
cache.put(3, 3)        # 淘汰键 2
print(cache.get(2))    # 返回 -1 (未找到)
print(cache.get(3))    # 返回 3
cache.put(4, 4)        # 淘汰键 1
print(cache.get(1))    # 返回 -1 (未找到)
print(cache.get(3))    # 返回 3
print(cache.get(4))    # 返回 4
```

## 扩展思考
1. 如果需要支持并发访问，应该如何修改设计？
2. 如何监控缓存命中率和性能指标？
3. 在实际系统中，LRU缓存通常与哪些组件配合使用？

完成实现后，请分析你的时间和空间复杂度，并考虑边界情况的处理。