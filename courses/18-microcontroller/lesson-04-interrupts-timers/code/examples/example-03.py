#!/usr/bin/env python3
"""
示例 03: 多中断优先级调度模拟

这个程序模拟单片机中的多中断优先级系统，展示不同优先级中断的处理顺序。
"""

import time
import threading
import queue
import random
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class InterruptEvent:
    """中断事件数据结构"""
    name: str
    priority: int  # 数值越小优先级越高
    duration_ms: float
    timestamp: float
    preemptive: bool = True  # 是否可抢占

class InterruptScheduler:
    """中断调度器"""
    
    def __init__(self):
        self.interrupt_queue = queue.PriorityQueue()
        self.current_interrupt: Optional[InterruptEvent] = None
        self.running = False
        self.total_processed = 0
        
    def add_interrupt(self, interrupt: InterruptEvent):
        """添加中断到队列"""
        # Priority Queue按元组的第一个元素排序，所以用(priority, timestamp, event)
        self.interrupt_queue.put((interrupt.priority, interrupt.timestamp, interrupt))
        print(f"[+] 中断 '{interrupt.name}' 已加入队列 (优先级: {interrupt.priority})")
        
    def process_interrupts(self):
        """处理中断（模拟ISR执行）"""
        self.running = True
        
        while self.running or not self.interrupt_queue.empty():
            try:
                # 获取最高优先级的中断
                priority, timestamp, interrupt = self.interrupt_queue.get(timeout=0.1)
                
                # 检查是否可以抢占当前中断
                if (self.current_interrupt and 
                    interrupt.priority < self.current_interrupt.priority and 
                    interrupt.preemptive):
                    print(f"[!] 中断 '{interrupt.name}' 抢占 '{self.current_interrupt.name}'")
                    # 在真实硬件中，这里会保存当前上下文并切换到新中断
                    # 我们简化处理，直接执行高优先级中断
                    self._execute_interrupt(interrupt)
                    # 然后继续执行被抢占的中断
                    self._execute_interrupt(self.current_interrupt)
                else:
                    self._execute_interrupt(interrupt)
                    
                self.total_processed += 1
                
            except queue.Empty:
                continue
                
        self.running = False
        
    def _execute_interrupt(self, interrupt: InterruptEvent):
        """执行单个中断（模拟ISR）"""
        self.current_interrupt = interrupt
        print(f"[>] 开始执行中断 '{interrupt.name}' (优先级: {interrupt.priority})")
        
        # 模拟ISR执行时间
        time.sleep(interrupt.duration_ms / 1000.0)
        
        print(f"[<] 完成中断 '{interrupt.name}'")
        self.current_interrupt = None
        
    def stop(self):
        """停止调度器"""
        self.running = False

def simulate_interrupt_scenarios():
    """模拟不同的中断场景"""
    print("=== 多中断优先级调度模拟 ===\n")
    
    # 场景1: 不同优先级中断同时到达
    print("场景1: 不同优先级中断同时到达")
    scheduler = InterruptScheduler()
    
    # 创建多个中断事件（同时发生）
    current_time = time.time()
    interrupts = [
        InterruptEvent("低优先级任务", 3, 50, current_time),
        InterruptEvent("高优先级任务", 1, 20, current_time),
        InterruptEvent("中优先级任务", 2, 30, current_time)
    ]
    
    for intr in interrupts:
        scheduler.add_interrupt(intr)
    
    # 启动处理线程
    processor_thread = threading.Thread(target=scheduler.process_interrupts)
    processor_thread.start()
    processor_thread.join()
    
    print(f"场景1完成，共处理 {scheduler.total_processed} 个中断\n")
    
    # 场景2: 中断嵌套
    print("场景2: 中断嵌套（高优先级中断在低优先级执行时到达）")
    scheduler2 = InterruptScheduler()
    
    # 先添加一个长时间运行的低优先级中断
    low_intr = InterruptEvent("长时低优先级", 2, 100, time.time())
    scheduler2.add_interrupt(low_intr)
    
    # 启动处理
    processor_thread2 = threading.Thread(target=scheduler2.process_interrupts)
    processor_thread2.start()
    
    # 等待一小段时间，然后添加高优先级中断
    time.sleep(0.03)  # 30ms后
    high_intr = InterruptEvent("紧急高优先级", 0, 10, time.time())
    scheduler2.add_interrupt(high_intr)
    
    processor_thread2.join()
    print(f"场景2完成，共处理 {scheduler2.total_processed} 个中断\n")
    
    # 场景3: 相同优先级中断
    print("场景3: 相同优先级中断按到达顺序处理")
    scheduler3 = InterruptScheduler()
    
    base_time = time.time()
    same_priority_interrupts = [
        InterruptEvent("任务A", 1, 15, base_time + 0.01),
        InterruptEvent("任务B", 1, 15, base_time + 0.02),
        InterruptEvent("任务C", 1, 15, base_time + 0.03)
    ]
    
    for intr in same_priority_interrupts:
        scheduler3.add_interrupt(intr)
    
    processor_thread3 = threading.Thread(target=scheduler3.process_interrupts)
    processor_thread3.start()
    processor_thread3.join()
    
    print(f"场景3完成，共处理 {scheduler3.total_processed} 个中断")

def create_realistic_scenario():
    """创建更真实的嵌入式系统场景"""
    print("=== 真实场景模拟：嵌入式控制系统 ===\n")
    
    scheduler = InterruptScheduler()
    
    # 模拟一个典型的嵌入式系统中断源
    system_interrupts = [
        # 紧急故障处理（最高优先级）
        InterruptEvent("电源故障", 0, 5, time.time() + 0.05),
        
        # 通信中断
        InterruptEvent("UART接收", 1, 10, time.time() + 0.02),
        InterruptEvent("SPI传输完成", 2, 8, time.time() + 0.03),
        
        # 定时器中断
        InterruptEvent("1ms系统滴答", 3, 2, time.time() + 0.01),
        InterruptEvent("10ms任务调度", 4, 5, time.time() + 0.04),
        
        # 外部事件
        InterruptEvent("按键按下", 5, 15, time.time() + 0.06),
        InterruptEvent("ADC转换完成", 6, 12, time.time() + 0.07)
    ]
    
    # 随机打乱到达时间以模拟真实情况
    random.shuffle(system_interrupts)
    
    for intr in system_interrupts:
        scheduler.add_interrupt(intr)
    
    processor_thread = threading.Thread(target=scheduler.process_interrupts)
    processor_thread.start()
    processor_thread.join()
    
    print(f"真实场景完成，共处理 {scheduler.total_processed} 个中断")
    print("\n关键观察:")
    print("• 高优先级中断总是先执行")
    print("• 相同优先级按到达顺序处理") 
    print("• 紧急事件（如电源故障）能立即得到响应")

if __name__ == "__main__":
    simulate_interrupt_scenarios()
    print("\n" + "="*60 + "\n")
    create_realistic_scenario()