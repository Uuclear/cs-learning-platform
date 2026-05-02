#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: B+树可视化
这个脚本演示了B+树的基本结构和插入操作。
B+树是一种平衡的多路搜索树，广泛用于数据库索引。
"""

import math
from typing import List, Optional, Any


class BPlusTreeNode:
    """B+树节点类"""

    def __init__(self, order: int, is_leaf: bool = False):
        """
        初始化B+树节点

        Args:
            order: B+树的阶数（每个节点最多包含order-1个键）
            is_leaf: 是否为叶子节点
        """
        self.order = order
        self.is_leaf = is_leaf
        self.keys: List[Any] = []  # 存储键值
        self.children: List['BPlusTreeNode'] = []  # 存储子节点（内部节点使用）
        self.data: List[Any] = []  # 存储实际数据（叶子节点使用）
        self.next: Optional['BPlusTreeNode'] = None  # 叶子节点链表指针


class BPlusTree:
    """B+树实现类"""

    def __init__(self, order: int = 4):
        """
        初始化B+树

        Args:
            order: B+树的阶数，默认为4（即每个节点最多3个键）
        """
        self.order = order
        self.root: Optional[BPlusTreeNode] = BPlusTreeNode(order, is_leaf=True)
        self.leaf_head: Optional[BPlusTreeNode] = self.root  # 叶子节点链表头

    def insert(self, key: Any, value: Any) -> None:
        """
        插入键值对到B+树中

        Args:
            key: 索引键
            value: 对应的数据值
        """
        if self.root is None:
            self.root = BPlusTreeNode(self.order, is_leaf=True)
            self.leaf_head = self.root

        # 在叶子节点中插入
        leaf = self._find_leaf(key)

        # 找到插入位置
        insert_pos = 0
        while insert_pos < len(leaf.keys) and leaf.keys[insert_pos] < key:
            insert_pos += 1

        # 插入键和数据
        leaf.keys.insert(insert_pos, key)
        leaf.data.insert(insert_pos, value)

        # 如果叶子节点满了，需要分裂
        if len(leaf.keys) >= self.order:
            self._split_leaf(leaf)

    def _find_leaf(self, key: Any) -> BPlusTreeNode:
        """找到应该包含给定键的叶子节点"""
        current = self.root

        while not current.is_leaf:
            # 找到第一个大于等于key的子节点
            child_index = 0
            while (child_index < len(current.keys) and
                   current.keys[child_index] <= key):
                child_index += 1

            current = current.children[child_index]

        return current

    def _split_leaf(self, leaf: BPlusTreeNode) -> None:
        """分裂叶子节点"""
        # 创建新的叶子节点
        new_leaf = BPlusTreeNode(self.order, is_leaf=True)

        # 计算分裂点（中间位置）
        mid = len(leaf.keys) // 2

        # 将后半部分移到新节点
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.data = leaf.data[mid:]

        # 保留前半部分在原节点
        leaf.keys = leaf.keys[:mid]
        leaf.data = leaf.data[:mid]

        # 维护叶子节点链表
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        # 如果是根节点分裂，需要创建新的根
        if leaf == self.root:
            new_root = BPlusTreeNode(self.order, is_leaf=False)
            new_root.keys = [new_leaf.keys[0]]
            new_root.children = [leaf, new_leaf]
            self.root = new_root
        else:
            # 向父节点插入新键
            self._insert_internal(leaf, new_leaf.keys[0], new_leaf)

    def _insert_internal(self, parent: BPlusTreeNode, key: Any, new_child: BPlusTreeNode) -> None:
        """向内部节点插入键和子节点"""
        # 找到插入位置
        insert_pos = 0
        while insert_pos < len(parent.keys) and parent.keys[insert_pos] < key:
            insert_pos += 1

        # 插入键和子节点
        parent.keys.insert(insert_pos, key)
        parent.children.insert(insert_pos + 1, new_child)

        # 如果内部节点满了，需要继续分裂
        if len(parent.keys) >= self.order:
            self._split_internal(parent)

    def _split_internal(self, node: BPlusTreeNode) -> None:
        """分裂内部节点"""
        # 创建新的内部节点
        new_node = BPlusTreeNode(self.order, is_leaf=False)

        # 计算分裂点
        mid = len(node.keys) // 2
        mid_key = node.keys[mid]

        # 将后半部分键和子节点移到新节点
        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]

        # 保留前半部分在原节点
        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        # 如果是根节点，创建新的根
        if node == self.root:
            new_root = BPlusTreeNode(self.order, is_leaf=False)
            new_root.keys = [mid_key]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            # 向父节点插入中间键
            parent = self._find_parent(self.root, node)
            self._insert_internal(parent, mid_key, new_node)

    def _find_parent(self, node: BPlusTreeNode, child: BPlusTreeNode) -> Optional[BPlusTreeNode]:
        """找到子节点的父节点"""
        if node.is_leaf:
            return None

        for c in node.children:
            if c == child:
                return node

        # 递归查找
        for c in node.children:
            parent = self._find_parent(c, child)
            if parent is not None:
                return parent

        return None

    def search(self, key: Any) -> Optional[Any]:
        """
        在B+树中搜索键对应的值

        Args:
            key: 要搜索的键

        Returns:
            对应的数据值，如果不存在则返回None
        """
        leaf = self._find_leaf(key)

        # 在叶子节点中线性搜索
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.data[i]

        return None

    def print_tree(self) -> None:
        """打印B+树的结构（用于可视化）"""
        if self.root is None:
            print("空树")
            return

        print("=== B+树结构可视化 ===")
        self._print_level(self.root, 0)

        print("\n=== 叶子节点链表 ===")
        current = self.leaf_head
        level = 0
        while current:
            print(f"叶子层 {level}: 键 = {current.keys}, 数据 = {current.data}")
            current = current.next
            level += 1

    def _print_level(self, node: BPlusTreeNode, level: int) -> None:
        """递归打印树的每一层"""
        indent = "  " * level
        if node.is_leaf:
            print(f"{indent}叶子节点: 键 = {node.keys}, 数据 = {node.data}")
        else:
            print(f"{indent}内部节点: 键 = {node.keys}")
            for child in node.children:
                self._print_level(child, level + 1)


def main():
    """主函数：演示B+树的操作"""
    print("📚 B+树可视化演示")
    print("=" * 50)

    # 创建一个阶数为4的B+树（每个节点最多3个键）
    bptree = BPlusTree(order=4)

    # 插入一些数据
    data_to_insert = [
        (10, "数据10"),
        (20, "数据20"),
        (5, "数据5"),
        (15, "数据15"),
        (25, "数据25"),
        (30, "数据30"),
        (35, "数据35"),
        (40, "数据40")
    ]

    print("🔧 正在插入数据...")
    for key, value in data_to_insert:
        print(f"  插入: 键={key}, 值='{value}'")
        bptree.insert(key, value)

    print("\n" + "=" * 50)
    bptree.print_tree()

    print("\n" + "=" * 50)
    print("🔍 搜索测试:")
    test_keys = [15, 25, 100]  # 100不存在
    for key in test_keys:
        result = bptree.search(key)
        if result is not None:
            print(f"  键 {key} 找到了! 值 = '{result}'")
        else:
            print(f"  键 {key} 未找到")


if __name__ == "__main__":
    main()