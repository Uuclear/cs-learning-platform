#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的流式处理管道模拟

本示例演示一个完整的流式处理管道，包含：
1. 数据源模拟
2. 窗口处理
3. 状态管理
4. 水印处理
5. 结果输出
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
import json
import time


class StreamEvent:
    """流式事件"""
    def __init__(self, event_time: datetime, processing_time: datetime, user_id: str, action: str, value: float = 0.0):
        self.event_time = event_time          # 事件发生时间
        self.processing_time = processing_time  # 事件处理时间
        self.user_id = user_id                # 用户ID
        self.action = action                  # 动作类型
        self.value = value                    # 数值（如交易金额）

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_time": self.event_time.isoformat(),
            "processing_time": self.processing_time.isoformat(),
            "user_id": self.user_id,
            "action": self.action,
            "value": self.value
        }

    def __str__(self):
        return f"StreamEvent(user={self.user_id}, action={self.action}, value={self.value}, event_time={self.event_time})"


class StateManager:
    """状态管理器，模拟流式处理中的状态存储"""

    def __init__(self):
        self.user_states = {}  # 用户状态: {user_id: state_data}

    def get_state(self, user_id: str, default: Any = None) -> Any:
        """获取用户状态"""
        return self.user_states.get(user_id, default)

    def update_state(self, user_id: str, new_state: Any):
        """更新用户状态"""
        self.user_states[user_id] = new_state

    def clear_state(self, user_id: str):
        """清除用户状态"""
        if user_id in self.user_states:
            del self.user_states[user_id]


class StreamProcessor:
    """流式处理器"""

    def __init__(self, window_size_minutes: int = 5, max_lateness_minutes: int = 2):
        self.window_size = timedelta(minutes=window_size_minutes)
        self.max_lateness = timedelta(minutes=max_lateness_minutes)
        self.state_manager = StateManager()
        self.current_max_event_time = None
        self.watermark = None
        self.results = []

    def update_watermark(self, event_time: datetime):
        """更新水印"""
        if self.current_max_event_time is None or event_time > self.current_max_event_time:
            self.current_max_event_time = event_time
            self.watermark = event_time - self.max_lateness

    def get_window_key(self, event_time: datetime) -> str:
        """获取窗口键"""
        window_start = event_time.replace(
            minute=(event_time.minute // 5) * 5,  # 5分钟窗口
            second=0, microsecond=0
        )
        return window_start.strftime("%Y-%m-%d %H:%M")

    def process_event(self, event: StreamEvent) -> Optional[Dict[str, Any]]:
        """
        处理单个事件

        Returns:
            如果触发窗口计算，返回结果；否则返回None
        """
        # 更新水印
        self.update_watermark(event.event_time)

        # 检查是否为延迟事件
        if self.watermark and event.event_time < self.watermark:
            print(f"✗ 延迟事件丢弃: {event}")
            return None

        # 更新用户状态（例如：累计交易金额）
        current_state = self.state_manager.get_state(event.user_id, {"total_value": 0.0, "event_count": 0})
        current_state["total_value"] += event.value
        current_state["event_count"] += 1
        current_state["last_event_time"] = event.event_time
        self.state_manager.update_state(event.user_id, current_state)

        # 这里简化了窗口触发逻辑，实际系统会基于水印触发
        # 在真实系统中，当水印超过窗口结束时间时触发计算
        result = self._maybe_trigger_window_computation(event.event_time)
        return result

    def _maybe_trigger_window_computation(self, current_time: datetime) -> Optional[Dict[str, Any]]:
        """
        模拟窗口计算触发（简化版）
        在真实系统中，这会在水印超过窗口边界时触发
        """
        # 简化：每处理几个事件后触发一次计算
        if len(self.results) == 0 or (len(self.results) + 1) % 3 == 0:
            # 计算当前窗口的聚合结果
            window_results = {
                "window_end": current_time.strftime("%Y-%m-%d %H:%M"),
                "user_count": len(self.state_manager.user_states),
                "total_events": sum(state["event_count"] for state in self.state_manager.user_states.values()),
                "total_value": sum(state["total_value"] for state in self.state_manager.user_states.values()),
                "active_users": list(self.state_manager.user_states.keys())
            }
            self.results.append(window_results)
            return window_results
        return None


def generate_sample_events() -> List[StreamEvent]:
    """生成示例事件流"""
    base_time = datetime(2026, 5, 3, 10, 0, 0)
    events = []

    # 模拟用户交易事件
    users = ["user_A", "user_B", "user_C"]
    actions = ["purchase", "click", "view"]

    for i in range(15):
        event_time = base_time + timedelta(minutes=i)
        processing_time = event_time + timedelta(seconds=1)  # 处理时间略晚于事件时间
        user_id = users[i % len(users)]
        action = actions[i % len(actions)]
        value = 10.0 + (i * 5.0) if action == "purchase" else 0.0

        events.append(StreamEvent(event_time, processing_time, user_id, action, value))

    # 添加一些延迟事件
    delayed_events = [
        StreamEvent(base_time + timedelta(minutes=2), base_time + timedelta(minutes=8), "user_D", "purchase", 25.0),
        StreamEvent(base_time + timedelta(minutes=4), base_time + timedelta(minutes=9), "user_E", "click", 0.0),
    ]
    events.extend(delayed_events)

    # 按处理时间排序（模拟真实到达顺序）
    events.sort(key=lambda e: e.processing_time)
    return events


def main():
    """主函数：运行完整的流式处理管道"""
    print("=== 完整流式处理管道模拟 ===\n")

    # 创建流式处理器
    processor = StreamProcessor(window_size_minutes=5, max_lateness_minutes=2)

    # 生成示例事件
    events = generate_sample_events()
    print(f"生成 {len(events)} 个事件进行处理...\n")

    # 处理事件流
    for i, event in enumerate(events):
        print(f"处理事件 {i+1}: {event}")
        result = processor.process_event(event)

        if result:
            print(f"✓ 触发窗口计算: {json.dumps(result, indent=2, ensure_ascii=False)}")
        print()

    # 输出最终统计
    print("=== 最终处理统计 ===")
    print(f"总处理事件数: {len(events)}")
    print(f"窗口计算次数: {len(processor.results)}")
    print(f"活跃用户数: {len(processor.state_manager.user_states)}")

    # 显示最终用户状态
    print("\n最终用户状态:")
    for user_id, state in processor.state_manager.user_states.items():
        print(f"  {user_id}: 总金额={state['total_value']:.2f}, 事件数={state['event_count']}")


if __name__ == "__main__":
    main()