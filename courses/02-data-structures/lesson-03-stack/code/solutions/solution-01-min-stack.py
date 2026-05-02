# 解答1: 最小栈
# 双栈方案：数据栈 + 最小值栈

class MinStack:
    """
    最小栈：支持O(1)时间获取最小值
    核心思路：用辅助栈同步记录每个状态下的最小值
    """
    def __init__(self):
        self.data = []    # 数据栈：存所有元素
        self.mins = []    # 最小值栈：min[i] = data[0..i]中的最小值

    def push(self, x):
        """入栈：数据栈直接入，最小值栈取min(当前值, 之前的最小值)"""
        self.data.append(x)
        if not self.mins:
            self.mins.append(x)
        else:
            self.mins.append(min(x, self.mins[-1]))

    def pop(self):
        """出栈：两个栈同时弹"""
        if not self.data:
            return None
        self.mins.pop()
        return self.data.pop()

    def peek(self):
        """查看栈顶"""
        return self.data[-1] if self.data else None

    def get_min(self):
        """O(1)获取当前最小值"""
        return self.mins[-1] if self.mins else None


if __name__ == "__main__":
    s = MinStack()
    s.push(3)
    print(f"push(3), min={s.get_min()}")  # min=3
    s.push(5)
    print(f"push(5), min={s.get_min()}")  # min=3
    s.push(2)
    print(f"push(2), min={s.get_min()}")  # min=2
    s.push(1)
    print(f"push(1), min={s.get_min()}")  # min=1
    s.pop()
    print(f"pop(),   min={s.get_min()}")  # min=2
    s.pop()
    print(f"pop(),   min={s.get_min()}")  # min=3

# 输出:
# push(3), min=3
# push(5), min=3
# push(2), min=2
# push(1), min=1
# pop(),   min=2
# pop(),   min=3
