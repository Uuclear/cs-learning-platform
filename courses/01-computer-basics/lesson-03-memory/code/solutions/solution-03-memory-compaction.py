# 练习3解答：内存碎片整理模拟

class MemoryBlock:
    """内存块"""
    def __init__(self, start, size):
        self.start = start
        self.size = size

    def end(self):
        return self.start + self.size - 1

    def __repr__(self):
        return f"[{self.start}-{self.end()}]"


class MemoryAllocator:
    """带整理功能的内存分配器"""

    def __init__(self, size):
        self.size = size
        self.allocated = []  # 已分配的块列表

    def allocate(self, size):
        """分配内存（使用首次适应）"""
        # 找到第一个足够大的空闲区域
        allocated_sorted = sorted(self.allocated, key=lambda b: b.start)

        # 检查0到第一个块之间
        prev_end = -1
        for block in allocated_sorted:
            gap_start = prev_end + 1
            gap_size = block.start - gap_start
            if gap_size >= size:
                new_block = MemoryBlock(gap_start, size)
                self.allocated.append(new_block)
                return gap_start
            prev_end = block.end()

        # 检查最后一个块之后
        gap_start = prev_end + 1 if allocated_sorted else 0
        gap_size = self.size - gap_start
        if gap_size >= size:
            new_block = MemoryBlock(gap_start, size)
            self.allocated.append(new_block)
            return gap_start

        return -1  # 分配失败

    def free(self, address):
        """释放内存"""
        for i, block in enumerate(self.allocated):
            if block.start == address:
                self.allocated.pop(i)
                return True
        return False

    def compact(self):
        """
        执行内存整理
        返回旧地址到新地址的映射字典
        """
        if not self.allocated:
            return {}

        # 按地址排序
        self.allocated.sort(key=lambda b: b.start)

        # 移动块并记录映射
        address_map = {}
        current_addr = 0

        for block in self.allocated:
            if block.start != current_addr:
                # 需要移动
                old_start = block.start
                block.start = current_addr
                address_map[old_start] = current_addr
            current_addr += block.size

        return address_map

    def get_largest_free_block(self):
        """获取最大连续空闲块大小"""
        if not self.allocated:
            return self.size

        allocated_sorted = sorted(self.allocated, key=lambda b: b.start)
        max_free = 0
        prev_end = -1

        for block in allocated_sorted:
            gap = block.start - prev_end - 1
            max_free = max(max_free, gap)
            prev_end = block.end()

        # 最后一块之后
        gap = self.size - prev_end - 1
        max_free = max(max_free, gap)

        return max_free

    def get_total_free(self):
        """获取总空闲空间"""
        used = sum(b.size for b in self.allocated)
        return self.size - used

    def print_memory(self):
        """打印内存状态"""
        if not self.allocated:
            print(f"[空闲: 0-{self.size-1}]")
            return

        allocated_sorted = sorted(self.allocated, key=lambda b: b.start)
        parts = []
        prev_end = -1

        for block in allocated_sorted:
            if block.start > prev_end + 1:
                parts.append(f"[空闲: {prev_end+1}-{block.start-1}]")
            parts.append(f"[已分配: {block.start}-{block.end()}]")
            prev_end = block.end()

        if prev_end < self.size - 1:
            parts.append(f"[空闲: {prev_end+1}-{self.size-1}]")

        print(" ".join(parts))


# 测试代码
if __name__ == "__main__":
    print("=== 内存碎片整理演示 ===\n")

    allocator = MemoryAllocator(100)

    # 分配几个块
    print("1. 分配3个20字节的块:")
    addr1 = allocator.allocate(20)
    addr2 = allocator.allocate(20)
    addr3 = allocator.allocate(20)
    print(f"   addr1={addr1}, addr2={addr2}, addr3={addr3}")
    allocator.print_memory()

    # 释放中间的块
    print("\n2. 释放中间的块 (addr2):")
    allocator.free(addr2)
    allocator.print_memory()

    print(f"   总空闲: {allocator.get_total_free()} 字节")
    print(f"   最大连续空闲: {allocator.get_largest_free_block()} 字节")

    # 尝试分配较大的块
    print("\n3. 尝试分配30字节的块:")
    addr4 = allocator.allocate(30)
    print(f"   结果: {'成功' if addr4 != -1 else '失败'}")

    # 执行整理
    print("\n4. 执行内存整理:")
    moved = allocator.compact()
    print(f"   地址映射: {moved}")
    allocator.print_memory()

    # 更新addr3（因为被移动了）
    if addr3 in moved:
        addr3 = moved[addr3]
        print(f"   addr3 更新为: {addr3}")

    # 再次尝试分配
    print("\n5. 再次尝试分配30字节的块:")
    addr4 = allocator.allocate(30)
    print(f"   结果: {'成功' if addr4 != -1 else '失败'}, addr4={addr4}")
    allocator.print_memory()

    # 展示碎片问题
    print("\n=== 碎片问题演示 ===\n")

    allocator2 = MemoryAllocator(100)
    # 交替分配和释放，产生碎片
    addresses = []
    for i in range(5):
        addr = allocator2.allocate(10)
        addresses.append(addr)

    print("分配5个10字节块:")
    allocator2.print_memory()

    # 释放第1、3、5个（索引0、2、4）
    allocator2.free(addresses[0])
    allocator2.free(addresses[2])
    allocator2.free(addresses[4])

    print("\n释放其中3个（产生碎片）:")
    allocator2.print_memory()
    print(f"总空闲: {allocator2.get_total_free()} 字节")
    print(f"最大连续空闲: {allocator2.get_largest_free_block()} 字节")

    print("\n尝试分配25字节块（失败，虽然总空闲足够）:")
    addr = allocator2.allocate(25)
    print(f"结果: {'成功' if addr != -1 else '失败'}")

    print("\n执行整理后:")
    allocator2.compact()
    allocator2.print_memory()
    print(f"最大连续空闲: {allocator2.get_largest_free_block()} 字节")

    print("\n再次尝试分配25字节块（成功）:")
    addr = allocator2.allocate(25)
    print(f"结果: 成功, addr={addr}")
    allocator2.print_memory()
