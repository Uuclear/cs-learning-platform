#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双链表实现示例

双链表就像一队手拉手的小朋友，每个小朋友（节点）不仅知道下一个小朋友是谁，
还知道前面的小朋友是谁。这样就可以双向移动了！
"""

class DoublyListNode:
    """双链表节点类"""
    def __init__(self, val=0):
        self.val = val          # 节点存储的值
        self.next = None        # 指向下一个节点的指针
        self.prev = None        # 指向前一个节点的指针


class DoublyLinkedList:
    """双链表类"""
    def __init__(self):
        self.head = None        # 头节点
        self.tail = None        # 尾节点

    def append(self, val):
        """在链表末尾添加节点"""
        new_node = DoublyListNode(val)
        if not self.head:
            # 链表为空
            self.head = new_node
            self.tail = new_node
        else:
            # 连接到当前尾节点
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def prepend(self, val):
        """在链表头部添加节点"""
        new_node = DoublyListNode(val)
        if not self.head:
            # 链表为空
            self.head = new_node
            self.tail = new_node
        else:
            # 连接到当前头节点
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def delete(self, val):
        """删除第一个值为val的节点"""
        current = self.head
        while current:
            if current.val == val:
                # 如果是头节点
                if current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                    else:
                        self.tail = None  # 链表变空
                # 如果是尾节点
                elif current == self.tail:
                    self.tail = current.prev
                    self.tail.next = None
                # 如果是中间节点
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

    def find(self, val):
        """查找值为val的节点"""
        current = self.head
        index = 0
        while current:
            if current.val == val:
                return index
            current = current.next
            index += 1
        return -1

    def display_forward(self):
        """正向显示链表"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.val))
            current = current.next
        return " <-> ".join(elements) + " <-> None"

    def display_backward(self):
        """反向显示链表"""
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.val))
            current = current.prev
        return " <-> ".join(elements) + " <-> None"


# 示例使用
if __name__ == "__main__":
    # 创建一个双链表
    dll = DoublyLinkedList()

    print("=== 双链表演示 ===")
    print(f"初始链表(正向): {dll.display_forward()}")
    print(f"初始链表(反向): {dll.display_backward()}")

    # 添加元素
    dll.append(1)
    dll.append(2)
    dll.append(3)
    print(f"添加1,2,3后(正向): {dll.display_forward()}")
    print(f"添加1,2,3后(反向): {dll.display_backward()}")

    # 在头部添加元素
    dll.prepend(0)
    print(f"在头部添加0后(正向): {dll.display_forward()}")
    print(f"在头部添加0后(反向): {dll.display_backward()}")

    # 查找和删除
    print(f"查找元素2的位置: {dll.find(2)}")
    print(f"查找元素5的位置: {dll.find(5)}")

    dll.delete(2)
    print(f"删除元素2后(正向): {dll.display_forward()}")
    print(f"删除元素2后(反向): {dll.display_backward()}")

    dll.delete(0)
    print(f"删除头节点0后(正向): {dll.display_forward()}")
    print(f"删除头节点0后(反向): {dll.display_backward()}")
