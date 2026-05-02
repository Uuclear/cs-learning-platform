# ============================================
# 解答1：两数之和
# 使用哈希表在O(n)时间内解决
# ============================================

def two_sum(nums, target):
    """
    使用哈希表在O(n)时间内找到两数之和
    核心思路：遍历数组，对于每个数num
    检查 target-num 是否已在哈希表中
    """
    seen = {}  # 哈希表：值 → 索引
    for i, num in enumerate(nums):
        complement = target - num  # 我们要找的另一半
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i  # 记录当前数和它的索引
    return []  # 题目保证有解，理论上不会走到这里


# 测试
if __name__ == "__main__":
    print("=== 两数之和 ===")
    
    result1 = two_sum([2, 7, 11, 15], 9)
    print(f"nums = [2, 7, 11, 15], target = 9")
    print(f"结果: {result1}  (nums[{result1[0]}] + nums[{result1[1]}] = 2 + 7 = 9)")
    print()
    
    result2 = two_sum([3, 2, 4], 6)
    print(f"nums = [3, 2, 4], target = 6")
    print(f"结果: {result2}  (nums[{result2[0]}] + nums[{result2[1]}] = 2 + 4 = 6)")
    print()
    
    result3 = two_sum([3, 3], 6)
    print(f"nums = [3, 3], target = 6")
    print(f"结果: {result3}  (nums[{result3[0]}] + nums[{result3[1]}] = 3 + 3 = 6)")

# 输出:
# === 两数之和 ===
# nums = [2, 7, 11, 15], target = 9
# 结果: [0, 1]  (nums[0] + nums[1] = 2 + 7 = 9)
#
# nums = [3, 2, 4], target = 6
# 结果: [1, 2]  (nums[1] + nums[2] = 2 + 4 = 6)
#
# nums = [3, 3], target = 6
# 结果: [0, 1]  (nums[0] + nums[1] = 3 + 3 = 6)
