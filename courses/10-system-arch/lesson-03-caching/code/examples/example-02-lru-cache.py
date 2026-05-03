#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LRU 缓存实现：使用字典和双向链表实现最近最少使用缓存
支持自动淘汰最久未使用的数据项
"""

from collections import OrderedDict
from typing import Any, Optional

class LRUCache:
    """
    LRU (Least Recently Used) 缓存实现
    使用 OrderedDict 来维护访问顺序
    """

    def __init__(self, capacity: int):
        """
        初始化 LRU 缓存

        Args:
            capacity: 缓存的最大容量
        """
        self.capacity = capacity
        self.cache = OrderedDict()
        self.eviction_count = 0  # 记录淘汰次数

    def get(self, key: Any) -> Optional[Any]:
        """
        获取缓存中的值

        如果键存在，将其移动到末尾（标记为最近使用）
        如果键不存在，返回 None

        Args:
            key: 要获取的键

        Returns:
            键对应的值，如果不存在则返回 None
        """
        if key not in self.cache:
            return None

        # 将访问的键移动到末尾（最近使用）
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        """
        插入或更新缓存中的键值对

        如果键已存在，更新值并移动到末尾
        如果键不存在：
            - 如果缓存未满，直接添加
            - 如果缓存已满，删除最久未使用的项（开头），然后添加新项

        Args:
            key: 键
            value: 值
        """
        if key in self.cache:
            # 更新现有键的值，并移动到末尾
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # 缓存已满，删除最久未使用的项（第一个）
            self.cache.popitem(last=False)
            self.eviction_count += 1

        # 添加或更新键值对
        self.cache[key] = value

    def delete(self, key: Any) -> bool:
        """
        删除指定的键

        Args:
            key: 要删除的键

        Returns:
            如果键存在并成功删除返回 True，否则返回 False
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def size(self) -> int:
        """获取当前缓存大小"""
        return len(self.cache)

    def is_full(self) -> bool:
        """检查缓存是否已满"""
        return len(self.cache) >= self.capacity

    def get_eviction_count(self) -> int:
        """获取淘汰次数"""
        return self.eviction_count

    def display_cache(self) -> None:
        """显示缓存内容（用于调试）"""
        print("缓存内容（从最久未使用到最近使用）:")
        for key, value in self.cache.items():
            print(f"  {key}: {value}")

def simulate_lru_operations():
    """模拟 LRU 缓存操作"""
    print("=== LRU 缓存模拟 ===")

    # 创建容量为 3 的 LRU 缓存
    lru_cache = LRUCache(3)

    print("1. 插入数据 A, B, C:")
    lru_cache.put("A", 1)
    lru_cache.put("B", 2)
    lru_cache.put("C", 3)
    lru_cache.display_cache()

    print("\n2. 访问 B (使其变为最近使用):")
    lru_cache.get("B")
    lru_cache.display_cache()

    print("\n3. 插入 D (会淘汰最久未使用的 A):")
    lru_cache.put("D", 4)
    lru_cache.display_cache()
    print(f"淘汰次数: {lru_cache.get_eviction_count()}")

    print("\n4. 插入 E (会淘汰最久未使用的 C):")
    lru_cache.put("E", 5)
    lru_cache.display_cache()
    print(f"淘汰次数: {lru_cache.get_eviction_count()}")

    print("\n5. 访问 D 和 E:")
    lru_cache.get("D")
    lru_cache.get("E")
    lru_cache.display_cache()

    print("\n6. 插入 F (会淘汰最久未使用的 B):")
    lru_cache.put("F", 6)
    lru_cache.display_cache()
    print(f"淘汰次数: {lru_cache.get_eviction_count()}")

def main():
    """主函数"""
    simulate_lru_operations()
    print("\n=== 模拟完成 ===")

if __name__ == "__main__":
    main()