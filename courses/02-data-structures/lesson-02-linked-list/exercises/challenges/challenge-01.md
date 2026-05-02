# 挑战1：反转单向链表

## 难度
⭐⭐

## 描述
实现一个函数，将给定的单向链表反转。反转后，原来的最后一个节点变成头节点，原来的头节点变成最后一个节点。

例如：
```
原链表: 1 -> 2 -> 3 -> 4 -> None
反转后: 4 -> 3 -> 2 -> 1 -> None
```

## 输入
一个单向链表的头节点

## 输出
反转后的链表头节点

## 示例

**示例 1:**
```
输入: 1 -> 2 -> 3 -> None
输出: 3 -> 2 -> 1 -> None
解释: 将链表的箭头方向全部反过来
```

**示例 2:**
```
输入: 5 -> None
输出: 5 -> None
解释: 只有一个节点的链表，反转后不变
```

## 约束条件
- 链表长度范围: 0 <= n <= 100
- 节点数据范围: -100 <= data <= 100

## 提示
- 需要三个指针：prev（前一个）、current（当前）、next_node（下一个）
- 核心思路：让每个节点的next指针反过来指向prev
- 小心不要丢失对下一个节点的引用！

## 进阶思考
- 你能用递归的方式实现吗？
- 如果要求原地反转（不使用额外空间），怎么做？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
使用迭代法，用三个指针遍历链表：
1. `prev` 指向前一个节点（初始None）
2. `current` 指向当前节点（初始为head）
3. 保存 `next_node` 防止丢失下一个节点
4. 将 `current.next` 反转为指向 `prev`
5. 向前移动三个指针

### 代码
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def reverse_linked_list(head):
    """
    反转单向链表
    参数: head - 链表头节点
    返回: 反转后的链表头节点
    """
    prev = None           # 前一个节点，初始为空
    current = head        # 当前节点，从头开始

    while current is not None:
        next_node = current.next   # 先保存下一个节点（否则会丢失！）
        current.next = prev        # 反转：让当前节点指向前一个
        prev = current             # prev 向前走一步
        current = next_node        # current 向前走一步

    return prev  # 循环结束时，prev 是新的头节点


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
    # 测试1：普通链表
    print("测试1：反转 1 -> 2 -> 3 -> 4")
    head = create_linked_list([1, 2, 3, 4])
    print(f"  反转前: {print_linked_list(head)}")
    head = reverse_linked_list(head)
    print(f"  反转后: {print_linked_list(head)}")

    # 测试2：单元素
    print("\n测试2：反转 5")
    head = create_linked_list([5])
    print(f"  反转前: {print_linked_list(head)}")
    head = reverse_linked_list(head)
    print(f"  反转后: {print_linked_list(head)}")

    # 测试3：空链表
    print("\n测试3：反转空链表")
    head = reverse_linked_list(None)
    print(f"  反转后: {print_linked_list(head)}")

# 输出:
# 测试1：反转 1 -> 2 -> 3 -> 4
#   反转前: 1 -> 2 -> 3 -> 4 -> None
#   反转后: 4 -> 3 -> 2 -> 1 -> None
#
# 测试2：反转 5
#   反转前: 5 -> None
#   反转后: 5 -> None
#
# 测试3：反转空链表
#   反转后:  -> None
```

### 复杂度分析
- 时间复杂度: O(n)，只需遍历一次链表
- 空间复杂度: O(1)，只用了三个指针变量，不需要额外空间

</details>
