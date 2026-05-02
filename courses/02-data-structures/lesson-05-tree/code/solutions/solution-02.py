# ============================================
# 练习2解答：验证二叉搜索树
# 难度：⭐⭐
# ============================================

class TreeNode:
    """二叉树节点"""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def is_valid_bst(root):
    """
    验证一棵二叉树是否是合法的二叉搜索树
    
    方法：递归时维护上下界，每个节点的值必须在(min_val, max_val)范围内
    
    参数:
        root: 二叉树的根节点
    返回:
        布尔值
    """
    return _validate(root, float('-inf'), float('inf'))


def _validate(node, min_val, max_val):
    """
    递归验证节点值是否在合法范围内
    
    参数:
        node: 当前节点
        min_val: 下界（不包含）
        max_val: 上界（不包含）
    """
    # 空节点视为合法
    if node is None:
        return True

    # 当前节点值必须在上下界之间（开区间）
    if node.val <= min_val or node.val >= max_val:
        return False

    # 递归验证左右子树
    # 左子树：值必须小于当前节点值
    # 右子树：值必须大于当前节点值
    return (_validate(node.left, min_val, node.val) and
            _validate(node.right, node.val, max_val))


# 测试
if __name__ == "__main__":
    print("=== 练习2：验证BST ===\n")

    # 测试1: 合法BST
    #       5
    #     /   \
    #    3     7
    #   / \   / \
    #  2   4 6   8
    root1 = TreeNode(5)
    root1.left = TreeNode(3)
    root1.right = TreeNode(7)
    root1.left.left = TreeNode(2)
    root1.left.right = TreeNode(4)
    root1.right.left = TreeNode(6)
    root1.right.right = TreeNode(8)
    print(f"测试1（合法BST）: 期望=True, 结果={is_valid_bst(root1)} {'✅' if is_valid_bst(root1) else '❌'}")

    # 测试2: 不合法 - 右子树中有比根小的值
    #       5
    #     /   \
    #    3     2   <-- 2比5小，不应该在右边
    root2 = TreeNode(5)
    root2.left = TreeNode(3)
    root2.right = TreeNode(2)
    print(f"测试2（右子树非法）: 期望=False, 结果={is_valid_bst(root2)} {'✅' if not is_valid_bst(root2) else '❌'}")

    # 测试3: 空树视为合法BST
    print(f"测试3（空树）: 期望=True, 结果={is_valid_bst(None)} {'✅' if is_valid_bst(None) else '❌'}")

    # 测试4: 单节点
    root4 = TreeNode(1)
    print(f"测试4（单节点）: 期望=True, 结果={is_valid_bst(root4)} {'✅' if is_valid_bst(root4) else '❌'}")

    # 测试5: 看似BST但实际不合法
    #         10
    #       /    \
    #      5      15
    #     / \    /  \
    #    1  12  14   20
    #    ^ 12 > 10 不应在10的左子树中！
    root5 = TreeNode(10)
    root5.left = TreeNode(5)
    root5.right = TreeNode(15)
    root5.left.left = TreeNode(1)
    root5.left.right = TreeNode(12)  # 12 > 10，非法！
    root5.right.left = TreeNode(14)
    root5.right.right = TreeNode(20)
    print(f"测试5（跨层不合法）: 期望=False, 结果={is_valid_bst(root5)} {'✅' if not is_valid_bst(root5) else '❌'}")

# 输出:
# === 练习2：验证BST ===
#
# 测试1（合法BST）: 期望=True, 结果=True ✅
# 测试2（右子树非法）: 期望=False, 结果=False ✅
# 测试3（空树）: 期望=True, 结果=True ✅
# 测试4（单节点）: 期望=True, 结果=True ✅
# 测试5（跨层不合法）: 期望=False, 结果=False ✅
