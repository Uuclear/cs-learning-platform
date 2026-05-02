# 练习2解答: 最近请求次数
# 计算过去3000毫秒内的请求数

from collections import deque


class RecentCounter:
    """
    请求计数器 - 统计最近3000ms内的请求数
    核心思路：用队列存储时间戳，过期自动清理
    """
    def __init__(self):
        self.queue = deque()  # 存储请求时间戳
        self.window = 3000    # 时间窗口：3000ms

    def ping(self, timestamp):
        """
        添加新请求，返回过去3000ms内的请求总数
        参数: timestamp - 当前请求的时间戳（毫秒）
        返回: int - 有效请求数量
        """
        # 新请求入队
        self.queue.append(timestamp)

        # 移除过期的请求（超过3000ms窗口的）
        while self.queue and self.queue[0] < timestamp - self.window:
            expired = self.queue.popleft()
            print(f"    移除过期请求: {expired}")

        # 返回当前有效请求数
        count = len(self.queue)
        print(f"  ping({timestamp}) → 返回 {count}, 队列: {list(self.queue)}")
        return count


def test_recent_counter():
    """测试最近请求计数器"""
    print("=== 最近请求次数测试 ===\n")

    counter = RecentCounter()

    # 测试用例
    timestamps = [1, 100, 3001, 3002]
    for ts in timestamps:
        counter.ping(ts)

    print()
    print("--- 更多测试 ---")

    # 大量请求，测试过期逻辑
    counter2 = RecentCounter()
    for ts in range(0, 5000, 500):  # 0, 500, 1000, ..., 4500
        counter2.ping(ts)

    print()
    print("这个模式在LeetCode上是第933题，经典的队列应用题！")


if __name__ == "__main__":
    test_recent_counter()

# 预期输出:
# === 最近请求次数测试 ===
#
#   ping(1) → 返回 1, 队列: [1]
#   ping(100) → 返回 2, 队列: [1, 100]
#   ping(3001) → 返回 3, 队列: [1, 100, 3001]
#   ping(3002) → 返回 3, 队列: [100, 3001, 3002]
#     移除过期请求: 1
#
# --- 更多测试 ---
#   ping(0) → 返回 1, 队列: [0]
#   ping(500) → 返回 2, 队列: [0, 500]
#   ping(1000) → 返回 3, 队列: [0, 500, 1000]
#   ping(1500) → 返回 4, 队列: [0, 500, 1000, 1500]
#   ping(2000) → 返回 5, 队列: [0, 500, 1000, 1500, 2000]
#   ping(2500) → 返回 6, 队列: [0, 500, 1000, 1500, 2000, 2500]
#   ping(3000) → 返回 7, 队列: [0, 500, 1000, 1500, 2000, 2500, 3000]
#   ping(3500) → 返回 7, 队列: [500, 1000, 1500, 2000, 2500, 3000, 3500]
#     移除过期请求: 0
#   ping(4000) → 返回 7, 队列: [1000, 1500, 2000, 2500, 3000, 3500, 4000]
#     移除过期请求: 500
#   ping(4500) → 返回 7, 队列: [1500, 2000, 2500, 3000, 3500, 4000, 4500]
#     移除过期请求: 1000
#
# 这个模式在LeetCode上是第933题，经典的队列应用题！
