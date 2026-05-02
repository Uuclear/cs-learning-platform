# 解答：挑战1 - 反转单向链表
# 核心思路：用三个指针，把链表的箭头方向反过来


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
    print("测试1：反转 1 -> 2 -> 3 -> 4")
    head = create_linked_list([1, 2, 3, 4])
    print(f"  反转前: {print_linked_list(head)}")
    head = reverse_linked_list(head)
    print(f"  反转后: {print_linked_list(head)}")
    # 输出: 4 -> 3 -> 2 -> 1 -> None

    print("\n测试2：反转 5")
    head = create_linked_list([5])
    print(f"  反转前: {print_linked_list(head)}")
    head = reverse_linked_list(head)
    print(f"  反转后: {print_linked_list(head)}")
    # 输出: 5 -> None

    print("\n测试3：反转空链表")
    head = reverse_linked_list(None)
    print(f"  反转后: {print_linked_list(head)}")
    # 输出:  -> None

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
