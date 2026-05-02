# 栈的基本实现：数组版和链表版
# 核心思想：后进先出（LIFO），就像一叠盘子，只能从上面放和取

class ArrayStack:
    """
    用数组（Python列表）实现的栈
    优点：简单直观，入栈出栈都是O(1)
    """
    def __init__(self):
        self.items = []  # 用列表模拟数组

    def push(self, item):
        """入栈：把盘子放到最上面"""
        self.items.append(item)
        print(f"  push({item!r}) → 栈: {self.items}")

    def pop(self):
        """出栈：从最上面拿走一个盘子"""
        if self.is_empty():
            print("  pop() → 栈为空，无法出栈！")
            return None
        item = self.items.pop()
        print(f"  pop() → 弹出 {item!r}, 栈: {self.items}")
        return item

    def peek(self):
        """查看栈顶：看看最上面的盘子是什么，但不拿走"""
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        """判断栈是否为空：盘子上还有没有东西？"""
        return len(self.items) == 0

    def size(self):
        """返回栈中元素个数：数数有多少个盘子"""
        return len(self.items)


class Node:
    """链表节点：每个节点存一个数据和一个指向下一个节点的指针"""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedListStack:
    """
    用链表实现的栈
    优点：动态大小，不需要预估容量
    头节点就是栈顶，push/pop都在头部操作
    """
    def __init__(self):
        self.top = None  # 栈顶指针
        self._size = 0   # 栈的大小

    def push(self, item):
        """入栈：新节点成为新的栈顶"""
        new_node = Node(item)
        new_node.next = self.top  # 新节点指向原来的栈顶
        self.top = new_node       # 更新栈顶为新节点
        self._size += 1
        print(f"  push({item!r}) → 栈顶: {item!r}, 大小: {self._size}")

    def pop(self):
        """出栈：移除栈顶节点"""
        if self.is_empty():
            print("  pop() → 栈为空，无法出栈！")
            return None
        item = self.top.data
        self.top = self.top.next  # 栈顶指针下移
        self._size -= 1
        print(f"  pop() → 弹出 {item!r}, 大小: {self._size}")
        return item

    def peek(self):
        """查看栈顶"""
        if self.is_empty():
            return None
        return self.top.data

    def is_empty(self):
        """判断栈是否为空"""
        return self.top is None

    def size(self):
        """返回栈的大小"""
        return self._size


def demo_array_stack():
    """演示数组版栈的操作"""
    print("=" * 50)
    print("数组版栈演示")
    print("=" * 50)

    stack = ArrayStack()
    print(f"\n初始状态: 栈为空? {stack.is_empty()}, 大小: {stack.size()}")

    print("\n--- 入栈操作 ---")
    stack.push("盘子1")
    stack.push("盘子2")
    stack.push("盘子3")

    print(f"\n--- 查看栈顶 ---")
    print(f"  peek() → {stack.peek()!r}")
    print(f"  栈不变: {stack.items}")

    print(f"\n--- 出栈操作 ---")
    stack.pop()
    stack.pop()
    stack.pop()
    stack.pop()  # 再次pop，测试空栈

    print(f"\n最终状态: 栈为空? {stack.is_empty()}, 大小: {stack.size()}")


def demo_linked_list_stack():
    """演示链表版栈的操作"""
    print("\n" + "=" * 50)
    print("链表版栈演示")
    print("=" * 50)

    stack = LinkedListStack()
    print(f"\n初始状态: 栈为空? {stack.is_empty()}, 大小: {stack.size()}")

    print("\n--- 入栈操作 ---")
    for i in range(1, 4):
        stack.push(f"数据{i}")

    print(f"\n--- 查看栈顶 ---")
    print(f"  peek() → {stack.peek()!r}")

    print(f"\n--- 出栈操作 ---")
    while not stack.is_empty():
        stack.pop()

    print(f"\n最终状态: 栈为空? {stack.is_empty()}, 大小: {stack.size()}")


if __name__ == "__main__":
    demo_array_stack()
    demo_linked_list_stack()

# 预期输出:
# ==================================================
# 数组版栈演示
# ==================================================
#
# 初始状态: 栈为空? True, 大小: 0
#
# --- 入栈操作 ---
#   push('盘子1') → 栈: ['盘子1']
#   push('盘子2') → 栈: ['盘子1', '盘子2']
#   push('盘子3') → 栈: ['盘子1', '盘子2', '盘子3']
#
# --- 查看栈顶 ---
#   peek() → '盘子3'
#   栈不变: ['盘子1', '盘子2', '盘子3']
#
# --- 出栈操作 ---
#   pop() → 弹出 '盘子3', 栈: ['盘子1', '盘子2']
#   pop() → 弹出 '盘子2', 栈: ['盘子1']
#   pop() → 弹出 '盘子1', 栈: []
#   pop() → 栈为空，无法出栈！
#
# 最终状态: 栈为空? True, 大小: 0
#
# ==================================================
# 链表版栈演示
# ==================================================
#
# 初始状态: 栈为空? True, 大小: 0
#
# --- 入栈操作 ---
#   push('数据1') → 栈顶: '数据1', 大小: 1
#   push('数据2') → 栈顶: '数据2', 大小: 2
#   push('数据3') → 栈顶: '数据3', 大小: 3
#
# --- 查看栈顶 ---
#   peek() → '数据3'
#
# --- 出栈操作 ---
#   pop() → 弹出 '数据3', 大小: 2
#   pop() → 弹出 '数据2', 大小: 1
#   pop() → 弹出 '数据1', 大小: 0
#
# 最终状态: 栈为空? True, 大小: 0
