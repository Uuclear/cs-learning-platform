#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 03: 完整流式处理管道

此文件包含完整流式处理管道的参考实现
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class StreamEvent:
    def __init__(self, event_time: datetime, processing_time: datetime, user_id: str, action: str, value: float = 0.0):
        self.event_time = event_time
        self.processing_time = processing_time
        self.user_id = user_id
        self.action = action
        self.value = value


class StateManager:
    def __init__(self):
        self.user_states = {}

    def get_state(self, user_id: str, default: Any = None) -> Any:
        return self.user_states.get(user_id, default)

    def update_state(self, user_id: str, new_state: Any):
        self.user_states[user_id] = new_state


class StreamProcessor:
    def __init__(self, window_size_minutes: int = 5, max_lateness_minutes: int = 2):
        self.window_size = timedelta(minutes=window_size_minutes)
        self.max_lateness = timedelta(minutes=max_lateness_minutes)
        self.state_manager = StateManager()
        self.current_max_event_time = None
        self.watermark = None
        self.results = []

    def update_watermark(self, event_time: datetime):
        if self.current_max_event_time is None or event_time > self.current_max_event_time:
            self.current_max_event_time = event_time
            self.watermark = event_time - self.max_lateness

    def get_window_key(self, event_time: datetime) -> str:
        window_start = event_time.replace(
            minute=(event_time.minute // 5) * 5,
            second=0, microsecond=0
        )
        return window_start.strftime("%Y-%m-%d %H:%M")

    def process_event(self, event: StreamEvent) -> Optional[Dict[str, Any]]:
        self.update_watermark(event.event_time)

        if self.watermark and event.event_time < self.watermark:
            return None  # 延迟事件丢弃

        current_state = self.state_manager.get_state(event.user_id, {"total_value": 0.0, "event_count": 0})
        current_state["total_value"] += event.value
        current_state["event_count"] += 1
        current_state["last_event_time"] = event.event_time
        self.state_manager.update_state(event.user_id, current_state)

        # 简化的窗口触发逻辑
        if len(self.results) == 0 or (len(self.results) + 1) % 3 == 0:
            result = {
                "window_end": event.event_time.strftime("%Y-%m-%d %H:%M"),
                "user_count": len(self.state_manager.user_states),
                "total_events": sum(state["event_count"] for state in self.state_manager.user_states.values()),
                "total_value": sum(state["total_value"] for state in self.state_manager.user_states.values()),
            }
            self.results.append(result)
            return result
        return None