# 解答2: 用两个栈实现队列
# 核心思想：入队栈 + 出队栈，"倒水"实现FIFO

class MyQueue:
    """
    用两个栈模拟队列
    in_stack:  负责入队（新元素）
    out_stack: 负责出队（老元素）
    """
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def enqueue(self, x):
        """入队：压入入队栈"""
        self.in_stack.append(x)

    def dequeue(self):
        """出队：如果出队栈为空就倒水，然后弹出"""
        self._transfer()
        if self.out_stack:
            return self.out_stack.pop()
        return None

    def peek(self):
        """查看队首：倒水后看栈顶"""
        self._transfer()
        return self.out_stack[-1] if self.out_stack else None

    def is_empty(self):
        return not self.in_stack and not self.out_stack

    def _transfer(self):
        """倒水：把入队栈的元素全部倒到出队栈"""
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())


if __name__ == "__main__":
    q = MyQueue()
    for i in range(1, 5):
        q.enqueue(i)
        print(f"enqueue({i}), 队首={q.peek()}")

    print()
    while not q.is_empty():
        val = q.dequeue()
        print(f"dequeue() → {val}, 队首={q.peek()}")

# 输出:
# enqueue(1), 队首=1
# enqueue(2), 队首=1
# enqueue(3), 队首=1
# enqueue(4), 队首=1
#
# dequeue() → 1, 队首=2
# dequeue() → 2, 队首=3
# dequeue() → 3, 队首=4
# dequeue() → 4, 队首=None
