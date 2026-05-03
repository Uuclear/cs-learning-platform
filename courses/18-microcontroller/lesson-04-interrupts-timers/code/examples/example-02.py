#!/usr/bin/env python3
"""
示例 02: 定时器精确延时计算器

这个程序帮助计算单片机定时器的配置参数，实现精确的延时。
支持不同的系统时钟频率和目标延时时间。
"""

import math

class TimerCalculator:
    """定时器参数计算器"""
    
    def __init__(self, system_clock_mhz):
        """
        初始化计算器
        
        Args:
            system_clock_mhz: 系统时钟频率（MHz）
        """
        self.system_clock = system_clock_mhz * 1_000_000  # 转换为Hz
    
    def calculate_timer_params(self, target_delay_us, max_prescaler=65535, max_reload=65535):
        """
        计算定时器参数
        
        Args:
            target_delay_us: 目标延时时间（微秒）
            max_prescaler: 最大预分频值
            max_reload: 最大自动重载值
            
        Returns:
            dict: 包含最佳配置参数的字典
        """
        target_ticks = (self.system_clock * target_delay_us) / 1_000_000
        
        if target_ticks <= 0:
            raise ValueError("目标延时必须大于0")
        
        best_error = float('inf')
        best_config = None
        
        # 尝试不同的预分频值
        for prescaler in range(1, min(max_prescaler + 1, int(target_ticks) + 1)):
            reload_value = target_ticks / prescaler - 1
            
            if reload_value < 0 or reload_value > max_reload:
                continue
                
            # 计算实际延时和误差
            actual_ticks = (prescaler) * (math.floor(reload_value) + 1)
            actual_delay_us = (actual_ticks * 1_000_000) / self.system_clock
            error = abs(actual_delay_us - target_delay_us)
            
            if error < best_error:
                best_error = error
                best_config = {
                    'prescaler': prescaler - 1,  # 寄存器值是实际值减1
                    'reload': int(math.floor(reload_value)),
                    'actual_delay_us': actual_delay_us,
                    'error_us': error,
                    'error_percent': (error / target_delay_us) * 100
                }
        
        return best_config
    
    def format_config_output(self, config, target_delay_us):
        """格式化配置输出"""
        if not config:
            return "无法找到合适的配置参数"
        
        output = f"""
目标延时: {target_delay_us:.3f} μs
系统时钟: {self.system_clock/1_000_000:.0f} MHz

最佳配置:
  预分频值 (PSC): {config['prescaler']}
  自动重载值 (ARR): {config['reload']}
  
实际延时: {config['actual_delay_us']:.3f} μs
误差: {config['error_us']:.3f} μs ({config['error_percent']:.3f}%)

C代码示例:
  TIMx->PSC = {config['prescaler']};
  TIMx->ARR = {config['reload']};
  TIMx->CR1 |= TIM_CR1_CEN; // 启动定时器
"""
        return output

def interactive_calculator():
    """交互式计算器"""
    print("=== 定时器精确延时计算器 ===")
    print("帮助您计算单片机定时器的最佳配置参数\n")
    
    try:
        # 获取系统时钟频率
        system_clock = float(input("请输入系统时钟频率 (MHz): "))
        calculator = TimerCalculator(system_clock)
        
        while True:
            print("\n" + "-" * 40)
            target_delay_input = input("请输入目标延时 (μs) 或输入 'q' 退出: ")
            
            if target_delay_input.lower() == 'q':
                break
                
            try:
                target_delay = float(target_delay_input)
                config = calculator.calculate_timer_params(target_delay)
                print(calculator.format_config_output(config, target_delay))
                
            except ValueError as e:
                print(f"输入错误: {e}")
            except Exception as e:
                print(f"计算错误: {e}")
                
    except KeyboardInterrupt:
        print("\n程序已退出")
    except Exception as e:
        print(f"初始化错误: {e}")

def demo_examples():
    """演示常见用例"""
    print("=== 常见用例演示 ===\n")
    
    # STM32F103 示例 (72MHz)
    calculator = TimerCalculator(72.0)
    
    test_cases = [
        (1, "1微秒延时"),
        (10, "10微秒延时"), 
        (100, "100微秒延时"),
        (1000, "1毫秒延时"),
        (10000, "10毫秒延时"),
        (1000000, "1秒延时")
    ]
    
    for delay_us, description in test_cases:
        print(f"{description}:")
        config = calculator.calculate_timer_params(delay_us)
        if config:
            print(f"  PSC={config['prescaler']}, ARR={config['reload']}, 误差={config['error_percent']:.3f}%")
        else:
            print("  无法配置")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_examples()
    else:
        interactive_calculator()