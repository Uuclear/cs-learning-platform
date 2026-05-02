## 挑战1: 递归计算幂

### 难度
⭐⭐

### 描述
用递归实现计算 `base^exponent`（base 的 exponent 次幂）。要求使用"分治"思想来优化计算。

### 输入
- `base`: 底数（整数）
- `exponent`: 指数（非负整数）

### 输出
- 返回 `base^exponent` 的结果

### 示例

**示例 1:**
```
输入: base=2, exponent=10
输出: 1024
解释: 2^10 = 1024
```

**示例 2:**
```
输入: base=3, exponent=0
输出: 1
解释: 任何数的0次方等于1（基准情况）
```

**示例 3:**
```
输入: base=5, exponent=3
输出: 125
解释: 5^3 = 5 × 5 × 5 = 125
```

### 约束条件
- exponent >= 0
- 不需要处理负指数

### 提示
- 基准情况：`base^0 = 1`
- 分治思路：
  - 如果 exponent 是偶数：`base^n = (base^(n/2))^2`
  - 如果 exponent 是奇数：`base^n = base * base^(n-1)`
- 这种方法的时间复杂度是 O(log n)，比逐次相乘的 O(n) 快得多！

### 进阶思考
- 这种方法叫"快速幂"算法，你能解释为什么时间复杂度是 O(log n) 吗？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
利用分治思想，把 `base^n` 拆成更小的子问题。当 n 是偶数时，只需要计算一半的幂然后平方；当 n 是奇数时，拆出一个 base 再递归处理偶数情况。

### 代码
```python
def power(base, exponent):
    """
    快速幂递归实现
    时间复杂度: O(log n)
    空间复杂度: O(log n) —— 调用栈深度
    """
    # 基准情况：任何数的0次方等于1
    if exponent == 0:
        return 1
    
    # 偶数：base^n = (base^(n/2))^2
    if exponent % 2 == 0:
        half = power(base, exponent // 2)
        return half * half
    
    # 奇数：base^n = base * base^(n-1)
    return base * power(base, exponent - 1)


if __name__ == "__main__":
    print("=== 快速幂 ===\n")
    
    test_cases = [
        (2, 10),
        (3, 0),
        (5, 3),
        (2, 30),
    ]
    
    for base, exp in test_cases:
        result = power(base, exp)
        print(f"  {base}^{exp} = {result}")

# 预期输出:
# === 快速幂 ===
#
#   2^10 = 1024
#   3^0 = 1
#   5^3 = 125
#   2^30 = 1073741824
```

### 复杂度分析
- 时间复杂度: O(log n) —— 每次把指数减半
- 空间复杂度: O(log n) —— 调用栈深度

</details>
