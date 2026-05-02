# 挑战1：两数之和

## 难度
⭐

## 描述

给定一个整数数组 `nums` 和一个整数目标值 `target`，请你在该数组中找出**和为目标值**的那**两个**整数，并返回它们的**数组下标**。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

## 输入

- `nums`: 整数数组，长度范围 [2, 10^4]
- `target`: 整数目标值，范围 [-10^9, 10^9]

## 输出

返回两个整数的索引（从0开始），以列表形式 `[index1, index2]` 返回。

## 示例

**示例 1:**
```
输入: nums = [2, 7, 11, 15], target = 9
输出: [0, 1]
解释: 因为 nums[0] + nums[1] == 2 + 7 == 9
```

**示例 2:**
```
输入: nums = [3, 2, 4], target = 6
输出: [1, 2]
解释: 因为 nums[1] + nums[2] == 2 + 4 == 6
```

**示例 3:**
```
输入: nums = [3, 3], target = 6
输出: [0, 1]
```

## 约束条件

- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- 只会存在一个有效答案

## 提示

- 暴力解法：遍历所有可能的组合，时间复杂度 O(n²)
- 优化思路：使用哈希表（字典）存储已经遍历过的数字，时间复杂度 O(n)
- 思考：如果数组已经排序，能否用双指针法？

## 进阶思考

1. 如果数组是有序的，如何优化？
2. 如果要求找出所有满足条件的数对（不止一个答案），代码需要如何修改？
3. 时间复杂度和空间复杂度如何权衡？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

**解法1：暴力枚举（适合初学者理解）**
- 使用两层循环，枚举所有可能的数对
- 外层循环遍历第一个数，内层循环遍历第二个数
- 如果两数之和等于target，返回它们的索引

**解法2：哈希表优化（推荐）**
- 遍历数组时，用字典记录每个数的索引
- 对于当前数 `num`，检查 `target - num` 是否在字典中
- 如果在，说明找到了答案；如果不在，把当前数加入字典

### 代码

```python
# 解法1：暴力枚举
# 时间复杂度: O(n²)
# 空间复杂度: O(1)
def two_sum_brute_force(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# 解法2：哈希表优化
# 时间复杂度: O(n)
# 空间复杂度: O(n)
def two_sum_hash(nums, target):
    # key: 数字, value: 索引
    num_to_index = {}
    
    for i, num in enumerate(nums):
        complement = target - num  # 需要找的另一个数
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    
    return []


# 测试
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
    ]
    
    for nums, target, expected in test_cases:
        result = two_sum_hash(nums, target)
        print(f"nums={nums}, target={target}")
        print(f"结果: {result}, 期望: {expected}")
        assert result == expected, "测试失败！"
        print("✅ 通过\n")
```

### 复杂度分析

| 解法 | 时间复杂度 | 空间复杂度 | 说明 |
|------|-----------|-----------|------|
| 暴力枚举 | O(n²) | O(1) | 简单直接，但效率低 |
| 哈希表 | O(n) | O(n) | 用空间换时间，推荐 |

</details>
