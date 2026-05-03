#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 02: 水印模拟

此文件包含水印机制的参考实现
"""

from datetime import datetime, timedelta
from typing import List, Tuple


class WatermarkProcessor:
    def __init__(self, max_lateness_minutes: int):
        self.max_lateness = timedelta(minutes=max_lateness_minutes)
        self.current_max_event_time = None
        self.watermark = None
        self.late_events = []
        self.processed_events = []

    def update_watermark(self, event_time: datetime) -> datetime:
        if self.current_max_event_time is None or event_time > self.current_max_event_time:
            self.current_max_event_time = event_time
        self.watermark = self.current_max_event_time - self.max_lateness
        return self.watermark

    def process_event(self, event_time: datetime, data: str) -> Tuple[bool, str]:
        current_watermark = self.update_watermark(event_time)

        if event_time >= current_watermark:
            self.processed_events.append((event_time, data))
            return True, "按时处理"
        else:
            self.late_events.append((event_time, data))
            return False, "延迟事件"


def calculate_watermark(event_times: List[datetime], max_lateness_minutes: int) -> List[datetime]:
    """计算水印序列"""
    max_lateness = timedelta(minutes=max_lateness_minutes)
    current_max = None
    watermarks = []

    for event_time in event_times:
        if current_max is None or event_time > current_max:
            current_max = event_time
        watermark = current_max - max_lateness
        watermarks.append(watermark)

    return watermarks