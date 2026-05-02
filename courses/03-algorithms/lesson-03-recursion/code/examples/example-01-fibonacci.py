# 斐波那契数列：朴素递归 vs 记忆化递归
# 展示递归的力量和陷阱

def fibonacci_naive(n):
    """
    朴素递归实现斐波那契数列
    公式: F(n) = F(n-1) + F(n-2)
    基准: F(0)=0, F(1)=1
    
    时间复杂度: O(2^n) —— 指数级爆炸！
    """
    # 基准情况：前两项直接返回
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    # 递归情况：前两项之和
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memo(n, memo=None):
    """
    记忆化递归实现斐波那契数列
    用字典缓存已经算过的结果，避免重复计算
    
    时间复杂度: O(n) —— 从指数级降到线性！
    """
    # 初始化缓存字典
    if memo is None:
        memo = {}
    
    # 先查缓存：算过的直接拿来用
    if n in memo:
        return memo[n]
    
    # 基准情况
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    # 递归计算，并保存到缓存
    result = fibonacci_memo(n - 1, memo) + fibonacci_memo(n - 2, memo)
    memo[n] = result  # 记住这个结果
    
    return result


if __name__ == "__main__":
    print("=== 斐波那契数列 ===\n")
    
    # 朴素递归（小心！n太大会很慢）
    print("--- 朴素递归 O(2^n) ---")
    for i in range(10):
        print(f"  F({i}) = {fibonacci_naive(i)}")
    
    print()
    
    # 记忆化递归（快如闪电）
    print("--- 记忆化递归 O(n) ---")
    for i in range(15):
        print(f"  F({i}) = {fibonacci_memo(i)}")
    
    print()
    
    # 性能对比
    import time
    
    print("--- 性能对比：计算 F(35) ---")
    start = time.time()
    result1 = fibonacci_naive(35)
    t1 = time.time() - start
    print(f"  朴素递归: F(35) = {result1}, 耗时 {t1:.3f}s")
    
    start = time.time()
    result2 = fibonacci_memo(35)
    t2 = time.time() - start
    print(f"  记忆化递归: F(35) = {result2}, 耗时 {t2:.6f}s")
    print(f"  速度提升: {t1/t2:.0f} 倍！")

# 预期输出:
# === 斐波那契数列 ===
#
# --- 朴素递归 O(2^n) ---
#   F(0) = 0
#   F(1) = 1
#   F(2) = 1
#   F(3) = 2
#   F(4) = 3
#   F(5) = 5
#   F(6) = 8
#   F(7) = 13
#   F(8) = 21
#   F(9) = 34
#
# --- 记忆化递归 O(n) ---
#   F(0) = 0
#   F(1) = 1
#   F(2) = 1
#   F(3) = 2
#   F(4) = 3
#   F(5) = 5
#   F(6) = 8
#   F(7) = 13
#   F(8) = 21
#   F(9) = 34
#   F(10) = 55
#   F(11) = 89
#   F(12) = 144
#   F(13) = 233
#   F(14) = 377
#
# --- 性能对比：计算 F(35) ---
#   朴素递归: F(35) = 9227465, 耗时 0.852s
#   记忆化递归: F(35) = 9227465, 耗时 0.000012s
#   速度提升: 71000 倍！
