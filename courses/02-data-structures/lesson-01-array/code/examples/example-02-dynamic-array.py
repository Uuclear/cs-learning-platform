# ============================================
# 示例2：手动实现动态数组
# 理解Python列表背后的扩容机制
# ============================================

class DynamicArray:
    """
    动态数组的实现
    核心思想：容量不够时，搬家到更大的地方
    """
    
    def __init__(self, initial_capacity=4):
        """
        初始化动态数组
        capacity: 当前容量（能装多少）
        size: 当前大小（装了多少）
        """
        self.capacity = initial_capacity
        self.size = 0
        self.data = [None] * self.capacity  # 预分配空间
        print(f"🎉 创建了容量为 {self.capacity} 的动态数组")
    
    def append(self, value):
        """
        在末尾添加元素
        如果满了，先扩容再添加
        """
        # 检查是否需要扩容
        if self.size >= self.capacity:
            self._resize()
        
        self.data[self.size] = value
        self.size += 1
        print(f"  添加 {value}，当前大小: {self.size}/{self.capacity}")
    
    def _resize(self):
        """
        扩容操作：容量翻倍
        这就像搬家到更大的房子
        """
        old_capacity = self.capacity
        self.capacity *= 2  # 容量翻倍
        
        # 创建新的大数组
        new_data = [None] * self.capacity
        
        # 把旧数据搬过去
        for i in range(self.size):
            new_data[i] = self.data[i]
        
        self.data = new_data
        print(f"  🚚 扩容！{old_capacity} → {self.capacity}")
    
    def get(self, index):
        """获取指定索引的元素"""
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError("索引越界啦！")
    
    def __str__(self):
        """打印数组内容"""
        return f"[{', '.join(str(self.data[i]) for i in range(self.size))}]"


# 测试动态数组
print("=== 测试动态数组 ===")
arr = DynamicArray(initial_capacity=4)

print("\n开始添加元素...")
for i in range(10):
    arr.append(i * 10)

print(f"\n最终数组: {arr}")
print(f"最终大小: {arr.size}")
print(f"最终容量: {arr.capacity}")

# 访问元素
print(f"\n访问索引3的元素: {arr.get(3)}")

# 输出:
# === 测试动态数组 ===
# 🎉 创建了容量为 4 的动态数组
#
# 开始添加元素...
#   添加 0，当前大小: 1/4
#   添加 10，当前大小: 2/4
#   添加 20，当前大小: 3/4
#   添加 30，当前大小: 4/4
#   🚚 扩容！4 → 8
#   添加 40，当前大小: 5/8
#   添加 50，当前大小: 6/8
#   添加 60，当前大小: 7/8
#   添加 70，当前大小: 8/8
#   🚚 扩容！8 → 16
#   添加 80，当前大小: 9/16
#   添加 90，当前大小: 10/16
#
# 最终数组: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
# 最终大小: 10
# 最终容量: 16
#
# 访问索引3的元素: 30
