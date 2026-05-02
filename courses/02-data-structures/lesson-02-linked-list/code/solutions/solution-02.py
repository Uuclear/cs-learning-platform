#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答：实现链表的中间节点查找

要求：给定链表头节点，返回链表的中间节点
如果链表长度为偶数，返回第二个中间节点
"""

class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


def find_middle_node(head):
    """
    查找链表的中间节点（快慢指针法）
    
    Args:
        head: 链表头节点
        
    Returns:
        ListNode: 中间节点
    """
    if not head:
        return None
    
    slow = head
    fast = head
    
    # 快指针每次走两步，慢指针每次走一步
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow


# 测试函数
def create_linked_list(values):
    """辅助函数：根据值列表创建链表"""
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    return head


def display_from_node(node):
    """从指定节点开始显示链表"""
    if not node:
        return "None"
    
    elements = []
    current = node
    while current:
        elements.append(str(current.val))
        current = current.next
    return " -> ".join(elements) + " -> None"


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [],                    # 空链表
        [1],                   # 单个节点
        [1, 2],                # 两个节点（偶数）
        [1, 2, 3],             # 三个节点（奇数）
        [1, 2, 3, 4],          # 四个节点（偶数）
        [1, 2, 3, 4, 5]        # 五个节点（奇数）
    ]
    
    for i, values in enumerate(test_cases):
        head = create_linked_list(values)
        middle = find_middle_node(head)
        print(f"测试用例 {i+1}: {values}")
        print(f"中间节点开始的链表: {display_from_node(middle)}")
        if middle:
            print(f"中间节点值: {middle.val}")
        print("-" * 30)
