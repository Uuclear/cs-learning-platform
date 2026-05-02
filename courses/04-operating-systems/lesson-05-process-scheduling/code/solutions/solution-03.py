#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答：多级反馈队列调度算法（MLFQ）

MLFQ使用多个优先级队列，新进程进入最高优先级队列，
如果时间片用完还未完成，则降级到下一级队列。
"""

from typing import List, Tuple, Deque
from collections import deque
import heapq


class Process:
    def __init__(self, pid: int, arrival_time: int, burst_time: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.current_queue = 0  # 当前所在队列级别（0为最高优先级）


def mlfq_scheduling(processes: List[Process], num_queues: int = 3, quanta: List[int] = None) -> Tuple[List[Process], float, float]:
    """
    多级反馈队列调度算法

    Args:
        processes: 进程列表
        num_queues: 队列数量
        quanta: 每个队列的时间片大小
    """
    from copy import deepcopy
    processes = deepcopy(processes)

    if quanta is None:
        quanta = [2, 4, 8]  # 默认时间片：高优先级队列时间片短

    # 初始化队列（0为最高优先级）
    queues: List[Deque[Process]] = [deque() for _ in range(num_queues)]

    current_time = 0
    completed = 0
    n = len(processes)
    process_index = 0

    total_turnaround_time = 0
    total_waiting_time = 0

    print(f"MLFQ调度过程 ({num_queues}级队列):")
    print(f"{'时间':<6} {'事件':<30} {'队列状态':<30}")
    print("-" * 70)

    while completed < n:
        # 将新到达的进程加入最高优先级队列
        while process_index < n and processes[process_index].arrival_time <= current_time:
            processes[process_index].current_queue = 0
            queues[0].append(processes[process_index])
            process_index += 1

        # 找到最高优先级的非空队列
        current_queue_idx = -1
        for i in range(num_queues):
            if queues[i]:
                current_queue_idx = i
                break

        if current_queue_idx == -1:
            # CPU空闲
            if process_index < n:
                current_time = processes[process_index].arrival_time
            continue

        # 从当前队列取出进程
        current_process = queues[current_queue_idx].popleft()
        quantum = quanta[current_queue_idx] if current_queue_idx < len(quanta) else quanta[-1]

        # 执行时间片或剩余时间（取较小值）
        execution_time = min(quantum, current_process.remaining_time)
        print(f"{current_time:<6} P{current_process.pid}在Q{current_queue_idx}执行({execution_time}) "
              f"{[(f'Q{i}', list(q)) for i, q in enumerate(queues) if q]}")

        current_time += execution_time
        current_process.remaining_time -= execution_time

        # 将在此期间到达的新进程加入最高优先级队列
        while process_index < n and processes[process_index].arrival_time <= current_time:
            processes[process_index].current_queue = 0
            queues[0].append(processes[process_index])
            process_index += 1

        if current_process.remaining_time == 0:
            # 进程完成
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

            total_turnaround_time += current_process.turnaround_time
            total_waiting_time += current_process.waiting_time
            completed += 1

            print(f"{current_time:<6} P{current_process.pid}完成 "
                  f"{[(f'Q{i}', list(q)) for i, q in enumerate(queues) if q]}")
        else:
            # 进程未完成，降级到下一级队列（如果还有更低优先级队列）
            if current_queue_idx < num_queues - 1:
                current_process.current_queue = current_queue_idx + 1
                queues[current_queue_idx + 1].append(current_process)
            else:
                # 已经在最低优先级队列，继续留在该队列
                queues[current_queue_idx].append(current_process)

    avg_turnaround_time = total_turnaround_time / n
    avg_waiting_time = total_waiting_time / n

    return processes, avg_turnaround_time, avg_waiting_time


def main():
    processes = [
        Process(1, 0, 8),
        Process(2, 1, 4),
        Process(3, 2, 9),
        Process(4, 3, 5),
    ]

    scheduled_processes, avg_tat, avg_wt = mlfq_scheduling(processes)

    print(f"\n性能统计:")
    print(f"平均周转时间: {avg_tat:.2f}")
    print(f"平均等待时间: {avg_wt:.2f}")


if __name__ == "__main__":
    main()