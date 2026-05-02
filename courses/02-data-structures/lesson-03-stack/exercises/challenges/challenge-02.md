# 挑战2: 用两个栈实现队列

## 难度
⭐⭐⭐

## 描述
只用两个栈（不能使用其他数据结构）来实现一个队列，支持先进先出（FIFO）的语义。

## 要求
- 实现 `MyQueue` 类
- `enqueue(x)` — 将元素x加入队列末尾
- `dequeue()` — 从队列头部移除并返回元素
- `peek()` — 查看队列头部元素（不删除）
- `is_empty()` — 判断队列是否为空

## 示例
```
操作: enqueue(1) → enqueue(2) → enqueue(3) → dequeue() → peek()
返回: -          → -          → -          → 1         → 2
```

## 约束条件
- 只能使用两个栈，不能引入其他数据结构
- 所有操作的摊还（均摊）时间复杂度应为O(1)

## 提示
- 一个栈负责入队（in_stack），一个栈负责出队（out_stack）
- 当out_stack为空时，把in_stack里的元素全部弹出并压入out_stack
- 想想这样做的"倒水"效果如何实现FIFO

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
核心思想是"倒水"：入队时把元素压入in_stack；出队时如果out_stack为空，就把in_stack全部倒过来。这样两次栈反转，最先进来的元素就到了out_stack的栈顶。

### 代码
```python
class MyQueue:
    def __init__(self):
        self.in_stack = []   # 入队栈
        self.out_stack = []  # 出队栈

    def enqueue(self, x):
        """入队：直接压入in_stack"""
        self.in_stack.append(x)

    def dequeue(self):
        """出队：从out_stack弹，空了就倒水"""
        self._transfer()
        if self.out_stack:
            return self.out_stack.pop()
        return None

    def peek(self):
        """查看队首"""
        self._transfer()
        if self.out_stack:
            return self.out_stack[-1]
        return None

    def is_empty(self):
        return not self.in_stack and not self.out_stack

    def _transfer(self):
        """倒水：把in_stack的元素全部倒到out_stack"""
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())


# 测试
if __name__ == "__main__":
    q = MyQueue()
    q.enqueue(1); print(f"enqueue(1) → 队列: in={q.in_stack}, out={q.out_stack}")
    q.enqueue(2); print(f"enqueue(2) → 队列: in={q.in_stack}, out={q.out_stack}")
    q.enqueue(3); print(f"enqueue(3) → 队列: in={q.in_stack}, out={q.out_stack}")
    print(f"dequeue() → {q.dequeue()}")
    print(f"peek()    → {q.peek()}")
    print(f"dequeue() → {q.dequeue()}")
    print(f"dequeue() → {q.dequeue()}")
    print(f"dequeue() → {q.dequeue()}")  # 空队列
    print(f"is_empty?  → {q.is_empty()}")

# 输出:
# enqueue(1) → 队列: in=[1], out=[]
# enqueue(2) → 队列: in=[1, 2], out=[]
# enqueue(3) → 队列: in=[1, 2, 3], out=[]
# dequeue() → 1
# peek()    → 2
# dequeue() → 2
# dequeue() → 3
# dequeue() → None
# is_empty?  → True
```

### 复杂度分析
- 时间复杂度: enqueue O(1)，dequeue 摊还O(1)（每个元素最多进出各一次栈）
- 空间复杂度: O(n)，两个栈共存储n个元素

</details>
