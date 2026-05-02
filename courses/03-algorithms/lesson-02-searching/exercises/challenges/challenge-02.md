# 挑战2: 二分查找 —— 猜数字游戏

### 难度
⭐⭐

### 描述
你和朋友玩一个猜数字游戏。朋友心里想了一个1到N之间的整数，你每次可以猜一个数，朋友会告诉你"猜大了"、"猜小了"还是"猜对了"。

你的任务是：用最少次数猜出朋友心里的数字。聪明的你一定想到了——二分查找！

实现一个函数，用二分查找策略猜出目标数字，并返回猜了多少次。

### 输入
- `n`: 整数，数字范围的上限（1到n）
- `target`: 整数，朋友心里想的数字（1 <= target <= n）

### 输出
- 返回猜对的次数

### 示例

**示例 1:**
```
输入: n = 10, target = 6
输出: 3
解释:
  第1次猜: 5 -> 猜小了
  第2次猜: 8 -> 猜大了
  第3次猜: 6 -> 猜对了！
  共猜了3次
```

**示例 2:**
```
输入: n = 100, target = 50
输出: 1
解释:
  第1次猜: 50 -> 猜对了！
  共猜了1次（运气真好）
```

**示例 3:**
```
输入: n = 1000, target = 1
输出: 10
解释:
  最多猜10次就能找到（log₂(1000) ≈ 10）
```

### 约束条件
- 1 <= n <= 1,000,000
- 1 <= target <= n

### 提示
- 维护left=1和right=n两个边界
- 每次猜中间值 mid = (left + right) // 2
- 根据猜的结果调整边界
- 用一个计数器记录猜的次数

### 进阶思考
- n=1,000,000时，二分查找最多需要多少次？线性查找呢？
- 如果target是随机均匀的，平均需要猜多少次？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
这就是二分查找的标准实现。维护搜索范围[left, right]，每次猜中间的值，根据结果缩小范围。用计数器记录比较次数。

### 代码
```python
def guess_number(n, target):
    """
    用二分查找策略猜数字
    返回猜对的次数
    """
    left = 1
    right = n
    guesses = 0

    while left <= right:
        guesses += 1
        mid = (left + right) // 2

        if mid == target:
            print(f"  第{guesses}次猜: {mid} -> 猜对了！")
            return guesses
        elif mid < target:
            print(f"  第{guesses}次猜: {mid} -> 猜小了")
            left = mid + 1
        else:
            print(f"  第{guesses}次猜: {mid} -> 猜大了")
            right = mid - 1

    return guesses


# 测试
if __name__ == "__main__":
    print("=== 猜数字游戏 ===\n")

    # 测试1：小范围
    print("范围1-10，心里想的是6:")
    times = guess_number(10, 6)
    print(f"共猜了{times}次\n")

    # 测试2：刚好猜中
    print("范围1-100，心里想的是50:")
    times = guess_number(100, 50)
    print(f"共猜了{times}次\n")

    # 测试3：大范围验证
    print("范围1-1000，心里想的是1:")
    times = guess_number(1000, 1)
    print(f"共猜了{times}次（最多只需10次！）\n")

    # 验证：100万个数最多需要多少次
    import math
    max_guesses = math.ceil(math.log2(1000000))
    print(f"验证: 100万个数，二分查找最多需要 {max_guesses} 次")
    print(f"而线性查找最多需要 1,000,000 次")
    print(f"二分查找快了约 {1000000 / max_guesses:.0f} 倍！")
```

### 复杂度分析
- 时间复杂度: O(log n)，每次缩小一半搜索范围
- 空间复杂度: O(1)，只需要几个变量

</details>
