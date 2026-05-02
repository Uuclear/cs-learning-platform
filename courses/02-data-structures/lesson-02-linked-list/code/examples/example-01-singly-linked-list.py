#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单链表实现示例

链表就像一队手拉手的小朋友，每个小朋友（节点）只知道下一个小朋友是谁，
但不知道前面的小朋友是谁。这就是单链表的特点！
"""

class ListNode:
    """链表节点类"""
    def __init__(self, val=0):
        self.val = val          # 节点存储的值
        self.next = None        # 指向下一个节点的指针


class SinglyLinkedList:
    """单链表类"""
    def __init__(self):
        self.head = None        # 头节点，指向链表的第一个节点

    def append(self, val):
        """在链表末尾添加节点"""
        new_node = ListNode(val)
        if not self.head:
            # 如果链表为空，新节点就是头节点
            self.head = new_node
        else:
            # 找到链表的最后一个节点
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def insert_at_head(self, val):
        """在链表头部插入节点"""
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node

    def delete(self, val):
        """删除第一个值为val的节点"""
        if not self.head:
            return False

        # 如果要删除的是头节点
        if self.head.val == val:
            self.head = self.head.next
            return True

        # 查找要删除的节点
        current = self.head
        while current.next and current.next.val != val:
            current = current.next

        # 如果找到了要删除的节点
        if current.next:
            current.next = current.next.next
            return True

        return False

    def find(self, val):
        """查找值为val的节点，返回索引位置"""
        current = self.head
        index = 0
        while current:
            if current.val == val:
                return index
            current = current.next
            index += 1
        return -1  # 未找到

    def display(self):
        """显示链表内容"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.val))
            current = current.next
        return " -> ".join(elements) + " -> None"


# 示例使用
if __name__ == "__main__":
    # 创建一个单链表
    linked_list = SinglyLinkedList()

    print("=== 单链表演示 ===")
    print(f"初始链表: {linked_list.display()}")

    # 在末尾添加元素
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    print(f"添加1,2,3后: {linked_list.display()}")

    # 在头部插入元素
    linked_list.insert_at_head(0)
    print(f"在头部插入0后: {linked_list.display()}")

    # 查找元素
    print(f"查找元素2的位置: {linked_list.find(2)}")
    print(f"查找元素5的位置: {linked_list.find(5)}")

    # 删除元素
    linked_list.delete(2)
    print(f"删除元素2后: {linked_list.display()}")

    linked_list.delete(0)
    print(f"删除头节点0后: {linked_list.display()}")
