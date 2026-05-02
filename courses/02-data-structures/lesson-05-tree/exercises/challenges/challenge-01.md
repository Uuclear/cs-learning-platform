# 挑战1：翻转二叉树

## 难度
⭐

## 描述

给定一棵二叉树的根节点，将其左右子树**翻转**（也叫镜像）。每个节点的左右孩子都要交换位置。

这就像照镜子一样——树变成了它的镜像。

## 输入

- `root`: 二叉树根节点（TreeNode 类型）

## 输出

- 返回翻转后的二叉树的根节点

## 示例

**示例 1:**
```
输入树:
       1
     /   \
    2     3
   / \   / \
  4   5 6   7

输出树:
       1
     /   \
    3     2
   / \   / \
  7   6 5   4
```

**示例 2:**
```
输入树:
       1
      /
     2

输出树:
     1
      \
       2
```

## 约束条件

- 树的节点数范围: [0, 100]
- 节点值范围: [-100, 100]

## 提示

- 递归思路：翻转当前节点的左右子树，然后递归翻转左子树和右子树
- 递归终止条件：空节点直接返回

## 进阶思考

1. 能否用迭代方式（层序遍历）实现？
2. 翻转操作的时间复杂度和空间复杂度分别是多少？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

递归交换每个节点的左右孩子。对于每个节点：
1. 交换它的左孩子和右孩子
2. 递归处理新的左子树
3. 递归处理新的右子树

### 代码

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def invert_tree(root):
    """
    翻转二叉树
    参数: root - 二叉树的根节点
    返回: 翻转后的根节点
    """
    # 终止条件：空节点直接返回
    if root is None:
        return None

    # 交换左右孩子
    root.left, root.right = root.right, root.left

    # 递归翻转新的左右子树
    invert_tree(root.left)
    invert_tree(root.right)

    return root


# 辅助函数：层序打印树
def print_level_order(root):
    """层序遍历打印树"""
    if root is None:
        return []

    result = []
    queue = [root]

    while queue:
        level = []
        next_queue = []
        for node in queue:
            if node:
                level.append(node.val)
                next_queue.append(node.left)
                next_queue.append(node.right)
            else:
                level.append(None)
        # 去掉末尾全是None的部分
        while level and level[-1] is None:
            level.pop()
        if level:
            result.append(level)
        queue = next_queue

    return result


# 测试
if __name__ == "__main__":
    # 构建测试树
    #        1
    #      /   \
    #     2     3
    #    / \   / \
    #   4   5 6   7
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)

    print("翻转前:", print_level_order(root))

    invert_tree(root)

    print("翻转后:", print_level_order(root))
    # 期望: [[1], [3, 2], [7, 6, 5, 4]]
```

### 复杂度分析

- 时间复杂度: O(n)，每个节点恰好访问一次
- 空间复杂度: O(h)，h为树的高度，递归调用栈的开销

</details>
