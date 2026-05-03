#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红黑树基础实现示例 - 示例1：基本节点结构和旋转操作

这个示例展示了红黑树的核心组件：
- 节点定义（包含颜色属性）
- 左旋转和右旋转操作
- 基本的树结构验证

预期输出：
初始树结构 (插入 10, 20, 30 后):
  20(B)
 /    \
10(R)  30(R)

左旋转后:
  30(B)
 /
20(R)
 \
  10(R)
"""

class RBNode:
    """红黑树节点类"""
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color  # 'red' 或 'black'
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return f"{self.key}({self.color[0].upper()})"

class RedBlackTreeBasic:
    """简化版红黑树，仅用于演示旋转操作"""

    def __init__(self):
        self.root = None

    def left_rotate(self, x):
        """左旋转操作 - 将x的右子节点提升为新的根"""
        if x is None or x.right is None:
            return

        y = x.right  # y 是 x 的右子节点

        # 步骤1: 将y的左子树设为x的右子树
        x.right = y.left
        if y.left is not None:
            y.left.parent = x

        # 步骤2: 将y的父节点设为x的父节点
        y.parent = x.parent
        if x.parent is None:
            self.root = y  # x是根节点
        elif x == x.parent.left:
            x.parent.left = y  # x是左子节点
        else:
            x.parent.right = y  # x是右子节点

        # 步骤3: 将x设为y的左子节点
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        """右旋转操作 - 将y的左子节点提升为新的根"""
        if y is None or y.left is None:
            return

        x = y.left  # x 是 y 的左子节点

        # 步骤1: 将x的右子树设为y的左子树
        y.left = x.right
        if x.right is not None:
            x.right.parent = y

        # 步骤2: 将x的父节点设为y的父节点
        x.parent = y.parent
        if y.parent is None:
            self.root = x  # y是根节点
        elif y == y.parent.right:
            y.parent.right = x  # y是右子节点
        else:
            y.parent.left = x  # y是左子节点

        # 步骤3: 将y设为x的右子节点
        x.right = y
        y.parent = x

    def insert_without_balance(self, key):
        """不进行平衡的简单插入（仅用于演示）"""
        if self.root is None:
            self.root = RBNode(key, 'black')
            return

        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = RBNode(key)
                    current.left.parent = current
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = RBNode(key)
                    current.right.parent = current
                    break
                current = current.right

    def print_tree(self, node=None, prefix="", is_last=True):
        """打印树结构（用于可视化）"""
        if node is None:
            node = self.root
            if node is None:
                print("空树")
                return

        if node.parent is None:
            print(f"{node}")
        else:
            print(f"{prefix}{'└── ' if is_last else '├── '}{node}")

        children = []
        if node.left is not None:
            children.append((node.left, False))
        if node.right is not None:
            children.append((node.right, True))

        for i, (child, is_right) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            extension = "    " if is_last else "│   "
            self.print_tree(child, prefix + extension, is_last_child)

def main():
    # 创建红黑树实例
    tree = RedBlackTreeBasic()

    # 插入数据构建不平衡树
    keys = [10, 20, 30]
    for key in keys:
        tree.insert_without_balance(key)

    print("初始树结构 (插入 10, 20, 30 后):")
    tree.print_tree()
    print()

    # 执行左旋转（以根节点20为轴）
    tree.left_rotate(tree.root)

    print("左旋转后:")
    tree.print_tree()

if __name__ == "__main__":
    main()