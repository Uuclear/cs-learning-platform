#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 虚拟内存和页面置换模拟
演示虚拟内存的基本概念，包括页表、缺页中断和LRU页面置换算法。
"""

from typing import Dict, List, Optional, Set
from collections import OrderedDict


class VirtualMemorySimulator:
    """虚拟内存模拟器"""
    def __init__(self, physical_pages: int = 4):
        self.physical_pages = physical_pages  # 物理内存中的页框数量
        self.page_table: Dict[int, Optional[int]] = {}  # 虚拟页号 -> 物理页框号
        self.lru_cache = OrderedDict()  # LRU缓存：虚拟页号 -> 访问时间戳
        self.access_counter = 0  # 访问计数器（用于LRU）
        self.page_faults = 0     # 缺页次数
        self.total_accesses = 0  # 总访问次数

    def access_virtual_page(self, virtual_page: int) -> bool:
        """
        访问虚拟页
        返回True表示命中，False表示缺页
        """
        self.total_accesses += 1

        if virtual_page in self.page_table and self.page_table[virtual_page] is not None:
            # 页面在物理内存中（命中）
            print(f"✅ 虚拟页 {virtual_page} 命中！物理页框 {self.page_table[virtual_page]}")
            self._update_lru(virtual_page)
            return True
        else:
            # 缺页中断
            self.page_faults += 1
            print(f"❌ 缺页中断！虚拟页 {virtual_page} 不在物理内存中")

            # 执行页面置换
            self._handle_page_fault(virtual_page)
            self._update_lru(virtual_page)
            return False

    def _handle_page_fault(self, virtual_page: int):
        """处理缺页中断"""
        # 检查是否有空闲的物理页框
        used_frames = set(frame for frame in self.page_table.values() if frame is not None)
        available_frames = set(range(self.physical_pages)) - used_frames

        if available_frames:
            # 有空闲页框，直接分配
            frame = min(available_frames)
            self.page_table[virtual_page] = frame
            print(f"   → 分配空闲物理页框 {frame} 给虚拟页 {virtual_page}")
        else:
            # 需要页面置换 - 使用LRU算法
            if len(self.page_table) >= self.physical_pages:
                # 找到最久未使用的页面
                lru_page = next(iter(self.lru_cache))
                old_frame = self.page_table[lru_page]
                print(f"   → LRU置换：移出虚拟页 {lru_page} (物理页框 {old_frame})")

                # 更新页表
                del self.page_table[lru_page]
                self.page_table[virtual_page] = old_frame
                print(f"   → 分配物理页框 {old_frame} 给虚拟页 {virtual_page}")
            else:
                # 这种情况不应该发生，但为了安全起见
                frame = len([v for v in self.page_table.values() if v is not None])
                self.page_table[virtual_page] = frame
                print(f"   → 分配物理页框 {frame} 给虚拟页 {virtual_page}")

    def _update_lru(self, virtual_page: int):
        """更新LRU缓存"""
        if virtual_page in self.lru_cache:
            del self.lru_cache[virtual_page]
        self.lru_cache[virtual_page] = self.access_counter
        self.access_counter += 1

        # 确保LRU缓存大小不超过物理页框数
        while len(self.lru_cache) > self.physical_pages:
            self.lru_cache.popitem(last=False)

    def get_statistics(self) -> Dict[str, float]:
        """获取统计信息"""
        hit_rate = (self.total_accesses - self.page_faults) / self.total_accesses if self.total_accesses > 0 else 0
        return {
            "总访问次数": self.total_accesses,
            "缺页次数": self.page_faults,
            "命中率": f"{hit_rate:.2%}",
            "缺页率": f"{self.page_faults/self.total_accesses:.2%}" if self.total_accesses > 0 else "0%"
        }

    def print_page_table(self):
        """打印页表"""
        print("\n📋 当前页表:")
        print("-" * 40)
        for virtual_page, frame in sorted(self.page_table.items()):
            if frame is not None:
                print(f"  虚拟页 {virtual_page} → 物理页框 {frame}")
        print("-" * 40)


def simulate_memory_access():
    """模拟内存访问模式"""
    print("🚀 虚拟内存和LRU页面置换模拟")
    print("=" * 50)

    # 创建有4个物理页框的虚拟内存系统
    vm = VirtualMemorySimulator(physical_pages=4)

    # 模拟访问序列：有些页面会被频繁访问，有些很少
    access_sequence = [0, 1, 2, 3, 0, 1, 4, 0, 1, 2, 3, 4]

    print(f"🔧 物理内存页框数: {vm.physical_pages}")
    print(f"📊 访问序列: {access_sequence}")
    print()

    for i, page in enumerate(access_sequence):
        print(f"第 {i+1} 次访问:")
        vm.access_virtual_page(page)
        vm.print_page_table()

    # 显示统计信息
    stats = vm.get_statistics()
    print("\n📈 最终统计:")
    print("-" * 30)
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    simulate_memory_access()