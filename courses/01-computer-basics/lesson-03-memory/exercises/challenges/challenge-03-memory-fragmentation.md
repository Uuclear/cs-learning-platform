# 挑战3: 内存碎片整理模拟

## 难度
⭐⭐⭐

## 描述

模拟内存碎片问题并实现简单的内存整理（Compaction）。当内存经过多次分配和释放后，会产生大量碎片，导致虽然有足够的总空闲空间，但无法分配较大的连续块。

内存整理通过移动已分配的内存块，将所有空闲空间合并成一块连续的区域。

## 输入

通过方法调用来操作：
- `allocate(size)` - 分配指定大小的内存块
- `free(address)` - 释放指定地址的内存块
- `compact()` - 执行内存整理
- `print_memory()` - 显示当前内存使用情况

## 输出

- `allocate` 返回分配内存的起始地址，失败返回 -1
- `compact` 返回一个字典，记录旧地址到新地址的映射

## 示例

```python
allocator = MemoryAllocator(size=100)

# 分配几个块
addr1 = allocator.allocate(20)  # 0-19
addr2 = allocator.allocate(20)  # 20-39
addr3 = allocator.allocate(20)  # 40-59

# 释放中间的块，产生碎片
allocator.free(addr2)
allocator.print_memory()
# 输出: [已分配: 0-19] [空闲: 20-39] [已分配: 40-59] [空闲: 60-99]

# 尝试分配一个较大的块，失败（虽然有60空闲，但不连续）
addr4 = allocator.allocate(30)  # 返回 -1

# 执行内存整理
moved = allocator.compact()
# 返回: {40: 20} 表示原来在40的块移动到了20
allocator.print_memory()
# 输出: [已分配: 0-19] [已分配: 20-39] [空闲: 40-99]

# 现在可以分配了
addr4 = allocator.allocate(30)  # 返回 40
```

## 约束条件

- 内存总大小：100-1000
- 分配大小：正整数
- 整理时需要更新所有指向移动块的引用（地址）
- 整理后已分配块应该紧密排列在内存前端

## 提示

1. 维护一个已分配块的列表，记录起始地址和大小
2. 整理时，将所有已分配块按地址排序后，依次移动到内存前端
3. 返回地址映射表，让调用者知道哪些地址发生了变化
4. 注意：在真实系统中，整理内存需要暂停程序或更新所有指针，非常复杂

## 进阶思考

- 为什么现代操作系统很少做内存整理？
- 虚拟内存如何解决碎片问题？
- 垃圾回收器（GC）是如何处理内存碎片和整理的？
- C/C++和Java/Python在内存管理上有什么不同？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

内存整理的核心步骤：
1. 收集所有已分配的内存块
2. 按地址排序
3. 依次将它们移动到内存前端（从地址0开始）
4. 记录旧地址到新地址的映射
5. 更新内部数据结构

关键点：
- 需要返回地址映射，让调用者更新引用
- 整理后空闲空间应该是一块连续的区域

### 代码

```python
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
    def __init__(self, size):
        self.size = size
        self.allocated = []  # 已分配的块列表
        self.next_alloc = 0  # 下一个分配地址（简单分配策略）

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


# 测试
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
    print(f"   最大连续空闲: {allocator.get_total_free()} 字节")

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
```

### 复杂度分析

- 时间复杂度：
  - allocate: O(n)，需要查找空闲区域
  - free: O(n)，需要查找要释放的块
  - compact: O(n log n)，需要排序
- 空间复杂度：O(n)，存储块信息

### 为什么操作系统很少做内存整理？

1. **需要更新所有指针**：内存中的对象可能互相引用，移动后需要更新所有引用
2. **需要暂停程序**：整理期间不能访问内存，需要暂停或冻结程序
3. **虚拟内存解决了这个问题**：每个进程有独立的虚拟地址空间，物理内存碎片不影响
4. **代价太高**：相比收益，整理的开销通常不值得

### 虚拟内存如何解决碎片？

- 每个进程看到连续的虚拟地址空间
- 物理内存可以是碎片化的
- 通过页表映射，虚拟地址到物理地址的转换由硬件完成
- 进程不需要关心物理内存是否连续

### 垃圾回收器如何处理碎片？

- **标记-清除**：会产生碎片
- **标记-整理**：移动存活对象，消除碎片（类似本题的compact）
- **复制算法**：将存活对象复制到新区域，完全消除碎片
- **分代收集**：针对不同代使用不同策略

现代GC（如Java的G1、ZGC）使用复杂算法在减少停顿的同时处理碎片。

</details>
