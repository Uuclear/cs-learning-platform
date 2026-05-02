# 练习3解答：CPU性能计算器
# 根据主频、IPC、核心数等参数估算理论性能

class CPU:
    """CPU性能模型"""
    
    def __init__(self, name, frequency_ghz, ipc, cores, 
                 cache_mb=0, tdp_w=0, architecture="Unknown"):
        """
        初始化CPU参数
        frequency_ghz: 主频(GHz)
        ipc: 每时钟周期指令数
        cores: 核心数
        cache_mb: 缓存大小(MB)
        tdp_w: 热设计功耗(W)
        """
        self.name = name
        self.frequency_ghz = frequency_ghz
        self.ipc = ipc
        self.cores = cores
        self.cache_mb = cache_mb
        self.tdp_w = tdp_w
        self.architecture = architecture
    
    def calculate_integer_performance(self):
        """
        计算理论整数性能(GIPS)
        公式: 主频 × IPC × 核心数
        """
        return self.frequency_ghz * self.ipc * self.cores
    
    def calculate_float_performance(self, flops_per_instruction=2):
        """
        计算理论浮点性能(GFLOPS)
        公式: 主频 × IPC × 核心数 × 每指令浮点操作数
        """
        return self.frequency_ghz * self.ipc * self.cores * flops_per_instruction
    
    def calculate_single_core_performance(self):
        """计算单核性能"""
        return self.frequency_ghz * self.ipc
    
    def efficiency_score(self):
        """
        计算能效比 (性能/功耗)
        单位: GIPS/W
        """
        if self.tdp_w > 0:
            return self.calculate_integer_performance() / self.tdp_w
        return 0
    
    def display_specs(self):
        """显示CPU规格"""
        print(f"\n{self.name}")
        print(f"  架构: {self.architecture}")
        print(f"  主频: {self.frequency_ghz} GHz")
        print(f"  IPC: {self.ipc}")
        print(f"  核心数: {self.cores}")
        print(f"  缓存: {self.cache_mb} MB")
        print(f"  TDP: {self.tdp_w} W")
    
    def display_performance(self):
        """显示性能计算结果"""
        int_perf = self.calculate_integer_performance()
        float_perf = self.calculate_float_performance()
        single_perf = self.calculate_single_core_performance()
        efficiency = self.efficiency_score()
        
        print(f"  理论整数性能: {int_perf:.1f} GIPS")
        print(f"  理论浮点性能: {float_perf:.1f} GFLOPS")
        print(f"  单核整数性能: {single_perf:.1f} GIPS")
        if efficiency > 0:
            print(f"  能效比: {efficiency:.2f} GIPS/W")


def compare_cpus(cpu_list):
    """比较多个CPU的性能"""
    print("\n" + "=" * 70)
    print("CPU性能对比")
    print("=" * 70)
    
    # 显示各CPU规格
    for cpu in cpu_list:
        cpu.display_specs()
        cpu.display_performance()
    
    # 性能对比表
    print("\n" + "-" * 70)
    print("性能对比表")
    print("-" * 70)
    print(f"{'CPU型号':<25} {'整数性能':<12} {'浮点性能':<12} {'单核性能':<12} {'相对性能':<10}")
    print("-" * 70)
    
    baseline_perf = cpu_list[0].calculate_integer_performance()
    for cpu in cpu_list:
        int_perf = cpu.calculate_integer_performance()
        float_perf = cpu.calculate_float_performance()
        single_perf = cpu.calculate_single_core_performance()
        ratio = int_perf / baseline_perf
        print(f"{cpu.name:<25} {int_perf:<12.1f} {float_perf:<12.1f} {single_perf:<12.1f} {ratio:<10.2f}x")
    
    print("-" * 70)


def analyze_real_world_factors():
    """分析影响实际性能的因素"""
    print("\n" + "=" * 70)
    print("为什么理论性能和实际跑分有差距？")
    print("=" * 70)
    
    factors = [
        ("1. 内存带宽限制", 
         "CPU再快，数据跟不上也没用。内存带宽是瓶颈之一。",
         "影响程度: ★★★★☆"),
        
        ("2. 缓存命中率", 
         "缓存命中率高，CPU不用等内存。L1/L2/L3缓存很重要。",
         "影响程度: ★★★★★"),
        
        ("3. 程序并行度", 
         "程序不能拆分给多核心执行，核心再多也没用。",
         "影响程度: ★★★★☆"),
        
        ("4. 指令依赖", 
         "下条指令需要上条指令的结果，必须等待。",
         "影响程度: ★★★☆☆"),
        
        ("5. 分支预测失败", 
         "猜错了程序走向，流水线要清空重来。",
         "影响程度: ★★★☆☆"),
        
        ("6. 散热和功耗限制", 
         "太热会降频，功耗墙会限制性能发挥。",
         "影响程度: ★★★★☆"),
        
        ("7. 操作系统调度", 
         "任务调度、上下文切换都有开销。",
         "影响程度: ★★☆☆☆"),
    ]
    
    for name, desc, impact in factors:
        print(f"\n{name}")
        print(f"  {desc}")
        print(f"  {impact}")
    
    print("\n" + "-" * 70)
    print("实际性能通常只有理论性能的 30%-70%")
    print("优化良好的程序可以达到 80% 以上")
    print("-" * 70)


# 创建几款真实CPU进行对比
cpus = [
    CPU("Intel Core i9-13900K", 5.8, 1.5, 24, 36, 125, "x86 (Raptor Lake)"),
    CPU("AMD Ryzen 9 7950X", 5.7, 1.6, 16, 64, 170, "x86 (Zen 4)"),
    CPU("Apple M3 Max", 4.0, 2.2, 16, 48, 78, "ARM (Apple Silicon)"),
    CPU("Qualcomm Snapdragon 8 Gen 3", 3.3, 1.8, 8, 12, 8, "ARM (Cortex-X4)"),
]

# 生成报告
print("=" * 70)
print("CPU性能计算器 - 练习3解答")
print("=" * 70)

compare_cpus(cpus)
analyze_real_world_factors()

print("\n" + "=" * 70)
print("核心结论")
print("=" * 70)
print("""
1. 主频不是唯一指标，IPC同样重要
   - Apple M3虽然主频低(4.0GHz)，但高IPC(2.2)使其单核性能强劲
   - 对比i9-13900K：主频5.8GHz，IPC 1.5，单核性能 8.7 vs 8.8
   
2. 核心数要配合软件优化
   - 多核心只在并行任务中有优势
   - 游戏等串行任务更看重单核性能
   
3. 能效比越来越重要
   - Apple M3: 1.81 GIPS/W
   - i9-13900K: 1.67 GIPS/W
   - 高性能 + 低功耗 = 更好的用户体验

4. 理论性能仅供参考
   - 实际性能受多种因素影响
   - 选购CPU要看实际跑分和评测
   
5. ARM架构正在崛起
   - 手机CPU(Snapdragon)能效比极高
   - Apple Silicon证明了ARM也能做高性能桌面CPU
""")
print("=" * 70)

# 性能计算公式总结
print("\n" + "=" * 70)
print("性能计算公式总结")
print("=" * 70)
print("""
理论整数性能(GIPS) = 主频(GHz) × IPC × 核心数

理论浮点性能(GFLOPS) = 主频(GHz) × IPC × 核心数 × FLOPs/指令

单核性能 = 主频(GHz) × IPC

能效比 = 整数性能(GIPS) / TDP(W)

其中:
- IPC (Instructions Per Clock): 每时钟周期执行的指令数
- 现代x86 CPU的IPC通常在1.0-2.0之间
- 高性能ARM CPU的IPC可以达到2.0-2.5
- FLOPs/指令：通常假设为2（一条指令执行2次浮点运算）
""")
print("=" * 70)
