#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: 高级虚拟 DOM Diffing

这个解决方案实现了更高效的虚拟 DOM diffing 算法，
包括 key-based reconciliation 和子树优化。
"""

from typing import List, Dict, Any, Optional, Set
import json


class AdvancedVirtualNode:
    """高级虚拟 DOM 节点，支持 key 和类型"""

    def __init__(self, node_type: str, props: Dict[str, Any] = None,
                 children: List['AdvancedVirtualNode'] = None, key: str = None):
        self.type = node_type  # 'tag' 或 'text'
        self.tag = node_type if node_type != 'text' else None
        self.text = node_type if node_type == 'text' else None
        self.props = props or {}
        self.children = children or []
        self.key = key or props.get('key') if props else None

    def __eq__(self, other):
        if not isinstance(other, AdvancedVirtualNode):
            return False
        return (self.type == other.type and
                self.tag == other.tag and
                self.text == other.text and
                self.props == other.props and
                self.key == other.key)

    def to_dict(self) -> Dict[str, Any]:
        result = {'type': self.type}
        if self.tag:
            result['tag'] = self.tag
        if self.text:
            result['text'] = self.text
        if self.props:
            result['props'] = self.props
        if self.key:
            result['key'] = self.key
        if self.children:
            result['children'] = [child.to_dict() for child in self.children]
        return result


class AdvancedDOMDiff:
    """高级虚拟 DOM Diffing 算法"""

    def __init__(self):
        self.operations = []

    def diff(self, old_tree: Optional[AdvancedVirtualNode],
             new_tree: Optional[AdvancedVirtualNode]) -> List[Dict[str, Any]]:
        """执行高级 diffing"""
        self.operations = []
        self._diff_recursive(old_tree, new_tree, "root")
        return self.operations

    def _diff_recursive(self, old_node: Optional[AdvancedVirtualNode],
                        new_node: Optional[AdvancedVirtualNode], path: str):
        """递归 diff 节点"""
        # 处理 null 情况
        if new_node is None:
            if old_node is not None:
                self._add_operation("DELETE", path, old_node.to_dict())
            return

        if old_node is None:
            self._add_operation("CREATE", path, new_node.to_dict())
            for i, child in enumerate(new_node.children):
                self._diff_recursive(None, child, f"{path}.children[{i}]")
            return

        # 节点类型不同 - 完全替换
        if old_node.type != new_node.type:
            self._add_operation("REPLACE", path, {
                'old': old_node.to_dict(),
                'new': new_node.to_dict()
            })
            return

        # 文本节点 - 直接比较文本内容
        if new_node.type == 'text':
            if old_node.text != new_node.text:
                self._add_operation("UPDATE_TEXT", path, {
                    'old': old_node.text,
                    'new': new_node.text
                })
            return

        # 标签节点 - 比较属性和子节点
        if old_node.props != new_node.props:
            self._add_operation("UPDATE_PROPS", path, {
                'old': old_node.props,
                'new': new_node.props
            })

        # 使用 key 优化子节点 diffing
        self._diff_children_with_keys(old_node.children, new_node.children, path)

    def _diff_children_with_keys(self, old_children: List[AdvancedVirtualNode],
                                 new_children: List[AdvancedVirtualNode], parent_path: str):
        """使用 key 优化的子节点 diffing"""
        # 创建 key 到索引的映射
        old_key_map = {child.key: i for i, child in enumerate(old_children) if child.key is not None}
        new_key_map = {child.key: i for i, child in enumerate(new_children) if child.key is not None}

        # 处理有 key 的节点
        processed_new_indices: Set[int] = set()
        processed_old_indices: Set[int] = set()

        for new_key, new_idx in new_key_map.items():
            new_child = new_children[new_idx]
            if new_key in old_key_map:
                # key 存在 - 复用节点
                old_idx = old_key_map[new_key]
                old_child = old_children[old_idx]
                child_path = f"{parent_path}.children[{new_idx}]"
                self._diff_recursive(old_child, new_child, child_path)
                processed_new_indices.add(new_idx)
                processed_old_indices.add(old_idx)
            else:
                # 新增节点
                child_path = f"{parent_path}.children[{new_idx}]"
                self._diff_recursive(None, new_child, child_path)
                processed_new_indices.add(new_idx)

        # 删除未使用的旧节点
        for old_idx, old_child in enumerate(old_children):
            if old_idx not in processed_old_indices:
                child_path = f"{parent_path}.children[{old_idx}]"
                self._diff_recursive(old_child, None, child_path)

        # 处理没有 key 的节点（简单按索引匹配）
        max_common_length = min(
            len([c for c in old_children if c.key is None]),
            len([c for c in new_children if c.key is None])
        )

        old_no_key_idx = 0
        new_no_key_idx = 0

        for i in range(max(len(old_children), len(new_children))):
            old_in_range = old_no_key_idx < len(old_children) and old_children[old_no_key_idx].key is None
            new_in_range = new_no_key_idx < len(new_children) and new_children[new_no_key_idx].key is None

            if old_in_range and new_in_range:
                # 两者都存在且无 key - 比较
                child_path = f"{parent_path}.children[{len(processed_new_indices) + new_no_key_idx}]"
                self._diff_recursive(old_children[old_no_key_idx], new_children[new_no_key_idx], child_path)
                old_no_key_idx += 1
                new_no_key_idx += 1
            elif old_in_range:
                # 只有旧节点存在 - 删除
                child_path = f"{parent_path}.children[{old_no_key_idx}]"
                self._diff_recursive(old_children[old_no_key_idx], None, child_path)
                old_no_key_idx += 1
            elif new_in_range:
                # 只有新节点存在 - 创建
                child_path = f"{parent_path}.children[{len(processed_new_indices) + new_no_key_idx}]"
                self._diff_recursive(None, new_children[new_no_key_idx], child_path)
                new_no_key_idx += 1

    def _add_operation(self, op_type: str, path: str, payload: Any):
        """添加操作到列表"""
        self.operations.append({
            'type': op_type,
            'path': path,
            'payload': payload
        })


def create_optimized_list(old_items: List[str], new_items: List[str]) -> tuple:
    """创建带 key 的优化列表"""
    old_children = [
        AdvancedVirtualNode("li", {"key": f"item-{item}"}, [
            AdvancedVirtualNode("text", {}, [], item)
        ]) for item in old_items
    ]

    new_children = [
        AdvancedVirtualNode("li", {"key": f"item-{item}"}, [
            AdvancedVirtualNode("text", {}, [], item)
        ]) for item in new_items
    ]

    old_tree = AdvancedVirtualNode("ul", {"class": "list"}, old_children)
    new_tree = AdvancedVirtualNode("ul", {"class": "list"}, new_children)

    return old_tree, new_tree


def main():
    """演示高级 diffing 算法"""
    print("🎯 高级虚拟 DOM Diffing 解决方案")
    print("=" * 40)

    # 创建带 key 的列表示例
    old_items = ["苹果", "香蕉", "橙子"]
    new_items = ["苹果", "葡萄", "橙子", "芒果"]

    old_tree, new_tree = create_optimized_list(old_items, new_items)

    print(f"\n📋 原始列表: {old_items}")
    print(f"📋 更新列表: {new_items}")

    # 执行 diffing
    differ = AdvancedDOMDiff()
    operations = differ.diff(old_tree, new_tree)

    print(f"\n🔧 生成的操作 ({len(operations)} 个):")
    for i, op in enumerate(operations, 1):
        print(f"   {i}. {op['type']} at {op['path']}")

    print(f"\n✅ 使用 key 优化后，只对变化的部分执行操作!")
    print("   传统方法会重新渲染整个列表，而这里只更新必要的部分。")


if __name__ == "__main__":
    main()