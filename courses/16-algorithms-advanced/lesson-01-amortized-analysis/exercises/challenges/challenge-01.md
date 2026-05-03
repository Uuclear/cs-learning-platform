# 挑战1：摊销队列实现 ⭐⭐

## 问题描述

使用两个栈实现一个队列，使得 `enqueue`（入队）和 `dequeue`（出队）操作的**摊销时间复杂度都是 O(1)**。

传统的队列实现使用数组或链表，但这里要求使用两个栈来实现。这种方法在函数式编程语言中很常见，因为栈是更基础的数据结构。

## 输入/输出规格

### 类定义
```python
class AmortizedQueue:
    def __init__(self):
        # 初始化两个栈
        pass
    
    def enqueue(self, item):
        # 入队操作
        pass
    
    def dequeue(self):
        # 出队操作，返回队首元素
        # 如果队列为空，返回 None
        pass
    
    def is_empty(self):
        # 检查队列是否为空
        pass
```

### 示例
```python
q = AmortizedQueue()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
print(q.dequeue())  # 输出: 1
print(q.dequeue())  # 输出: 2
q.enqueue(4)
print(q.dequeue())  # 输出: 3
print(q.dequeue())  # 输出: 4
print(q.dequeue())  # 输出: None (队列为空)
```

## 约束条件

- 只能使用栈的基本操作：`push`、`pop`、`peek`、`is_empty`
- 不能使用数组的随机访问或其他数据结构
- 空间复杂度应为 O(n)，其中 n 是队列中的元素数量
- 必须保证摊销时间复杂度为 O(1)

## 提示

1. **双栈策略**：使用一个栈作为"输入栈"，另一个作为"输出栈"
2. **懒惰转移**：只有当输出栈为空时，才将输入栈的所有元素转移到输出栈
3. **摊销分析**：每个元素最多被 push 和 pop 各两次（一次在输入栈，一次在输出栈）

<details>
<summary>参考解决方案</summary>

```python
class AmortizedQueue:
    """
    使用两个栈实现的摊销队列
    """
    
    def __init__(self):
        self.input_stack = []   # 用于入队操作
        self.output_stack = []  # 用于出队操作
    
    def enqueue(self, item):
        """入队操作 - O(1) 实际时间"""
        self.input_stack.append(item)
    
    def dequeue(self):
        """出队操作 - O(1) 摊销时间"""
        # 如果输出栈为空，将输入栈的所有元素转移到输出栈
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())
        
        # 如果输出栈仍然为空，说明队列为空
        if not self.output_stack:
            return None
        
        return self.output_stack.pop()
    
    def is_empty(self):
        """检查队列是否为空"""
        return len(self.input_stack) == 0 and len(self.output_stack) == 0

# 摊销分析说明：
# - enqueue 操作总是 O(1)
# - dequeue 操作在最坏情况下需要 O(k) 时间（k 是输入栈大小）
# - 但是每个元素最多被转移一次，所以 n 次操作的总时间是 O(n)
# - 因此摊销时间复杂度为 O(1)
```

</details>