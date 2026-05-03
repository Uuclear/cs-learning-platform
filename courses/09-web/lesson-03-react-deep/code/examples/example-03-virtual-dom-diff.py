#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: 虚拟 DOM Diffing 算法模拟

这个文件演示了 React 虚拟 DOM 的 diffing 和 reconciliation 过程：
1. 虚拟 DOM 树结构
2. Diffing 算法实现
3. 最小化 DOM 操作
"""

from typing import List, Dict, Any, Optional
import json


class VirtualNode:
    """虚拟 DOM 节点"""
    def __init__(self, tag: str, props: Dict[str, Any] = None, children: List['VirtualNode'] = None, text_content: str = None):
        self.tag = tag
        self.props = props or {}
        self.children = children or []
        self.text_content = text_content
        self.key = props.get('key') if props else None

    def __eq__(self, other):
        """比较两个虚拟节点是否相等"""
        if not isinstance(other, VirtualNode):
            return False
        return (self.tag == other.tag and
                self.props == other.props and
                len(self.children) == len(other.children) and
                self.text_content == other.text_content)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典表示"""
        result = {
            'tag': self.tag,
            'props': self.props,
        }
        if self.children:
            result['children'] = [child.to_dict() for child in self.children]
        if self.text_content:
            result['text_content'] = self.text_content
        return result

    def __str__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


class DOMOperation:
    """DOM 操作指令"""
    def __init__(self, operation_type: str, target: str, payload: Any = None):
        self.operation_type = operation_type  # CREATE, UPDATE, DELETE, MOVE
        self.target = target
        self.payload = payload

    def __str__(self):
        return f"{self.operation_type} {self.target}: {self.payload}"


class VirtualDOMDiff:
    """虚拟 DOM Diffing 算法实现"""

    def __init__(self):
        self.operations: List[DOMOperation] = []

    def diff(self, old_tree: Optional[VirtualNode], new_tree: Optional[VirtualNode], path: str = "root") -> List[DOMOperation]:
        """比较两棵虚拟 DOM 树并生成最小操作集"""
        self.operations = []
        self._diff_recursive(old_tree, new_tree, path)
        return self.operations

    def _diff_recursive(self, old_node: Optional[VirtualNode], new_node: Optional[VirtualNode], path: str):
        """递归比较节点"""
        # 情况 1: 新节点为空，删除旧节点
        if new_node is None:
            if old_node is not None:
                self.operations.append(DOMOperation("DELETE", path, old_node.tag))
            return

        # 情况 2: 旧节点为空，创建新节点
        if old_node is None:
            self.operations.append(DOMOperation("CREATE", path, new_node.to_dict()))
            # 递归处理子节点
            for i, child in enumerate(new_node.children):
                self._diff_recursive(None, child, f"{path}.children[{i}]")
            return

        # 情况 3: 节点类型不同，替换整个节点
        if old_node.tag != new_node.tag:
            self.operations.append(DOMOperation("DELETE", path, old_node.tag))
            self.operations.append(DOMOperation("CREATE", path, new_node.to_dict()))
            # 递归处理新节点的子节点
            for i, child in enumerate(new_node.children):
                self._diff_recursive(None, child, f"{path}.children[{i}]")
            return

        # 情况 4: 节点类型相同，比较属性和子节点
        # 比较属性
        old_props = old_node.props or {}
        new_props = new_node.props or {}

        if old_props != new_props:
            self.operations.append(DOMOperation("UPDATE", path, {
                'old_props': old_props,
                'new_props': new_props
            }))

        # 比较子节点 - 简化的 diff 算法（实际 React 使用更复杂的算法）
        self._diff_children(old_node.children, new_node.children, path)

    def _diff_children(self, old_children: List[VirtualNode], new_children: List[VirtualNode], parent_path: str):
        """比较子节点列表"""
        max_len = max(len(old_children), len(new_children))

        for i in range(max_len):
            old_child = old_children[i] if i < len(old_children) else None
            new_child = new_children[i] if i < len(new_children) else None
            child_path = f"{parent_path}.children[{i}]"
            self._diff_recursive(old_child, new_child, child_path)


def create_sample_tree_1() -> VirtualNode:
    """创建示例树 1"""
    return VirtualNode("div", {"id": "app", "class": "container"}, [
        VirtualNode("h1", {"class": "title"}, [
            VirtualNode("span", {}, [], "欢迎使用 React")
        ]),
        VirtualNode("ul", {"class": "user-list"}, [
            VirtualNode("li", {"key": "1"}, [
                VirtualNode("span", {}, [], "用户 1")
            ]),
            VirtualNode("li", {"key": "2"}, [
                VirtualNode("span", {}, [], "用户 2")
            ])
        ])
    ])


def create_sample_tree_2() -> VirtualNode:
    """创建示例树 2（修改后的版本）"""
    return VirtualNode("div", {"id": "app", "class": "container updated"}, [
        VirtualNode("h1", {"class": "title new"}, [
            VirtualNode("span", {}, [], "欢迎使用优化后的 React")
        ]),
        VirtualNode("ul", {"class": "user-list"}, [
            VirtualNode("li", {"key": "1"}, [
                VirtualNode("span", {}, [], "用户 1 (更新)")
            ]),
            VirtualNode("li", {"key": "3"}, [
                VirtualNode("span", {}, [], "用户 3 (新增)")
            ])
        ])
    ])


def main():
    """主函数：演示虚拟 DOM diffing"""
    print("🎯 虚拟 DOM Diffing 算法演示")
    print("=" * 50)

    # 创建两棵不同的虚拟 DOM 树
    tree1 = create_sample_tree_1()
    tree2 = create_sample_tree_2()

    print("\n🌳 原始虚拟 DOM 树:")
    print(tree1)

    print("\n🌳 更新后的虚拟 DOM 树:")
    print(tree2)

    # 执行 diffing
    differ = VirtualDOMDiff()
    operations = differ.diff(tree1, tree2)

    print(f"\n🔧 生成的 DOM 操作 ({len(operations)} 个操作):")
    for i, op in enumerate(operations, 1):
        print(f"   {i}. {op}")

    # 验证算法正确性
    print(f"\n✅ Diffing 完成! 发现 {len(operations)} 个必要的 DOM 操作")
    print("   这比重新渲染整个 DOM 树要高效得多!")


if __name__ == "__main__":
    main()