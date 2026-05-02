# ============================================
# 示例2：二叉树的四种遍历方式
# 前序、中序、后序、层序遍历
# 每种遍历就像用不同"路线"走遍整棵树
# ============================================

from collections import deque


class TreeNode:
    """二叉树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# ---------- 前序遍历：根 -> 左 -> 右 ----------
# 口诀：先见领导（根），再跑左边（左子树），最后跑右边（右子树）
# 应用：复制一棵树（先造根，再造左右）
def preorder(root):
    """前序遍历（递归）"""
    if root is None:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)


# ---------- 中序遍历：左 -> 根 -> 右 ----------
# 口诀：先跑左边，回来见领导（根），最后跑右边
# 应用：BST的中序遍历会得到有序序列
def inorder(root):
    """中序遍历（递归）"""
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


# ---------- 后序遍历：左 -> 右 -> 根 ----------
# 口诀：先跑左边，再跑右边，最后见领导
# 应用：删除一棵树（先删叶子，再删根）
def postorder(root):
    """后序遍历（递归）"""
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


# ---------- 层序遍历：一层一层地走 ----------
# 口诀：从上到下，从左到右，逐层扫描
# 应用：计算树的高度、宽度，BFS搜索
def level_order(root):
    """层序遍历（迭代，使用队列）"""
    if root is None:
        return []

    result = []
    queue = deque([root])  # 用队列来模拟"排队"

    while queue:
        level_size = len(queue)  # 当前层有多少个节点
        level_nodes = []

        for _ in range(level_size):
            node = queue.popleft()     # 出队：轮到你了！
            level_nodes.append(node.val)

            # 把孩子节点加入队列（下一层排队）
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level_nodes)

    return result


# ============================================
# 测试：构建一棵树并演示四种遍历
#
#         1
#       /   \
#      2     3
#     / \   /
#    4   5 6
# ============================================
if __name__ == "__main__":
    # 构建测试树
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)

    print("=== 测试树 ===")
    print("         1")
    print("       /   \\")
    print("      2     3")
    print("     / \\   /")
    print("    4   5 6")
    print()

    # 前序遍历
    print(f"前序遍历（根-左-右）: {preorder(root)}")
    # 输出: [1, 2, 4, 5, 3, 6]
    # 解释：先访问1，再递归访问2及其子树(2,4,5)，最后访问3及其子树(3,6)

    # 中序遍历
    print(f"中序遍历（左-根-右）: {inorder(root)}")
    # 输出: [4, 2, 5, 1, 6, 3]
    # 解释：先访问最左的4，回到2，访问2，再访问5，回到1...

    # 后序遍历
    print(f"后序遍历（左-右-根）: {postorder(root)}")
    # 输出: [4, 5, 2, 6, 3, 1]
    # 解释：先处理完所有子树，最后才访问根

    # 层序遍历
    print(f"层序遍历（逐层）:     {level_order(root)}")
    # 输出: [[1], [2, 3], [4, 5, 6]]
    # 解释：第1层[1]，第2层[2,3]，第3层[4,5,6]

    print()
    print("=== 遍历速记口诀 ===")
    print("前序：根左右 —— 先打卡，再逛两边")
    print("中序：左根右 —— 从左开始，依次路过")
    print("后序：左右根 —— 先逛完，最后回来")
    print("层序：一层层 —— 从上到下，从左到右")

# 输出:
# === 测试树 ===
#          1
#        /   \
#       2     3
#      / \   /
#     4   5 6
#
# 前序遍历（根-左-右）: [1, 2, 4, 5, 3, 6]
# 中序遍历（左-根-右）: [4, 2, 5, 1, 6, 3]
# 后序遍历（左-右-根）: [4, 5, 2, 6, 3, 1]
# 层序遍历（逐层）:     [[1], [2, 3], [4, 5, 6]]
#
# === 遍历速记口诀 ===
# 前序：根左右 —— 先打卡，再逛两边
# 中序：左根右 —— 从左开始，依次路过
# 后序：左右根 —— 先逛完，最后回来
# 层序：一层层 —— 从上到下，从左到右
