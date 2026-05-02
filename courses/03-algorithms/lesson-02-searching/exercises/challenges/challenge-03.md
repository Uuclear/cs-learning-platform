# 挑战3: 旋转有序数组查找

### 难度
⭐⭐⭐

### 描述
一个升序排列的数组在某个未知的点被"旋转"了。例如：
- 原始数组: [0, 1, 2, 4, 5, 6, 7]
- 在索引3处旋转后: [4, 5, 6, 7, 0, 1, 2]

旋转后的数组仍然保持"部分有序"——至少有一边是有序的。请你在这个旋转后的有序数组中查找目标值。

**注意：不能使用线性查找！请利用二分查找的思想在O(log n)时间内完成。**

### 输入
- `nums`: 整数列表，一个在未知位置旋转过一次的原升序数组
- `target`: 整数，要查找的目标值

### 输出
- 返回目标值在数组中的索引，如果不存在返回-1

### 示例

**示例 1:**
```
输入: nums = [4, 5, 6, 7, 0, 1, 2], target = 0
输出: 4
解释: 0在索引4的位置
```

**示例 2:**
```
输入: nums = [4, 5, 6, 7, 0, 1, 2], target = 3
输出: -1
解释: 3不在数组中
```

**示例 3:**
```
输入: nums = [1], target = 0
输出: -1
解释: 单元素数组
```

### 约束条件
- 1 <= 数组长度 <= 10000
- 数组中无重复元素
- -10000 <= nums[i], target <= 10000

### 提示
- 虽然数组被旋转了，但每次二分后至少有一边是有序的
- 先判断mid的左边还是右边是有序的
- 如果目标值在有序的那一边的范围内，就在该边查找
- 否则在另一边查找

### 进阶思考
- 如果数组中有重复元素，这个算法还适用吗？为什么？
- 这道题的核心思想是什么？它如何体现了二分查找的灵活性？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
这是二分查找的经典变体题。核心思路是：虽然数组旋转了，但每次取mid后，至少有一边是有序的。

1. 计算mid = (left + right) // 2
2. 如果nums[mid] == target，找到了
3. 判断哪一边有序：如果nums[left] <= nums[mid]，左边有序
4. 如果target在有序的那一边的范围内（nums[left] <= target < nums[mid]），去左边找
5. 否则去另一边找

### 代码
```python
def search_rotated(nums, target):
    """
    在旋转有序数组中查找目标值
    使用二分查找的变体，O(log n)时间复杂度
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        # 找到了
        if nums[mid] == target:
            return mid

        # 判断左边是否有序
        if nums[left] <= nums[mid]:
            # 左边有序
            if nums[left] <= target < nums[mid]:
                # 目标在左边的有序部分中
                right = mid - 1
            else:
                # 目标在右边
                left = mid + 1
        else:
            # 右边有序
            if nums[mid] < target <= nums[right]:
                # 目标在右边的有序部分中
                left = mid + 1
            else:
                # 目标在左边
                right = mid - 1

    return -1


# 测试
if __name__ == "__main__":
    print("=== 旋转有序数组查找 ===\n")

    # 测试1：常规情况
    nums = [4, 5, 6, 7, 0, 1, 2]
    print(f"数组: {nums}")
    print(f"查找 0: 索引={search_rotated(nums, 0)}")  # 输出: 4
    print(f"查找 3: 索引={search_rotated(nums, 3)}")  # 输出: -1
    print(f"查找 6: 索引={search_rotated(nums, 6)}")  # 输出: 2
    print()

    # 测试2：没有旋转的情况
    nums2 = [1, 2, 3, 4, 5, 6, 7]
    print(f"数组: {nums2}")
    print(f"查找 4: 索引={search_rotated(nums2, 4)}")  # 输出: 3
    print(f"查找 8: 索引={search_rotated(nums2, 8)}")  # 输出: -1
    print()

    # 测试3：单元素数组
    nums3 = [1]
    print(f"数组: {nums3}")
    print(f"查找 1: 索引={search_rotated(nums3, 1)}")  # 输出: 0
    print(f"查找 0: 索引={search_rotated(nums3, 0)}")  # 输出: -1
    print()

    # 测试4：旋转点在第一个元素
    nums4 = [5, 1, 3]
    print(f"数组: {nums4}")
    print(f"查找 5: 索引={search_rotated(nums4, 5)}")  # 输出: 0
    print(f"查找 3: 索引={search_rotated(nums4, 3)}")  # 输出: 2
```

### 复杂度分析
- 时间复杂度: O(log n)，每次缩小一半搜索范围，和普通二分查找一样
- 空间复杂度: O(1)，只需要几个变量

</details>
