#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 内存泄漏检测器
"""

import gc
import sys
from typing import Dict, List, Any


class MemoryLeakDetector:
    def __init__(self):
        self.object_counts: Dict[type, int] = {}
        self.snapshot_objects: List[Any] = []

    def take_snapshot(self):
        """拍摄当前对象快照"""
        # 获取所有对象
        all_objects = gc.get_objects()
        self.snapshot_objects = all_objects.copy()

        # 统计各类型对象数量
        self.object_counts.clear()
        for obj in all_objects:
            obj_type = type(obj)
            self.object_counts[obj_type] = self.object_counts.get(obj_type, 0) + 1

    def compare_with_snapshot(self) -> Dict[type, int]:
        """比较当前状态与快照的差异"""
        current_counts: Dict[type, int] = {}
        current_objects = gc.get_objects()

        for obj in current_objects:
            obj_type = type(obj)
            current_counts[obj_type] = current_counts.get(obj_type, 0) + 1

        # 计算差异
        differences = {}
        for obj_type, current_count in current_counts.items():
            snapshot_count = self.object_counts.get(obj_type, 0)
            diff = current_count - snapshot_count
            if diff > 0:
                differences[obj_type] = diff

        return differences


def demonstrate_leak_detection():
    """演示内存泄漏检测"""
    detector = MemoryLeakDetector()

    print("拍摄初始快照...")
    detector.take_snapshot()

    # 创建一些对象（模拟内存泄漏）
    leaked_objects = []
    for i in range(1000):
        leaked_objects.append({"id": i, "data": "leaked" * 100})

    print("创建1000个对象后...")
    differences = detector.compare_with_snapshot()

    print("新增的对象类型:")
    for obj_type, count in differences.items():
        if count > 10:  # 只显示显著增加的类型
            print(f"  {obj_type.__name__}: +{count}")

    # 清理泄漏的对象
    del leaked_objects
    gc.collect()

    print("\n清理后...")
    differences = detector.compare_with_snapshot()
    print("清理后的差异:")
    for obj_type, count in differences.items():
        if count > 10:
            print(f"  {obj_type.__name__}: +{count}")


if __name__ == "__main__":
    demonstrate_leak_detection()