# 挑战3：判断一棵树是否为另一棵树的子树

## 难度
⭐⭐⭐

## 描述

给定两棵二叉树 `root` 和 `sub_root`，判断 `sub_root` 是否是 `root` 的子树。

**子树定义**：`sub_root` 和 `root` 的某个节点及其子树结构和值**完全相同**。

## 输入

- `root`: 主二叉树的根节点
- `sub_root`: 要检查的子树的根节点

## 输出

- 返回布尔值：`True` 表示是子树，`False` 表示不是

## 示例

**示例 1:**
```
主树 root:
        3
      /   \
     4     5
    / \
   1   2

子树 sub_root:
     4
    / \
   1   2

输出: True
解释: sub_root 与 root 的左子树完全相同
```

**示例 2:**
```
主树 root:
        3
      /   \
     4     5
    / \
   1   2
      /
     0

子树 sub_root:
     4
    / \
   1   2

输出: False
解释: root的左子树多了下面的节点0，不完全匹配
```

## 约束条件

- 两棵树的节点数: [1, 1000]
- 节点值范围: [-10^4, 10^4]

## 提示

- 两层递归：
  - 第一层：遍历root的每个节点，看是否有节点与sub_root相同
  - 第二层：判断两棵树是否完全相同
- 两棵树相同意味着：根相同、左子树相同、右子树相同

## 进阶思考

1. 能否通过"序列化"（前序/中序遍历结果转字符串）后用字符串匹配来解决？
2. 序列化方法的陷阱：`[1, 2]` 和 `[1, null, 2]` 的序列化可能相同，如何避免？
3. 时间和空间复杂度是多少？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

分两步：
1. `is_same_tree(s, t)`：判断两棵树是否完全相同（结构+值都一样）
2. `is_subtree(root, sub_root)`：遍历root的每个节点，调用is_same_tree检查

is_same_tree是基础：两棵树相同当且仅当根相同且左右子树分别相同。
is_subtree是应用：sub_root是root的子树，要么root和sub_root相同，要么sub_root是root左子树的子树，要么是右子树的子树。

### 代码

```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def is_same_tree(s, t):
    """
    判断两棵树是否完全相同
    参数:
        s: 第一棵树的根节点
        t: 第二棵树的根节点
    返回: 布尔值
    """
    # 两棵都空 → 相同
    if s is None and t is None:
        return True
    # 一棵空一棵非空 → 不同
    if s is None or t is None:
        return False
    # 根不同 → 不同
    if s.val != t.val:
        return False
    # 根相同，递归检查左右子树
    return is_same_tree(s.left, t.left) and is_same_tree(s.right, t.right)


def is_subtree(root, sub_root):
    """
    判断sub_root是否是root的子树
    参数:
        root: 主树的根节点
        sub_root: 子树的根节点
    返回: 布尔值
    """
    # 主树空 → 找不到子树
    if root is None:
        return False

    # 检查当前节点是否匹配
    if is_same_tree(root, sub_root):
        return True

    # 递归检查左右子树
    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)


# 辅助函数：根据层序数组构建树
def build_tree(values):
    """根据层序遍历数组构建二叉树，None表示空节点"""
    if not values:
        return None

    root = TreeNode(values[0])
    queue = [root]
    i = 1

    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


# 测试
if __name__ == "__main__":
    print("=== 判断子树 ===\n")

    # 测试1: True
    root1 = build_tree([3, 4, 5, 1, 2])
    sub1 = build_tree([4, 1, 2])
    ans1 = is_subtree(root1, sub1)
    print(f"测试1: 期望=True, 结果={ans1} {'✅' if ans1 else '❌'}")

    # 测试2: False
    root2 = build_tree([3, 4, 5, 1, 2, None, None, None, None, 0])
    sub2 = build_tree([4, 1, 2])
    ans2 = is_subtree(root2, sub2)
    print(f"测试2: 期望=False, 结果={ans2} {'✅' if not ans2 else '❌'}")

    # 测试3: 子树和主树完全相同
    root3 = build_tree([1, 2, 3])
    sub3 = build_tree([1, 2, 3])
    ans3 = is_subtree(root3, sub3)
    print(f"测试3: 期望=True, 结果={ans3} {'✅' if ans3 else '❌'}")

    # 测试4: 子树为空树
    root4 = build_tree([1, 2, 3])
    sub4 = None
    # 约定：空树是任何树的子树
    ans4 = sub4 is None or is_subtree(root4, sub4)
    print(f"测试4: 期望=True, 结果={ans4} {'✅' if ans4 else '❌'}")
```

### 复杂度分析

- 时间复杂度: O(m × n)，m为root的节点数，n为sub_root的节点数。最坏情况遍历root的每个节点，每次比较需要O(n)
- 空间复杂度: O(max(m, n))，递归调用栈的最大深度

</details>
