# 练习2解答：实现LRU缓存

class ListNode:
    """双向链表节点"""
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """LRU缓存实现（使用双向链表+哈希表）"""

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

    def print_cache(self):
        """打印当前缓存内容"""
        items = [f"{k}:{v}" for k, v in self.cache.items()]
        print(f"缓存内容（从旧到新）: {' -> '.join(items)}")


# 测试代码
if __name__ == "__main__":
    print("=== 手动实现版本 ===\n")

    cache = LRUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    cache.print_cache()

    print(f"\nget(1) = {cache.get(1)}")
    cache.print_cache()

    cache.put(3, 3)
    print(f"\nput(3,3)后（淘汰2）:")
    cache.print_cache()
    print(f"get(2) = {cache.get(2)}")

    cache.put(4, 4)
    print(f"\nput(4,4)后（淘汰1）:")
    cache.print_cache()
    print(f"get(1) = {cache.get(1)}")
    print(f"get(3) = {cache.get(3)}")
    cache.print_cache()
    print(f"get(4) = {cache.get(4)}")
    cache.print_cache()

    print("\n=== OrderedDict版本 ===\n")

    cache2 = LRUCacheOrderedDict(2)
    cache2.put(1, 1)
    cache2.put(2, 2)
    cache2.print_cache()
    print(f"get(1) = {cache2.get(1)}")
    cache2.put(3, 3)
    print(f"get(2) = {cache2.get(2)}")
    cache2.print_cache()
