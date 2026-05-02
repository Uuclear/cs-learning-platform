#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链表常见操作示例

这里展示一些链表的经典操作，比如反转链表、检测环、合并链表等。
这些是面试中经常遇到的问题！
"""

class ListNode:
    """链表节点类"""
    def __init__(self, val=0):
        self.val = val
        self.next = None


def create_linked_list(values):
    """根据值列表创建链表"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def display_linked_list(head):
    """显示链表内容"""
    elements = []
    current = head
    while current:
        elements.append(str(current.val))
        current = current.next
    return " -> ".join(elements) + " -> None"


def reverse_linked_list(head):
    """
    反转链表
    
    时间复杂度: O(n)
    空间复杂度: O(1)
    """
    prev = None
    current = head
    
    while current:
        next_temp = current.next  # 保存下一个节点
        current.next = prev       # 反转当前节点的指针
        prev = current           # 移动prev指针
        current = next_temp      # 移动current指针
    
    return prev  # prev现在是新的头节点


def has_cycle(head):
    """
    检测链表是否有环（Floyd's Cycle Detection Algorithm）
    
    使用快慢指针：快指针每次走两步，慢指针每次走一步
    如果有环，快指针最终会追上慢指针
    """
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    
    return True


def merge_two_sorted_lists(list1, list2):
    """
    合并两个有序链表
    
    时间复杂度: O(m + n)
    空间复杂度: O(1)
    """
    dummy = ListNode(0)  # 虚拟头节点
    current = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    
    # 连接剩余的节点
    current.next = list1 if list1 else list2
    
    return dummy.next


# 示例使用
if __name__ == "__main__":
    print("=== 链表操作演示 ===")
    
    # 1. 反转链表
    print("\n1. 反转链表:")
    original_list = create_linked_list([1, 2, 3, 4, 5])
    print(f"原链表: {display_linked_list(original_list)}")
    reversed_list = reverse_linked_list(original_list)
    print(f"反转后: {display_linked_list(reversed_list)}")
    
    # 2. 检测环
    print("\n2. 检测环:")
    acyclic_list = create_linked_list([1, 2, 3])
    print(f"无环链表: {display_linked_list(acyclic_list)}")
    print(f"是否有环: {has_cycle(acyclic_list)}")
    
    # 创建有环链表
    cyclic_list = create_linked_list([1, 2, 3, 4])
    # 让最后一个节点指向第二个节点，形成环
    current = cyclic_list
    while current.next:
        current = current.next
    current.next = cyclic_list.next  # 指向第二个节点
    print("有环链表: 1 -> 2 -> 3 -> 4 -> 2 (形成环)")
    print(f"是否有环: {has_cycle(cyclic_list)}")
    
    # 3. 合并有序链表
    print("\n3. 合并有序链表:")
    list_a = create_linked_list([1, 3, 5, 7])
    list_b = create_linked_list([2, 4, 6, 8])
    print(f"链表A: {display_linked_list(list_a)}")
    print(f"链表B: {display_linked_list(list_b)}")
    merged_list = merge_two_sorted_lists(list_a, list_b)
    print(f"合并后: {display_linked_list(merged_list)}")
