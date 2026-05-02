# ============================================
# 练习1解答：求二叉树的最大深度
# 难度：⭐
# ============================================

class TreeNode:
    """二叉树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def max_depth(root):
    """
    计算二叉树的最大深度
    递归思路：树的最大深度 = max(左子树最大深度, 右子树最大深度) + 1
    
    参数:
        root: 二叉树的根节点
    返回:
        树的最大深度（整数）
    """
    # 终止条件：空节点深度为0
    if root is None:
        return 0

    # 递归计算左右子树的最大深度
    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)

    # 取较大值再加1（当前节点本身）
    return max(left_depth, right_depth) + 1


# 测试
if __name__ == "__main__":
    # 测试1: 普通二叉树
    #         1
    #       /   \
    #      2     3
    #     / \
    #    4   5
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)
    root1.left.left = TreeNode(4)
    root1.left.right = TreeNode(5)

    print("=== 练习1：二叉树最大深度 ===")
    print(f"测试1: 期望=3, 结果={max_depth(root1)} {'✅' if max_depth(root1) == 3 else '❌'}")

    # 测试2: 只有根节点
    root2 = TreeNode(1)
    print(f"测试2: 期望=1, 结果={max_depth(root2)} {'✅' if max_depth(root2) == 1 else '❌'}")

    # 测试3: 空树
    print(f"测试3: 期望=0, 结果={max_depth(None)} {'✅' if max_depth(None) == 0 else '❌'}")

    # 测试4: 链状树（退化情况）
    #    1
    #     \
    #      2
    #       \
    #        3
    root4 = TreeNode(1)
    root4.right = TreeNode(2)
    root4.right.right = TreeNode(3)
    print(f"测试4: 期望=3, 结果={max_depth(root4)} {'✅' if max_depth(root4) == 3 else '❌'}")

# 输出:
# === 练习1：二叉树最大深度 ===
# 测试1: 期望=3, 结果=3 ✅
# 测试2: 期望=1, 结果=1 ✅
# 测试3: 期望=0, 结果=0 ✅
# 测试4: 期望=3, 结果=3 ✅
