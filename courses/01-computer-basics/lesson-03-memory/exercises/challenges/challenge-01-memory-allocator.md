# 挑战1: 模拟内存分配器

## 难度
⭐

## 描述

实现一个简单的内存分配器，管理一块固定大小的内存空间。这是理解操作系统内存管理的基础。

## 输入

通过方法调用来操作内存分配器：
- `allocate(size)` - 分配指定大小的内存块
- `free(address)` - 释放指定地址的内存块
- `print_memory()` - 显示当前内存使用情况

## 输出

- `allocate` 返回分配内存的起始地址（整数），如果分配失败返回 -1
- `print_memory` 打印内存使用状态

## 示例

```python
allocator = MemoryAllocator(size=100)

addr1 = allocator.allocate(20)  # 返回 0
addr2 = allocator.allocate(30)  # 返回 20
addr3 = allocator.allocate(10)  # 返回 50

allocator.print_memory()
# 输出:
# [已分配: 0-19] [已分配: 20-49] [已分配: 50-59] [空闲: 60-99]

allocator.free(addr2)
allocator.print_memory()
# 输出:
# [已分配: 0-19] [空闲: 20-49] [已分配: 50-59] [空闲: 60-99]

addr4 = allocator.allocate(15)  # 返回 20（首次适应）
```

## 约束条件

- 内存总大小：正整数（100-10000）
- 分配大小：正整数
- 使用"首次适应"（First Fit）算法：找到第一个足够大的空闲块进行分配
- 地址从 0 开始

## 提示

1. 维护一个已分配块的列表，记录每个块的起始地址和大小
2. 分配时遍历查找第一个满足大小的空闲区域
3. 释放时标记对应区域为空闲
4. 可选：实现空闲块合并，避免碎片过多

## 进阶思考

- 如果实现"最佳适应"（Best Fit）算法，会有什么不同？
- 内存碎片问题如何影响分配效率？
- 真实操作系统是如何管理物理内存的？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

1. 使用列表记录已分配的内存块，每个块包含起始地址和大小
2. 使用列表记录空闲块，或者通过计算得出空闲区域
3. 分配时找到第一个足够大的空闲块，分割它
4. 释放时将对应块标记为空闲，并尝试合并相邻的空闲块

### 代码

```python
class MemoryAllocator:
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


# 测试
if __name__ == "__main__":
    allocator = MemoryAllocator(100)

    addr1 = allocator.allocate(20)
    addr2 = allocator.allocate(30)
    addr3 = allocator.allocate(10)

    print(f"分配 addr1={addr1}, addr2={addr2}, addr3={addr3}")
    allocator.print_memory()

    allocator.free(addr2)
    print("释放 addr2 后:")
    allocator.print_memory()

    addr4 = allocator.allocate(15)
    print(f"分配 addr4={addr4}")
    allocator.print_memory()
```

### 复杂度分析

- 时间复杂度：
  - allocate: O(n)，n为空闲块数量
  - free: O(n)，需要查找和合并
- 空间复杂度：O(n)，存储块信息

### 扩展思考

- 首次适应算法简单快速，但可能产生碎片
- 最佳适应算法选择最小的满足条件的块，减少浪费但搜索更慢
- 最坏适应算法选择最大的块，保留大块给大请求

</details>
