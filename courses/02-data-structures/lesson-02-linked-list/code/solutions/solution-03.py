#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答：实现链表的回文检测

要求：判断一个链表是否为回文链表
"""

class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


def is_palindrome(head):
    """
    判断链表是否为回文（使用快慢指针 + 反转后半部分）
    
    Args:
        head: 链表头节点
        
    Returns:
        bool: 是否为回文
    """
    if not head or not head.next:
        return True
    
    # 1. 找到中点
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # 2. 反转后半部分
    second_half = reverse_list(slow.next)
    
    # 3. 比较前半部分和反转后的后半部分
    first_half = head
    result = True
    while second_half:
        if first_half.val != second_half.val:
            result = False
            break
        first_half = first_half.next
        second_half = second_half.next
    
    # 4. 恢复链表（可选，如果需要保持原链表不变）
    slow.next = reverse_list(second_half) if second_half else None
    
    return result


def reverse_list(head):
    """辅助函数：反转链表"""
    prev = None
    current = head
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    return prev


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


def display_linked_list(head):
    """显示链表内容"""
    elements = []
    current = head
    while current:
        elements.append(str(current.val))
        current = current.next
    return " -> ".join(elements) + " -> None"


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        [],                              # 空链表
        [1],                             # 单个节点
        [1, 2],                          # 非回文
        [1, 2, 1],                       # 回文（奇数长度）
        [1, 2, 2, 1],                    # 回文（偶数长度）
        [1, 2, 3, 2, 1],                 # 回文（奇数长度）
        [1, 2, 3, 4, 5],                 # 非回文
        [1, 2, 3, 3, 2, 1]               # 回文（偶数长度）
    ]
    
    for i, values in enumerate(test_cases):
        head = create_linked_list(values)
        is_pal = is_palindrome(head)
        print(f"测试用例 {i+1}: {values}")
        print(f"链表: {display_linked_list(head)}")
        print(f"是否为回文: {is_pal}")
        print("-" * 30)
