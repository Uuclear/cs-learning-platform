#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01: 窗口模拟

此文件包含窗口模拟的参考实现
"""

from datetime import datetime, timedelta
from typing import List, Dict


class Event:
    def __init__(self, event_time: datetime, data: str):
        self.event_time = event_time
        self.data = data


def tumbling_window(events: List[Event], window_size_minutes: int) -> Dict[str, List[Event]]:
    """滚动窗口实现"""
    windows = {}
    for event in events:
        window_start = event.event_time.replace(
            minute=(event.event_time.minute // window_size_minutes) * window_size_minutes,
            second=0, microsecond=0
        )
        window_key = window_start.strftime("%Y-%m-%d %H:%M")
        if window_key not in windows:
            windows[window_key] = []
        windows[window_key].append(event)
    return windows


def sliding_window(events: List[Event], window_size_minutes: int, slide_interval_minutes: int) -> Dict[str, List[Event]]:
    """滑动窗口实现"""
    if not events:
        return {}

    windows = {}
    min_time = min(e.event_time for e in events)
    max_time = max(e.event_time for e in events)

    current_start = min_time.replace(second=0, microsecond=0)
    while current_start <= max_time:
        window_end = current_start + timedelta(minutes=window_size_minutes)
        window_events = [e for e in events if current_start <= e.event_time < window_end]
        if window_events:
            window_key = f"{current_start.strftime('%Y-%m-%d %H:%M')} - {window_end.strftime('%H:%M')}"
            windows[window_key] = window_events
        current_start += timedelta(minutes=slide_interval_minutes)

    return windows


def session_window(events: List[Event], session_gap_minutes: int) -> Dict[str, List[Event]]:
    """会话窗口实现"""
    if not events:
        return {}

    sorted_events = sorted(events, key=lambda e: e.event_time)
    windows = {}
    current_session = [sorted_events[0]]
    session_start = sorted_events[0].event_time
    session_end = sorted_events[0].event_time
    gap = timedelta(minutes=session_gap_minutes)

    for event in sorted_events[1:]:
        if event.event_time - session_end <= gap:
            current_session.append(event)
            session_end = event.event_time
        else:
            key = f"Session_{session_start.strftime('%Y%m%d_%H%M')}_{session_end.strftime('%H%M')}"
            windows[key] = current_session.copy()
            current_session = [event]
            session_start = event.event_time
            session_end = event.event_time

    if current_session:
        key = f"Session_{session_start.strftime('%Y%m%d_%H%M')}_{session_end.strftime('%H%M')}"
        windows[key] = current_session

    return windows