# 汉诺塔问题：递归的优雅典范
# n个盘子从源柱移到目标柱，借助辅助柱

move_count = 0  # 全局计数器


def hanoi(n, source, target, auxiliary):
    """
    汉诺塔递归解法
    参数:
        n: 盘子数量
        source: 源柱子（起始位置）
        target: 目标柱子（最终位置）
        auxiliary: 辅助柱子（中间借用）
    
    核心思路（三步走）:
        1. 把 n-1 个盘子从 source 移到 auxiliary（借助 target）
        2. 把最底下的最大盘子从 source 移到 target
        3. 把 n-1 个盘子从 auxiliary 移到 target（借助 source）
    """
    global move_count
    
    # 基准情况：只有一个盘子，直接移
    if n == 1:
        move_count += 1
        print(f"  第{move_count}步: {source} -> {target}  (移动盘子1)")
        return
    
    # 递归情况：三步走
    
    # 第一步：把上面 n-1 个盘子移到辅助柱
    hanoi(n - 1, source, auxiliary, target)
    
    # 第二步：把最底下的盘子移到目标柱
    move_count += 1
    print(f"  第{move_count}步: {source} -> {target}  (移动盘子{n})")
    
    # 第三步：把 n-1 个盘子从辅助柱移到目标柱
    hanoi(n - 1, auxiliary, target, source)


if __name__ == "__main__":
    print("=== 汉诺塔问题 ===\n")
    
    print("--- 3个盘子 ---")
    move_count = 0
    hanoi(3, 'A', 'C', 'B')
    print(f"  总共移动 {move_count} 步 (2^3 - 1 = 7)")
    
    print()
    
    print("--- 4个盘子 ---")
    move_count = 0
    hanoi(4, 'A', 'C', 'B')
    print(f"  总共移动 {move_count} 步 (2^4 - 1 = 15)")
    
    print()
    
    # 步数规律
    print("--- 步数规律 ---")
    for n in range(1, 7):
        moves = 2 ** n - 1
        print(f"  {n}个盘子需要 {moves} 步")

# 预期输出:
# === 汉诺塔问题 ===
#
# --- 3个盘子 ---
#   第1步: A -> C  (移动盘子1)
#   第2步: A -> B  (移动盘子2)
#   第3步: C -> B  (移动盘子1)
#   第4步: A -> C  (移动盘子3)
#   第5步: B -> A  (移动盘子1)
#   第6步: B -> C  (移动盘子2)
#   第7步: A -> C  (移动盘子1)
#   总共移动 7 步 (2^3 - 1 = 7)
#
# --- 4个盘子 ---
#   第1步: A -> B  (移动盘子1)
#   第2步: A -> C  (移动盘子2)
#   第3步: B -> C  (移动盘子1)
#   第4步: A -> B  (移动盘子3)
#   第5步: C -> A  (移动盘子1)
#   第6步: C -> B  (移动盘子2)
#   第7步: A -> B  (移动盘子1)
#   第8步: A -> C  (移动盘子4)
#   第9步: B -> C  (移动盘子1)
#   第10步: B -> A  (移动盘子2)
#   第11步: C -> A  (移动盘子1)
#   第12步: B -> C  (移动盘子3)
#   第13步: A -> B  (移动盘子1)
#   第14步: A -> C  (移动盘子2)
#   第15步: B -> C  (移动盘子1)
#   总共移动 15 步 (2^4 - 1 = 15)
#
# --- 步数规律 ---
#   1个盘子需要 1 步
#   2个盘子需要 3 步
#   3个盘子需要 7 步
#   4个盘子需要 15 步
#   5个盘子需要 31 步
#   6个盘子需要 63 步
