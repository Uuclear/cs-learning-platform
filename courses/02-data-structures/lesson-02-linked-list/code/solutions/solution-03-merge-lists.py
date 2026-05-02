# 解答：挑战3 - 合并两个有序链表
# 核心思路：双指针+哨兵节点，像合并排序的merge步骤


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
    # 哨兵节点：简化边界处理
    dummy = Node(-1)
    tail = dummy

    # 每次比较两个链表当前节点的值，选较小的接在后面
    while l1 is not None and l2 is not None:
        if l1.data <= l2.data:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next

    # 其中一个链表走完了，把剩余的接上
    tail.next = l1 if l1 is not None else l2

    return dummy.next


# ===== 测试代码 =====
def create_linked_list(values):
    if not values:
        return None
    head = Node(values[0])
    current = head
    for v in values[1:]:
        current.next = Node(v)
        current = current.next
    return head


def print_linked_list(head):
    values = []
    current = head
    while current is not None:
        values.append(str(current.data))
        current = current.next
    return " -> ".join(values) + " -> None"


if __name__ == "__main__":
    print("测试1：")
    l1 = create_linked_list([1, 3, 5])
    l2 = create_linked_list([2, 4, 6])
    print(f"  l1: {print_linked_list(l1)}")
    print(f"  l2: {print_linked_list(l2)}")
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")
    # 输出: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> None

    print("\n测试2：")
    l1 = create_linked_list([1, 2, 4])
    l2 = create_linked_list([1, 3, 4])
    print(f"  l1: {print_linked_list(l1)}")
    print(f"  l2: {print_linked_list(l2)}")
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")
    # 输出: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> None

    print("\n测试3：")
    l1 = None
    l2 = create_linked_list([0])
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")
    # 输出: 0 -> None

    print("\n测试4：")
    l1 = create_linked_list([1, 5, 10, 20])
    l2 = create_linked_list([3, 7])
    print(f"  l1: {print_linked_list(l1)}")
    print(f"  l2: {print_linked_list(l2)}")
    merged = merge_two_lists(l1, l2)
    print(f"  合并: {print_linked_list(merged)}")
    # 输出: 1 -> 3 -> 5 -> 7 -> 10 -> 20 -> None

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
#   合并: 0 -> None
#
# 测试4：
#   l1: 1 -> 5 -> 10 -> 20 -> None
#   l2: 3 -> 7 -> None
#   合并: 1 -> 3 -> 5 -> 7 -> 10 -> 20 -> None
