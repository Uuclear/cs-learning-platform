# 挑战1：区间合并问题 - 解答
# 给定一组区间，合并所有重叠的区间

def merge_intervals(intervals):
    """
    合并重叠区间
    参数: intervals - 区间列表，每个区间为[开始, 结束]
    返回: 合并后的区间列表
    """
    if not intervals:
        return []

    # 按区间起点排序
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        last = merged[-1]
        # 如果当前区间与上一个区间重叠，合并
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            # 不重叠，添加新区间
            merged.append(current)

    return merged


if __name__ == "__main__":
    # 测试
    test1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(f"输入: {test1}")
    print(f"输出: {merge_intervals(test1)}")
    # 输出: [[1, 6], [8, 10], [15, 18]]

    test2 = [[1, 4], [4, 5]]
    print(f"输入: {test2}")
    print(f"输出: {merge_intervals(test2)}")
    # 输出: [[1, 5]]

# 思路:
# 贪心策略：按起点排序，然后贪心地合并所有重叠区间。
# 每次遇到不重叠的区间，就知道上一个合并结果已经确定。
# 时间复杂度: O(n log n)，主要是排序的时间
# 空间复杂度: O(n)，存储结果
