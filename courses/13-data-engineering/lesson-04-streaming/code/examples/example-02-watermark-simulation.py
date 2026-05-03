#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
水印模拟示例

本示例演示流式处理中的水印机制，用于处理延迟数据。
水印 = 当前最大事件时间 - 允许的最大延迟时间
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
import heapq


class WatermarkProcessor:
    """水印处理器，模拟Flink/Spark中的水印机制"""

    def __init__(self, max_lateness_minutes: int):
        """
        初始化水印处理器

        Args:
            max_lateness_minutes: 允许的最大延迟时间（分钟）
        """
        self.max_lateness = timedelta(minutes=max_lateness_minutes)
        self.current_max_event_time = None
        self.watermark = None
        self.late_events = []
        self.processed_events = []

    def update_watermark(self, event_time: datetime) -> datetime:
        """
        更新水印基于新的事件时间

        Args:
            event_time: 新事件的时间戳

        Returns:
            更新后的水印时间
        """
        if self.current_max_event_time is None or event_time > self.current_max_event_time:
            self.current_max_event_time = event_time

        # 水印 = 最大事件时间 - 允许的最大延迟
        self.watermark = self.current_max_event_time - self.max_lateness
        return self.watermark

    def process_event(self, event_time: datetime, data: str) -> Tuple[bool, str]:
        """
        处理事件，判断是否为延迟事件

        Args:
            event_time: 事件时间戳
            data: 事件数据

        Returns:
            (is_on_time, message) - 是否按时到达及处理消息
        """
        current_watermark = self.update_watermark(event_time)

        if event_time >= current_watermark:
            # 按时事件
            self.processed_events.append((event_time, data))
            return True, f"按时处理: {data} (事件时间: {event_time}, 水印: {current_watermark})"
        else:
            # 延迟事件
            self.late_events.append((event_time, data))
            return False, f"延迟事件: {data} (事件时间: {event_time}, 水印: {current_watermark}, 延迟: {current_watermark - event_time})"


def simulate_watermark_processing():
    """模拟水印处理过程"""
    print("=== 水印机制模拟演示 ===\n")

    # 创建水印处理器，允许最大5分钟延迟
    processor = WatermarkProcessor(max_lateness_minutes=5)

    # 模拟事件流（包含按时和延迟事件）
    base_time = datetime(2026, 5, 3, 10, 0, 0)
    events = [
        (base_time + timedelta(minutes=1), "订单_001"),
        (base_time + timedelta(minutes=3), "订单_002"),
        (base_time + timedelta(minutes=7), "订单_003"),
        (base_time + timedelta(minutes=2), "订单_004"),  # 延迟事件（事件时间早于当前水印）
        (base_time + timedelta(minutes=8), "订单_005"),
        (base_time + timedelta(minutes=4), "订单_006"),  # 延迟事件
        (base_time + timedelta(minutes=12), "订单_007"),
        (base_time + timedelta(minutes=6), "订单_008"),  # 可能按时或延迟，取决于水印
    ]

    print(f"配置: 允许最大延迟 = {processor.max_lateness.total_seconds() / 60} 分钟\n")
    print("事件处理结果:")

    for event_time, data in events:
        is_on_time, message = processor.process_event(event_time, data)
        status = "✓" if is_on_time else "✗"
        print(f"  {status} {message}")

    print(f"\n统计:")
    print(f"  按时事件: {len(processor.processed_events)}")
    print(f"  延迟事件: {len(processor.late_events)}")

    if processor.late_events:
        print(f"\n延迟事件详情:")
        for event_time, data in sorted(processor.late_events):
            print(f"  - {data}: {event_time}")


def demonstrate_watermark_calculation():
    """演示水印计算过程"""
    print("\n=== 水印计算详细过程 ===\n")

    max_lateness = timedelta(minutes=3)
    current_max_event_time = None
    watermark = None

    # 按到达顺序的事件时间
    event_times = [
        datetime(2026, 5, 3, 10, 1, 0),  # 10:01
        datetime(2026, 5, 3, 10, 3, 0),  # 10:03
        datetime(2026, 5, 3, 10, 7, 0),  # 10:07
        datetime(2026, 5, 3, 10, 2, 0),  # 10:02 (延迟)
        datetime(2026, 5, 3, 10, 8, 0),  # 10:08
    ]

    print("事件到达顺序与水印更新:")
    for i, event_time in enumerate(event_times):
        # 更新最大事件时间
        if current_max_event_time is None or event_time > current_max_event_time:
            old_max = current_max_event_time
            current_max_event_time = event_time
            max_updated = True
        else:
            max_updated = False

        # 计算新水印
        new_watermark = current_max_event_time - max_lateness

        print(f"事件 {i+1}: 时间={event_time.strftime('%H:%M')}")
        if max_updated:
            print(f"  → 最大事件时间更新: {old_max.strftime('%H:%M') if old_max else 'None'} → {current_max_event_time.strftime('%H:%M')}")
        print(f"  → 水印更新: {watermark.strftime('%H:%M') if watermark else 'None'} → {new_watermark.strftime('%H:%M')}")

        watermark = new_watermark
        print()


if __name__ == "__main__":
    simulate_watermark_processing()
    demonstrate_watermark_calculation()