# 解决方案1：扩展的编码模式实现（包含BFS/DFS）
from typing import List, Optional
from collections import deque

class TreeNode:
    """二叉树节点定义"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def bfs_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    BFS层序遍历二叉树
    时间复杂度: O(n)
    空间复杂度: O(w) w为树的最大宽度

    :param root: 二叉树根节点
    :return: 按层分组的节点值列表
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result

def dfs_inorder(root: Optional[TreeNode]) -> List[int]:
    """
    DFS中序遍历二叉树（递归实现）
    时间复杂度: O(n)
    空间复杂度: O(h) h为树的高度（递归栈）

    :param root: 二叉树根节点
    :return: 中序遍历结果
    """
    if not root:
        return []

    result = []

    def inorder(node):
        if node:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)

    inorder(root)
    return result

def dfs_inorder_iterative(root: Optional[TreeNode]) -> List[int]:
    """
    DFS中序遍历二叉树（迭代实现）
    时间复杂度: O(n)
    空间复杂度: O(h)

    :param root: 二叉树根节点
    :return: 中序遍历结果
    """
    if not root:
        return []

    result = []
    stack = []
    current = root

    while stack or current:
        # 到达最左边的节点
        while current:
            stack.append(current)
            current = current.left

        # 处理当前节点
        current = stack.pop()
        result.append(current.val)

        # 转向右子树
        current = current.right

    return result

# 测试示例
if __name__ == "__main__":
    # 构建测试二叉树:     3
    #                   /   \
    #                  9     20
    #                       /  \
    #                      15   7
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    # 测试BFS
    bfs_result = bfs_level_order(root)
    print(f"BFS层序遍历结果: {bfs_result}")

    # 测试DFS（递归）
    dfs_recursive = dfs_inorder(root)
    print(f"DFS中序遍历（递归）: {dfs_recursive}")

    # 测试DFS（迭代）
    dfs_iterative = dfs_inorder_iterative(root)
    print(f"DFS中序遍历（迭代）: {dfs_iterative}")