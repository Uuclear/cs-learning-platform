#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红黑树解决方案1：完整实现包含删除操作

这个解决方案提供了完整的红黑树实现，包括：
- 插入操作（已在此前示例中展示）
- 删除操作及删除后的修复
- 所有红黑树性质的验证

注意：这是一个简化的教学版本，实际生产环境中的实现可能更复杂。
"""

class RBNode:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTreeComplete:
    def __init__(self):
        self.NIL = RBNode(None, 'black')
        self.root = self.NIL

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
        # BST插入
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

    def delete(self, key):
        """删除操作"""
        # 找到要删除的节点
        z = self._search_node(key)
        if z == self.NIL:
            return False  # 节点不存在

        # 确定实际要删除的节点y
        if z.left == self.NIL or z.right == self.NIL:
            y = z
        else:
            # 找到z的后继节点
            y = self._tree_successor(z)

        # 确定y的子节点x
        if y.left != self.NIL:
            x = y.left
        else:
            x = y.right

        # 将x的父节点设为y的父节点
        x.parent = y.parent

        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        # 如果y不是z，将y的数据复制到z
        if y != z:
            z.key = y.key

        # 如果删除的是黑色节点，需要修复
        if y.color == 'black':
            self._delete_fixup(x)

        return True

    def _search_node(self, key):
        """查找节点"""
        current = self.root
        while current != self.NIL:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return self.NIL

    def _tree_successor(self, x):
        """找到后继节点"""
        if x.right != self.NIL:
            return self._tree_minimum(x.right)

        y = x.parent
        while y != self.NIL and x == y.right:
            x = y
            y = y.parent
        return y

    def _tree_minimum(self, x):
        """找到子树中的最小节点"""
        while x.left != self.NIL:
            x = x.left
        return x

    def _delete_fixup(self, x):
        """删除后的修复操作"""
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right  # 兄弟节点

                if w.color == 'red':
                    # 情况1: 兄弟是红色
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == 'black' and w.right.color == 'black':
                    # 情况2: 兄弟是黑色，且两个子节点都是黑色
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        # 情况3: 兄弟是黑色，右子是黑色，左子是红色
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.parent.right

                    # 情况4: 兄弟是黑色，右子是红色
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                # 对称情况（x是右子节点）
                w = x.parent.left

                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = 'black'

    def validate_red_black_properties(self):
        """验证红黑树性质"""
        if self.root == self.NIL:
            return True

        if self.root.color != 'black':
            return False

        def check_no_consecutive_red(node):
            if node == self.NIL:
                return True
            if node.color == 'red':
                if node.left.color == 'red' or node.right.color == 'red':
                    return False
            return check_no_consecutive_red(node.left) and check_no_consecutive_red(node.right)

        if not check_no_consecutive_red(self.root):
            return False

        def get_black_height(node):
            if node == self.NIL:
                return 1
            left_height = get_black_height(node.left)
            right_height = get_black_height(node.right)
            if left_height != right_height:
                return -1
            black_count = 1 if node.color == 'black' else 0
            return left_height + black_count

        return get_black_height(self.root) != -1

# 测试代码
def test_complete_rbt():
    tree = RedBlackTreeComplete()

    # 插入测试
    keys = [10, 20, 30, 15, 25, 5, 1, 7]
    for key in keys:
        tree.insert(key)

    assert tree.validate_red_black_properties(), "插入后红黑树性质不满足"

    # 删除测试
    tree.delete(10)
    assert tree.validate_red_black_properties(), "删除根节点后红黑树性质不满足"

    tree.delete(5)
    assert tree.validate_red_black_properties(), "删除叶子节点后红黑树性质不满足"

    tree.delete(20)
    assert tree.validate_red_black_properties(), "删除内部节点后红黑树性质不满足"

    print("所有测试通过！")

if __name__ == "__main__":
    test_complete_rbt()