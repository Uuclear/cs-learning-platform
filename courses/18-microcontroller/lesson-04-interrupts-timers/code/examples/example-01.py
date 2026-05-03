#!/usr/bin/env python3
"""
示例 01: 中断与轮询性能对比模拟

这个程序演示了中断驱动和轮询方式在处理事件时的性能差异。
通过模拟等待随机事件的发生，展示两种方法的CPU使用效率。
"""

import time
import threading
import random
import sys

class EventSimulator:
    """事件模拟器，用于生成随机事件"""

    def __init__(self, min_delay=0.1, max_delay=2.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.event_occurred = False
        self.event_time = None

    def start_event_generation(self):
        """启动事件生成（模拟外部中断源）"""
        delay = random.uniform(self.min_delay, self.max_delay)
        self.event_time = time.time() + delay

        def trigger_event():
            time.sleep(delay)
            self.event_occurred = True
            print(f"[事件发生] 在 {delay:.3f} 秒后触发")

        thread = threading.Thread(target=trigger_event)
        thread.daemon = True
        thread.start()
        return delay

def polling_method(simulator, check_interval=0.01):
    """
    轮询方法：不断检查事件是否发生

    Args:
        simulator: EventSimulator 实例
        check_interval: 检查间隔（秒）

    Returns:
        tuple: (总耗时, 检查次数)
    """
    print("=== 轮询方法 ===")
    start_time = time.time()
    check_count = 0

    # 启动事件生成
    expected_delay = simulator.start_event_generation()

    while not simulator.event_occurred:
        check_count += 1
        # 模拟检查操作（比如读取GPIO状态）
        time.sleep(check_interval)  # 避免CPU占用过高

    total_time = time.time() - start_time
    print(f"轮询结果:")
    print(f"  总耗时: {total_time:.3f} 秒")
    print(f"  检查次数: {check_count}")
    print(f"  CPU利用率: 高（持续检查）")
    print(f"  效率: {(expected_delay/total_time)*100:.1f}%")

    return total_time, check_count

def interrupt_method(simulator):
    """
    中断方法：使用回调机制处理事件

    Args:
        simulator: EventSimulator 实例

    Returns:
        float: 总耗时
    """
    print("\n=== 中断方法 ===")
    start_time = time.time()
    main_work_done = False

    # 定义中断处理函数（ISR）
    def interrupt_handler():
        """中断服务程序 - 处理事件"""
        handler_start = time.time()
        print(f"[ISR执行] 中断处理开始 ({handler_start - start_time:.3f}秒)")

        # ISR应该尽可能快！这里只做必要操作
        isr_duration = random.uniform(0.001, 0.005)  # 1-5ms的ISR执行时间
        time.sleep(isr_duration)

        print(f"[ISR完成] 处理耗时 {isr_duration*1000:.1f}ms")

    # 启动事件生成，但使用定时器回调模拟中断
    expected_delay = simulator.start_event_generation()

    # 设置中断处理（使用定时器模拟硬件中断）
    interrupt_timer = threading.Timer(expected_delay, interrupt_handler)
    interrupt_timer.start()

    # 主程序可以做其他有用的工作
    print("主程序正在执行其他任务...")
    work_iterations = 0
    while not simulator.event_occurred:
        # 模拟主程序的有用工作
        time.sleep(0.1)
        work_iterations += 1
        if work_iterations % 5 == 0:
            print(f"  主程序工作进度: {work_iterations * 10}%")
        if work_iterations >= 10:  # 最多工作1秒
            break

    # 等待中断处理完成
    interrupt_timer.join()
    total_time = time.time() - start_time

    print(f"中断结果:")
    print(f"  总耗时: {total_time:.3f} 秒")
    print(f"  主程序完成有用工作: {min(work_iterations * 10, 100)}%")
    print(f"  CPU利用率: 低（只在需要时唤醒）")
    print(f"  效率: 高（无需持续检查）")

    return total_time

def main():
    """主函数：运行对比测试"""
    print("中断 vs 轮询性能对比模拟")
    print("=" * 50)

    # 测试多次以获得平均结果
    num_tests = 3
    polling_total = 0
    interrupt_total = 0

    for test_num in range(num_tests):
        print(f"\n--- 测试 {test_num + 1} ---")

        # 轮询测试
        simulator1 = EventSimulator()
        polling_time, _ = polling_method(simulator1)
        polling_total += polling_time

        # 中断测试
        simulator2 = EventSimulator()
        interrupt_time = interrupt_method(simulator2)
        interrupt_total += interrupt_time

        # 短暂休息
        time.sleep(0.5)

    # 显示总结
    print("\n" + "=" * 50)
    print("性能对比总结:")
    print(f"轮询平均耗时: {polling_total/num_tests:.3f} 秒")
    print(f"中断平均耗时: {interrupt_total/num_tests:.3f} 秒")
    print(f"性能提升: {(polling_total/interrupt_total)*100:.1f}%")

    print("\n关键结论:")
    print("• 轮询方式浪费CPU资源进行无意义的状态检查")
    print("• 中断方式让CPU专注于有用工作，事件发生时才处理")
    print("• 在嵌入式系统中，中断能显著降低功耗并提高响应性")

if __name__ == "__main__":
    main()
