# 找零钱问题 - 贪心算法及其失败示例
# 问题：给定一些面值的硬币，找零时如何用最少数量的硬币？

# 贪心策略：每次都选面值最大的、不超过剩余金额的硬币

def coin_change_greedy(coins, amount):
    """
    找零钱 - 贪心算法
    参数: coins - 硬币面值列表（从大到小排序）
          amount - 需要找零的金额
    返回: 使用的硬币列表，如果无法找零返回None
    """
    # 从大到小排序
    coins_sorted = sorted(coins, reverse=True)
    result = []
    remaining = amount

    for coin in coins_sorted:
        # 尽可能多地使用当前最大面值硬币
        while remaining >= coin:
            result.append(coin)
            remaining -= coin

    # 如果还有剩余金额，说明无法完全找零
    if remaining > 0:
        return None
    return result


def coin_change_dp(coins, amount):
    """
    找零钱 - 动态规划（求最优解）
    参数: coins - 硬币面值列表
          amount - 需要找零的金额
    返回: 最少硬币数量，如果无法找零返回-1
    """
    # dp[i] 表示凑齐金额 i 需要的最少硬币数
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 凑齐0元需要0个硬币

    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


if __name__ == "__main__":
    # 场景1：贪心算法成功的情况（美国硬币系统：1, 5, 10, 25）
    print("=== 场景1：美国硬币系统（贪心正确）===")
    us_coins = [25, 10, 5, 1]
    amount1 = 63
    result1 = coin_change_greedy(us_coins, amount1)
    dp_result1 = coin_change_dp(us_coins, amount1)
    print(f"金额: {amount1} 分")
    print(f"贪心解法: {result1} (共 {len(result1)} 个硬币)")
    print(f"最优解法: 需要 {dp_result1} 个硬币")
    print(f"结论: {'贪心正确！' if len(result1) == dp_result1 else '贪心错误！'}")

    print()

    # 场景2：贪心算法失败的情况（特殊硬币系统：1, 3, 4）
    print("=== 场景2：特殊硬币系统（贪心失败）===")
    special_coins = [4, 3, 1]
    amount2 = 6
    result2 = coin_change_greedy(special_coins, amount2)
    dp_result2 = coin_change_dp(special_coins, amount2)
    print(f"金额: {amount2} 分")
    print(f"贪心解法: {result2} (共 {len(result2)} 个硬币)")
    print(f"最优解法: 需要 {dp_result2} 个硬币")
    print(f"结论: {'贪心正确！' if len(result2) == dp_result2 else '贪心失败！'}")
    print("  贪心: 4+1+1 = 3个硬币")
    print("  最优: 3+3 = 2个硬币")

# 输出:
# === 场景1：美国硬币系统（贪心正确）===
# 金额: 63 分
# 贪心解法: [25, 25, 10, 1, 1, 1] (共 6 个硬币)
# 最优解法: 需要 6 个硬币
# 结论: 贪心正确！
#
# === 场景2：特殊硬币系统（贪心失败）===
# 金额: 6 分
# 贪心解法: [4, 1, 1] (共 3 个硬币)
# 最优解法: 需要 2 个硬币
# 结论: 贪心失败！
#   贪心: 4+1+1 = 3个硬币
#   最优: 3+3 = 2个硬币
