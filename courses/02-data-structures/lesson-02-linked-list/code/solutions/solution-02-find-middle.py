# 解答：挑战2 - 查找链表中间节点
# 核心思路：快慢指针，龟兔赛跑


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

    while fast is not None and fast.next is not None:
        slow = slow.next          # 慢指针走一步
        fast = fast.next.next     # 快指针走两步

    return slow  # slow 正好在中间


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


if __name__ == "__main__":
    print("测试1：1 -> 2 -> 3 -> 4 -> 5")
    head = create_linked_list([1, 2, 3, 4, 5])
    mid = find_middle(head)
    print(f"  中间节点: {mid.data}")
    # 输出: 3

    print("\n测试2：1 -> 2 -> 3 -> 4")
    head = create_linked_list([1, 2, 3, 4])
    mid = find_middle(head)
    print(f"  中间节点（偶数取后一个）: {mid.data}")
    # 输出: 3

    print("\n测试3：只有一个节点 42")
    head = create_linked_list([42])
    mid = find_middle(head)
    print(f"  中间节点: {mid.data}")
    # 输出: 42

# 输出:
# 测试1：1 -> 2 -> 3 -> 4 -> 5
#   中间节点: 3
#
# 测试2：1 -> 2 -> 3 -> 4
#   中间节点（偶数取后一个）: 3
#
# 测试3：只有一个节点 42
#   中间节点: 42
