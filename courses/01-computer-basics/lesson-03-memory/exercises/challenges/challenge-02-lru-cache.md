# 挑战2: 实现LRU缓存

## 难度
⭐⭐

## 描述

实现一个LRU（Least Recently Used，最近最少使用）缓存机制。当缓存达到容量上限时，自动淘汰最久未被访问的数据。

这是实际系统中广泛使用的缓存策略，例如操作系统的页面置换、数据库缓存、Redis等都用到了类似的思想。

## 输入

通过方法调用来操作缓存：
- `get(key)` - 获取键对应的值
- `put(key, value)` - 插入或更新键值对

## 输出

- `get` 返回值，如果不存在返回 -1
- `put` 无返回值，如果缓存满则淘汰最久未使用的键

## 示例

```python
cache = LRUCache(capacity=2)

cache.put(1, 1)  # 缓存: {1:1}
cache.put(2, 2)  # 缓存: {1:1, 2:2}
print(cache.get(1))  # 返回 1，缓存: {2:2, 1:1}（1被访问，移到最新）
cache.put(3, 3)  # 淘汰2，缓存: {1:1, 3:3}
print(cache.get(2))  # 返回 -1（已被淘汰）
cache.put(4, 4)  # 淘汰1，缓存: {3:3, 4:4}
print(cache.get(1))  # 返回 -1
print(cache.get(3))  # 返回 3
print(cache.get(4))  # 返回 4
```

## 约束条件

- 容量范围：1 <= capacity <= 3000
- 键值范围：0 <= key <= 10000
- 值的范围：0 <= value <= 10^5
- 最多调用 2 * 10^5 次 get 和 put
- 两个操作都必须是 O(1) 时间复杂度

## 提示

1. 使用哈希表存储键到值的映射，实现 O(1) 查找
2. 使用双向链表维护访问顺序，最近访问的在尾部
3. 当访问一个键时，将其移到链表尾部
4. 当需要淘汰时，移除链表头部的元素

## 进阶思考

- 除了LRU，还有哪些缓存淘汰策略？（如FIFO、LFU）
- 在实际系统中，如何确定缓存的最佳大小？
- Redis的缓存淘汰策略有哪些？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

LRU缓存的核心需求：
1. get和put都要O(1)
2. 需要知道元素的访问顺序

解决方案：
- 哈希表：O(1)查找键值
- 双向链表：O(1)移动元素到尾部，O(1)删除头部元素

链表节点存储键、值，以及前后指针。
哈希表存储键到链表节点的映射。

### 代码

```python
class ListNode:
    """双向链表节点"""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # 键 -> 节点的映射

        # 使用伪头部和伪尾部节点简化操作
        self.head = ListNode()
        self.tail = ListNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        """获取值，如果不存在返回-1"""
        if key not in self.cache:
            return -1

        node = self.cache[key]
        # 移到尾部（标记为最近使用）
        self._remove(node)
        self._add_to_tail(node)

        return node.value

    def put(self, key: int, value: int) -> None:
        """插入或更新值"""
        if key in self.cache:
            # 更新值
            node = self.cache[key]
            node.value = value
            # 移到尾部
            self._remove(node)
            self._add_to_tail(node)
        else:
            # 新建节点
            if len(self.cache) >= self.capacity:
                # 淘汰最久未使用的（头部）
                lru = self.head.next
                self._remove(lru)
                del self.cache[lru.key]

            node = ListNode(key, value)
            self.cache[key] = node
            self._add_to_tail(node)

    def _remove(self, node: ListNode):
        """从链表中移除节点"""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_tail(self, node: ListNode):
        """将节点添加到尾部"""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def print_cache(self):
        """打印当前缓存内容（用于调试）"""
        current = self.head.next
        items = []
        while current != self.tail:
            items.append(f"{current.key}:{current.value}")
            current = current.next
        print(f"缓存内容（从旧到新）: {' -> '.join(items)}")


# 使用Python内置OrderedDict的简洁版本
from collections import OrderedDict

class LRUCacheOrderedDict:
    """使用OrderedDict的LRU缓存实现"""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # 移到末尾（标记为最新）
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # 弹出最旧的
            self.cache.popitem(last=False)


# 测试
if __name__ == "__main__":
    print("=== 手动实现版本 ===")
    cache = LRUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    cache.print_cache()  # 1:1 -> 2:2

    print(f"get(1) = {cache.get(1)}")  # 1
    cache.print_cache()  # 2:2 -> 1:1

    cache.put(3, 3)  # 淘汰2
    print(f"get(2) = {cache.get(2)}")  # -1
    cache.print_cache()  # 1:1 -> 3:3

    cache.put(4, 4)  # 淘汰1
    print(f"get(1) = {cache.get(1)}")  # -1
    print(f"get(3) = {cache.get(3)}")  # 3
    print(f"get(4) = {cache.get(4)}")  # 4

    print("\n=== OrderedDict版本 ===")
    cache2 = LRUCacheOrderedDict(2)
    cache2.put(1, 1)
    cache2.put(2, 2)
    print(f"get(1) = {cache2.get(1)}")
    cache2.put(3, 3)
    print(f"get(2) = {cache2.get(2)}")
```

### 复杂度分析

- 时间复杂度：
  - get: O(1)
  - put: O(1)
- 空间复杂度：O(capacity)，最多存储capacity个键值对

### 其他缓存淘汰策略

1. **FIFO** (First In First Out)：先进先出，最早进入的先淘汰
2. **LFU** (Least Frequently Used)：最少使用，使用次数最少的被淘汰
3. **Random**：随机淘汰
4. **TTL** (Time To Live)：根据过期时间淘汰

在实际系统中，通常需要根据访问模式选择合适的策略。

</details>
