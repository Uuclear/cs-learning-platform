# 练习3解答：猜数字游戏

import random
import math


def computer_guesses(n, target):
    """
    电脑猜玩家的数字（二分查找）
    """
    left = 1
    right = n
    guesses = 0

    while left <= right:
        guesses += 1
        mid = (left + right) // 2

        if mid == target:
            print(f"  电脑第{guesses}次猜: {mid} -> 对了！")
            return guesses
        elif mid < target:
            print(f"  电脑第{guesses}次猜: {mid} -> 小了")
            left = mid + 1
        else:
            print(f"  电脑第{guesses}次猜: {mid} -> 大了")
            right = mid - 1

    return guesses


def efficiency_comparison():
    """
    对比二分查找和线性查找的效率
    """
    print("\n--- 效率对比 ---\n")

    for n in [100, 1000, 10000, 1000000]:
        target = n  # 最坏情况：目标在最后
        binary = computer_guesses(n, target)
        linear = n
        max_binary = math.ceil(math.log2(n))
        print(f"\nN={n}:")
        print(f"  线性查找最坏: {linear} 次")
        print(f"  二分查找最坏: {max_binary} 次")
        print(f"  二分查找快了 {linear / max_binary:.0f} 倍")


if __name__ == "__main__":
    print("=== 猜数字游戏 ===\n")

    # 场景1：N=100，目标=73
    print("场景1: N=100，目标=73")
    guesses = computer_guesses(100, 73)
    print(f"电脑猜了 {guesses} 次")

    # 场景2：N=100，目标=50（第一次就猜中）
    print("\n场景2: N=100，目标=50（第一次就中）")
    guesses = computer_guesses(100, 50)
    print(f"电脑猜了 {guesses} 次")

    # 场景3：效率对比
    efficiency_comparison()

    # 验证理论值
    print("\n--- 理论验证 ---")
    print(f"N=100时，二分查找最多需要: {math.ceil(math.log2(100))} 次（2^7=128>100）")
    print(f"N=1,000,000时，二分查找最多需要: {math.ceil(math.log2(1000000))} 次")
    print(f"N=1,000,000时，线性查找最多需要: 1,000,000 次")
    print(f"二分查找比线性查找快: {1000000 / math.ceil(math.log2(1000000)):.0f} 倍！")
