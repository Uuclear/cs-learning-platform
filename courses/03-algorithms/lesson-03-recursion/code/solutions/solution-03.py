# 练习3解答：递归生成全排列

def permutations(lst):
    """
    递归生成列表的全排列
    思路: 遍历每个元素作为首元素，递归生成剩余元素的排列
    基准: 空列表或单元素列表，排列就是它自己
    
    时间复杂度: O(n!) —— n个元素有n!种排列
    空间复杂度: O(n!) —— 存储所有排列结果
    """
    # 基准情况：空列表
    if len(lst) == 0:
        return [[]]
    
    # 基准情况：单元素列表
    if len(lst) == 1:
        return [lst[:]]  # 返回拷贝
    
    result = []
    
    # 递归情况：每个元素都当一次"排头兵"
    for i in range(len(lst)):
        # 当前元素作为第一个
        current = lst[i]
        # 剩余元素
        rest = lst[:i] + lst[i+1:]
        # 递归生成剩余元素的全排列
        for perm in permutations(rest):
            result.append([current] + perm)
    
    return result


if __name__ == "__main__":
    print("=== 递归生成全排列 ===\n")
    
    print("--- [1, 2, 3] 的全排列 ---")
    perms = permutations([1, 2, 3])
    for i, p in enumerate(perms, 1):
        print(f"  {i}. {p}")
    print(f"  共 {len(perms)} 种排列 (3! = 6)")
    
    print()
    
    print("--- ['a', 'b'] 的全排列 ---")
    perms = permutations(['a', 'b'])
    for i, p in enumerate(perms, 1):
        print(f"  {i}. {p}")
    print(f"  共 {len(perms)} 种排列 (2! = 2)")
    
    print()
    
    print("--- [1, 2, 3, 4] 的全排列数量 ---")
    perms = permutations([1, 2, 3, 4])
    print(f"  共 {len(perms)} 种排列 (4! = 24)")

# 预期输出:
# === 递归生成全排列 ===
#
# --- [1, 2, 3] 的全排列 ---
#   1. [1, 2, 3]
#   2. [1, 3, 2]
#   3. [2, 1, 3]
#   4. [2, 3, 1]
#   5. [3, 1, 2]
#   6. [3, 2, 1]
#   共 6 种排列 (3! = 6)
#
# --- ['a', 'b'] 的全排列 ---
#   1. ['a', 'b']
#   2. ['b', 'a']
#   共 2 种排列 (2! = 2)
#
# --- [1, 2, 3, 4] 的全排列数量 ---
#   共 24 种排列 (4! = 24)
