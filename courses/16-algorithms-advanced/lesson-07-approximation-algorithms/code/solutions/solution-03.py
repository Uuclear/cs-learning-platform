#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
近似算法解决方案3：作业调度的列表调度算法

这个解决方案实现了作业调度问题的列表调度2-近似算法，
以及LPT（最长处理时间优先）4/3-近似算法。
"""

import random
import heapq

def list_scheduling(jobs, m):
    """
    列表调度算法（2-近似）

    算法思路:
    按任意顺序处理作业，将每个作业分配给当前负载最小的机器

    近似比: 2
    时间复杂度: O(n log m)
    """
    # 初始化m台机器的负载
    machine_loads = [0] * m
    machine_assignments = [[] for _ in range(m)]

    # 使用最小堆跟踪机器负载
    heap = [(0, i) for i in range(m)]
    heapq.heapify(heap)

    for job_id, processing_time in enumerate(jobs):
        # 找到负载最小的机器
        min_load, machine_id = heapq.heappop(heap)

        # 分配作业
        machine_loads[machine_id] += processing_time
        machine_assignments[machine_id].append(job_id)

        # 更新堆
        heapq.heappush(heap, (machine_loads[machine_id], machine_id))

    makespan = max(machine_loads)
    return machine_assignments, makespan

def lpt_scheduling(jobs, m):
    """
    LPT（最长处理时间优先）调度算法（4/3-近似）

    算法思路:
    按处理时间降序排序作业，然后使用列表调度

    近似比: 4/3 - 1/(3m)
    时间复杂度: O(n log n + n log m)
    """
    # 按处理时间降序排序（保持原始索引）
    indexed_jobs = [(processing_time, job_id) for job_id, processing_time in enumerate(jobs)]
    indexed_jobs.sort(reverse=True)

    # 初始化
    machine_loads = [0] * m
    machine_assignments = [[] for _ in range(m)]
    heap = [(0, i) for i in range(m)]
    heapq.heapify(heap)

    for processing_time, job_id in indexed_jobs:
        min_load, machine_id = heapq.heappop(heap)
        machine_loads[machine_id] += processing_time
        machine_assignments[machine_id].append(job_id)
        heapq.heappush(heap, (machine_loads[machine_id], machine_id))

    makespan = max(machine_loads)
    return machine_assignments, makespan

def optimal_scheduling_brute_force(jobs, m):
    """
    小规模作业调度的最优解（暴力搜索）
    时间复杂度: O(m^n)
    """
    if len(jobs) > 10 or m > 4:
        return None, float('inf')

    n = len(jobs)
    best_makespan = float('inf')
    best_assignment = None

    # 枚举所有可能的分配方案
    def backtrack(job_idx, machine_loads, current_assignment):
        nonlocal best_makespan, best_assignment

        if job_idx == n:
            current_makespan = max(machine_loads)
            if current_makespan < best_makespan:
                best_makespan = current_makespan
                best_assignment = current_assignment.copy()
            return

        # 剪枝：如果当前最大负载已经超过最优解，剪枝
        if max(machine_loads) >= best_makespan:
            return

        processing_time = jobs[job_idx]
        for machine_id in range(m):
            machine_loads[machine_id] += processing_time
            current_assignment.append(machine_id)
            backtrack(job_idx + 1, machine_loads, current_assignment)
            current_assignment.pop()
            machine_loads[machine_id] -= processing_time

    backtrack(0, [0] * m, [])
    return best_assignment, best_makespan

def calculate_lower_bound(jobs, m):
    """计算理论下界"""
    total_processing = sum(jobs)
    max_job = max(jobs)
    return max(total_processing / m, max_job)

def test_scheduling_algorithms():
    """测试调度算法"""
    random.seed(42)

    # 测试数据
    jobs = [random.randint(1, 20) for _ in range(15)]
    m = 3

    print("作业调度问题测试:")
    print(f"作业数量: {len(jobs)}")
    print(f"机器数量: {m}")
    print(f"作业处理时间: {jobs}")
    print()

    # 计算理论下界
    lower_bound = calculate_lower_bound(jobs, m)
    print(f"理论下界: {lower_bound:.2f}")
    print()

    # 列表调度
    list_assign, list_makespan = list_scheduling(jobs, m)
    print(f"列表调度结果:")
    print(f"最大完成时间: {list_makespan:.2f}")
    print(f"近似比: {list_makespan/lower_bound:.2f} (理论上限: 2.0)")
    print()

    # LPT调度
    lpt_assign, lpt_makespan = lpt_scheduling(jobs, m)
    print(f"LPT调度结果:")
    print(f"最大完成时间: {lpt_makespan:.2f}")
    print(f"近似比: {lpt_makespan/lower_bound:.2f} (理论上限: {4/3 - 1/(3*m):.2f})")
    print()

    # 最优解（小规模子集）
    small_jobs = jobs[:8]
    optimal_assign, optimal_makespan = optimal_scheduling_brute_force(small_jobs, m)
    if optimal_assign is not None:
        small_lower_bound = calculate_lower_bound(small_jobs, m)
        print(f"最优解（前8个作业）:")
        print(f"最大完成时间: {optimal_makespan:.2f}")
        print(f"列表调度实际近似比: {list_scheduling(small_jobs, m)[1]/optimal_makespan:.2f}")
        print(f"LPT实际近似比: {lpt_scheduling(small_jobs, m)[1]/optimal_makespan:.2f}")

if __name__ == "__main__":
    test_scheduling_algorithms()