# 挑战2：动态哈希表摊销分析 ⭐⭐⭐

## 问题描述

实现一个**动态哈希表**，支持自动扩容和缩容，并分析其插入和删除操作的摊销时间复杂度。

当哈希表的负载因子（元素数量/容量）超过 0.75 时自动扩容（容量翻倍），当负载因子低于 0.25 时自动缩容（容量减半，但不低于初始容量）。

## 输入/输出规格

### 类定义
```python
class DynamicHashTable:
    def __init__(self, initial_capacity=8):
        # 初始化哈希表
        pass
    
    def insert(self, key, value):
        # 插入键值对，如果key已存在则更新value
        pass
    
    def delete(self, key):
        # 删除指定key，返回被删除的value，如果key不存在返回None
        pass
    
    def search(self, key):
        # 查找指定key对应的value，如果不存在返回None
        pass
    
    def get_load_factor(self):
        # 返回当前负载因子
        pass
```

### 示例
```python
ht = DynamicHashTable()
ht.insert("name", "Alice")
ht.insert("age", 25)
print(ht.search("name"))      # 输出: Alice
print(ht.get_load_factor())   # 输出: 0.25 (2/8)

# 触发扩容
for i in range(10):
    ht.insert(f"key{i}", i)

print(ht.get_load_factor())   # 输出: 约0.46 (12/26，因为扩容到16后又插入)

# 触发缩容
for i in range(8):
    ht.delete(f"key{i}")

print(ht.get_load_factor())   # 输出: 约0.25 (4/16，可能触发缩容到8)
```

## 约束条件

- 使用开放寻址法（线性探测）解决冲突
- 初始容量为 8，必须是 2 的幂次
- 扩容阈值：负载因子 > 0.75
- 缩容阈值：负载因子 < 0.25 且当前容量 > 初始容量
- 所有操作的摊销时间复杂度应为 O(1)
- 必须正确处理哈希冲突和重新哈希

## 提示

1. **重新哈希**：扩容/缩容时需要将所有元素重新插入到新表中
2. **摊销分析**：类似于动态数组，但需要考虑删除操作
3. **势能函数**：可以定义为与负载因子偏离理想值的程度相关
4. **边界情况**：注意处理空表、单元素表等特殊情况

<details>
<summary>参考解决方案</summary>

```python
class DynamicHashTable:
    """
    支持自动扩容/缩容的动态哈希表
    使用开放寻址法（线性探测）解决冲突
    """
    
    def __init__(self, initial_capacity=8):
        if initial_capacity < 1:
            initial_capacity = 8
        # 确保容量是2的幂次
        self.capacity = 1 << (initial_capacity - 1).bit_length()
        if self.capacity < initial_capacity:
            self.capacity <<= 1
        
        self.table = [None] * self.capacity
        self.size = 0
        self.initial_capacity = self.capacity
    
    def _hash(self, key):
        """计算哈希值"""
        return hash(key) & (self.capacity - 1)
    
    def _find_slot(self, key):
        """找到key对应的槽位，返回(索引, 是否存在)"""
        index = self._hash(key)
        probes = 0
        
        while probes < self.capacity:
            slot = self.table[index]
            if slot is None:
                # 找到空槽
                return index, False
            elif slot[0] == key:
                # 找到key
                return index, True
            
            # 线性探测
            index = (index + 1) & (self.capacity - 1)
            probes += 1
        
        # 表已满（理论上不应该发生，因为负载因子限制）
        return -1, False
    
    def _resize(self, new_capacity):
        """重新调整哈希表大小"""
        old_table = self.table
        old_capacity = self.capacity
        
        self.capacity = new_capacity
        self.table = [None] * new_capacity
        self.size = 0
        
        # 重新插入所有元素
        for slot in old_table:
            if slot is not None:
                self.insert(slot[0], slot[1])
    
    def insert(self, key, value):
        """插入或更新键值对"""
        # 检查是否需要扩容
        if self.size >= self.capacity * 0.75:
            self._resize(self.capacity * 2)
        
        index, exists = self._find_slot(key)
        if exists:
            # 更新现有键
            self.table[index] = (key, value)
        else:
            # 插入新键
            self.table[index] = (key, value)
            self.size += 1
    
    def delete(self, key):
        """删除键值对"""
        index, exists = self._find_slot(key)
        if not exists:
            return None
        
        value = self.table[index][1]
        self.table[index] = None  # 标记为删除
        self.size -= 1
        
        # 检查是否需要缩容
        if (self.capacity > self.initial_capacity and 
            self.size < self.capacity * 0.25):
            self._resize(max(self.initial_capacity, self.capacity // 2))
        
        return value
    
    def search(self, key):
        """查找键对应的值"""
        index, exists = self._find_slot(key)
        if exists:
            return self.table[index][1]
        return None
    
    def get_load_factor(self):
        """获取负载因子"""
        return self.size / self.capacity if self.capacity > 0 else 0

# 摊销分析说明：
# - 插入操作：类似于动态数组，摊销O(1)
# - 删除操作：虽然可能触发缩容，但每个元素最多参与常数次重新哈希
# - 总体摊销时间复杂度为O(1)
```

</details>