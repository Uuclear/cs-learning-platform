# ============================================
# 示例1：二叉树的基本实现
# 包含节点定义、树的构建和基本属性
# ============================================

class TreeNode:
    """
    二叉树节点
    每个节点包含：数据、左孩子、右孩子
    就像每个人手里最多牵着两个人（左一个右一个）
    """
    def __init__(self, val):
        self.val = val       # 节点存储的数据
        self.left = None     # 左孩子
        self.right = None    # 右孩子


class BinaryTree:
    """
    二叉树类
    包含根节点和一些常用方法
    """
    def __init__(self, root_val=None):
        if root_val is not None:
            self.root = TreeNode(root_val)
        else:
            self.root = None

    def get_height(self, node=None):
        """
        计算树的高度（从根到最深叶子的边数）
        递归思路：树的高度 = max(左子树高度, 右子树高度) + 1
        """
        if node is None:
            return 0
        # 递归计算左右子树高度，取大值再加1
        left_height = self.get_height(node.left)
        right_height = self.get_height(node.right)
        return max(left_height, right_height) + 1

    def get_node_count(self, node=None):
        """
        计算树中节点的总数
        递归思路：节点数 = 左子树节点数 + 右子树节点数 + 1（自己）
        """
        if node is None:
            return 0
        return 1 + self.get_node_count(node.left) + self.get_node_count(node.right)


# ============================================
# 测试：构建一棵简单的二叉树
#
#         爷爷(1)
#        /       \
#    爸爸(2)    叔叔(3)
#    /    \
# 我(4)  妹妹(5)
# ============================================
if __name__ == "__main__":
    # 手动构建一棵二叉树
    tree = BinaryTree(1)
    tree.root.left = TreeNode(2)
    tree.root.right = TreeNode(3)
    tree.root.left.left = TreeNode(4)
    tree.root.left.right = TreeNode(5)

    print("=== 二叉树基本属性 ===")
    print(f"树的高度: {tree.get_height(tree.root)}")      # 高度为3（爷爷->爸爸->我）
    print(f"节点总数: {tree.get_node_count(tree.root)}")  # 5个节点
    print()

    # 再演示一棵更完整的树
    #           A
    #         /   \
    #        B     C
    #       / \   / \
    #      D   E F   G
    print("=== 满二叉树示例 ===")
    full_tree = BinaryTree('A')
    full_tree.root.left = TreeNode('B')
    full_tree.root.right = TreeNode('C')
    full_tree.root.left.left = TreeNode('D')
    full_tree.root.left.right = TreeNode('E')
    full_tree.root.right.left = TreeNode('F')
    full_tree.root.right.right = TreeNode('G')

    print(f"满二叉树高度: {full_tree.get_height(full_tree.root)}")    # 3
    print(f"满二叉树节点数: {full_tree.get_node_count(full_tree.root)}")  # 7
    print()

    # 满二叉树的性质：节点数 = 2^高度 - 1
    height = full_tree.get_height(full_tree.root)
    print(f"满二叉树性质验证: 2^{height} - 1 = {2**height - 1} (实际节点数: {full_tree.get_node_count(full_tree.root)})")

# 输出:
# === 二叉树基本属性 ===
# 树的高度: 3
# 节点总数: 5
#
# === 满二叉树示例 ===
# 满二叉树高度: 3
# 满二叉树节点数: 7
#
# 满二叉树性质验证: 2^3 - 1 = 7 (实际节点数: 7)
