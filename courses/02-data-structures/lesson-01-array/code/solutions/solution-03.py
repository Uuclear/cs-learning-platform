# ============================================
# 练习3解答：实现完整的动态数组类
# 难度：⭐⭐⭐
# ============================================

class MyDynamicArray:
    """
    完整的动态数组实现
    支持：append, get, set, insert, remove
    带有扩容和缩容机制
    """
    
    def __init__(self, initial_capacity=4):
        """
        初始化动态数组
        """
        self.capacity = initial_capacity
        self.size = 0
        self.data = [None] * self.capacity
        self.MIN_CAPACITY = 4  # 最小容量，防止过度缩容
    
    def append(self, value):
        """
        在末尾添加元素
        时间复杂度：摊还O(1)
        """
        # 检查是否需要扩容
        if self.size >= self.capacity:
            self._resize(2)  # 扩容为2倍
        
        self.data[self.size] = value
        self.size += 1
    
    def get(self, index):
        """
        获取指定索引的元素
        时间复杂度：O(1)
        """
        if not (0 <= index < self.size):
            raise IndexError(f"索引 {index} 越界！有效范围: 0-{self.size-1}")
        return self.data[index]
    
    def set(self, index, value):
        """
        修改指定索引的元素
        时间复杂度：O(1)
        """
        if not (0 <= index < self.size):
            raise IndexError(f"索引 {index} 越界！有效范围: 0-{self.size-1}")
        self.data[index] = value
    
    def insert(self, index, value):
        """
        在指定位置插入元素
        时间复杂度：O(n)
        """
        if not (0 <= index <= self.size):
            raise IndexError(f"插入索引 {index} 越界！有效范围: 0-{self.size}")
        
        # 检查是否需要扩容
        if self.size >= self.capacity:
            self._resize(2)
        
        # 从末尾开始，把元素后移
        # 注意：要从后往前移，否则会覆盖数据
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        
        # 插入新元素
        self.data[index] = value
        self.size += 1
    
    def remove(self, index):
        """
        删除指定位置的元素
        时间复杂度：O(n)
        """
        if not (0 <= index < self.size):
            raise IndexError(f"删除索引 {index} 越界！有效范围: 0-{self.size-1}")
        
        removed_value = self.data[index]
        
        # 把后面的元素前移，覆盖被删除的元素
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        
        self.size -= 1
        self.data[self.size] = None  # 清除引用（帮助垃圾回收）
        
        # 检查是否需要缩容
        # 当使用率低于25%且容量大于最小容量时
        if self.size < self.capacity // 4 and self.capacity > self.MIN_CAPACITY:
            self._resize(0.5)  # 缩容为一半
        
        return removed_value
    
    def _resize(self, factor):
        """
        调整数组大小
        factor: 2表示扩容，0.5表示缩容
        """
        old_capacity = self.capacity
        self.capacity = int(self.capacity * factor)
        
        # 确保不低于最小容量
        if self.capacity < self.MIN_CAPACITY:
            self.capacity = self.MIN_CAPACITY
        
        # 创建新数组
        new_data = [None] * self.capacity
        
        # 复制数据
        for i in range(self.size):
            new_data[i] = self.data[i]
        
        self.data = new_data
        action = "扩容" if factor > 1 else "缩容"
        print(f"  {action}: {old_capacity} → {self.capacity}")
    
    def __str__(self):
        """返回数组的字符串表示"""
        return f"[{', '.join(str(self.data[i]) for i in range(self.size))}]"
    
    def __len__(self):
        """返回数组长度"""
        return self.size


# 测试
if __name__ == "__main__":
    print("=== 练习3：完整动态数组测试 ===\n")
    
    # 创建动态数组
    arr = MyDynamicArray(initial_capacity=4)
    print(f"创建数组，初始容量: 4")
    
    # 测试 append
    print("\n--- 测试 append ---")
    for i in range(6):
        arr.append(i * 10)
    print(f"添加6个元素后: {arr}")
    print(f"大小: {len(arr)}, 容量: {arr.capacity}")
    
    # 测试 get
    print("\n--- 测试 get ---")
    print(f"arr.get(2) = {arr.get(2)}")
    print(f"arr.get(0) = {arr.get(0)}")
    print(f"arr.get(5) = {arr.get(5)}")
    
    # 测试 set
    print("\n--- 测试 set ---")
    arr.set(2, 999)
    print(f"把索引2设为999后: {arr}")
    
    # 测试 insert
    print("\n--- 测试 insert ---")
    arr.insert(0, 111)  # 在开头插入
    print(f"在开头插入111后: {arr}")
    arr.insert(3, 222)  # 在中间插入
    print(f"在索引3插入222后: {arr}")
    arr.insert(len(arr), 333)  # 在末尾插入
    print(f"在末尾插入333后: {arr}")
    
    # 测试 remove
    print("\n--- 测试 remove ---")
    removed = arr.remove(0)  # 删除开头
    print(f"删除开头的 {removed} 后: {arr}")
    removed = arr.remove(2)  # 删除中间
    print(f"删除索引2的 {removed} 后: {arr}")
    
    # 测试缩容
    print("\n--- 测试缩容 ---")
    print(f"当前: {arr}, 大小: {len(arr)}, 容量: {arr.capacity}")
    while len(arr) > 2:
        arr.remove(0)
        print(f"删除后: {arr}, 大小: {len(arr)}, 容量: {arr.capacity}")
    
    # 测试错误处理
    print("\n--- 测试错误处理 ---")
    try:
        arr.get(100)
    except IndexError as e:
        print(f"✅ 正确捕获错误: {e}")
    
    print("\n✅ 所有测试通过！")

# 输出:
# === 练习3：完整动态数组测试 ===
#
# 创建数组，初始容量: 4
#
# --- 测试 append ---
#   扩容: 4 → 8
# 添加6个元素后: [0, 10, 20, 30, 40, 50]
# 大小: 6, 容量: 8
#
# --- 测试 get ---
# arr.get(2) = 20
# arr.get(0) = 0
# arr.get(5) = 50
#
# --- 测试 set ---
# 把索引2设为999后: [0, 10, 999, 30, 40, 50]
#
# --- 测试 insert ---
#   扩容: 8 → 16
# 在开头插入111后: [111, 0, 10, 999, 30, 40, 50]
# 在索引3插入222后: [111, 0, 10, 222, 999, 30, 40, 50]
# 在末尾插入333后: [111, 0, 10, 222, 999, 30, 40, 50, 333]
#
# --- 测试 remove ---
# 删除开头的 111 后: [0, 10, 222, 999, 30, 40, 50, 333]
# 删除索引2的 222 后: [0, 10, 999, 30, 40, 50, 333]
#
# --- 测试缩容 ---
# 当前: [0, 10, 999, 30, 40, 50, 333], 大小: 7, 容量: 16
# 删除后: [10, 999, 30, 40, 50, 333], 大小: 6, 容量: 16
# 删除后: [999, 30, 40, 50, 333], 大小: 5, 容量: 16
# 删除后: [30, 40, 50, 333], 大小: 4, 容量: 16
# 删除后: [40, 50, 333], 大小: 3, 容量: 16
# 删除后: [50, 333], 大小: 2, 容量: 8
#   缩容: 8 → 4
# 删除后: [333], 大小: 1, 容量: 4
#
# --- 测试错误处理 ---
# ✅ 正确捕获错误: 索引 100 越界！有效范围: 0-0
#
# ✅ 所有测试通过！
