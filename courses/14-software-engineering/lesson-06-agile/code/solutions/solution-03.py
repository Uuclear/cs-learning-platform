#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：看板指标实现
"""

from typing import List, Dict, Tuple
from datetime import datetime


def calculate_cycle_time(tasks: List[Dict]) -> Tuple[float, List[int]]:
    cycle_times = []

    for task in tasks:
        if task['start_date'] and task['end_date']:
            start = datetime.fromisoformat(task['start_date'])
            end = datetime.fromisoformat(task['end_date'])
            cycle_time_days = (end - start).days
            cycle_times.append(cycle_time_days)

    avg_cycle_time = sum(cycle_times) / len(cycle_times) if cycle_times else 0
    return avg_cycle_time, cycle_times


def calculate_throughput(tasks: List[Dict], period_start: str, period_end: str) -> float:
    period_start_dt = datetime.fromisoformat(period_start)
    period_end_dt = datetime.fromisoformat(period_end)
    period_days = (period_end_dt - period_start_dt).days

    if period_days <= 0:
        return 0.0

    completed_tasks = 0
    for task in tasks:
        if task['end_date']:
            end_dt = datetime.fromisoformat(task['end_date'])
            if period_start_dt <= end_dt <= period_end_dt:
                completed_tasks += 1

    return completed_tasks / period_days


def calculate_wip(tasks: List[Dict], date_point: str) -> int:
    query_date = datetime.fromisoformat(date_point)
    wip_count = 0

    for task in tasks:
        start_dt = datetime.fromisoformat(task['start_date']) if task['start_date'] else None
        end_dt = datetime.fromisoformat(task['end_date']) if task['end_date'] else None

        if start_dt and start_dt <= query_date and (not end_dt or end_dt > query_date):
            wip_count += 1

    return wip_count