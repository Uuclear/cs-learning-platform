# 挑战3：最少站台问题 - 解答
# 给定火车到达和离开时间，求火车站最少需要多少个站台

def min_platforms(arrivals, departures):
    """
    最少站台问题
    参数: arrivals - 到达时间列表
          departures - 离开时间列表
    返回: 最少需要的站台数
    """
    # 按到达和离开时间排序
    arrivals.sort()
    departures.sort()

    platforms = 0       # 当前使用的站台数
    max_platforms = 0   # 历史最大站台数
    i = 0  # 到达时间指针
    j = 0  # 离开时间指针

    # 遍历所有事件
    while i < len(arrivals):
        if arrivals[i] < departures[j]:
            # 有火车到达，需要一个站台
            platforms += 1
            max_platforms = max(max_platforms, platforms)
            i += 1
        else:
            # 有火车离开，释放一个站台
            platforms -= 1
            j += 1

    return max_platforms


if __name__ == "__main__":
    # 测试
    arrivals =   [900,  940,  950,  1100, 1500, 1800]
    departures = [910,  1200, 1120, 1130, 1900, 2000]
    # 时间格式: HHMM (900=9:00, 1200=12:00)

    print("火车时刻表:")
    for i in range(len(arrivals)):
        print(f"  到达: {arrivals[i]//100}:{arrivals[i]%100:02d}, 离开: {departures[i]//100}:{departures[i]%100:02d}")

    result = min_platforms(arrivals, departures)
    print(f"\n最少需要 {result} 个站台")

    # 分析：
    # 9:00 到达 -> 1站台
    # 9:40 到达 -> 2站台 (9:10那辆还没走)
    # 9:50 到达 -> 3站台 (9:10和12:00的还没走)
    # 11:00 到达 -> 12:00的走了，但11:20才走，所以还是需要3站台
    # ...
    # 最大同时存在3辆火车

# 输出:
# 火车时刻表:
#   到达: 9:00, 离开: 9:10
#   到达: 9:40, 离开: 12:00
#   到达: 9:50, 离开: 11:20
#   到达: 11:00, 离开: 11:30
#   到达: 15:00, 离开: 19:00
#   到达: 18:00, 离开: 20:00
#
# 最少需要 3 个站台

# 思路:
# 贪心策略：把到达和离开事件分别排序，用双指针模拟。
# 每次有火车到达时就+1站台，有火车离开时就-1站台。
# 记录过程中的最大值就是答案。
# 时间复杂度: O(n log n)，主要是排序时间
# 空间复杂度: O(1)，除了输入数组外只用常数额外空间
