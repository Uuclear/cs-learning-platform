#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：燃尽图实现
"""

from typing import List, Tuple


def calculate_burndown_data(
    total_story_points: int,
    daily_progress: List[int],
    sprint_days: int = 10
) -> Tuple[List[int], List[float]]:
    if len(daily_progress) > sprint_days:
        daily_progress = daily_progress[:sprint_days]

    while len(daily_progress) < sprint_days:
        daily_progress.append(0)

    actual_remaining = [total_story_points]
    cumulative_done = 0

    for day_progress in daily_progress:
        cumulative_done += day_progress
        remaining = max(0, total_story_points - cumulative_done)
        actual_remaining.append(remaining)

    ideal_remaining = []
    for day in range(sprint_days + 1):
        ideal_points = total_story_points * (1 - day / sprint_days)
        ideal_remaining.append(ideal_points)

    return actual_remaining, ideal_remaining