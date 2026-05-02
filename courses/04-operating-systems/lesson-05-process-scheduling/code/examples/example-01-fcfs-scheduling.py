#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进程调度算法示例1：FCFS (First Come First Serve) 先来先服务

FCFS是最简单的调度算法，按照进程到达的顺序依次执行。
优点：实现简单，公平性好
缺点：可能导致长进程阻塞短进程（Convoy Effect）
"""

from typing import List, Tuple


class Process:
    """进程类，包含进程ID、到达时间和执行时间"""
    def __init__(self, pid: int, arrival_time: int, burst_time: int):
        self.pid = pid                    # 进程ID
        self.arrival_time = arrival_time  # 到达时间
        self.burst_time = burst_time      # 执行时间（CPU burst time）
        self.completion_time = 0         # 完成时间
        self.turnaround_time = 0         # 周转时间
        self.waiting_time = 0            # 等待时间


def fcfs_scheduling(processes: List[Process]) -> Tuple[List[Process], float, float]:
    """
    FCFS调度算法实现

    Args:
        processes: 进程列表

    Returns:
        tuple: (调度后的进程列表, 平均周转时间, 平均等待时间)
    """
    # 按照到达时间排序（先来先服务）
    processes.sort(key=lambda p: p.arrival_time)

    current_time = 0
    total_turnaround_time = 0
    total_waiting_time = 0

    print("FCFS调度过程:")
    print(f"{'PID':<5} {'到达时间':<8} {'执行时间':<8} {'完成时间':<8} {'周转时间':<8} {'等待时间':<8}")
    print("-" * 60)

    for process in processes:
        # 如果当前时间小于进程到达时间，CPU空闲到进程到达
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        # 计算完成时间
        process.completion_time = current_time + process.burst_time
        # 计算周转时间 = 完成时间 - 到达时间
        process.turnaround_time = process.completion_time - process.arrival_time
        # 计算等待时间 = 周转时间 - 执行时间
        process.waiting_time = process.turnaround_time - process.burst_time

        # 更新当前时间
        current_time = process.completion_time

        # 累加统计信息
        total_turnaround_time += process.turnaround_time
        total_waiting_time += process.waiting_time

        print(f"{process.pid:<5} {process.arrival_time:<8} {process.burst_time:<8} "
              f"{process.completion_time:<8} {process.turnaround_time:<8} {process.waiting_time:<8}")

    avg_turnaround_time = total_turnaround_time / len(processes)
    avg_waiting_time = total_waiting_time / len(processes)

    return processes, avg_turnaround_time, avg_waiting_time


def main():
    """主函数：演示FCFS调度算法"""
    # 创建示例进程
    processes = [
        Process(1, 0, 8),   # PID=1, 到达时间=0, 执行时间=8
        Process(2, 1, 4),   # PID=2, 到达时间=1, 执行时间=4
        Process(3, 2, 9),   # PID=3, 到达时间=2, 执行时间=9
        Process(4, 3, 5),   # PID=4, 到达时间=3, 执行时间=5
    ]

    # 执行FCFS调度
    scheduled_processes, avg_tat, avg_wt = fcfs_scheduling(processes)

    print("\n性能统计:")
    print(f"平均周转时间: {avg_tat:.2f}")
    print(f"平均等待时间: {avg_wt:.2f}")


if __name__ == "__main__":
    main()