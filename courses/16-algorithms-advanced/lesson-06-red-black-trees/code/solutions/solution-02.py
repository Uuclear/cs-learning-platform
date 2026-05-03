#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
红黑树解决方案2：左倾红黑树（LLRB）实现

左倾红黑树是标准红黑树的简化版本，它只允许左倾的红色链接，
这使得实现更加简洁，同时保持了与2-3树的直接对应关系。
"""

class LLRBNode:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color  # 'red' or 'black'
        self.left = None
        self.right = None

class LeftLeaningRedBlackTree:
    """左倾红黑树实现"""

    def __init__(self):
        self.root = None

    def is_red(self, node):
        """检查节点是否为红色"""
        if node is None:
            return False
        return node.color == 'red'

    def rotate_left(self, h):
        """左旋转"""
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = 'red'
        return x

    def rotate_right(self, h):
        """右旋转"""
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = 'red'
        return x

    def flip_colors(self, h):
        """翻转颜色"""
        h.color = 'red' if h.color == 'black' else 'black'
        h.left.color = 'red' if h.left.color == 'black' else 'black'
        h.right.color = 'red' if h.right.color == 'black' else 'black'

    def insert(self, key):
        """插入操作"""
        self.root = self._insert(self.root, key)
        self.root.color = 'black'  # 根节点总是黑色

    def _insert(self, h, key):
        """递归插入"""
        if h is None:
            return LLRBNode(key)

        # BST插入逻辑
        if key < h.key:
            h.left = self._insert(h.left, key)
        elif key > h.key:
            h.right = self._insert(h.right, key)
        else:
            h.key = key  # 更新已存在的键

        # LLRB平衡操作
        if self.is_red(h.right) and not self.is_red(h.left):
            h = self.rotate_left(h)

        if self.is_red(h.left) and self.is_red(h.left.left):
            h = self.rotate_right(h)

        if self.is_red(h.left) and self.is_red(h.right):
            self.flip_colors(h)

        return h

    def search(self, key):
        """搜索操作"""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def height(self, node=None):
        """计算树的高度"""
        if node is None:
            node = self.root
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def validate_llrb_properties(self):
        """验证LLRB性质"""
        if self.root is None:
            return True

        if self.root.color != 'black':
            return False

        def check_properties(node):
            if node is None:
                return True, 1  # 返回(是否有效, 黑色高度)

            # 检查右子节点不能是红色（左倾性质）
            if self.is_red(node.right):
                return False, 0

            # 检查不能有两个连续的红色节点
            if self.is_red(node) and self.is_red(node.left):
                return False, 0

            left_valid, left_black = check_properties(node.left)
            right_valid, right_black = check_properties(node.right)

            if not left_valid or not right_valid:
                return False, 0

            # 检查黑色高度一致性
            if left_black != right_black:
                return False, 0

            black_height = left_black
            if not self.is_red(node):
                black_height += 1

            return True, black_height

        valid, _ = check_properties(self.root)
        return valid

# 性能比较测试
def compare_llrb_with_standard():
    import random
    import time

    # 测试数据
    test_size = 1000
    keys = random.sample(range(1, 10000), test_size)

    # 测试LLRB
    llrb = LeftLeaningRedBlackTree()
    start = time.time()
    for key in keys:
        llrb.insert(key)
    llrb_time = time.time() - start
    llrb_height = llrb.height()

    # 验证LLRB性质
    assert llrb.validate_llrb_properties(), "LLRB性质验证失败"

    print(f"左倾红黑树:")
    print(f"- 插入时间: {llrb_time:.4f}秒")
    print(f"- 树高度: {llrb_height}")
    print(f"- 性质验证: 通过")

    # 功能测试
    test_keys = random.sample(keys, 100)
    start = time.time()
    for key in test_keys:
        assert llrb.search(key), f"键 {key} 未找到"
    search_time = time.time() - start
    print(f"- 搜索时间 (100次): {search_time:.4f}秒")

if __name__ == "__main__":
    compare_llrb_with_standard()
    print("\n左倾红黑树实现完成！")