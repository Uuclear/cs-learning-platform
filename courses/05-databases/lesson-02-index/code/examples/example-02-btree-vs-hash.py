#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: B+树 vs 哈希索引模拟

通过简化实现来理解B+树索引和哈希索引的工作原理和适用场景。
"""

import bisect
import random
from collections import defaultdict

class SimpleBPlusTree:
    """简化版B+树模拟 - 展示有序索引的特点"""

    def __init__(self):
        self.keys = []      # 排序后的键列表（模拟B+树的叶子节点链表）
        self.values = {}    # 键值映射

    def insert(self, key, value):
        """插入键值对"""
        if key not in self.values:
            # 使用二分插入保持有序
            bisect.insort(self.keys, key)
        self.values[key] = value

    def search(self, key):
        """等值查询 - 时间复杂度 O(log n)"""
        # 二分查找
        pos = bisect.bisect_left(self.keys, key)
        if pos < len(self.keys) and self.keys[pos] == key:
            return self.values[key]
        return None

    def range_search(self, start_key, end_key):
        """范围查询 - 利用有序性高效查询"""
        start_pos = bisect.bisect_left(self.keys, start_key)
        end_pos = bisect.bisect_right(self.keys, end_key)
        return [(key, self.values[key]) for key in self.keys[start_pos:end_pos]]

class SimpleHashIndex:
    """简化版哈希索引模拟 - 展示哈希索引的特点"""

    def __init__(self):
        self.buckets = defaultdict(list)  # 哈希桶
        self.values = {}                  # 完整的键值映射（用于范围查询）

    def _hash(self, key):
        """简单的哈希函数"""
        return hash(key) % 1000

    def insert(self, key, value):
        """插入键值对"""
        bucket = self._hash(key)
        # 检查是否已存在
        if key not in [k for k, _ in self.buckets[bucket]]:
            self.buckets[bucket].append((key, value))
        self.values[key] = value

    def search(self, key):
        """等值查询 - 平均时间复杂度 O(1)"""
        bucket = self._hash(key)
        for k, v in self.buckets[bucket]:
            if k == key:
                return v
        return None

    def range_search(self, start_key, end_key):
        """范围查询 - 哈希索引不支持高效范围查询"""
        # 需要遍历所有数据
        result = []
        for key, value in self.values.items():
            if start_key <= key <= end_key:
                result.append((key, value))
        return result

def main():
    print("=== B+树 vs 哈希索引对比实验 ===\n")

    # 准备测试数据
    data_size = 1000
    data = {i: f"value_{i}" for i in range(1, data_size + 1)}

    # 测试B+树索引
    print("1. B+树索引测试")
    btree = SimpleBPlusTree()
    for key, value in data.items():
        btree.insert(key, value)

    print(f"   等值查询 (key=500): {btree.search(500)}")
    range_result = btree.range_search(100, 200)
    print(f"   范围查询 (100-200): 找到 {len(range_result)} 条记录")

    # 测试哈希索引
    print("\n2. 哈希索引测试")
    hash_index = SimpleHashIndex()
    for key, value in data.items():
        hash_index.insert(key, value)

    print(f"   等值查询 (key=500): {hash_index.search(500)}")
    range_result = hash_index.range_search(100, 200)
    print(f"   范围查询 (100-200): 找到 {len(range_result)} 条记录")

    print("\n💡 关键区别:")
    print("   - B+树: 等值查询 O(log n)，范围查询高效")
    print("   - 哈希索引: 等值查询 O(1)，范围查询需要全扫描")

if __name__ == "__main__":
    main()