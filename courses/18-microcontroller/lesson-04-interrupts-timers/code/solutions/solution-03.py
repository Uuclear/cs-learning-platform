#!/usr/bin/env python3
"""
解决方案 03: 多中断优先级调度模拟 - 完整实现

这个完整的解决方案提供了真实的中断调度行为模拟，
包括上下文切换、中断嵌套限制和实时性能分析。
"""

import time
import threading
import queue
import random
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class InterruptType(Enum):
    """中断类型"""
    EXTERNAL = "external"
    TIMER = "timer"
    UART = "uart"
    SPI = "spi"
    I2C = "i2c"
    ADC = "adc"
    DMA = "dma"

@dataclass
class InterruptEvent:
    """中断事件（增强版）"""
    name: str
    priority: int
    duration_ms: float
    timestamp: float
    interrupt_type: InterruptType
    preemptive: bool = True
    nesting_level: int = 0
    max_nesting: int = 3  # 最大嵌套层数
    
    def can_preempt(self, current_interrupt: 'InterruptEvent') -> bool:
        """判断是否可以抢占当前中断"""
        if not self.preemptive:
            return False
        if self.nesting_level >= self.max_nesting:
            return False
        return self.priority < current_interrupt.priority

class RealisticInterruptScheduler:
    """真实中断调度器"""
    
    def __init__(self, max_nesting_level: int = 3):
        self.interrupt_queue = queue.PriorityQueue()
        self.current_interrupt: Optional[InterruptEvent] = None
        self.running = False
        self.total_processed = 0
        self.context_switches = 0
        self.nesting_level = 0
        self.max_nesting_level = max_nesting_level
        self.interrupt_log: List[Dict[str, Any]] = []
        self.stats = {
            'total_interrupts': 0,
            'preemptions': 0,
            'nested_interrupts': 0,
            'average_response_time': 0.0,
            'max_nesting_reached': 0
        }
        
    def add_interrupt(self, interrupt: InterruptEvent):
        """添加中断到队列"""
        # 设置嵌套级别
        interrupt.nesting_level = self.nesting_level
        interrupt.max_nesting = self.max_nesting_level
        
        self.interrupt_queue.put((interrupt.priority, interrupt.timestamp, interrupt))
        self.stats['total_interrupts'] += 1
        
        log_entry = {
            'time': time.time(),
            'action': 'queued',
            'interrupt': interrupt.name,
            'priority': interrupt.priority,
            'nesting_level': interrupt.nesting_level
        }
        self.interrupt_log.append(log_entry)
        
    def process_interrupts(self):
        """处理中断（真实调度行为）"""
        self.running = True
        response_times = []
        
        while self.running or not self.interrupt_queue.empty():
            try:
                priority, timestamp, interrupt = self.interrupt_queue.get(timeout=0.1)
                
                # 计算响应时间
                response_time = time.time() - timestamp
                response_times.append(response_time)
                
                # 处理抢占逻辑
                if (self.current_interrupt and 
                    interrupt.can_preempt(self.current_interrupt)):
                    
                    self.stats['preemptions'] += 1
                    self._handle_preemption(interrupt)
                    
                else:
                    self._execute_interrupt(interrupt)
                    
                self.total_processed += 1
                
            except queue.Empty:
                continue
                
        # 计算平均响应时间
        if response_times:
            self.stats['average_response_time'] = sum(response_times) / len(response_times)
            
        self.running = False
        
    def _handle_preemption(self, new_interrupt: InterruptEvent):
        """处理中断抢占"""
        old_interrupt = self.current_interrupt
        
        # 保存被抢占中断的上下文（模拟）
        self.context_switches += 1
        self.nesting_level += 1
        
        log_entry = {
            'time': time.time(),
            'action': 'preempted',
            'old_interrupt': old_interrupt.name,
            'new_interrupt': new_interrupt.name,
            'nesting_level': self.nesting_level
        }
        self.interrupt_log.append(log_entry)
        
        # 执行高优先级中断
        new_interrupt.nesting_level = self.nesting_level
        self._execute_interrupt(new_interrupt)
        
        # 恢复被抢占的中断
        self.nesting_level -= 1
        self._execute_interrupt(old_interrupt)
        
        if self.nesting_level > 0:
            self.stats['nested_interrupts'] += 1
            
    def _execute_interrupt(self, interrupt: InterruptEvent):
        """执行中断（带完整日志）"""
        execution_start = time.time()
        self.current_interrupt = interrupt
        
        log_entry = {
            'time': execution_start,
            'action': 'started',
            'interrupt': interrupt.name,
            'priority': interrupt.priority,
            'duration_ms': interrupt.duration_ms,
            'nesting_level': interrupt.nesting_level
        }
        self.interrupt_log.append(log_entry)
        
        # 检查嵌套限制
        if interrupt.nesting_level >= self.max_nesting_level:
            self.stats['max_nesting_reached'] += 1
            print(f"[!] 警告: 中断 '{interrupt.name}' 达到最大嵌套层数 {self.max_nesting_level}")
            
        # 执行ISR
        time.sleep(interrupt.duration_ms / 1000.0)
        
        execution_end = time.time()
        self.current_interrupt = None
        
        log_entry = {
            'time': execution_end,
            'action': 'completed',
            'interrupt': interrupt.name,
            'actual_duration_ms': (execution_end - execution_start) * 1000
        }
        self.interrupt_log.append(log_entry)
        
    def get_statistics(self) -> Dict:
        """获取详细统计信息"""
        return {
            **self.stats,
            'context_switches': self.context_switches,
            'total_processed': self.total_processed,
            'current_nesting_level': self.nesting_level
        }
        
    def print_detailed_report(self):
        """打印详细报告"""
        stats = self.get_statistics()
        print("\n=== 中断调度详细报告 ===")
        print(f"总中断数: {stats['total_interrupts']}")
        print(f"已处理: {stats['total_processed']}")
        print(f"抢占次数: {stats['preemptions']}")
        print(f"嵌套中断: {stats['nested_interrupts']}")
        print(f"上下文切换: {stats['context_switches']}")
        print(f"平均响应时间: {stats['average_response_time']*1000:.2f} ms")
        print(f"最大嵌套限制触发: {stats['max_nesting_reached']} 次")
        
    def stop(self):
        """停止调度器"""
        self.running = False

def create_embedded_system_scenario():
    """创建真实的嵌入式系统场景"""
    print("=== 真实嵌入式系统中断场景 ===\n")
    
    # 创建具有不同特性的中断源
    base_time = time.time()
    
    interrupts = [
        # 紧急安全相关（最高优先级，不可抢占）
        InterruptEvent("看门狗超时", 0, 2.0, base_time + 0.1, InterruptType.TIMER, preemptive=False),
        
        # 实时通信（高优先级）
        InterruptEvent("UART接收完成", 1, 1.5, base_time + 0.2, InterruptType.UART),
        InterruptEvent("CAN总线错误", 1, 1.0, base_time + 0.8, InterruptType.EXTERNAL),
        
        # 定时器服务（中等优先级）
        InterruptEvent("1ms系统滴答", 2, 0.5, base_time + 0.05, InterruptType.TIMER),
        InterruptEvent("10ms任务调度", 3, 1.0, base_time + 0.3, InterruptType.TIMER),
        InterruptEvent("100ms数据采集", 4, 2.0, base_time + 0.4, InterruptType.TIMER),
        
        # 外设中断（较低优先级）
        InterruptEvent("SPI传输完成", 5, 1.2, base_time + 0.6, InterruptType.SPI),
        InterruptEvent("I2C从机地址匹配", 6, 0.8, base_time + 0.7, InterruptType.I2C),
        InterruptEvent("ADC转换完成", 7, 1.5, base_time + 0.9, InterruptType.ADC),
        InterruptEvent("DMA传输完成", 8, 1.0, base_time + 1.0, InterruptType.DMA),
        
        # 用户输入（最低优先级）
        InterruptEvent("按键按下", 9, 3.0, base_time + 0.5, InterruptType.EXTERNAL)
    ]
    
    # 随机化到达时间以模拟真实情况
    for intr in interrupts:
        intr.timestamp += random.uniform(-0.02, 0.02)
    
    scheduler = RealisticInterruptScheduler(max_nesting_level=3)
    
    # 添加所有中断
    for intr in interrupts:
        scheduler.add_interrupt(intr)
    
    # 启动处理
    processor_thread = threading.Thread(target=scheduler.process_interrupts)
    processor_thread.start()
    processor_thread.join()
    
    # 显示结果
    scheduler.print_detailed_report()
    
    # 分析关键指标
    print("\n=== 关键性能指标分析 ===")
    stats = scheduler.get_statistics()
    
    if stats['average_response_time'] < 0.005:  # 5ms
        print("✓ 实时性能: 优秀 (< 5ms 响应)")
    elif stats['average_response_time'] < 0.01:  # 10ms
        print("✓ 实时性能: 良好 (< 10ms 响应)")
    else:
        print("⚠ 实时性能: 需要优化 (> 10ms 响应)")
        
    if stats['max_nesting_reached'] == 0:
        print("✓ 嵌套深度: 在安全范围内")
    else:
        print(f"⚠ 嵌套深度: {stats['max_nesting_reached']} 次超出限制")
        
    if stats['preemptions'] > 0:
        print(f"✓ 抢占机制: 正常工作 ({stats['preemptions']} 次抢占)")
    else:
        print("ℹ 抢占机制: 本次测试未触发")

def stress_test_scenario():
    """压力测试场景"""
    print("\n=== 中断压力测试 ===\n")
    
    scheduler = RealisticInterruptScheduler(max_nesting_level=2)
    base_time = time.time()
    
    # 生成大量高频率中断
    high_frequency_interrupts = []
    for i in range(20):
        # 高优先级定时器中断（模拟高频事件）
        intr = InterruptEvent(
            f"高频定时器-{i}", 
            random.randint(1, 3),  # 高优先级
            random.uniform(0.5, 2.0),  # 短执行时间
            base_time + i * 0.05,  # 每50ms一个
            InterruptType.TIMER
        )
        high_frequency_interrupts.append(intr)
        
    # 添加一些低优先级长时中断
    for i in range(5):
        intr = InterruptEvent(
            f"长时任务-{i}",
            random.randint(6, 8),  # 低优先级
            random.uniform(5.0, 10.0),  # 长执行时间
            base_time + random.uniform(0.1, 0.8),
            InterruptType.EXTERNAL
        )
        high_frequency_interrupts.append(intr)
    
    # 添加中断
    for intr in high_frequency_interrupts:
        scheduler.add_interrupt(intr)
    
    # 处理
    processor_thread = threading.Thread(target=scheduler.process_interrupts)
    processor_thread.start()
    processor_thread.join()
    
    scheduler.print_detailed_report()
    
    print("\n压力测试结论:")
    stats = scheduler.get_statistics()
    if stats['max_nesting_reached'] > 0:
        print("系统在高负载下出现了嵌套深度超限，需要:")
        print("• 增加最大嵌套层数")
        print("• 优化ISR执行时间")  
        print("• 调整中断优先级")
    else:
        print("系统在高负载下表现稳定，中断处理能力充足")

if __name__ == "__main__":
    create_embedded_system_scenario()
    stress_test_scenario()