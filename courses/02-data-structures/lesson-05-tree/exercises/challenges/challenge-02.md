# 挑战2：二叉搜索树的第K小元素

## 难度
⭐⭐

## 描述

给定一棵**二叉搜索树（BST）**的根节点，找到其中**第k小**的元素值。

利用BST的性质：中序遍历BST会得到一个有序递增序列。所以第k小就是中序遍历结果中第k个元素。

## 输入

- `root`: BST的根节点（TreeNode 类型）
- `k`: 整数，表示找第k小（1-indexed，即k从1开始）

## 输出

- 返回第k小的元素值（整数）

## 示例

**示例 1:**
```
BST结构:
       5
     /   \
    3     7
   / \   / \
  2   4 6   8

中序遍历: [2, 3, 4, 5, 6, 7, 8]

输入: k = 3
输出: 4
解释: 第3小的元素是4
```

**示例 2:**
```
BST结构:
       1
        \
         2

中序遍历: [1, 2]

输入: k = 2
输出: 2
解释: 第2小的元素是2
```

## 约束条件

- 树中节点数: [1, 10^4]
- k 的范围: [1, 树中节点数]
- 保证k是有效的（不超过节点数）

## 提示

- 方法1：中序遍历得到完整有序数组，取第k-1个元素（简单但需要O(n)空间）
- 方法2：中序遍历时计数，到达第k个时停止（节省空间）

## 进阶思考

1. 如果BST经常被修改（插入/删除），而且需要频繁查询第k小，如何优化？
2. 能否在O(1)额外空间内完成？（提示：Morris遍历）

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

利用BST的中序遍历特性（结果有序）。我们用计数的方法：中序遍历BST，每访问一个节点计数器加1，当计数器等于k时，当前节点就是第k小的元素。

### 代码

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def kth_smallest(root, k):
    """
    找到BST中第k小的元素
    参数:
        root: BST的根节点
        k: 找第k小（1-indexed）
    返回: 第k小的元素值
    """
    result = [None]  # 用列表存结果（可变引用）
    counter = [0]    # 用列表做计数器（在闭包中可变）

    def inorder(node):
        if node is None or result[0] is not None:
            return

        # 先遍历左子树
        inorder(node.left)

        # 访问当前节点
        counter[0] += 1
        if counter[0] == k:
            result[0] = node.val
            return  # 找到了，提前退出

        # 再遍历右子树
        inorder(node.right)

    inorder(root)
    return result[0]


# 测试
if __name__ == "__main__":
    # 构建BST:
    #        5
    #      /   \
    #     3     7
    #    / \   / \
    #   2   4 6   8
    root = TreeNode(5)
    root.left = TreeNode(3)
    root.right = TreeNode(7)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(4)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(8)

    # 测试不同k值
    test_cases = [
        (1, 2),  # 第1小是2
        (3, 4),  # 第3小是4
        (5, 6),  # 第5小是6
        (7, 8),  # 第7小是8
    ]

    print("=== BST第K小元素 ===")
    for k, expected in test_cases:
        ans = kth_smallest(root, k)
        print(f"k={k}: 结果={ans}, 期望={expected}, {'✅' if ans == expected else '❌'}")
```

### 复杂度分析

- 时间复杂度: O(h + k)，h为树的高度。最坏情况O(n)，平均情况O(log n + k)
- 空间复杂度: O(h)，递归调用栈的开销

</details>
