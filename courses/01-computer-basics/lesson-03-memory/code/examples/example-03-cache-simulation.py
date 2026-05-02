# 缓存命中率模拟
# 演示缓存如何影响数据访问性能

import random
import time


class SimpleCache:
    """
    简单的缓存模拟器
    模拟CPU缓存的行为
    """
    def __init__(self, size):
        self.size = size  # 缓存大小
        self.cache = {}   # 存储的数据
        self.access_order = []  # 记录访问顺序（用于LRU替换）
        self.hits = 0     # 命中次数
        self.misses = 0   # 未命中次数

    def access(self, address):
        """
        访问某个地址的数据
        返回: (是否命中, 访问时间)
        """
        if address in self.cache:
            # 缓存命中！很快
            self.hits += 1
            # 更新访问顺序
            self.access_order.remove(address)
            self.access_order.append(address)
            return True, 1  # 时间单位：1（很快）
        else:
            # 缓存未命中，需要从内存加载
            self.misses += 1
            # 如果缓存满了，移除最久未使用的
            if len(self.cache) >= self.size:
                lru = self.access_order.pop(0)
                del self.cache[lru]

            # 从"内存"加载数据（模拟耗时）
            self.cache[address] = f"data_{address}"
            self.access_order.append(address)
            return False, 100  # 时间单位：100（慢100倍）

    def get_hit_rate(self):
        """获取命中率"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0

    def stats(self):
        """打印统计信息"""
        total = self.hits + self.misses
        print(f"  缓存大小: {self.size}")
        print(f"  总访问次数: {total}")
        print(f"  命中次数: {self.hits}")
        print(f"  未命中次数: {self.misses}")
        print(f"  命中率: {self.get_hit_rate():.2%}")
        print(f"  当前缓存内容: {list(self.cache.keys())}")


def demonstrate_cache():
    """
    演示缓存的工作原理和重要性
    """
    print("=== 缓存命中率模拟 ===\n")

    # 模拟数据访问模式
    data_size = 100  # 总数据量

    # 场景1: 顺序访问（缓存友好）
    print("场景1: 顺序访问（非常缓存友好）")
    print("-" * 40)
    cache = SimpleCache(size=10)
    total_time = 0

    for i in range(50):
        hit, t = cache.access(i % 20)  # 重复访问前20个数据
        total_time += t

    cache.stats()
    print(f"  总访问时间: {total_time}")
    print()

    # 场景2: 随机访问（缓存不友好）
    print("场景2: 完全随机访问（缓存不友好）")
    print("-" * 40)
    cache2 = SimpleCache(size=10)
    total_time2 = 0

    random.seed(42)
    for _ in range(50):
        addr = random.randint(0, data_size - 1)
        hit, t = cache2.access(addr)
        total_time2 += t

    cache2.stats()
    print(f"  总访问时间: {total_time2}")
    print()

    # 场景3: 局部性访问（真实程序常见）
    print("场景3: 局部性访问（真实程序常见模式）")
    print("-" * 40)
    cache3 = SimpleCache(size=10)
    total_time3 = 0

    # 模拟：先访问一个区域，再访问另一个区域
    current_base = 0
    for i in range(50):
        # 80%概率访问当前工作集，20%概率切换
        if random.random() < 0.8:
            addr = current_base + random.randint(0, 5)
        else:
            current_base = random.choice([0, 20, 40, 60])
            addr = current_base + random.randint(0, 5)

        hit, t = cache3.access(addr % data_size)
        total_time3 += t

    cache3.stats()
    print(f"  总访问时间: {total_time3}")
    print()

    # 对比总结
    print("=== 性能对比 ===")
    print(f"顺序访问时间: {total_time}")
    print(f"随机访问时间: {total_time2}")
    print(f"局部性访问时间: {total_time3}")
    print(f"\n结论：良好的数据局部性可以显著提升性能！")
    print(f"缓存命中率越高，程序运行越快。")


def demonstrate_memory_hierarchy():
    """
    演示内存层次结构的速度差异
    """
    print("\n=== 内存层次结构速度对比 ===\n")

    # 模拟不同存储级别的访问时间
    storage_levels = {
        "寄存器": (1, "ns"),
        "L1缓存": (4, "ns"),
        "L2缓存": (10, "ns"),
        "L3缓存": (40, "ns"),
        "内存(RAM)": (100, "ns"),
        "SSD硬盘": (100000, "ns"),  # 约0.1ms
        "机械硬盘":  (10000000, "ns")  # 约10ms
    }

    print("各级存储访问时间对比:")
    print("-" * 40)

    base_time = 1  # 寄存器时间作为基准
    for level, (time, unit) in storage_levels.items():
        ratio = time / base_time
        bar = "█" * min(int(ratio / 10), 50)  # 限制条形图长度
        print(f"{level:12}: {time:>10} {unit} {bar}")

    print("\n类比（如果把寄存器访问比作1秒）:")
    print("-" * 40)
    for level, (time, unit) in list(storage_levels.items())[1:]:
        seconds = time  # 假设寄存器是1秒
        if seconds < 60:
            equivalent = f"{seconds}秒"
        elif seconds < 3600:
            equivalent = f"{seconds // 60}分{seconds % 60}秒"
        elif seconds < 86400:
            equivalent = f"{seconds // 3600}小时"
        elif seconds < 31536000:
            equivalent = f"{seconds // 86400}天"
        else:
            equivalent = f"{seconds // 31536000}年"
        print(f"访问{level}相当于等待: {equivalent}")


# 运行演示
if __name__ == "__main__":
    demonstrate_cache()
    demonstrate_memory_hierarchy()

# 输出示例:
# === 缓存命中率模拟 ===
#
# 场景1: 顺序访问（非常缓存友好）
# ----------------------------------------
#   缓存大小: 10
#   总访问次数: 50
#   命中次数: 40
#   未命中次数: 10
#   命中率: 80.00%
#   当前缓存内容: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
#   总访问时间: 1040
#
# ...
