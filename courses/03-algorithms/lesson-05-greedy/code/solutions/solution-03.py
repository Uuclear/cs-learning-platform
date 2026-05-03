#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪心算法解决方案 03: 找零钱问题（贪心方法）
注意：贪心方法在某些硬币系统下不能得到最优解
"""

def coin_change_greedy(coins, amount):
    """
    找零钱 - 贪心算法

    参数:
        coins: 硬币面值列表
        amount: 需要找零的金额

    返回:
        使用的硬币列表，如果无法完全找零返回None
    """
    # 按面值从大到小排序
    coins_sorted = sorted(coins, reverse=True)
    result = []
    remaining = amount

    for coin in coins_sorted:
        # 尽可能多地使用当前面值的硬币
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

    参数:
        coins: 硬币面值列表
        amount: 需要找零的金额

    返回:
        最少硬币数量，如果无法找零返回-1
    """
    # dp[i] 表示凑出金额i所需的最少硬币数
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 凑0元需要0个硬币

    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def compare_greedy_vs_dp(coins, amount):
    """
    比较贪心算法和动态规划的结果

    参数:
        coins: 硬币面值列表
        amount: 需要找零的金额

    返回:
        贪心结果、DP结果和比较信息
    """
    greedy_result = coin_change_greedy(coins, amount)
    dp_result = coin_change_dp(coins, amount)

    comparison = {
        'coins': coins,
        'amount': amount,
        'greedy_coins': greedy_result,
        'greedy_count': len(greedy_result) if greedy_result else None,
        'dp_count': dp_result,
        'is_optimal': False
    }

    if greedy_result is not None and dp_result != -1:
        comparison['is_optimal'] = (len(greedy_result) == dp_result)

    return comparison


def main():
    """主函数：演示找零钱问题中贪心算法的适用性和局限性"""
    print("=== 找零钱问题贪心算法实现 ===\n")

    # 场景1：美国硬币系统 [25, 10, 5, 1] - 贪心正确
    print("1. 美国硬币系统（贪心正确）:")
    us_coins = [25, 10, 5, 1]
    amount1 = 63

    comparison1 = compare_greedy_vs_dp(us_coins, amount1)
    print(f"   硬币面值: {us_coins}")
    print(f"   找零金额: {amount1} 分")
    print(f"   贪心结果: {comparison1['greedy_coins']} (共 {comparison1['greedy_count']} 个)")
    print(f"   最优结果: {comparison1['dp_count']} 个")
    print(f"   贪心是否最优: {'✓' if comparison1['is_optimal'] else '✗'}\n")

    # 场景2：特殊硬币系统 [4, 3, 1] - 贪心失败
    print("2. 特殊硬币系统（贪心失败）:")
    special_coins = [4, 3, 1]
    amount2 = 6

    comparison2 = compare_greedy_vs_dp(special_coins, amount2)
    print(f"   硬币面值: {special_coins}")
    print(f"   找零金额: {amount2}")
    print(f"   贪心结果: {comparison2['greedy_coins']} (共 {comparison2['greedy_count']} 个)")
    print(f"   最优结果: {comparison2['dp_count']} 个")
    print(f"   贪心是否最优: {'✓' if comparison2['is_optimal'] else '✗'}")
    print(f"   最优方案: 3 + 3 = {amount2} (2个硬币)\n")

    # 场景3：欧元硬币系统 [200, 100, 50, 20, 10, 5, 2, 1] - 贪心正确
    print("3. 欧元硬币系统（贪心正确）:")
    euro_coins = [200, 100, 50, 20, 10, 5, 2, 1]  # 单位：欧分
    amount3 = 387  # 3.87欧元

    comparison3 = compare_greedy_vs_dp(euro_coins, amount3)
    print(f"   硬币面值: {euro_coins}")
    print(f"   找零金额: {amount3} 欧分 ({amount3/100:.2f} 欧元)")
    print(f"   贪心结果: {comparison3['greedy_coins']} (共 {comparison3['greedy_count']} 个)")
    print(f"   最优结果: {comparison3['dp_count']} 个")
    print(f"   贪心是否最优: {'✓' if comparison3['is_optimal'] else '✗'}\n")

    # 场景4：无法找零的情况
    print("4. 无法找零的情况:")
    limited_coins = [5, 10]  # 只有5和10分硬币
    amount4 = 7  # 需要找7分

    greedy_result4 = coin_change_greedy(limited_coins, amount4)
    dp_result4 = coin_change_dp(limited_coins, amount4)

    print(f"   硬币面值: {limited_coins}")
    print(f"   找零金额: {amount4}")
    print(f"   贪心结果: {greedy_result4}")
    print(f"   DP结果: {dp_result4}")
    print(f"   是否可找零: {'✗' if greedy_result4 is None else '✓'}\n")

    # 总结
    print("=== 总结 ===")
    print("贪心算法在找零钱问题中的表现取决于硬币系统的性质：")
    print("- 在标准货币系统（如美元、欧元）中，贪心算法通常能得到最优解")
    print("- 在特殊设计的硬币系统中，贪心算法可能无法得到最优解")
    print("- 当无法完全找零时，两种方法都会失败")
    print("\n关键教训：使用贪心算法前，必须验证其在特定问题上的正确性！")


if __name__ == "__main__":
    main()