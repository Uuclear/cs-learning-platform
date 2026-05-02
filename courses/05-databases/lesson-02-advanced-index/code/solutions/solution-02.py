#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2: B+树索引实现
实现一个完整的B+树，支持插入、搜索和范围查询操作。
"""

from typing import List, Optional, Any, Tuple


class BPlusTreeSolution:
    """B+树解决方案类"""

    class Node:
        """B+树节点"""

        def __init__(self, order: int, is_leaf: bool = False):
            self.order = order
            self.is_leaf = is_leaf
            self.keys: List[Any] = []
            self.children: List['BPlusTreeSolution.Node'] = []
            self.data: List[Any] = []  # 叶子节点存储数据
            self.next: Optional['BPlusTreeSolution.Node'] = None  # 叶子链表

    def __init__(self, order: int = 4):
        """
        初始化B+树

        Args:
            order: B+树的阶数
        """
        self.order = order
        self.root = self.Node(order, is_leaf=True)
        self.leaf_head = self.root

    def insert(self, key: Any, value: Any) -> None:
        """
        插入键值对

        Args:
            key: 索引键
            value: 数据值
        """
        leaf = self._find_leaf(key)

        # 找到插入位置
        pos = self._find_key_position(leaf.keys, key)

        # 插入键和数据
        leaf.keys.insert(pos, key)
        leaf.data.insert(pos, value)

        # 如果需要分裂
        if len(leaf.keys) >= self.order:
            self._split(leaf)

    def search(self, key: Any) -> Optional[Any]:
        """
        搜索键对应的值

        Args:
            key: 要搜索的键

        Returns:
            对应的数据值或None
        """
        leaf = self._find_leaf(key)

        # 在叶子节点中查找
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.data[i]

        return None

    def range_query(self, start_key: Any, end_key: Any) -> List[Tuple[Any, Any]]:
        """
        范围查询

        Args:
            start_key: 起始键（包含）
            end_key: 结束键（包含）

        Returns:
            键值对列表
        """
        results: List[Tuple[Any, Any]] = []

        # 找到起始叶子节点
        current = self._find_leaf(start_key)

        # 遍历叶子链表
        while current:
            for i, key in enumerate(current.keys):
                if key > end_key:
                    return results
                if key >= start_key:
                    results.append((key, current.data[i]))
            current = current.next

        return results

    def _find_leaf(self, key: Any) -> 'Node':
        """找到包含键的叶子节点"""
        current = self.root

        while not current.is_leaf:
            child_index = 0
            while (child_index < len(current.keys) and
                   current.keys[child_index] <= key):
                child_index += 1

            current = current.children[child_index]

        return current

    def _find_key_position(self, keys: List[Any], key: Any) -> int:
        """在有序键列表中找到插入位置"""
        pos = 0
        while pos < len(keys) and keys[pos] < key:
            pos += 1
        return pos

    def _split(self, node: 'Node') -> None:
        """分裂节点"""
        if node.is_leaf:
            self._split_leaf(node)
        else:
            self._split_internal(node)

    def _split_leaf(self, leaf: 'Node') -> None:
        """分裂叶子节点"""
        new_leaf = self.Node(self.order, is_leaf=True)
        mid = len(leaf.keys) // 2

        # 分割键和数据
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.data = leaf.data[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.data = leaf.data[:mid]

        # 维护链表
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        # 处理根节点分裂
        if leaf == self.root:
            new_root = self.Node(self.order, is_leaf=False)
            new_root.keys = [new_leaf.keys[0]]
            new_root.children = [leaf, new_leaf]
            self.root = new_root
        else:
            parent = self._find_parent(self.root, leaf)
            self._insert_in_parent(parent, new_leaf.keys[0], new_leaf)

    def _split_internal(self, node: 'Node') -> None:
        """分裂内部节点"""
        new_node = self.Node(self.order, is_leaf=False)
        mid = len(node.keys) // 2
        mid_key = node.keys[mid]

        # 分割键和子节点
        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]
        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        # 处理根节点分裂
        if node == self.root:
            new_root = self.Node(self.order, is_leaf=False)
            new_root.keys = [mid_key]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            parent = self._find_parent(self.root, node)
            self._insert_in_parent(parent, mid_key, new_node)

    def _find_parent(self, node: 'Node', child: 'Node') -> Optional['Node']:
        """找到子节点的父节点"""
        if node.is_leaf:
            return None

        for c in node.children:
            if c == child:
                return node

        for c in node.children:
            parent = self._find_parent(c, child)
            if parent:
                return parent

        return None

    def _insert_in_parent(self, parent: 'Node', key: Any, new_child: 'Node') -> None:
        """向父节点插入键和子节点"""
        pos = self._find_key_position(parent.keys, key)
        parent.keys.insert(pos, key)
        parent.children.insert(pos + 1, new_child)

        if len(parent.keys) >= self.order:
            self._split(parent)

    def print_structure(self) -> None:
        """打印B+树结构"""
        print("=== B+树结构 ===")
        self._print_node(self.root, 0)

        print("\n=== 叶子链表 ===")
        current = self.leaf_head
        while current:
            print(f"叶子: {current.keys}")
            current = current.next

    def _print_node(self, node: 'Node', level: int) -> None:
        """递归打印节点"""
        indent = "  " * level
        if node.is_leaf:
            print(f"{indent}叶子: {node.keys}")
        else:
            print(f"{indent}内部: {node.keys}")
            for child in node.children:
                self._print_node(child, level + 1)


def demonstrate_bplus_tree() -> None:
    """演示B+树功能"""
    print("📚 B+树索引实现演示")
    print("=" * 40)

    # 创建B+树（阶数为4）
    bpt = BPlusTreeSolution(order=4)

    # 插入数据
    data = [
        (10, "张三"),
        (20, "李四"),
        (5, "王五"),
        (15, "赵六"),
        (25, "钱七"),
        (30, "孙八"),
        (35, "周九"),
        (40, "吴十"),
        (45, "郑一"),
        (50, "王二")
    ]

    print("🔧 插入数据:")
    for key, value in data:
        print(f"  插入: {key} -> {value}")
        bpt.insert(key, value)

    print("\n📊 树结构:")
    bpt.print_structure()

    # 测试搜索
    print("\n🔍 搜索测试:")
    test_keys = [15, 25, 100]
    for key in test_keys:
        result = bpt.search(key)
        if result:
            print(f"  {key} -> {result}")
        else:
            print(f"  {key} -> 未找到")

    # 测试范围查询
    print("\n🎯 范围查询测试:")
    ranges = [(10, 30), (25, 45)]
    for start, end in ranges:
        results = bpt.range_query(start, end)
        print(f"  [{start}, {end}]: {results}")


def explain_bplus_tree_advantages() -> None:
    """解释B+树的优势"""
    print("\n💡 B+树作为数据库索引的优势:")
    print("1. 平衡性: 所有叶子节点在同一层，保证查询时间复杂度稳定")
    print("2. 高扇出: 每个节点可以有多个子节点，减少树的高度")
    print("3. 叶子链表: 支持高效的范围查询和顺序扫描")
    print("4. 内部节点紧凑: 只存储键，不存储数据，提高缓存效率")
    print("5. 插入/删除稳定: 通过分裂和合并保持平衡")


def main():
    """主函数"""
    demonstrate_bplus_tree()
    explain_bplus_tree_advantages()

    print("\n🎯 实际应用:")
    print("在实际数据库系统中，B+树被广泛用于:")
    print("- 主键索引（聚簇索引）")
    print("- 二级索引（非聚簇索引）")
    print("- 范围查询优化")
    print("- 顺序扫描加速")


if __name__ == "__main__":
    main()