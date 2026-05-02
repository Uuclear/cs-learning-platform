# 挑战2：查找链表中间节点

## 难度
⭐⭐⭐

## 描述
实现一个函数，在不先计算链表长度的情况下，找出单向链表的中间节点。如果链表长度为偶数，返回中间两个节点中的后一个。

**要求**：只能遍历链表一次！

这是一个经典的面试题，被称为"快慢指针"问题。

## 输入
一个单向链表的头节点

## 输出
链表的中间节点

## 示例

**示例 1:**
```
输入: 1 -> 2 -> 3 -> 4 -> 5 -> None
输出: 3
解释: 5个节点的中间节点是第3个，值为3
```

**示例 2:**
```
输入: 1 -> 2 -> 3 -> 4 -> None
输出: 3
解释: 4个节点，返回中间两个（2和3）中的后一个，即3
```

## 约束条件
- 链表长度范围: 1 <= n <= 100
- 不能先遍历一遍链表计算长度

## 提示
- 想象两个人从同一起点出发
- 一个人每次走一步（慢指针）
- 另一个人每次走两步（快指针）
- 当快的人走到终点时，慢的人刚好走到中间

## 进阶思考
- 如果链表长度为偶数时，你想返回中间两个节点中的前一个，怎么改？
- 这个方法能用来判断链表中是否有环吗？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
使用"快慢指针"技巧（也叫龟兔赛跑算法）：
1. 初始化两个指针，slow 和 fast，都指向头节点
2. slow 每次走一步，fast 每次走两步
3. 当 fast 到达链表末尾时，slow 恰好停在中间
4. 核心原理：fast 的速度是 slow 的两倍，所以 fast 走完全程时，slow 走了一半

### 代码
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def find_middle(head):
    """
    查找链表中间节点（只遍历一次）
    参数: head - 链表头节点
    返回: 中间节点
    """
    if head is None:
        return None

    slow = head      # 慢指针，每次走一步
    fast = head      # 快指针，每次走两步

    # fast 还能走两步时继续前进
    while fast is not None and fast.next is not None:
        slow = slow.next          # 慢指针走一步
        fast = fast.next.next     # 快指针走两步

    return slow  # slow 正好在中间


# ===== 测试代码 =====
def create_linked_list(values):
    """从列表创建链表"""
    if not values:
        return None
    head = Node(values[0])
    current = head
    for v in values[1:]:
        current.next = Node(v)
        current = current.next
    return head


def print_linked_list(head):
    """打印链表"""
    values = []
    current = head
    while current is not None:
        values.append(str(current.data))
        current = current.next
    return " -> ".join(values) + " -> None"


if __name__ == "__main__":
    # 测试1：奇数个节点
    print("测试1：1 -> 2 -> 3 -> 4 -> 5")
    head = create_linked_list([1, 2, 3, 4, 5])
    mid = find_middle(head)
    print(f"  链表: {print_linked_list(head)}")
    print(f"  中间节点: {mid.data}")  # 输出: 3

    # 测试2：偶数个节点
    print("\n测试2：1 -> 2 -> 3 -> 4")
    head = create_linked_list([1, 2, 3, 4])
    mid = find_middle(head)
    print(f"  链表: {print_linked_list(head)}")
    print(f"  中间节点（偶数取后一个）: {mid.data}")  # 输出: 3

    # 测试3：单节点
    print("\n测试3：只有一个节点")
    head = create_linked_list([42])
    mid = find_middle(head)
    print(f"  中间节点: {mid.data}")  # 输出: 42

# 输出:
# 测试1：1 -> 2 -> 3 -> 4 -> 5
#   链表: 1 -> 2 -> 3 -> 4 -> 5 -> None
#   中间节点: 3
#
# 测试2：1 -> 2 -> 3 -> 4
#   链表: 1 -> 2 -> 3 -> 4 -> None
#   中间节点（偶数取后一个）: 3
#
# 测试3：只有一个节点
#   中间节点: 42
```

### 复杂度分析
- 时间复杂度: O(n)，只需遍历链表一次
- 空间复杂度: O(1)，只用了两个指针

</details>
