# 练习3解答: 用两个栈实现队列
# 经典的面试问题

class MyQueue:
    """
    用两个栈实现的队列
    入队均摊 O(1)，出队均摊 O(1)

    核心思路：
    - in_stack 负责接收入队
    - out_stack 负责提供出队
    - 当 out_stack 为空时，将 in_stack 倒过来倒入 out_stack
    """
    def __init__(self):
        self.in_stack = []   # 入队栈：新元素都压到这里
        self.out_stack = []  # 出队栈：出队元素都从这里弹出

    def _transfer(self):
        """
        将 in_stack 的元素转移到 out_stack
        倒序转移，这样 in_stack 的栈底（最早元素）变成 out_stack 的栈顶
        """
        while self.in_stack:
            item = self.in_stack.pop()
            self.out_stack.append(item)

    def enqueue(self, item):
        """
        入队：直接压入 in_stack，O(1)
        """
        self.in_stack.append(item)
        print(f"  [入队] {item} → in_stack: {self.in_stack}")

    def dequeue(self):
        """
        出队：从 out_stack 弹出，均摊 O(1)
        如果 out_stack 为空，先从 in_stack 转移
        """
        if self.out_stack:
            item = self.out_stack.pop()
            print(f"  [出队] {item} ← out_stack: {self.out_stack}")
            return item

        if not self.in_stack:
            print("  [警告] 队列为空！")
            return None

        # out_stack 为空，需要转移
        print(f"  → out_stack 为空，从 in_stack 转移: {self.in_stack}")
        self._transfer()
        item = self.out_stack.pop()
        print(f"  [出队] {item} ← out_stack: {self.out_stack}")
        return item

    def is_empty(self):
        """判断队列是否为空"""
        return not self.in_stack and not self.out_stack


def test_my_queue():
    """测试两个栈实现的队列"""
    print("=== 两个栈实现队列测试 ===\n")

    q = MyQueue()

    # 入队
    print("--- 入队 ---")
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    print()

    # 出队
    print("--- 出队（触发转移） ---")
    print(f"出队: {q.dequeue()}")  # 返回 1
    print(f"出队: {q.dequeue()}")  # 返回 2
    print()

    # 再入队
    print("--- 再入队 ---")
    q.enqueue(4)
    q.enqueue(5)
    print()

    # 继续出队
    print("--- 继续出队 ---")
    print(f"出队: {q.dequeue()}")  # 返回 3
    print(f"出队: {q.dequeue()}")  # 返回 4
    print(f"出队: {q.dequeue()}")  # 返回 5
    print()

    # 空队列
    print("--- 空队列 ---")
    q.dequeue()

    print()
    print("均摊分析：每个元素最多被 push 2 次、pop 2 次")
    print("所以 enqueue 和 dequeue 的均摊时间复杂度都是 O(1)")


if __name__ == "__main__":
    test_my_queue()

# 预期输出:
# === 两个栈实现队列测试 ===
#
# --- 入队 ---
#   [入队] 1 → in_stack: [1]
#   [入队] 2 → in_stack: [1, 2]
#   [入队] 3 → in_stack: [1, 2, 3]
#
# --- 出队（触发转移） ---
#   → out_stack 为空，从 in_stack 转移: [1, 2, 3]
#   [出队] 1 ← out_stack: [3, 2]
# 出队: 1
#   [出队] 2 ← out_stack: [3]
# 出队: 2
#
# --- 再入队 ---
#   [入队] 4 → in_stack: [4]
#   [入队] 5 → in_stack: [4, 5]
#
# --- 继续出队 ---
#   [出队] 3 ← out_stack: []
# 出队: 3
#   → out_stack 为空，从 in_stack 转移: [4, 5]
#   [出队] 4 ← out_stack: [5]
# 出队: 4
#   [出队] 5 ← out_stack: []
# 出队: 5
#
# --- 空队列 ---
#   [警告] 队列为空！
#
# 均摊分析：每个元素最多被 push 2 次、pop 2 次
# 所以 enqueue 和 dequeue 的均摊时间复杂度都是 O(1)
