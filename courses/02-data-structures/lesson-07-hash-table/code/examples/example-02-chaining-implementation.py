# ============================================
# 示例2：手写哈希表 - 链地址法解决碰撞
# 理解哈希表的底层实现原理
# ============================================

class HashTable:
    """
    手写哈希表，使用链地址法解决碰撞
    核心思路：每个位置是一个链表，碰撞了就往链尾挂
    """

    def __init__(self, size=10):
        # 初始化桶数组，每个桶是一个空列表（链表）
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self.count = 0  # 当前存储的键值对数量
        print(f"🎉 创建了大小为 {size} 的哈希表")

    def _hash(self, key):
        """
        哈希函数：将键映射到桶的索引
        Python内置的hash()已经很好了，这里用它
        """
        return hash(key) % self.size

    def put(self, key, value):
        """
        插入或更新键值对
        如果键已存在，就更新值；否则新建
        """
        idx = self._hash(key)
        bucket = self.buckets[idx]

        # 检查这个键是否已经存在
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # 更新值
                print(f"  更新 [{key}] → {value} (桶{idx})")
                return

        # 键不存在，添加到链表尾部
        bucket.append((key, value))
        self.count += 1
        print(f"  插入 [{key}] → {value} (桶{idx})")

        # 检查是否需要扩容
        if self.count > self.size * 0.7:
            self._resize()

    def get(self, key, default=None):
        """
        查找键对应的值
        找不到就返回默认值
        """
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v

        return default

    def remove(self, key):
        """
        删除键值对
        """
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                print(f"  删除 [{key}] (桶{idx})")
                return True

        print(f"  警告: [{key}] 不存在！")
        return False

    def _resize(self):
        """
        扩容操作：桶数量翻倍，重新哈希所有元素
        """
        old_size = self.size
        old_buckets = self.buckets

        self.size *= 2
        self.buckets = [[] for _ in range(self.size)]
        self.count = 0

        print(f"  🔧 扩容: {old_size} → {self.size}，重新哈希...")

        # 把所有旧数据重新哈希到新表
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def display(self):
        """
        可视化展示哈希表的状态
        """
        print("\n=== 哈希表状态 ===")
        for i, bucket in enumerate(self.buckets):
            if bucket:
                pairs = " → ".join(f"[{k}:{v}]" for k, v in bucket)
                print(f"  桶{i}: {pairs}")
            else:
                print(f"  桶{i}: (空)")
        print(f"  总计: {self.count} 个键值对, 大小: {self.size}")
        print("=" * 30)


# 测试手写哈希表
print("=== 测试手写哈希表（链地址法）===")
ht = HashTable(size=5)

# 插入一些键值对
ht.put("name", "小明")
ht.put("age", 18)
ht.put("city", "北京")
ht.put("hobby", "编程")
ht.put("language", "Python")

# 查找
print(f"\n查找 'name': {ht.get('name')}")
print(f"查找 'city': {ht.get('city')}")
print(f"查找 '不存在的键': {ht.get('nope', '找不到！')}")

# 更新
ht.put("name", "小红")
print(f"\n更新后 'name': {ht.get('name')}")

# 删除
ht.remove("age")

# 展示最终状态
ht.display()
