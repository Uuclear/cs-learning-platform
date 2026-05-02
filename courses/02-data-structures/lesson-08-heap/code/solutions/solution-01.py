# 解答1：合并K个有序链表

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


import heapq


def merge_k_lists(lists):
    """
    使用最小堆合并K个有序链表
    核心思路：把每个链表的头节点放入堆，每次取最小，再放入下一个
    时间复杂度：O(N log K)，其中N是总节点数，K是链表数
    空间复杂度：O(K)，堆的大小
    """
    # 创建最小堆
    heap = []

    # 把每个非空链表的头节点放入堆
    # 元组格式：(节点值, 链表索引, 节点)
    # 链表索引用于处理值相同时的比较（Python 3要求元组可比较）
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))

    # 创建虚拟头节点
    dummy = ListNode(0)
    current = dummy

    # 计数器，用于生成唯一的tie-breaker
    counter = len(lists)

    while heap:
        # 取出最小节点
        val, _, node = heapq.heappop(heap)

        # 接到结果链表
        current.next = node
        current = current.next

        # 如果有下一个节点，放入堆中
        if node.next:
            heapq.heappush(heap, (node.next.val, counter, node.next))
            counter += 1

    return dummy.next


def print_list(head):
    """打印链表"""
    result = []
    while head:
        result.append(str(head.val))
        head = head.next
    print(" -> ".join(result))


def create_list(values):
    """从列表创建链表"""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


if __name__ == "__main__":
    print("=== 合并K个有序链表 ===\n")

    # 创建测试链表
    list1 = create_list([1, 4, 5])
    list2 = create_list([1, 3, 4])
    list3 = create_list([2, 6])

    print("输入链表:")
    print("链表1: ", end="")
    print_list(list1)
    print("链表2: ", end="")
    print_list(list2)
    print("链表3: ", end="")
    print_list(list3)

    # 合并
    merged = merge_k_lists([list1, list2, list3])

    print("\n合并结果: ", end="")
    print_list(merged)

    # 输出:
    # === 合并K个有序链表 ===
    #
    # 输入链表:
    # 链表1: 1 -> 4 -> 5
    # 链表2: 1 -> 3 -> 4
    # 链表3: 2 -> 6
    #
    # 合并结果: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6
