#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答：实现SJF（最短作业优先）调度算法

SJF选择执行时间最短的进程先执行，可以最小化平均等待时间。
"""

from typing import List, Tuple


class Process:
    def __init__(self, pid: int, arrival_time: int, burst_time: int):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def sjf_scheduling(processes: List[Process]) -> Tuple[List[Process], float, float]:
    """非抢占式SJF调度算法"""
    from copy import deepcopy
    processes = deepcopy(processes)

    current_time = 0
    completed = 0
    n = len(processes)

    total_turnaround_time = 0
    total_waiting_time = 0

    print("SJF调度过程:")
    print(f"{'PID':<5} {'到达时间':<8} {'执行时间':<8} {'完成时间':<8} {'周转时间':<8} {'等待时间':<8}")
    print("-" * 60)

    while completed < n:
        # 找出所有已到达且未完成的进程中执行时间最短的
        available_processes = [
            p for p in processes
            if p.arrival_time <= current_time and p.completion_time == 0
        ]

        if not available_processes:
            # CPU空闲，跳到下一个进程到达时间
            next_arrival = min(p.arrival_time for p in processes if p.completion_time == 0)
            current_time = next_arrival
            continue

        # 选择执行时间最短的进程
        shortest_process = min(available_processes, key=lambda p: p.burst_time)

        if current_time < shortest_process.arrival_time:
            current_time = shortest_process.arrival_time

        shortest_process.completion_time = current_time + shortest_process.burst_time
        shortest_process.turnaround_time = shortest_process.completion_time - shortest_process.arrival_time
        shortest_process.waiting_time = shortest_process.turnaround_time - shortest_process.burst_time

        current_time = shortest_process.completion_time

        total_turnaround_time += shortest_process.turnaround_time
        total_waiting_time += shortest_process.waiting_time
        completed += 1

        print(f"{shortest_process.pid:<5} {shortest_process.arrival_time:<8} {shortest_process.burst_time:<8} "
              f"{shortest_process.completion_time:<8} {shortest_process.turnaround_time:<8} {shortest_process.waiting_time:<8}")

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

    scheduled_processes, avg_tat, avg_wt = sjf_scheduling(processes)

    print(f"\n性能统计:")
    print(f"平均周转时间: {avg_tat:.2f}")
    print(f"平均等待时间: {avg_wt:.2f}")


if __name__ == "__main__":
    main()