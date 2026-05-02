# 挑战1: 最小栈

## 难度
⭐⭐

## 描述
设计一个"最小栈"，除了常规的push、pop、peek操作外，还需要能在O(1)时间内返回栈中的最小元素。

## 要求
- 实现 `MinStack` 类
- `push(x)` — 将元素x入栈
- `pop()` — 弹出栈顶元素
- `peek()` — 查看栈顶元素（不弹出）
- `get_min()` — 返回当前栈中的最小值，时间复杂度O(1)

## 示例
```
操作: push(3) → push(5) → push(2) → push(1) → get_min() → pop() → get_min()
最小值: -            -            -            -         → 1      → -     → 2
```

## 约束条件
- 所有操作都在O(1)时间内完成
- 保证在非空栈上调用pop、peek、get_min

## 提示
- 可以用一个辅助栈来记录每个状态下的最小值
- 每次push时，辅助栈同时记录当前最小值

## 进阶思考
- 如果不用辅助栈，还能怎么做？（提示：存差值法）

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
使用两个栈：一个数据栈存所有元素，一个最小值栈同步记录当前最小值。每次push时，最小值栈存入当前最小值和新元素中的较小者。

### 代码
```python
class MinStack:
    def __init__(self):
        self.data = []    # 数据栈
        self.mins = []    # 最小值栈

    def push(self, x):
        self.data.append(x)
        if not self.mins:
            self.mins.append(x)
        else:
            self.mins.append(min(x, self.mins[-1]))

    def pop(self):
        if self.data:
            self.mins.pop()
            return self.data.pop()
        return None

    def peek(self):
        return self.data[-1] if self.data else None

    def get_min(self):
        return self.mins[-1] if self.mins else None


# 测试
if __name__ == "__main__":
    s = MinStack()
    s.push(3); print(f"push(3) → min={s.get_min()}")
    s.push(5); print(f"push(5) → min={s.get_min()}")
    s.push(2); print(f"push(2) → min={s.get_min()}")
    s.push(1); print(f"push(1) → min={s.get_min()}")
    s.pop()
    print(f"pop()   → min={s.get_min()}")

# 输出:
# push(3) → min=3
# push(5) → min=3
# push(2) → min=2
# push(1) → min=1
# pop()   → min=2
```

### 复杂度分析
- 时间复杂度: push O(1), pop O(1), get_min O(1)
- 空间复杂度: O(n)，需要额外的最小值栈

</details>
