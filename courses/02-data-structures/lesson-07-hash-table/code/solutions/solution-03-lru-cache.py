# ============================================
# 解答3：LRU缓存
# 使用OrderedDict（哈希表+双向链表的组合）
# ============================================

from collections import OrderedDict

class LRUCache:
    """
    LRU（Least Recently Used）缓存实现
    使用OrderedDict：内部 = 哈希表（O(1)查找）+ 双向链表（O(1)移动）
    链表头部=最近使用，链表尾部=最久未用
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        """
        获取缓存中的值
        如果key存在，标记为最近使用并返回值
        不存在返回-1
        """
        if key not in self.cache:
            return -1
        # 移到末尾（标记为最近使用）
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        """
        插入或更新键值对
        如果key已存在，更新并标记为最近使用
        如果是新key，插入末尾
        超出容量时淘汰最久未用的（第一个元素）
        """
        if key in self.cache:
            # 已存在，标记为最近使用
            self.cache.move_to_end(key)
        self.cache[key] = value

        # 超出容量，淘汰头部的（最久未用的）
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# 测试
if __name__ == "__main__":
    print("=== LRU缓存 ===")
    cache = LRUCache(2)

    cache.put(1, 1)
    print("put(1, 1)")
    cache.put(2, 2)
    print("put(2, 2)")

    result1 = cache.get(1)
    print(f"get(1): {result1}")  # 1，最近使用

    cache.put(3, 3)  # 淘汰2
    print("put(3, 3) → 淘汰key=2")

    result2 = cache.get(2)
    print(f"get(2): {result2}")  # -1，已被淘汰

    cache.put(4, 4)  # 淘汰1
    print("put(4, 4) → 淘汰key=1")

    result3 = cache.get(1)
    print(f"get(1): {result3}")  # -1，已被淘汰

    result4 = cache.get(3)
    print(f"get(3): {result4}")  # 3

    result5 = cache.get(4)
    print(f"get(4): {result5}")  # 4

# 输出:
# === LRU缓存 ===
# put(1, 1)
# put(2, 2)
# get(1): 1
# put(3, 3) → 淘汰key=2
# get(2): -1
# put(4, 4) → 淘汰key=1
# get(1): -1
# get(3): 3
# get(4): 4
