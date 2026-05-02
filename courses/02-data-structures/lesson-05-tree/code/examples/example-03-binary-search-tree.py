# ============================================
# 示例3：二叉搜索树（BST）的完整实现
# 包含查找、插入、删除三大操作
# 核心规则：左子树所有节点 < 根 < 右子树所有节点
# ============================================

class TreeNode:
    """二叉搜索树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BinarySearchTree:
    """
    二叉搜索树
    核心性质：对于任意节点，左子树所有值 < 当前值 < 右子树所有值
    这就像一本字典：比当前页小的在左边，比当前页大的在右边
    """

    def __init__(self):
        self.root = None

    # ---------- 查找 ----------
    def search(self, val):
        """
        查找值为val的节点
        时间复杂度: O(h)，h为树的高度
        思路：从根开始，比当前值小就往左，大就往右
        """
        return self._search_node(self.root, val)

    def _search_node(self, node, val):
        """查找的递归实现"""
        if node is None:
            return None  # 没找到，树里没这个数
        if node.val == val:
            return node  # 找到了！
        elif val < node.val:
            return self._search_node(node.left, val)  # 比当前小，去左边找
        else:
            return self._search_node(node.right, val)  # 比当前大，去右边找

    # ---------- 插入 ----------
    def insert(self, val):
        """
        插入新值
        时间复杂度: O(h)
        思路：找到合适的位置，把新节点安上
        """
        self.root = self._insert_node(self.root, val)

    def _insert_node(self, node, val):
        """插入的递归实现"""
        if node is None:
            return TreeNode(val)  # 找到空位，安上新节点

        if val < node.val:
            node.left = self._insert_node(node.left, val)   # 小往左插
        elif val > node.val:
            node.right = self._insert_node(node.right, val)  # 大往右插
        # 如果相等，不插入（BST不允许重复值）

        return node

    # ---------- 删除 ----------
    def delete(self, val):
        """
        删除值为val的节点
        时间复杂度: O(h)
        分三种情况：
        1. 叶子节点：直接删
        2. 只有一个孩子：用孩子顶替
        3. 有两个孩子：用右子树的最小值（中序后继）顶替
        """
        self.root = self._delete_node(self.root, val)

    def _delete_node(self, node, val):
        """删除的递归实现"""
        if node is None:
            return None  # 找不到要删的节点

        # 先找到要删除的节点
        if val < node.val:
            node.left = self._delete_node(node.left, val)
        elif val > node.val:
            node.right = self._delete_node(node.right, val)
        else:
            # 找到节点了！分三种情况处理

            # 情况1：叶子节点（左右都空）—— 直接删除
            if node.left is None and node.right is None:
                return None

            # 情况2：只有一个孩子 —— 用孩子顶替
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # 情况3：有两个孩子 —— 用右子树的最小值（中序后继）替换
            # 找到右子树中的最小节点
            successor = self._find_min(node.right)
            node.val = successor.val  # 用后继的值替换当前节点
            node.right = self._delete_node(node.right, successor.val)  # 删除后继节点

        return node

    def _find_min(self, node):
        """找到以node为根的子树中的最小节点"""
        while node.left is not None:
            node = node.left
        return node

    # ---------- 辅助方法：中序遍历（用于打印BST） ----------
    def inorder(self):
        """中序遍历BST，返回有序列表"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.val)
            self._inorder_recursive(node.right, result)


# ============================================
# 测试：BST的增删查
# ============================================
if __name__ == "__main__":
    bst = BinarySearchTree()

    # 插入一组数字
    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    for v in values:
        bst.insert(v)

    print("=== BST 构建完成 ===")
    print(f"插入的值: {values}")
    print(f"中序遍历（有序输出）: {bst.inorder()}")
    # 输出: [1, 3, 4, 6, 7, 8, 10, 13, 14]
    print()

    # 查找
    print("=== 查找 ===")
    print(f"查找 6: {'找到' if bst.search(6) else '未找到'}")   # 找到
    print(f"查找 99: {'找到' if bst.search(99) else '未找到'}")  # 未找到
    print()

    # 删除测试
    print("=== 删除 ===")

    # 删除叶子节点 4
    bst.delete(4)
    print(f"删除 4 后: {bst.inorder()}")
    # 输出: [1, 3, 6, 7, 8, 10, 13, 14]

    # 删除有一个孩子的节点 3
    bst.delete(3)
    print(f"删除 3 后: {bst.inorder()}")
    # 输出: [1, 6, 7, 8, 10, 13, 14]

    # 删除有两个孩子的节点 10
    bst.delete(10)
    print(f"删除 10 后: {bst.inorder()}")
    # 输出: [1, 6, 7, 8, 13, 14]

# 输出:
# === BST 构建完成 ===
# 插入的值: [8, 3, 10, 1, 6, 14, 4, 7, 13]
# 中序遍历（有序输出）: [1, 3, 4, 6, 7, 8, 10, 13, 14]
#
# === 查找 ===
# 查找 6: 找到
# 查找 99: 未找到
#
# === 删除 ===
# 删除 4 后: [1, 3, 6, 7, 8, 10, 13, 14]
# 删除 3 后: [1, 6, 7, 8, 10, 13, 14]
# 删除 10 后: [1, 6, 7, 8, 13, 14]
