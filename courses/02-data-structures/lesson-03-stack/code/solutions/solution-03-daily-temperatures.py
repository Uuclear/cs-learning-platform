# 解答3: 每日温度问题
# 核心思想：单调递减栈，每个元素最多入栈出栈各一次

def daily_temperatures(temperatures):
    """
    计算每一天需要等待多少天才能遇到更高温度
    使用单调栈，时间复杂度O(n)
    """
    n = len(temperatures)
    result = [0] * n    # 默认都是0
    stack = []           # 单调递减栈，存索引

    for i, temp in enumerate(temperatures):
        # 当前温度比栈顶对应的温度更高 → 栈顶等到了
        while stack and temperatures[stack[-1]] < temp:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)

    return result


if __name__ == "__main__":
    tests = [
        [73, 74, 75, 71, 69, 72, 76, 73],
        [30, 40, 50, 60],
        [60, 50, 40, 30],
    ]

    for t in tests:
        result = daily_temperatures(t)
        print(f"温度: {t}")
        print(f"等待: {result}")
        print()

# 输出:
# 温度: [73, 74, 75, 71, 69, 72, 76, 73]
# 等待: [1, 1, 4, 2, 1, 1, 0, 0]
#
# 温度: [30, 40, 50, 60]
# 等待: [1, 1, 1, 0]
#
# 温度: [60, 50, 40, 30]
# 等待: [0, 0, 0, 0]
