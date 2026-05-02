#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进程调度算法示例2：Round Robin (RR) 轮转调度

轮转调度是分时系统中最常用的调度算法，每个进程分配固定时间片（quantum），
时间片用完后切换到下一个就绪进程。

优点：响应性好，适合交互式系统
缺点：时间片选择很重要，太小会导致频繁上下文切换，太大则退化为FCFS
"""

from typing import List, Tuple, Deque
from collections import deque


class Process:
    """进程类，包含进程ID、到达时间、执行时间和剩余执行时间"""
    def __init__(self, pid: int, arrival_time: int, burst_time: int):
        self.pid = pid                    # 进程ID
        self.arrival_time = arrival_time  # 到达时间
        self.burst_time = burst_time      # 总执行时间
        self.remaining_time = burst_time  # 剩余执行时间
        self.completion_time = 0         # 完成时间
        self.turnaround_time = 0         # 周转时间
        self.waiting_time = 0            # 等待时间
        self.started = False             # 是否已经开始执行


def round_robin_scheduling(processes: List[Process], quantum: int) -> Tuple[List[Process], float, float]:
    """
    轮转调度算法实现

    Args:
        processes: 进程列表
        quantum: 时间片大小

    Returns:
        tuple: (调度后的进程列表, 平均周转时间, 平均等待时间)
    """
    from copy import deepcopy
    processes = deepcopy(processes)  # 避免修改原始数据

    # 按到达时间排序
    processes.sort(key=lambda p: p.arrival_time)

    ready_queue: Deque[Process] = deque()
    current_time = 0
    completed = 0
    n = len(processes)
    process_index = 0

    # 统计信息
    total_turnaround_time = 0
    total_waiting_time = 0

    print(f"Round Robin调度过程 (时间片={quantum}):")
    print(f"{'时间':<6} {'事件':<20} {'就绪队列':<20}")
    print("-" * 50)

    while completed < n:
        # 将所有已到达的进程加入就绪队列
        while process_index < n and processes[process_index].arrival_time <= current_time:
            ready_queue.append(processes[process_index])
            process_index += 1

        if not ready_queue:
            # CPU空闲，跳到下一个进程到达时间
            if process_index < n:
                current_time = processes[process_index].arrival_time
            continue

        # 取出队首进程
        current_process = ready_queue.popleft()

        if not current_process.started:
            current_process.started = True

        # 执行时间片或剩余时间（取较小值）
        execution_time = min(quantum, current_process.remaining_time)
        print(f"{current_time:<6} 执行P{current_process.pid}({execution_time}单位) "
              f"{[f'P{p.pid}' for p in ready_queue]}")

        current_time += execution_time
        current_process.remaining_time -= execution_time

        # 将所有在此期间到达的进程加入就绪队列
        while process_index < n and processes[process_index].arrival_time <= current_time:
            ready_queue.append(processes[process_index])
            process_index += 1

        # 如果进程完成
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

            total_turnaround_time += current_process.turnaround_time
            total_waiting_time += current_process.waiting_time
            completed += 1
            print(f"{current_time:<6} P{current_process.pid}完成 "
                  f"{[f'P{p.pid}' for p in ready_queue]}")
        else:
            # 进程未完成，重新加入就绪队列末尾
            ready_queue.append(current_process)

    avg_turnaround_time = total_turnaround_time / n
    avg_waiting_time = total_waiting_time / n

    return processes, avg_turnaround_time, avg_waiting_time


def main():
    """主函数：演示轮转调度算法"""
    # 创建示例进程
    processes = [
        Process(1, 0, 8),   # PID=1, 到达时间=0, 执行时间=8
        Process(2, 1, 4),   # PID=2, 到达时间=1, 执行时间=4
        Process(3, 2, 9),   # PID=3, 到达时间=2, 执行时间=9
        Process(4, 3, 5),   # PID=4, 到达时间=3, 执行时间=5
    ]

    # 设置时间片为3
    quantum = 3

    # 执行轮转调度
    scheduled_processes, avg_tat, avg_wt = round_robin_scheduling(processes, quantum)

    print(f"\n性能统计 (时间片={quantum}):")
    print(f"平均周转时间: {avg_tat:.2f}")
    print(f"平均等待时间: {avg_wt:.2f}")


if __name__ == "__main__":
    main()