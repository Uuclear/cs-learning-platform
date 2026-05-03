#!/usr/bin/env python3
"""
解决方案 01: 中断与轮询性能对比模拟 - 完整实现

这个完整的解决方案展示了中断驱动和轮询方式的详细对比，
包括CPU使用率测量、内存占用分析和实际应用场景。
"""

import time
import threading
import random
import psutil
import os
from typing import Tuple, List

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        
    def get_cpu_usage(self) -> float:
        """获取CPU使用率"""
        return self.process.cpu_percent(interval=0.1)
    
    def get_memory_usage(self) -> int:
        """获取内存使用量（字节）"""
        return self.process.memory_info().rss

class AdvancedEventSimulator:
    """高级事件模拟器"""
    
    def __init__(self, event_probability=0.01, min_interval=0.05, max_interval=1.0):
        self.event_probability = event_probability
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.events = []
        self.running = False
        
    def start_continuous_simulation(self, duration: float):
        """启动连续事件模拟"""
        self.running = True
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < duration:
            if random.random() < self.event_probability:
                event_time = time.time()
                self.events.append(event_time)
                # 模拟事件处理延迟
                time.sleep(random.uniform(0.001, 0.01))
            time.sleep(random.uniform(self.min_interval, self.max_interval))
            
        self.running = False
        return self.events

def advanced_polling_method(duration: float = 5.0, check_interval: float = 0.001) -> dict:
    """
    高级轮询方法实现
    
    Args:
        duration: 测试持续时间
        check_interval: 轮询间隔
        
    Returns:
        dict: 性能统计数据
    """
    print("=== 高级轮询方法 ===")
    
    monitor = PerformanceMonitor()
    simulator = AdvancedEventSimulator(event_probability=0.005)
    
    start_time = time.time()
    check_count = 0
    cpu_samples = []
    memory_samples = []
    
    # 启动事件生成线程
    event_thread = threading.Thread(target=simulator.start_continuous_simulation, args=(duration,))
    event_thread.start()
    
    event_detected = 0
    last_check_time = start_time
    
    while (time.time() - start_time) < duration:
        current_time = time.time()
        
        # 轮询检查（模拟GPIO读取）
        if simulator.events and current_time >= simulator.events[0]:
            event_detected += 1
            simulator.events.pop(0)
            
        check_count += 1
        time.sleep(check_interval)
        
        # 采样性能数据
        if current_time - last_check_time >= 0.5:  # 每0.5秒采样一次
            cpu_samples.append(monitor.get_cpu_usage())
            memory_samples.append(monitor.get_memory_usage())
            last_check_time = current_time
    
    event_thread.join()
    
    # 计算统计结果
    avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0
    avg_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
    
    result = {
        'method': 'polling',
        'duration': time.time() - start_time,
        'check_count': check_count,
        'events_detected': event_detected,
        'avg_cpu_usage': avg_cpu,
        'avg_memory_usage': avg_memory,
        'checks_per_second': check_count / (time.time() - start_time)
    }
    
    print(f"轮询结果:")
    print(f"  执行时间: {result['duration']:.3f} 秒")
    print(f"  检查次数: {result['check_count']:,}")
    print(f"  检测事件: {result['events_detected']}")
    print(f"  平均CPU使用率: {result['avg_cpu_usage']:.1f}%")
    print(f"  平均内存使用: {result['avg_memory_usage']/1024:.1f} KB")
    print(f"  检查频率: {result['checks_per_second']:,.0f} 次/秒")
    
    return result

def advanced_interrupt_method(duration: float = 5.0) -> dict:
    """
    高级中断方法实现
    
    Args:
        duration: 测试持续时间
        
    Returns:
        dict: 性能统计数据
    """
    print("\n=== 高级中断方法 ===")
    
    monitor = PerformanceMonitor()
    simulator = AdvancedEventSimulator(event_probability=0.005)
    
    interrupt_count = 0
    isr_durations = []
    cpu_samples = []
    memory_samples = []
    
    def interrupt_handler():
        """中断服务程序"""
        nonlocal interrupt_count, isr_durations
        isr_start = time.time()
        interrupt_count += 1
        
        # ISR执行（应该尽可能快）
        isr_work_time = random.uniform(0.0005, 0.002)  # 0.5-2ms
        time.sleep(isr_work_time)
        
        isr_duration = time.time() - isr_start
        isr_durations.append(isr_duration * 1000)  # 转换为毫秒
        
    # 设置中断模拟
    def event_generator():
        start_time = time.time()
        while (time.time() - start_time) < duration:
            if random.random() < simulator.event_probability:
                # 模拟硬件中断触发
                threading.Timer(0, interrupt_handler).start()
                time.sleep(random.uniform(simulator.min_interval, simulator.max_interval))
            else:
                time.sleep(0.01)
    
    start_time = time.time()
    generator_thread = threading.Thread(target=event_generator)
    generator_thread.start()
    
    # 主程序执行有用工作
    main_work_units = 0
    last_sample_time = start_time
    
    while (time.time() - start_time) < duration:
        # 模拟主程序的有用计算工作
        work_time = random.uniform(0.01, 0.05)
        time.sleep(work_time)
        main_work_units += 1
        
        # 采样性能数据
        current_time = time.time()
        if current_time - last_sample_time >= 0.5:
            cpu_samples.append(monitor.get_cpu_usage())
            memory_samples.append(monitor.get_memory_usage())
            last_sample_time = current_time
    
    generator_thread.join()
    
    # 计算统计结果
    avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0
    avg_memory = sum(memory_samples) / len(memory_samples) if memory_samples else 0
    avg_isr_time = sum(isr_durations) / len(isr_durations) if isr_durations else 0
    
    result = {
        'method': 'interrupt',
        'duration': time.time() - start_time,
        'interrupt_count': interrupt_count,
        'main_work_units': main_work_units,
        'avg_cpu_usage': avg_cpu,
        'avg_memory_usage': avg_memory,
        'avg_isr_duration': avg_isr_time
    }
    
    print(f"中断结果:")
    print(f"  执行时间: {result['duration']:.3f} 秒")
    print(f"  中断次数: {result['interrupt_count']}")
    print(f"  主程序工作单元: {result['main_work_units']}")
    print(f"  平均CPU使用率: {result['avg_cpu_usage']:.1f}%")
    print(f"  平均内存使用: {result['avg_memory_usage']/1024:.1f} KB")
    print(f"  平均ISR执行时间: {result['avg_isr_duration']:.3f} ms")
    
    return result

def comprehensive_comparison():
    """综合性能对比"""
    print("中断 vs 轮询：综合性能对比")
    print("=" * 50)
    
    test_duration = 3.0  # 3秒测试
    
    # 轮询测试
    polling_result = advanced_polling_method(test_duration)
    
    # 短暂休息
    time.sleep(1)
    
    # 中断测试  
    interrupt_result = advanced_interrupt_method(test_duration)
    
    # 对比分析
    print("\n" + "=" * 50)
    print("综合对比分析:")
    print("-" * 30)
    
    cpu_ratio = polling_result['avg_cpu_usage'] / max(interrupt_result['avg_cpu_usage'], 0.1)
    print(f"CPU效率提升: {cpu_ratio:.1f}x")
    
    if polling_result['checks_per_second'] > 0:
        print(f"轮询开销: {polling_result['checks_per_second']:,.0f} 次/秒的无用检查")
    
    print(f"中断响应: 实时性高，无延迟")
    print(f"轮询响应: 最大延迟 {1/polling_result['checks_per_second']*1000:.2f} ms")
    
    print("\n嵌入式系统启示:")
    print("• 中断方式显著降低功耗（CPU使用率更低）")
    print("• 中断提供确定性的实时响应")
    print("• 轮询在简单系统中可能更易于调试")
    print("• 复杂系统应优先考虑中断驱动架构")

if __name__ == "__main__":
    comprehensive_comparison()