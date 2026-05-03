#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：Miller-Rabin素性测试

这个文件实现了Miller-Rabin素性测试算法，演示了Monte Carlo
随机算法的特点和错误概率分析。
"""

import random
import time

def miller_rabin_witness(a, n, d, r):
    """
    Miller-Rabin见证者测试

    Args:
        a (int): 测试底数
        n (int): 要测试的数
        d (int): n-1 = d * 2^r 中的d
        r (int): n-1 = d * 2^r 中的r

    Returns:
        bool: 如果a是n的见证者返回True（n是合数），否则返回False
    """
    # 计算 a^d mod n
    x = pow(a, d, n)

    # 如果 x == 1 或 x == n-1，则a不是见证者
    if x == 1 or x == n - 1:
        return False

    # 检查 x^(2^i) mod n 是否等于 n-1
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return False

    # 如果都没有找到n-1，则a是见证者
    return True

def miller_rabin_test(n, k=5):
    """
    Miller-Rabin素性测试主函数

    Args:
        n (int): 要测试的数
        k (int): 测试轮数

    Returns:
        tuple: (是否可能是素数, 详细信息字典)
    """
    if n < 2:
        return False, {'error': 'n < 2'}

    if n == 2 or n == 3:
        return True, {'trivial': True}

    if n % 2 == 0:
        return False, {'even': True}

    # 分解 n-1 = d * 2^r
    r = 0
    d = n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    witnesses_found = 0
    tested_bases = []

    # 进行k轮测试
    for i in range(k):
        # 随机选择底数 a ∈ [2, n-2]
        a = random.randint(2, n - 2)
        tested_bases.append(a)

        is_witness = miller_rabin_witness(a, n, d, r)
        if is_witness:
            witnesses_found += 1
            break  # 找到一个见证者就足够证明是合数

    is_probably_prime = witnesses_found == 0
    error_probability = 1 / (4 ** min(k, witnesses_found + (0 if is_probably_prime else 1)))

    details = {
        'decomposition': f"{n-1} = {d} * 2^{r}",
        'tested_bases': tested_bases,
        'witnesses_found': witnesses_found,
        'error_probability': error_probability,
        'rounds': min(k, witnesses_found + (0 if is_probably_prime else 1))
    }

    return is_probably_prime, details

def naive_primality_test(n):
    """
    朴素素性测试（用于小数字验证）

    Args:
        n (int): 要测试的数

    Returns:
        bool: 如果n是素数返回True
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def test_miller_rabin():
    """测试Miller-Rabin算法"""
    print("=== Miller-Rabin素性测试演示 ===\n")

    # 测试用例：包含素数、合数、Carmichael数等
    test_numbers = [
        17,           # 小素数
        97,           # 较大素数
        561,          # Carmichael数（费马测试会失败，但Miller-Rabin能检测）
        1105,         # 另一个Carmichael数
        1009,         # 素数
        2047,         # 2^11 - 1 = 23 * 89（合数）
        982451653,    # 大素数
        982451654,    # 大合数
    ]

    for num in test_numbers:
        print(f"测试数字: {num}")

        # Miller-Rabin测试
        start_time = time.time()
        is_probable_prime, details = miller_rabin_test(num, k=10)
        end_time = time.time()

        # 对于小数字，用朴素方法验证
        actual_is_prime = None
        if num < 1000000:
            actual_is_prime = naive_primality_test(num)

        print(f"  分解: {details['decomposition']}")
        print(f"  测试底数: {details['tested_bases'][:3]}{'...' if len(details['tested_bases']) > 3 else ''}")
        print(f"  结果: {'可能是素数' if is_probable_prime else '是合数'}")
        print(f"  错误概率: {details['error_probability']:.2e}")
        print(f"  实际结果: {actual_is_prime if actual_is_prime is not None else '未知'}")
        print(f"  测试时间: {end_time - start_time:.6f}s")
        print()

def analyze_error_probability():
    """分析错误概率"""
    print("=== 错误概率分析 ===\n")

    k_values = [1, 2, 3, 5, 10, 20]

    print("理论错误概率上限:")
    for k in k_values:
        error_prob = 1 / (4 ** k)
        print(f"  k={k:2d}: {error_prob:.2e}")

    print("\n实际测试（对已知合数）:")
    composite_numbers = [561, 1105, 1729, 2465, 2821]

    for num in composite_numbers:
        print(f"\n合数 {num}:")
        for k in [1, 3, 5]:
            false_positive_count = 0
            trials = 100

            for _ in range(trials):
                is_probable_prime, _ = miller_rabin_test(num, k=k)
                if is_probable_prime:
                    false_positive_count += 1

            empirical_error = false_positive_count / trials
            theoretical_error = 1 / (4 ** k)

            print(f"  k={k}: 经验错误率={empirical_error:.3f}, 理论上限={theoretical_error:.3f}")

def main():
    """主函数"""
    test_miller_rabin()
    analyze_error_probability()

if __name__ == "__main__":
    main()

# 预期输出示例:
# === Miller-Rabin素性测试演示 ===
#
# 测试数字: 17
#   分解: 16 = 1 * 2^4
#   测试底数: [5, 12, 3...]
#   结果: 可能是素数
#   错误概率: 9.54e-07
#   实际结果: True
#   测试时间: 0.000012s