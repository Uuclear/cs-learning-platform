## 挑战2: 递归绘制杨辉三角

### 难度
⭐⭐⭐

### 描述
杨辉三角（Pascal's Triangle）是一种经典的数学图案。用递归生成杨辉三角的前 n 行。

杨辉三角的规律：
- 每行第一个和最后一个数字都是 1
- 中间的数字 = 上一行相邻两个数字之和

```
        1
      1   1
    1   2   1
  1   3   3   1
1   4   6   4   1
```

### 输入
- `n`: 行数（正整数，1 <= n <= 20）

### 输出
- 返回列表的列表，每个子列表是一行的数字

### 示例

**示例 1:**
```
输入: n=1
输出: [[1]]
```

**示例 2:**
```
输入: n=4
输出: [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
```

**示例 3:**
```
输入: n=5
输出: [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
```

### 约束条件
- 1 <= n <= 20
- 不需要处理负数或0

### 提示
- 基准情况：第1行 = [1]
- 递归思路：第 n 行 = 基于第 n-1 行来生成
- 第 n 行的第 i 个元素（0 < i < n-1）= 第 n-1 行的第 i-1 个 + 第 i 个
- 每行首尾都是 1

### 进阶思考
- 杨辉三角的每一行其实就是组合数 C(n,k)，你能解释为什么吗？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
递归生成前 n-1 行，然后基于最后一行来生成第 n 行。第 n 行的每个中间元素都是上一行相邻两元素之和。

### 代码
```python
def pascal_triangle(n):
    """
    递归生成杨辉三角的前 n 行
    时间复杂度: O(n^2) —— 每行最多 n 个元素，共 n 行
    空间复杂度: O(n^2) —— 存储整个三角形
    """
    # 基准情况
    if n == 1:
        return [[1]]
    
    # 递归：先生成前 n-1 行
    triangle = pascal_triangle(n - 1)
    
    # 获取上一行
    prev_row = triangle[-1]
    
    # 生成当前行：首尾是1，中间是上一行相邻元素之和
    current_row = [1]  # 第一个元素
    for i in range(len(prev_row) - 1):
        current_row.append(prev_row[i] + prev_row[i + 1])
    current_row.append(1)  # 最后一个元素
    
    triangle.append(current_row)
    return triangle


def print_triangle(triangle):
    """格式化打印杨辉三角"""
    n = len(triangle)
    for i, row in enumerate(triangle):
        # 居中对齐
        spaces = " " * (n - i - 1)
        row_str = " ".join(str(x) for x in row)
        print(f"{spaces}{row_str}")


if __name__ == "__main__":
    print("=== 杨辉三角 ===\n")
    
    print("--- 前5行 ---")
    triangle = pascal_triangle(5)
    print_triangle(triangle)
    # 输出:
    #     1
    #    1 1
    #   1 2 1
    #  1 3 3 1
    # 1 4 6 4 1
    
    print()
    
    print("--- 前7行 ---")
    triangle = pascal_triangle(7)
    print_triangle(triangle)
    # 输出:
    #       1
    #      1 1
    #     1 2 1
    #    1 3 3 1
    #   1 4 6 4 1
    #  1 5 10 10 5 1
    # 1 6 15 20 15 6 1
```

### 复杂度分析
- 时间复杂度: O(n^2) —— 每行最多 n 个元素，共 n 行
- 空间复杂度: O(n^2) —— 存储整个三角形

</details>
