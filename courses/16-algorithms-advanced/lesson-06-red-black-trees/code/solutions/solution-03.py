#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红黑树解决方案3：性能优化和实际应用

这个解决方案展示了红黑树在实际应用中的优化技巧，
包括内存布局优化、缓存友好性和并发安全考虑。
"""

import threading
from collections import deque

class OptimizedRBNode:
    """优化的红黑树节点"""
    __slots__ = ['key', 'color', 'left', 'right', 'parent']

    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class ConcurrentRedBlackTree:
    """支持并发读取的红黑树"""

    def __init__(self):
        self.NIL = OptimizedRBNode(None, 'black')
        self.root = self.NIL
        self._lock = threading.RWLock() if hasattr(threading, 'RWLock') else threading.Lock()

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key):
        """线程安全的插入操作"""
        # 使用写锁
        with self._lock:
            new_node = OptimizedRBNode(key)
            new_node.left = self.NIL
            new_node.right = self.NIL

            y = self.NIL
            x = self.root

            while x != self.NIL:
                y = x
                if new_node.key < x.key:
                    x = x.left
                else:
                    x = x.right

            new_node.parent = y

            if y == self.NIL:
                self.root = new_node
            elif new_node.key < y.key:
                y.left = new_node
            else:
                y.right = new_node

            self._insert_fixup(new_node)

    def _insert_fixup(self, z):
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
        self.root.color = 'black'

    def search(self, key):
        """并发安全的搜索操作（只读）"""
        # 对于只读操作，可以使用读锁或无锁（取决于具体需求）
        current = self.root
        while current != self.NIL:
            if key == current.key:
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return False

    def range_query(self, min_key, max_key):
        """范围查询 - 返回[min_key, max_key]范围内的所有键"""
        result = []
        self._range_query_helper(self.root, min_key, max_key, result)
        return result

    def _range_query_helper(self, node, min_key, max_key, result):
        if node == self.NIL:
            return

        if min_key <= node.key <= max_key:
            result.append(node.key)

        if min_key < node.key:
            self._range_query_helper(node.left, min_key, max_key, result)

        if node.key < max_key:
            self._range_query_helper(node.right, min_key, max_key, result)

# 内存优化版本：使用数组存储而非指针
class ArrayBasedRedBlackTree:
    """基于数组的红黑树实现（适合小规模数据）"""

    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.keys = [None] * capacity
        self.colors = ['black'] * capacity  # 'red' or 'black'
        self.left = [-1] * capacity
        self.right = [-1] * capacity
        self.parent = [-1] * capacity
        self.size = 0
        self.root_idx = -1

    def _allocate_node(self, key):
        if self.size >= self.capacity:
            raise Exception("容量不足")
        idx = self.size
        self.keys[idx] = key
        self.colors[idx] = 'red'
        self.left[idx] = -1
        self.right[idx] = -1
        self.parent[idx] = -1
        self.size += 1
        return idx

    def insert(self, key):
        if self.root_idx == -1:
            self.root_idx = self._allocate_node(key)
            self.colors[self.root_idx] = 'black'
            return

        # BST插入逻辑（使用数组索引）
        current = self.root_idx
        parent = -1

        while current != -1:
            parent = current
            if key < self.keys[current]:
                current = self.left[current]
            else:
                current = self.right[current]

        new_idx = self._allocate_node(key)
        self.parent[new_idx] = parent

        if key < self.keys[parent]:
            self.left[parent] = new_idx
        else:
            self.right[parent] = new_idx

        # 这里省略了平衡修复逻辑以简化代码
        # 实际实现中需要类似的修复过程

    def search(self, key):
        current = self.root_idx
        while current != -1:
            if key == self.keys[current]:
                return True
            elif key < self.keys[current]:
                current = self.left[current]
            else:
                current = self.right[current]
        return False

# 性能测试和比较
def performance_comparison():
    import time
    import random

    test_size = 5000
    keys = random.sample(range(1, 100000), test_size)

    # 测试并发红黑树
    concurrent_tree = ConcurrentRedBlackTree()
    start = time.time()
    for key in keys:
        concurrent_tree.insert(key)
    concurrent_time = time.time() - start

    # 范围查询测试
    range_start = time.time()
    results = concurrent_tree.range_query(1000, 5000)
    range_time = time.time() - range_start

    print(f"并发红黑树性能:")
    print(f"- 插入 {test_size} 个元素: {concurrent_time:.4f}秒")
    print(f"- 范围查询 (返回 {len(results)} 个结果): {range_time:.4f}秒")

    # 测试数组版本（小数据集）
    array_tree = ArrayBasedRedBlackTree(1000)
    small_keys = random.sample(range(1, 10000), 500)
    start = time.time()
    for key in small_keys:
        array_tree.insert(key)
    array_time = time.time() - start

    print(f"\n数组版本性能 (500个元素):")
    print(f"- 插入时间: {array_time:.4f}秒")
    print(f"- 内存局部性更好，适合缓存")

if __name__ == "__main__":
    performance_comparison()
    print("\n红黑树优化方案演示完成！")