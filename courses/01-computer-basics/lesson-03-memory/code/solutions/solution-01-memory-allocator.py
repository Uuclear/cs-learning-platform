# 练习1解答：模拟内存分配器

class MemoryAllocator:
    """简单内存分配器实现"""

    def __init__(self, size):
        self.size = size
        # 存储已分配的块: [(start, size), ...]
        self.allocated = []
        # 存储空闲块: [(start, size), ...]
        self.free_blocks = [(0, size)]

    def allocate(self, size):
        """使用首次适应算法分配内存"""
        for i, (start, free_size) in enumerate(self.free_blocks):
            if free_size >= size:
                # 找到合适的块
                self.allocated.append((start, size))
                self.allocated.sort()  # 保持有序

                # 更新空闲块
                if free_size == size:
                    self.free_blocks.pop(i)
                else:
                    self.free_blocks[i] = (start + size, free_size - size)

                return start
        return -1  # 分配失败

    def free(self, address):
        """释放内存"""
        for i, (start, size) in enumerate(self.allocated):
            if start == address:
                self.allocated.pop(i)
                # 添加回空闲列表
                self.free_blocks.append((start, size))
                self._merge_free_blocks()
                return True
        return False

    def _merge_free_blocks(self):
        """合并相邻的空闲块"""
        self.free_blocks.sort()
        merged = []
        for start, size in self.free_blocks:
            if merged and merged[-1][0] + merged[-1][1] == start:
                # 可以合并
                merged[-1] = (merged[-1][0], merged[-1][1] + size)
            else:
                merged.append((start, size))
        self.free_blocks = merged

    def print_memory(self):
        """打印内存状态"""
        # 合并所有块并按地址排序
        all_blocks = []
        for start, size in self.allocated:
            all_blocks.append((start, size, 'allocated'))
        for start, size in self.free_blocks:
            all_blocks.append((start, size, 'free'))
        all_blocks.sort()

        parts = []
        for start, size, typ in all_blocks:
            end = start + size - 1
            if typ == 'allocated':
                parts.append(f"[已分配: {start}-{end}]")
            else:
                parts.append(f"[空闲: {start}-{end}]")

        print(" ".join(parts))


# 测试代码
if __name__ == "__main__":
    print("=== 内存分配器测试 ===\n")

    allocator = MemoryAllocator(100)

    # 测试分配
    print("1. 分配内存:")
    addr1 = allocator.allocate(20)
    addr2 = allocator.allocate(30)
    addr3 = allocator.allocate(10)
    print(f"   分配 addr1={addr1}, addr2={addr2}, addr3={addr3}")
    allocator.print_memory()

    # 测试释放
    print("\n2. 释放 addr2:")
    allocator.free(addr2)
    allocator.print_memory()

    # 再次分配（应该使用首次适应找到的空闲块）
    print("\n3. 分配15字节（应该使用 addr2 的空闲位置）:")
    addr4 = allocator.allocate(15)
    print(f"   分配 addr4={addr4}")
    allocator.print_memory()

    # 测试分配失败
    print("\n4. 尝试分配超大块（应该失败）:")
    addr5 = allocator.allocate(100)
    print(f"   结果: {'成功' if addr5 != -1 else '失败'}")

    # 测试边界情况
    print("\n5. 分配剩余空间:")
    addr6 = allocator.allocate(25)
    print(f"   分配 addr6={addr6}")
    allocator.print_memory()
