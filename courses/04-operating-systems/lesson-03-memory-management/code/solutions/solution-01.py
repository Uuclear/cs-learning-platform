#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 实现简单的首次适应(First Fit)内存分配算法
"""

class FirstFitMemoryManager:
    def __init__(self, size: int):
        self.size = size
        self.free_blocks = [(0, size)]  # (start, size) 的列表
        self.allocated_blocks = {}  # address -> size

    def allocate(self, size: int) -> int:
        """首次适应分配算法"""
        for i, (start, block_size) in enumerate(self.free_blocks):
            if block_size >= size:
                # 找到合适的块
                self.free_blocks.pop(i)

                # 如果有剩余空间，添加回空闲列表
                if block_size > size:
                    self.free_blocks.insert(i, (start + size, block_size - size))

                self.allocated_blocks[start] = size
                return start

        raise MemoryError("Not enough memory")

    def deallocate(self, address: int):
        """释放内存"""
        if address not in self.allocated_blocks:
            raise ValueError("Invalid address")

        size = self.allocated_blocks[pop(address)]
        self.free_blocks.append((address, size))
        # 简单排序以便合并相邻块
        self.free_blocks.sort()

        # 合并相邻的空闲块
        i = 0
        while i < len(self.free_blocks) - 1:
            curr_start, curr_size = self.free_blocks[i]
            next_start, next_size = self.free_blocks[i + 1]

            if curr_start + curr_size == next_start:
                # 合并
                self.free_blocks[i] = (curr_start, curr_size + next_size)
                self.free_blocks.pop(i + 1)
            else:
                i += 1


def test_first_fit():
    mm = FirstFitMemoryManager(100)
    addr1 = mm.allocate(30)
    addr2 = mm.allocate(20)
    addr3 = mm.allocate(40)

    print(f"Allocated: {addr1}, {addr2}, {addr3}")
    print(f"Free blocks: {mm.free_blocks}")

    mm.deallocate(addr2)
    print(f"After deallocating {addr2}: {mm.free_blocks}")


if __name__ == "__main__":
    test_first_fit()