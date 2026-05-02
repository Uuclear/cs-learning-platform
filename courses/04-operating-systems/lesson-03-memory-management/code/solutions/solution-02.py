#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 实现FIFO页面置换算法
"""

from collections import deque
from typing import List, Set


class FIFOPageReplacement:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.pages = deque()  # FIFO队列
        self.page_set: Set[int] = set()  # 快速查找
        self.page_faults = 0

    def access_page(self, page: int) -> bool:
        """访问页面，返回是否发生缺页"""
        if page in self.page_set:
            return True  # 命中

        self.page_faults += 1

        if len(self.page_set) >= self.capacity:
            # 需要置换
            removed_page = self.pages.popleft()
            self.page_set.remove(removed_page)
            print(f"置换页面 {removed_page} -> {page}")

        self.pages.append(page)
        self.page_set.add(page)
        return False

    def get_hit_rate(self, accesses: int) -> float:
        return (accesses - self.page_faults) / accesses if accesses > 0 else 0


def simulate_fifo():
    fifo = FIFOPageReplacement(3)
    reference_string = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]

    for page in reference_string:
        fifo.access_page(page)

    hit_rate = fifo.get_hit_rate(len(reference_string))
    print(f"FIFO缺页次数: {fifo.page_faults}")
    print(f"命中率: {hit_rate:.2%}")


if __name__ == "__main__":
    simulate_fifo()