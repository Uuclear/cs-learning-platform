#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 内存分配模拟
演示基本的内存分配和释放过程，模拟操作系统如何管理内存块。
"""

import random
from typing import Dict, List, Optional, Tuple


class MemoryBlock:
    """内存块表示"""
    def __init__(self, start: int, size: int, allocated: bool = False, process_id: Optional[int] = None):
        self.start = start      # 起始地址
        self.size = size        # 大小
        self.allocated = allocated  # 是否已分配
        self.process_id = process_id  # 分配给哪个进程

    def __str__(self):
        status = f"已分配(进程{self.process_id})" if self.allocated else "空闲"
        return f"[{self.start}-{self.start + self.size - 1}] {status}"


class SimpleMemoryManager:
    """简单内存管理器"""
    def __init__(self, total_size: int = 1024):
        self.total_size = total_size
        # 初始化一个大的空闲内存块
        self.memory_blocks: List[MemoryBlock] = [MemoryBlock(0, total_size)]
        self.process_counter = 1

    def allocate(self, size: int) -> Optional[int]:
        """
        分配内存
        返回分配的起始地址，如果失败返回None
        """
        for i, block in enumerate(self.memory_blocks):
            if not block.allocated and block.size >= size:
                # 找到合适的空闲块
                allocated_block = MemoryBlock(
                    block.start, size, True, self.process_counter
                )
                self.process_counter += 1

                # 更新内存块列表
                remaining_size = block.size - size
                if remaining_size > 0:
                    # 还有剩余空间，分割块
                    remaining_block = MemoryBlock(
                        block.start + size, remaining_size, False
                    )
                    self.memory_blocks[i] = allocated_block
                    self.memory_blocks.insert(i + 1, remaining_block)
                else:
                    # 完全使用这个块
                    self.memory_blocks[i] = allocated_block

                print(f"✅ 成功分配 {size} 字节内存给进程 {allocated_block.process_id}")
                return allocated_block.start

        print(f"❌ 内存不足！无法分配 {size} 字节")
        return None

    def deallocate(self, address: int) -> bool:
        """释放内存"""
        for i, block in enumerate(self.memory_blocks):
            if block.allocated and block.start == address:
                block.allocated = False
                block.process_id = None
                print(f"✅ 释放地址 {address} 的内存")

                # 合并相邻的空闲块（简化版）
                self._merge_adjacent_free_blocks()
                return True

        print(f"❌ 无效地址 {address}，无法释放")
        return False

    def _merge_adjacent_free_blocks(self):
        """合并相邻的空闲块（简化实现）"""
        i = 0
        while i < len(self.memory_blocks) - 1:
            current = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]

            if not current.allocated and not next_block.allocated:
                # 合并两个空闲块
                merged_block = MemoryBlock(
                    current.start, current.size + next_block.size, False
                )
                self.memory_blocks[i] = merged_block
                self.memory_blocks.pop(i + 1)
            else:
                i += 1

    def print_memory_map(self):
        """打印内存映射"""
        print("\n📊 当前内存状态:")
        print("-" * 50)
        for block in self.memory_blocks:
            print(f"  {block}")
        print("-" * 50)


def main():
    """主函数 - 演示内存分配过程"""
    print("🚀 内存分配模拟演示")
    print("=" * 50)

    # 创建1KB内存管理器
    mm = SimpleMemoryManager(1024)

    # 初始状态
    mm.print_memory_map()

    # 分配一些内存
    allocations = []
    alloc_sizes = [256, 128, 512, 64]

    print("\n🔧 开始分配内存...")
    for size in alloc_sizes:
        addr = mm.allocate(size)
        if addr is not None:
            allocations.append(addr)
        mm.print_memory_map()

    # 尝试分配超出剩余内存的空间
    print("\n💡 尝试分配超出可用内存的空间...")
    mm.allocate(1000)

    # 释放一些内存
    print("\n🔄 释放部分内存...")
    if allocations:
        mm.deallocate(allocations[0])  # 释放第一个分配
        mm.deallocate(allocations[2])  # 释放第三个分配
        mm.print_memory_map()


if __name__ == "__main__":
    main()