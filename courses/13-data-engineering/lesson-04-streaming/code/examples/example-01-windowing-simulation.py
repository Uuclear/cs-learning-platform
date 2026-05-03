#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
流式处理窗口模拟示例

本示例演示三种主要的窗口类型：
1. 滚动窗口 (Tumbling Windows) - 不重叠的固定大小窗口
2. 滑动窗口 (Sliding Windows) - 重叠的固定大小窗口
3. 会话窗口 (Session Windows) - 基于活动间隔的动态窗口
"""

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any
import time


class Event:
    """事件类，包含事件时间和数据"""
    def __init__(self, event_time: datetime, data: str):
        self.event_time = event_time
        self.data = data

    def __str__(self):
        return f"Event(time={self.event_time}, data='{self.data}')"


def simulate_tumbling_window(events: List[Event], window_size_minutes: int) -> Dict[str, List[Event]]:
    """
    模拟滚动窗口处理

    Args:
        events: 事件列表
        window_size_minutes: 窗口大小（分钟）

    Returns:
        按窗口键分组的事件字典
    """
    windows = {}
    window_size = timedelta(minutes=window_size_minutes)

    for event in events:
        # 计算窗口开始时间（向下取整到窗口边界）
        window_start = event.event_time.replace(
            minute=(event.event_time.minute // window_size_minutes) * window_size_minutes,
            second=0, microsecond=0
        )
        window_key = window_start.strftime("%Y-%m-%d %H:%M")

        if window_key not in windows:
            windows[window_key] = []
        windows[window_key].append(event)

    return windows


def simulate_sliding_window(events: List[Event], window_size_minutes: int, slide_interval_minutes: int) -> Dict[str, List[Event]]:
    """
    模拟滑动窗口处理

    Args:
        events: 事件列表
        window_size_minutes: 窗口大小（分钟）
        slide_interval_minutes: 滑动间隔（分钟）

    Returns:
        按窗口键分组的事件字典
    """
    windows = {}
    window_size = timedelta(minutes=window_size_minutes)
    slide_interval = timedelta(minutes=slide_interval_minutes)

    if not events:
        return windows

    # 找到最早和最晚的事件时间
    min_time = min(e.event_time for e in events)
    max_time = max(e.event_time for e in events)

    # 从最早时间开始，按滑动间隔创建窗口
    current_start = min_time.replace(second=0, microsecond=0)
    while current_start <= max_time:
        window_end = current_start + window_size
        window_key = f"{current_start.strftime('%Y-%m-%d %H:%M')} - {window_end.strftime('%H:%M')}"

        # 收集属于此窗口的事件
        window_events = [e for e in events if current_start <= e.event_time < window_end]
        if window_events:
            windows[window_key] = window_events

        current_start += timedelta(minutes=slide_interval_minutes)

    return windows


def simulate_session_window(events: List[Event], session_gap_minutes: int) -> Dict[str, List[Event]]:
    """
    模拟会话窗口处理

    Args:
        events: 事件列表（应按时间排序）
        session_gap_minutes: 会话间隔（分钟），超过此间隔认为是新会话

    Returns:
        按会话键分组的事件字典
    """
    if not events:
        return {}

    # 确保事件按时间排序
    sorted_events = sorted(events, key=lambda e: e.event_time)
    windows = {}
    current_session_events = [sorted_events[0]]
    session_start = sorted_events[0].event_time
    session_end = sorted_events[0].event_time
    session_gap = timedelta(minutes=session_gap_minutes)

    for event in sorted_events[1:]:
        if event.event_time - session_end <= session_gap:
            # 属于当前会话
            current_session_events.append(event)
            session_end = event.event_time
        else:
            # 开始新会话
            session_key = f"Session_{session_start.strftime('%Y%m%d_%H%M')}_{session_end.strftime('%H%M')}"
            windows[session_key] = current_session_events.copy()

            # 重置会话
            current_session_events = [event]
            session_start = event.event_time
            session_end = event.event_time

    # 添加最后一个会话
    if current_session_events:
        session_key = f"Session_{session_start.strftime('%Y%m%d_%H%M')}_{session_end.strftime('%H%M')}"
        windows[session_key] = current_session_events

    return windows


def main():
    """主函数：演示三种窗口类型"""
    print("=== 流式处理窗口模拟演示 ===\n")

    # 创建示例事件（模拟用户点击事件）
    base_time = datetime(2026, 5, 3, 10, 0, 0)
    events = [
        Event(base_time + timedelta(minutes=2), "click_button_A"),
        Event(base_time + timedelta(minutes=5), "view_product_X"),
        Event(base_time + timedelta(minutes=8), "add_to_cart"),
        Event(base_time + timedelta(minutes=12), "click_button_B"),
        Event(base_time + timedelta(minutes=15), "checkout"),
        Event(base_time + timedelta(minutes=25), "click_home"),  # 新会话开始
        Event(base_time + timedelta(minutes=28), "search_item"),
        Event(base_time + timedelta(minutes=32), "view_product_Y"),
    ]

    print("原始事件序列:")
    for i, event in enumerate(events):
        print(f"  {i+1}. {event}")
    print()

    # 1. 滚动窗口（5分钟窗口）
    print("1. 滚动窗口 (5分钟):")
    tumbling_windows = simulate_tumbling_window(events, 5)
    for window_key, window_events in sorted(tumbling_windows.items()):
        print(f"   窗口 [{window_key}]: {len(window_events)} 个事件")
        for event in window_events:
            print(f"     - {event}")
    print()

    # 2. 滑动窗口（10分钟窗口，5分钟滑动）
    print("2. 滑动窗口 (10分钟窗口，5分钟滑动):")
    sliding_windows = simulate_sliding_window(events, 10, 5)
    for window_key, window_events in sorted(sliding_windows.items()):
        print(f"   窗口 [{window_key}]: {len(window_events)} 个事件")
        for event in window_events:
            print(f"     - {event}")
    print()

    # 3. 会话窗口（10分钟间隔）
    print("3. 会话窗口 (10分钟间隔):")
    session_windows = simulate_session_window(events, 10)
    for session_key, session_events in sorted(session_windows.items()):
        print(f"   {session_key}: {len(session_events)} 个事件")
        for event in session_events:
            print(f"     - {event}")


if __name__ == "__main__":
    main()