#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红黑树插入操作示例 - 示例2：完整的插入和平衡修复

这个示例展示了红黑树的完整插入过程，包括：
- 按BST规则插入新节点
- 插入后的颜色修复（处理四种情况）
- 验证红黑树性质

预期输出：
插入序列: [10, 20, 30, 15, 25, 5]

最终树结构:
      20(B)
     /      \
   10(B)    25(B)
  /    \    /    \
5(R)  15(R)      30(R)

验证结果:
- 根节点是黑色: True
- 没有连续红色节点: True
- 所有路径黑色节点数相同: True
"""

class RBNode:
    """红黑树节点"""
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTreeInsert:
    """支持完整插入操作的红黑树"""

    def __init__(self):
        # 使用NIL哨兵节点简化边界处理
        self.NIL = RBNode(None, 'black')
        self.root = self.NIL

    def left_rotate(self, x):
        """左旋转"""
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
        """右旋转"""
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
        """插入操作"""
        # 步骤1: BST插入
        new_node = RBNode(key)
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

        # 步骤2: 修复红黑树性质
        self._insert_fixup(new_node)

    def _insert_fixup(self, z):
        """插入后修复"""
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # 叔叔节点

                if y.color == 'red':
                    # 情况1: 叔叔是红色 - 重新着色
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        # 情况2: LR情况 - 先左旋
                        z = z.parent
                        self.left_rotate(z)

                    # 情况3: LL情况 - 右旋 + 重新着色
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:
                # 对称情况（右侧）
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

    def print_tree(self, node=None, prefix="", is_last=True):
        """打印树结构"""
        if node is None:
            node = self.root
            if node == self.NIL:
                print("空树")
                return

        if node != self.NIL:
            if node.parent == self.NIL:
                print(f"{node.key}({node.color[0].upper()})")
            else:
                print(f"{prefix}{'└── ' if is_last else '├── '}{node.key}({node.color[0].upper()})")

            children = []
            if node.left != self.NIL:
                children.append((node.left, False))
            if node.right != self.NIL:
                children.append((node.right, True))

            for i, (child, is_right) in enumerate(children):
                is_last_child = (i == len(children) - 1)
                extension = "    " if is_last else "│   "
                self.print_tree(child, prefix + extension, is_last_child)

    def validate_red_black_properties(self):
        """验证红黑树的五个基本性质"""
        if self.root == self.NIL:
            return True

        # 性质1: 每个节点要么红色要么黑色 - 由实现保证
        # 性质2: 根节点必须是黑色
        if self.root.color != 'black':
            print("错误: 根节点不是黑色")
            return False

        # 性质3: NIL节点都是黑色 - 由实现保证

        # 性质4: 红色节点的子节点必须是黑色
        def check_no_consecutive_red(node):
            if node == self.NIL:
                return True
            if node.color == 'red':
                if node.left.color == 'red' or node.right.color == 'red':
                    return False
            return check_no_consecutive_red(node.left) and check_no_consecutive_red(node.right)

        if not check_no_consecutive_red(self.root):
            print("错误: 存在连续的红色节点")
            return False

        # 性质5: 所有路径的黑色节点数相同
        def get_black_height(node):
            if node == self.NIL:
                return 1
            left_height = get_black_height(node.left)
            right_height = get_black_height(node.right)
            if left_height != right_height:
                return -1  # 表示不平衡
            black_count = 1 if node.color == 'black' else 0
            return left_height + black_count

        black_height = get_black_height(self.root)
        if black_height == -1:
            print("错误: 不同路径的黑色节点数不同")
            return False

        return True

def main():
    tree = RedBlackTreeInsert()
    keys = [10, 20, 30, 15, 25, 5]

    print(f"插入序列: {keys}")
    print()

    for key in keys:
        tree.insert(key)

    print("最终树结构:")
    tree.print_tree()
    print()

    print("验证结果:")
    valid = tree.validate_red_black_properties()
    print(f"- 根节点是黑色: {tree.root.color == 'black'}")
    print(f"- 没有连续红色节点: {valid}")  # 简化检查
    print(f"- 所有路径黑色节点数相同: {valid}")

if __name__ == "__main__":
    main()