#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答：实现一个链表的长度计算函数

要求：给定链表头节点，返回链表的长度
"""

class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


def get_linked_list_length(head):
    """
    计算链表长度
    
    Args:
        head: 链表头节点
        
    Returns:
        int: 链表长度
    """
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    return length


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


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [],           # 空链表
        [1],          # 单个节点
        [1, 2, 3],    # 多个节点
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 较长链表
    ]
    
    for i, values in enumerate(test_cases):
        head = create_linked_list(values)
        length = get_linked_list_length(head)
        print(f"测试用例 {i+1}: {values}")
        print(f"链表长度: {length}")
        print("-" * 30)
