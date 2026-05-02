# 挑战3：合并两个有序链表

## 难度
⭐⭐⭐⭐

## 描述
给定两个升序排列的单向链表，将它们合并成一个新的升序链表。

**要求**：
- 合并后的链表也应该保持升序
- 尽量复用原有节点（不需要创建新节点）
- 如果其中一个链表为空，直接返回另一个

这是一个LeetCode经典题（#21），也是面试高频题。

## 输入
两个升序单向链表的头节点

## 输出
合并后的升序链表的头节点

## 示例

**示例 1:**
```
输入: l1 = 1 -> 3 -> 5 -> None
      l2 = 2 -> 4 -> 6 -> None
输出: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> None
解释: 像两排排队的人，按身高合并成一队
```

**示例 2:**
```
输入: l1 = 1 -> 2 -> 4 -> None
      l2 = 1 -> 3 -> 4 -> None
输出: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> None
解释: 相等的元素都保留
```

**示例 3:**
```
输入: l1 = None
      l2 = 0 -> None
输出: 0 -> None
解释: 空链表直接返回另一个
```

## 约束条件
- 每个链表长度: 0 <= n <= 50
- 节点数据范围: -100 <= data <= 100
- 两个链表都已经按升序排列

## 提示
- 可以创建一个"哨兵"节点（虚拟头节点）来简化边界处理
- 每次比较两个链表当前节点的值，选较小的那个接到结果链表后面
- 其中一个链表遍历完后，直接把另一个接在后面

## 进阶思考
- 如果要合并k个有序链表怎么办？能用最小堆优化吗？
- 递归版本的实现是怎样的？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
使用双指针+哨兵节点：
1. 创建一个虚拟的"哨兵"节点作为结果链表的起始点
2. 用tail指针追踪结果链表的最后一个节点
3. 每次比较l1和l2当前节点的值：
   - l1.val <= l2.val：把l1接在后面，l1前进
   - 否则：把l2接在后面，l2前进
4. 当其中一个链表遍历完后，把另一个直接接在tail后面
5. 返回哨兵节点的下一个节点（真正的头节点）

### 代码
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def merge_two_lists(l1, l2):
    """
    合并两个升序链表为一个升序链表
    参数: l1, l2 - 两个有序链表的头节点
    返回: 合并后链表的头节点
    """
    # 哨兵节点：简化边界处理，它的next才是真正的头
    dummy = Node(-1)
    tail = dummy  # tail指向结果链表的最后一个节点

    # 两个链表都还没走完时，比较并连接较小的节点
    while l1 is not None and l2 is not None:
        if l1.data <= l2.data:
            tail.next = l1    # 把l1接到结果链表后面
            l1 = l1.next      # l1前进一步
        else:
            tail.next = l2    # 把l2接到结果链表后面
            l2 = l2.next      # l2前进一步
        tail = tail.next      # tail前进一步

    # 其中一个链表走完了，把剩余的接上
    tail.next = l1 if l1 is not None else l2

    return dummy.next  # 哨兵节点的下一个才是真正头节点


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
    # 测试1：两个普通链表
    print("测试1：")
    l1 = create_linked_list([1, 3, 5])
    l2 = create_linked_list([2, 4, 6])
    print(f"  l1: {print_linked_list(l1)}")
    print(f"  l2: {print_linked_list(l2)}")
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")

    # 测试2：有重复元素
    print("\n测试2：")
    l1 = create_linked_list([1, 2, 4])
    l2 = create_linked_list([1, 3, 4])
    print(f"  l1: {print_linked_list(l1)}")
    print(f"  l2: {print_linked_list(l2)}")
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")

    # 测试3：一个为空
    print("\n测试3：")
    l1 = None
    l2 = create_linked_list([0])
    print(f"  l1: {print_linked_list(l1)}")
    print(f"  l2: {print_linked_list(l2)}")
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")

    # 测试4：长度不同
    print("\n测试4：")
    l1 = create_linked_list([1, 5, 10, 20])
    l2 = create_linked_list([3, 7])
    print(f"  l1: {print_linked_list(l1)}")
    print(f"  l2: {print_linked_list(l2)}")
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")

# 输出:
# 测试1：
#   l1: 1 -> 3 -> 5 -> None
#   l2: 2 -> 4 -> 6 -> None
#   合并: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> None
#
# 测试2：
#   l1: 1 -> 2 -> 4 -> None
#   l2: 1 -> 3 -> 4 -> None
#   合并: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> None
#
# 测试3：
#   l1:  -> None
#   l2: 0 -> None
#   合并: 0 -> None
#
# 测试4：
#   l1: 1 -> 5 -> 10 -> 20 -> None
#   l2: 3 -> 7 -> None
#   合并: 1 -> 3 -> 5 -> 7 -> 10 -> 20 -> None
```

### 复杂度分析
- 时间复杂度: O(m + n)，m和n分别是两个链表的长度，每个节点只被访问一次
- 空间复杂度: O(1)，只用了几个指针变量，不需要创建新节点

</details>
