#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进程调度算法示例3：Priority Scheduling 优先级调度

优先级调度根据进程的优先级来决定执行顺序，优先级高的进程先执行。
可以是抢占式（Preemptive）或非抢占式（Non-preemptive）。

优点：可以根据进程重要性分配CPU时间
缺点：可能导致低优先级进程饥饿（Starvation）
"""

from typing import List, Tuple
import heapq


class Process:
    """进程类，包含进程ID、到达时间、执行时间和优先级"""
    def __init__(self, pid: int, arrival_time: int, burst_time: int, priority: int):
        self.pid = pid                    # 进程ID
        self.arrival_time = arrival_time  # 到达时间
        self.burst_time = burst_time      # 执行时间
        self.priority = priority          # 优先级（数值越小优先级越高）
        self.remaining_time = burst_time  # 剩余执行时间（用于抢占式）
        self.completion_time = 0         # 完成时间
        self.turnaround_time = 0         # 周转时间
        self.waiting_time = 0            # 等待时间


def priority_scheduling_non_preemptive(processes: List[Process]) -> Tuple[List[Process], float, float]:
    """
    非抢占式优先级调度算法实现

    Args:
        processes: 进程列表

    Returns:
        tuple: (调度后的进程列表, 平均周转时间, 平均等待时间)
    """
    from copy import deepcopy
    processes = deepcopy(processes)

    current_time = 0
    completed = 0
    n = len(processes)
    ready_queue = []  # 使用堆实现优先级队列

    total_turnaround_time = 0
    total_waiting_time = 0

    print("非抢占式优先级调度过程:")
    print(f"{'PID':<5} {'到达时间':<8} {'执行时间':<8} {'优先级':<8} {'完成时间':<8} {'周转时间':<8} {'等待时间':<8}")
    print("-" * 70)

    while completed < n:
        # 将所有新到达的进程加入就绪队列（避免重复添加已完成的进程）
        for process in processes:
            if (process.arrival_time <= current_time and
                process.completion_time == 0 and
                (process.priority, process.pid, process) not in [(p[0], p[1], p[2]) for p in ready_queue]):
                # 使用负的优先级值，因为heapq是最小堆，但我们希望高优先级（数值小）先执行
                heapq.heappush(ready_queue, (process.priority, process.pid, process))

        if not ready_queue:
            # CPU空闲，跳到下一个进程到达时间
            next_arrival = min(p.arrival_time for p in processes if p.completion_time == 0)
            current_time = next_arrival
            continue

        # 取出最高优先级的进程
        _, _, current_process = heapq.heappop(ready_queue)

        # 执行完整个进程
        if current_time < current_process.arrival_time:
            current_time = current_process.arrival_time

        current_process.completion_time = current_time + current_process.burst_time
        current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
        current_process.waiting_time = current_process.turnaround_time - current_process.burst_time

        current_time = current_process.completion_time

        total_turnaround_time += current_process.turnaround_time
        total_waiting_time += current_process.waiting_time
        completed += 1

        print(f"{current_process.pid:<5} {current_process.arrival_time:<8} {current_process.burst_time:<8} "
              f"{current_process.priority:<8} {current_process.completion_time:<8} "
              f"{current_process.turnaround_time:<8} {current_process.waiting_time:<8}")

    avg_turnaround_time = total_turnaround_time / n
    avg_waiting_time = total_waiting_time / n

    return processes, avg_turnaround_time, avg_waiting_time


def main():
    """主函数：演示优先级调度算法"""
    # 创建示例进程（优先级：1最高，10最低）
    processes = [
        Process(1, 0, 8, 3),   # PID=1, 到达时间=0, 执行时间=8, 优先级=3
        Process(2, 1, 4, 1),   # PID=2, 到达时间=1, 执行时间=4, 优先级=1（最高）
        Process(3, 2, 9, 4),   # PID=3, 到达时间=2, 执行时间=9, 优先级=4
        Process(4, 3, 5, 2),   # PID=4, 到达时间=3, 执行时间=5, 优先级=2
    ]

    # 执行非抢占式优先级调度
    scheduled_processes, avg_tat, avg_wt = priority_scheduling_non_preemptive(processes)

    print(f"\n性能统计:")
    print(f"平均周转时间: {avg_tat:.2f}")
    print(f"平均等待时间: {avg_wt:.2f}")


if __name__ == "__main__":
    main()