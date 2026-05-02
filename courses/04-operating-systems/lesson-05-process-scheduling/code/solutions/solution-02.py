#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答：实现抢占式优先级调度算法

抢占式优先级调度允许高优先级进程中断正在执行的低优先级进程。
"""

from typing import List, Tuple
import heapq


class Process:
    def __init__(self, pid: int, arrival_time: int, burst_time: int, priority: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def preemptive_priority_scheduling(processes: List[Process]) -> Tuple[List[Process], float, float]:
    """抢占式优先级调度算法"""
    from copy import deepcopy
    processes = deepcopy(processes)

    current_time = 0
    completed = 0
    n = len(processes)
    ready_queue = []

    # 当前正在执行的进程
    current_process = None

    total_turnaround_time = 0
    total_waiting_time = 0

    print("抢占式优先级调度过程:")
    print(f"{'时间':<6} {'事件':<25} {'就绪队列':<20}")
    print("-" * 55)

    while completed < n:
        # 将所有新到达的进程加入就绪队列
        for process in processes:
            if (process.arrival_time <= current_time and
                process.remaining_time > 0 and
                process not in [p[2] for p in ready_queue] and
                process != current_process):
                heapq.heappush(ready_queue, (process.priority, process.pid, process))

        if current_process is None and not ready_queue:
            # CPU空闲，跳到下一个进程到达时间
            next_arrival = min(p.arrival_time for p in processes if p.remaining_time > 0)
            current_time = next_arrival
            continue

        # 检查是否需要抢占
        if ready_queue:
            highest_priority_process = ready_queue[0][2]
            if (current_process is None or
                highest_priority_process.priority < current_process.priority):
                # 发生抢占或开始新进程
                if current_process is not None:
                    # 将当前进程放回就绪队列
                    heapq.heappush(ready_queue, (current_process.priority, current_process.pid, current_process))

                # 取出最高优先级进程
                _, _, current_process = heapq.heappop(ready_queue)
                print(f"{current_time:<6} 开始执行P{current_process.pid} "
                      f"{[f'P{p[1]}' for p in ready_queue]}")

        # 执行一个时间单位
        if current_process:
            current_process.remaining_time -= 1
            current_time += 1

            # 检查是否有新进程到达
            for process in processes:
                if (process.arrival_time == current_time and
                    process.remaining_time > 0 and
                    process not in [p[2] for p in ready_queue] and
                    process != current_process):
                    heapq.heappush(ready_queue, (process.priority, process.pid, process))

            # 检查当前进程是否完成
            if current_process.remaining_time == 0:
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

                total_turnaround_time += current_process.turnaround_time
                total_waiting_time += current_process.waiting_time
                completed += 1

                print(f"{current_time:<6} P{current_process.pid}完成 "
                      f"{[f'P{p[1]}' for p in ready_queue]}")
                current_process = None

    avg_turnaround_time = total_turnaround_time / n
    avg_waiting_time = total_waiting_time / n

    return processes, avg_turnaround_time, avg_waiting_time


def main():
    processes = [
        Process(1, 0, 8, 3),
        Process(2, 1, 4, 1),
        Process(3, 2, 9, 4),
        Process(4, 3, 5, 2),
    ]

    scheduled_processes, avg_tat, avg_wt = preemptive_priority_scheduling(processes)

    print(f"\n性能统计:")
    print(f"平均周转时间: {avg_tat:.2f}")
    print(f"平均等待时间: {avg_wt:.2f}")


if __name__ == "__main__":
    main()