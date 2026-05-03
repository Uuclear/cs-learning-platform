#!/usr/bin/env python3
"""
解决方案 02: 定时器精确延时计算器 - 完整实现

这个完整的解决方案提供了多定时器支持、误差分析和代码生成功能。
"""

import math
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass
class TimerConfig:
    """定时器配置结果"""
    prescaler: int
    reload: int
    actual_delay_us: float
    error_us: float
    error_percent: float
    timer_frequency_hz: float
    resolution_ns: float

class AdvancedTimerCalculator:
    """高级定时器计算器"""
    
    def __init__(self, system_clock_mhz: float, timer_bits: int = 16):
        """
        初始化高级计算器
        
        Args:
            system_clock_mhz: 系统时钟频率（MHz）
            timer_bits: 定时器位数（16或32位）
        """
        self.system_clock = system_clock_mhz * 1_000_000
        self.timer_bits = timer_bits
        self.max_reload = (1 << timer_bits) - 1
        self.max_prescaler = 65535  # STM32标准
        
    def calculate_all_possible_configs(self, target_delay_us: float) -> List[TimerConfig]:
        """
        计算所有可能的配置方案
        
        Args:
            target_delay_us: 目标延时（微秒）
            
        Returns:
            List[TimerConfig]: 所有可能的配置列表
        """
        target_ticks = (self.system_clock * target_delay_us) / 1_000_000
        configs = []
        
        if target_ticks <= 0:
            return configs
            
        # 尝试所有合理的预分频值
        max_prescaler_to_try = min(self.max_prescaler, int(target_ticks))
        
        for prescaler_val in range(1, max_prescaler_to_try + 1):
            reload_val_float = target_ticks / prescaler_val - 1
            
            if reload_val_float < 0 or reload_val_float > self.max_reload:
                continue
                
            reload_val = int(math.floor(reload_val_float))
            if reload_val < 0:
                continue
                
            # 计算实际参数
            actual_ticks = prescaler_val * (reload_val + 1)
            actual_delay_us = (actual_ticks * 1_000_000) / self.system_clock
            error_us = abs(actual_delay_us - target_delay_us)
            error_percent = (error_us / target_delay_us) * 100
            
            # 计算定时器频率和分辨率
            timer_freq = self.system_clock / prescaler_val
            resolution_ns = (1_000_000_000 / timer_freq)
            
            config = TimerConfig(
                prescaler=prescaler_val - 1,
                reload=reload_val,
                actual_delay_us=actual_delay_us,
                error_us=error_us,
                error_percent=error_percent,
                timer_frequency_hz=timer_freq,
                resolution_ns=resolution_ns
            )
            configs.append(config)
            
        return configs
    
    def find_optimal_config(self, target_delay_us: float, 
                          criteria: str = "error") -> Optional[TimerConfig]:
        """
        找到最优配置
        
        Args:
            target_delay_us: 目标延时（微秒）
            criteria: 优化标准 ("error", "prescaler", "reload")
            
        Returns:
            Optional[TimerConfig]: 最优配置
        """
        configs = self.calculate_all_possible_configs(target_delay_us)
        if not configs:
            return None
            
        if criteria == "error":
            return min(configs, key=lambda c: c.error_percent)
        elif criteria == "prescaler":
            return min(configs, key=lambda c: c.prescaler)
        elif criteria == "reload":
            return min(configs, key=lambda c: c.reload)
        else:
            return configs[0]
    
    def generate_c_code(self, config: TimerConfig, timer_name: str = "TIMx") -> str:
        """生成C代码"""
        code = f"""// {timer_name} 配置 - 目标延时: {config.actual_delay_us:.3f} μs (误差: {config.error_percent:.3f}%)
{timer_name}->PSC = {config.prescaler};     // 预分频值
{timer_name}->ARR = {config.reload};       // 自动重载值
{timer_name}->CR1 |= TIM_CR1_CEN;          // 启动定时器

// 定时器频率: {config.timer_frequency_hz/1000:.1f} kHz
// 时间分辨率: {config.resolution_ns:.1f} ns"""
        return code
    
    def analyze_timing_requirements(self, requirements: List[Tuple[float, str]]) -> Dict:
        """
        分析多个定时需求
        
        Args:
            requirements: [(delay_us, description), ...]
            
        Returns:
            Dict: 分析结果
        """
        analysis = {
            'requirements': requirements,
            'configs': [],
            'shared_timer_possible': False,
            'recommendations': []
        }
        
        configs = []
        for delay_us, desc in requirements:
            config = self.find_optimal_config(delay_us)
            if config:
                configs.append((delay_us, desc, config))
                analysis['configs'].append({
                    'delay_us': delay_us,
                    'description': desc,
                    'config': config
                })
        
        # 检查是否可以共享同一个定时器
        if len(configs) > 1:
            base_config = configs[0][2]
            can_share = True
            
            for delay_us, desc, config in configs[1:]:
                # 如果预分频值相同，可能可以共享
                if config.prescaler != base_config.prescaler:
                    can_share = False
                    break
                    
            analysis['shared_timer_possible'] = can_share
            
            if can_share:
                analysis['recommendations'].append(
                    "所有定时需求可以使用同一个定时器（相同预分频值）"
                )
            else:
                analysis['recommendations'].append(
                    "需要使用多个定时器或动态重新配置"
                )
        
        return analysis

def interactive_advanced_calculator():
    """交互式高级计算器"""
    print("=== 高级定时器配置计算器 ===")
    print("支持多需求分析和代码生成\n")
    
    try:
        system_clock = float(input("系统时钟频率 (MHz): "))
        timer_bits = int(input("定时器位数 (16/32): ") or "16")
        
        calculator = AdvancedTimerCalculator(system_clock, timer_bits)
        
        while True:
            print("\n选项:")
            print("1. 单个延时计算")
            print("2. 多需求分析")  
            print("3. 退出")
            
            choice = input("请选择 (1-3): ").strip()
            
            if choice == "1":
                delay_us = float(input("目标延时 (μs): "))
                config = calculator.find_optimal_config(delay_us)
                
                if config:
                    print(f"\n最佳配置:")
                    print(f"  预分频: {config.prescaler}")
                    print(f"  重载值: {config.reload}")
                    print(f"  实际延时: {config.actual_delay_us:.3f} μs")
                    print(f"  误差: {config.error_percent:.3f}%")
                    print(f"  定时器频率: {config.timer_frequency_hz/1000:.1f} kHz")
                    
                    generate_code = input("\n生成C代码? (y/n): ").lower() == 'y'
                    if generate_code:
                        timer_name = input("定时器名称 (默认TIMx): ").strip() or "TIMx"
                        print("\n" + calculator.generate_c_code(config, timer_name))
                else:
                    print("无法找到合适的配置")
                    
            elif choice == "2":
                requirements = []
                print("输入多个定时需求 (输入0结束):")
                while True:
                    delay_input = input("延时 (μs) 或 0 结束: ").strip()
                    if delay_input == "0":
                        break
                    try:
                        delay_us = float(delay_input)
                        desc = input("描述: ").strip() or f"{delay_us}μs"
                        requirements.append((delay_us, desc))
                    except ValueError:
                        print("无效输入")
                        
                if requirements:
                    analysis = calculator.analyze_timing_requirements(requirements)
                    print(f"\n分析结果:")
                    print(f"可共享定时器: {'是' if analysis['shared_timer_possible'] else '否'}")
                    for rec in analysis['recommendations']:
                        print(f"建议: {rec}")
                        
                    for item in analysis['configs']:
                        config = item['config']
                        print(f"\n{item['description']}:")
                        print(f"  PSC={config.prescaler}, ARR={config.reload}")
                        print(f"  误差: {config.error_percent:.3f}%")
                        
            elif choice == "3":
                break
            else:
                print("无效选择")
                
    except KeyboardInterrupt:
        print("\n程序退出")
    except Exception as e:
        print(f"错误: {e}")

def demo_comprehensive_examples():
    """综合示例演示"""
    print("=== 综合示例演示 ===\n")
    
    # STM32F4 示例 (168MHz, 32位定时器)
    calculator = AdvancedTimerCalculator(168.0, 32)
    
    # 常见应用场景
    scenarios = [
        ([1, 10, 100], "高精度测量"),
        ([1000, 5000, 10000], "LED闪烁控制"), 
        ([50000, 100000, 500000], "数据采集周期"),
        ([1000000, 2000000, 5000000], "通信协议定时")
    ]
    
    for delays, scenario_name in scenarios:
        print(f"{scenario_name}:")
        requirements = [(d, f"{d}μs") for d in delays]
        analysis = calculator.analyze_timing_requirements(requirements)
        
        print(f"  共享定时器: {'✓' if analysis['shared_timer_possible'] else '✗'}")
        best_errors = [item['config'].error_percent for item in analysis['configs']]
        avg_error = sum(best_errors) / len(best_errors)
        print(f"  平均误差: {avg_error:.3f}%")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_comprehensive_examples()
    else:
        interactive_advanced_calculator()