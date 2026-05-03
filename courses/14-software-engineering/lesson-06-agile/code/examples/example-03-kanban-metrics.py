#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：看板指标计算
从任务完成数据计算看板指标：周期时间、吞吐量、在制品数量（WIP）
"""

from typing import List, Dict, Tuple
from datetime import datetime, timedelta


def calculate_cycle_time(
    tasks: List[Dict]
) -> Tuple[float, List[int]]:
    """
    计算周期时间（任务从开始到完成的时间）

    :param tasks: 任务列表，每个任务包含 'start_date', 'end_date'
    :return: (平均周期时间, 所有任务的周期时间列表)
    """
    cycle_times = []

    for task in tasks:
        if task['start_date'] and task['end_date']:
            start = datetime.fromisoformat(task['start_date'])
            end = datetime.fromisoformat(task['end_date'])
            cycle_time_days = (end - start).days
            cycle_times.append(cycle_time_days)

    avg_cycle_time = sum(cycle_times) / len(cycle_times) if cycle_times else 0
    return avg_cycle_time, cycle_times


def calculate_throughput(
    tasks: List[Dict],
    period_start: str,
    period_end: str
) -> float:
    """
    计算吞吐量（在指定时间段内完成的任务数量）

    :param tasks: 任务列表
    :param period_start: 统计周期开始日期 (ISO格式)
    :param period_end: 统计周期结束日期 (ISO格式)
    :return: 平均每日吞吐量
    """
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


def calculate_wip(
    tasks: List[Dict],
    date_point: str
) -> int:
    """
    计算指定日期的在制品数量（WIP - Work In Progress）

    :param tasks: 任务列表，每个任务包含 'start_date', 'end_date'
    :param date_point: 查询日期 (ISO格式)
    :return: 在制品数量
    """
    query_date = datetime.fromisoformat(date_point)
    wip_count = 0

    for task in tasks:
        start_dt = datetime.fromisoformat(task['start_date']) if task['start_date'] else None
        end_dt = datetime.fromisoformat(task['end_date']) if task['end_date'] else None

        # 任务在查询日期处于进行中状态
        if start_dt and start_dt <= query_date and (not end_dt or end_dt > query_date):
            wip_count += 1

    return wip_count


def calculate_cumulative_flow(
    tasks: List[Dict],
    start_date: str,
    end_date: str
) -> Dict[str, List[int]]:
    """
    计算累积流图数据

    :param tasks: 任务列表
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 包含各状态任务数量的字典
    """
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    # 生成日期范围
    current = start_dt
    dates = []
    while current <= end_dt:
        dates.append(current.isoformat()[:10])  # YYYY-MM-DD
        current += timedelta(days=1)

    # 初始化累积数据
    cumulative_data = {
        'todo': [],
        'in_progress': [],
        'done': []
    }

    for date_str in dates:
        date_dt = datetime.fromisoformat(date_str)

        todo_count = 0
        in_progress_count = 0
        done_count = 0

        for task in tasks:
            start_dt_task = datetime.fromisoformat(task['start_date']) if task['start_date'] else None
            end_dt_task = datetime.fromisoformat(task['end_date']) if task['end_date'] else None

            if end_dt_task and end_dt_task <= date_dt:
                done_count += 1
            elif start_dt_task and start_dt_task <= date_dt:
                in_progress_count += 1
            else:
                todo_count += 1

        cumulative_data['todo'].append(todo_count)
        cumulative_data['in_progress'].append(in_progress_count)
        cumulative_data['done'].append(done_count)

    return cumulative_data


def main():
    """主函数：演示看板指标计算"""
    # 模拟任务数据
    tasks_data = [
        {'id': 'TASK-001', 'start_date': '2026-04-01T09:00:00', 'end_date': '2026-04-03T16:00:00'},
        {'id': 'TASK-002', 'start_date': '2026-04-02T10:00:00', 'end_date': '2026-04-05T14:00:00'},
        {'id': 'TASK-003', 'start_date': '2026-04-03T08:00:00', 'end_date': '2026-04-04T17:00:00'},
        {'id': 'TASK-004', 'start_date': '2026-04-04T09:00:00', 'end_date': '2026-04-07T11:00:00'},
        {'id': 'TASK-005', 'start_date': '2026-04-05T11:00:00', 'end_date': '2026-04-06T15:00:00'},
        {'id': 'TASK-006', 'start_date': '2026-04-06T10:00:00', 'end_date': None},  # 进行中
        {'id': 'TASK-007', 'start_date': '2026-04-07T09:00:00', 'end_date': None},  # 进行中
    ]

    print("看板指标计算演示")
    print("=" * 50)

    # 计算周期时间
    avg_cycle, all_cycles = calculate_cycle_time(tasks_data)
    print(f"平均周期时间: {avg_cycle:.1f} 天")
    print(f"各任务周期时间: {all_cycles} 天")

    # 计算吞吐量（4月1日到4月7日）
    throughput = calculate_throughput(tasks_data, '2026-04-01', '2026-04-07')
    print(f"平均每日吞吐量: {throughput:.2f} 个任务/天")

    # 计算WIP（4月6日）
    wip_4_6 = calculate_wip(tasks_data, '2026-04-06')
    print(f"4月6日在制品数量 (WIP): {wip_4_6}")

    # 计算WIP（4月7日）
    wip_4_7 = calculate_wip(tasks_data, '2026-04-07')
    print(f"4月7日在制品数量 (WIP): {wip_4_7}")

    # 计算累积流图数据
    flow_data = calculate_cumulative_flow(tasks_data, '2026-04-01', '2026-04-07')
    print("\n累积流图数据 (4月1日-4月7日):")
    print("日期\t待办\t进行中\t已完成")
    for i, date in enumerate(['4/1', '4/2', '4/3', '4/4', '4/5', '4/6', '4/7']):
        print(f"{date}\t{flow_data['todo'][i]}\t{flow_data['in_progress'][i]}\t{flow_data['done'][i]}")


if __name__ == "__main__":
    main()