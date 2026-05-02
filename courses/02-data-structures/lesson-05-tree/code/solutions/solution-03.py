# ============================================
# 练习3解答：二叉树的最近公共祖先（LCA）
# 难度：⭐⭐⭐
# ============================================

class TreeNode:
    """二叉树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def lowest_common_ancestor(root, p, q):
    """
    找到二叉树中节点p和q的最近公共祖先
    
    递归思路：
    1. 如果当前节点是p或q，返回当前节点
    2. 递归在左右子树中查找
    3. 如果左右子树各找到一个 → 当前节点就是LCA
    4. 如果只在一侧找到 → LCA在那一侧
    
    参数:
        root: 二叉树的根节点
        p: 目标节点p
        q: 目标节点q
    返回:
        p和q的最近公共祖先节点
    """
    # 终止条件：空节点或当前节点就是p或q
    if root is None or root == p or root == q:
        return root

    # 在左右子树中分别查找
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # 如果左右各找到一个 → 当前节点是LCA
    if left and right:
        return root

    # 否则返回非空的那一侧
    return left if left else right


# 测试
if __name__ == "__main__":
    print("=== 练习3：最近公共祖先 ===\n")

    # 构建测试树:
    #            3
    #         /     \
    #        5       1
    #      /   \    /  \
    #     6     2  0    8
    #         / \
    #        7   4
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)

    # 测试1: LCA(6, 4) = 5
    p1, q1 = root.left.left, root.left.right.right
    ans1 = lowest_common_ancestor(root, p1, q1)
    print(f"测试1: LCA(6, 4) = 期望=5, 结果={ans1.val} {'✅' if ans1.val == 5 else '❌'}")

    # 测试2: LCA(6, 8) = 3
    p2, q2 = root.left.left, root.right.right
    ans2 = lowest_common_ancestor(root, p2, q2)
    print(f"测试2: LCA(6, 8) = 期望=3, 结果={ans2.val} {'✅' if ans2.val == 3 else '❌'}")

    # 测试3: LCA(7, 4) = 2
    p3, q3 = root.left.right.left, root.left.right.right
    ans3 = lowest_common_ancestor(root, p3, q3)
    print(f"测试3: LCA(7, 4) = 期望=2, 结果={ans3.val} {'✅' if ans3.val == 2 else '❌'}")

    # 测试4: LCA(5, 2) = 5（其中一个是另一个的祖先）
    p4, q4 = root.left, root.left.right
    ans4 = lowest_common_ancestor(root, p4, q4)
    print(f"测试4: LCA(5, 2) = 期望=5, 结果={ans4.val} {'✅' if ans4.val == 5 else '❌'}")

# 输出:
# === 练习3：最近公共祖先 ===
#
# 测试1: LCA(6, 4) = 期望=5, 结果=5 ✅
# 测试2: LCA(6, 8) = 期望=3, 结果=3 ✅
# 测试3: LCA(7, 4) = 期望=2, 结果=2 ✅
# 测试4: LCA(5, 2) = 期望=5, 结果=5 ✅
