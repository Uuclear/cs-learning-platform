## 挑战1: 两数之和

### 难度
⭐

### 描述
给定一个整数数组和一个目标值，找出数组中两个数，使它们的和等于目标值。返回这两个数的索引。

这是LeetCode第1题，使用哈希表可以在O(n)时间内优雅解决。

### 输入
- 一个整数列表 `nums`
- 一个整数 `target`

### 输出
- 包含两个整数索引的列表

### 示例

**示例 1:**
```
输入: nums = [2, 7, 11, 15], target = 9
输出: [0, 1]
解释: nums[0] + nums[1] = 2 + 7 = 9
```

**示例 2:**
```
输入: nums = [3, 2, 4], target = 6
输出: [1, 2]
解释: nums[1] + nums[2] = 2 + 4 = 6
```

### 约束条件
- 2 <= len(nums) <= 1000
- 每组输入恰好有一个答案
- 不能重复使用同一个元素
- -10^9 <= nums[i] <= 10^9

### 提示
- 不要使用两层循环（O(n²)），试试用哈希表存储"值→索引"的映射
- 遍历数组时，对每个数num，检查(target - num)是否已在哈希表中

### 进阶思考
- 如果数组是已排序的，还有更优解法吗？

---

## 挑战2: 字母异位词分组

### 难度
⭐⭐

### 描述
给定一个字符串数组，将字母异位词（包含相同字母但排列不同的词）分在一组。

### 输入
- 一个字符串列表 `strs`

### 输出
- 一个二维列表，每个子列表包含一组字母异位词

### 示例

**示例 1:**
```
输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
解释: "eat"/"tea"/"ate"是异位词，"tan"/"nat"是异位词
```

**示例 2:**
```
输入: strs = [""]
输出: [[""]]
```

### 约束条件
- 1 <= len(strs) <= 100
- 0 <= len(strs[i]) <= 100
- strs[i] 只包含小写字母

### 提示
- 字母异位词排序后是相同的字符串
- 可以用"排序后的字符串"作为哈希表的Key

### 进阶思考
- 不用排序，用字符计数数组作为Key会更高效吗？

---

## 挑战3: LRU缓存

### 难度
⭐⭐⭐

### 描述
实现一个LRU（Least Recently Used，最近最少使用）缓存。它具有固定容量，当容量满了时，淘汰最久没有访问过的元素。

### 输入
- 缓存容量 `capacity`（正整数）
- 操作序列：`get(key)` 和 `put(key, value)`

### 输出
- `get(key)`：返回key对应的值，不存在返回-1
- `put(key, value)`：无返回值

### 示例
```
LRUCache cache = LRUCache(2)

cache.put(1, 1)      # 缓存: {1=1}
cache.put(2, 2)      # 缓存: {1=1, 2=2}
cache.get(1)         # 返回 1，缓存: {2=2, 1=1}
cache.put(3, 3)      # 淘汰2，缓存: {1=1, 3=3}
cache.get(2)         # 返回 -1（2已被淘汰）
cache.put(4, 4)      # 淘汰1，缓存: {3=3, 4=4}
cache.get(1)         # 返回 -1
cache.get(3)         # 返回 3
cache.get(4)         # 返回 4
```

### 约束条件
- 1 <= capacity <= 3000
- 0 <= key <= 10000
- 0 <= value <= 10^5
- get和put操作总次数不超过20000
- **get和put都必须是O(1)时间复杂度**

### 提示
- 需要两个数据结构配合：哈希表（O(1)查找）+ 双向链表（O(1)移动节点）
- 双向链表头部放"最近使用"节点，尾部放"最久未用"节点
- Python可以用`collections.OrderedDict`来简化实现

### 进阶思考
- 如果不允许使用OrderedDict，如何纯手工实现双向链表+哈希表的组合？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 挑战1思路

遍历数组，用哈希表记录"值→索引"的映射。对每个数num，先检查target-num是否已在表中。

### 挑战1代码
```python
def two_sum(nums, target):
    """
    使用哈希表在O(n)时间内找到两数之和
    """
    seen = {}  # 哈希表：值 → 索引
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []  # 理论上不会走到这里（题目保证有解）

# 测试
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
print(two_sum([3, 3], 6))           # [0, 1]
```

### 挑战1复杂度
- 时间复杂度: O(n)，只遍历一次
- 空间复杂度: O(n)，哈希表最多存储n个元素

---

### 挑战2思路

字母异位词排序后相同。用排序后的字符串作为Key，将原词append到对应的列表中。

### 挑战2代码
```python
def group_anagrams(strs):
    """
    将字母异位词分组
    使用排序后的字符串作为哈希表的Key
    """
    groups = {}
    for s in strs:
        # 排序后的字符串作为Key
        sorted_key = "".join(sorted(s))
        if sorted_key not in groups:
            groups[sorted_key] = []
        groups[sorted_key].append(s)
    return list(groups.values())

# 测试
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]

print(group_anagrams([""]))
# [['']]

print(group_anagrams(["a"]))
# [['a']]
```

### 挑战2复杂度
- 时间复杂度: O(n × k log k)，n是字符串数量，k是最长字符串长度（排序开销）
- 空间复杂度: O(n × k)，存储所有字符串

---

### 挑战3思路

哈希表提供O(1)查找，双向链表提供O(1)移动。链表头部是"最近使用"，尾部是"最久未用"。Python简化版用OrderedDict。

### 挑战3代码（OrderedDict简化版）
```python
from collections import OrderedDict

class LRUCache:
    """
    LRU缓存实现
    使用OrderedDict：它内部 = 哈希表 + 双向链表
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        # 标记为最近使用（移到末尾）
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # 已存在，更新并标记为最近使用
            self.cache.move_to_end(key)
        self.cache[key] = value

        # 超出容量，淘汰最久未用的（第一个元素）
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# 测试
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(f"get(1): {cache.get(1)}")  # 1
cache.put(3, 3)  # 淘汰2
print(f"get(2): {cache.get(2)}")  # -1
cache.put(4, 4)  # 淘汰1
print(f"get(1): {cache.get(1)}")  # -1
print(f"get(3): {cache.get(3)}")  # 3
print(f"get(4): {cache.get(4)}")  # 4
```

### 挑战3复杂度
- 时间复杂度: O(1) for both get and put
- 空间复杂度: O(capacity)，最多存储capacity个元素

</details>
