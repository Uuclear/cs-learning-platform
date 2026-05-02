# 练习2解答：流水线性能分析
# 比较流水线执行和非流水线执行的效率差异

def analyze_pipeline_performance(program, num_stages=4):
    """
    分析流水线性能
    num_stages: 流水线阶段数（默认4：取指、解码、执行、写回）
    """
    num_instructions = len(program)
    
    # 非流水线执行
    non_pipeline_cycles = num_instructions * num_stages
    
    # 流水线执行
    # 公式：周期数 = 指令数 + 阶段数 - 1
    pipeline_cycles = num_instructions + num_stages - 1
    
    # 效率提升
    improvement = (non_pipeline_cycles - pipeline_cycles) / non_pipeline_cycles * 100
    
    print("=" * 70)
    print("流水线性能分析报告")
    print("=" * 70)
    
    print("\n程序指令:")
    for i, instr in enumerate(program):
        print(f"  [{i}] {instr}")
    
    print(f"\n流水线阶段数: {num_stages}")
    print(f"指令数: {num_instructions}")
    
    print("\n" + "-" * 70)
    print("非流水线执行:")
    print("-" * 70)
    print(f"  每条指令需要{num_stages}个周期（顺序执行）")
    print(f"  总周期数 = {num_instructions} × {num_stages} = {non_pipeline_cycles} 周期")
    print("  执行时间线:")
    for i, instr in enumerate(program):
        start = i * num_stages + 1
        end = start + num_stages - 1
        print(f"    指令{i} [{instr:15}]: 周期 {start:2} - {end:2}")
    
    print("\n" + "-" * 70)
    print("流水线执行:")
    print("-" * 70)
    print(f"  公式: 周期数 = 指令数 + 阶段数 - 1")
    print(f"  总周期数 = {num_instructions} + {num_stages} - 1 = {pipeline_cycles} 周期")
    print("  执行时间线:")
    for i, instr in enumerate(program):
        start = i + 1
        end = start + num_stages - 1
        print(f"    指令{i} [{instr:15}]: 周期 {start:2} - {end:2}")
    
    print("\n" + "-" * 70)
    print("性能对比:")
    print("-" * 70)
    print(f"  非流水线周期数: {non_pipeline_cycles}")
    print(f"  流水线周期数:   {pipeline_cycles}")
    print(f"  节省周期数:     {non_pipeline_cycles - pipeline_cycles}")
    print(f"  效率提升:       {improvement:.1f}%")
    print(f"  加速比:         {non_pipeline_cycles / pipeline_cycles:.2f}x")
    
    # 可视化流水线
    print("\n" + "-" * 70)
    print("流水线可视化（每个字母代表一个阶段）:")
    print("-" * 70)
    print("F=取指(Fetch), D=解码(Decode), E=执行(Execute), W=写回(Writeback)")
    print()
    
    stage_labels = ['F', 'D', 'E', 'W']
    header = "        " + " ".join([f"{i+1:2}" for i in range(pipeline_cycles)])
    print(header)
    print("-" * len(header))
    
    for i, instr in enumerate(program):
        line = f"指令{i}:  "
        for cycle in range(1, pipeline_cycles + 1):
            # 计算这条指令在哪个阶段
            instr_start = i + 1
            stage_idx = cycle - instr_start
            if 0 <= stage_idx < num_stages:
                line += f"{stage_labels[stage_idx]} "
            else:
                line += ". "
        print(line)
    
    print("=" * 70)
    
    return {
        'non_pipeline': non_pipeline_cycles,
        'pipeline': pipeline_cycles,
        'improvement': improvement,
        'speedup': non_pipeline_cycles / pipeline_cycles
    }


# 测试程序（8条指令）
program = [
    "LOAD R0, 5",     # R0 = 5
    "LOAD R1, 3",     # R1 = 3
    "ADD R0, R1",     # R0 = R0 + R1 = 8
    "LOAD R2, 2",     # R2 = 2
    "MUL R0, R2",     # R0 = R0 * R2 = 16
    "LOAD R1, 1",     # R1 = 1
    "SUB R0, R1",     # R0 = R0 - R1 = 15
    "HALT"            # 停止
]

print("\n")
results = analyze_pipeline_performance(program, num_stages=4)

print("\n\n")
print("=" * 70)
print("不同流水线阶段数的对比:")
print("=" * 70)
print(f"{'阶段数':<10} {'非流水线':<12} {'流水线':<12} {'节省':<10} {'提升':<10}")
print("-" * 70)
for stages in [3, 4, 5, 6, 10]:
    num_instr = len(program)
    non_pipe = num_instr * stages
    pipe = num_instr + stages - 1
    saved = non_pipe - pipe
    impr = (saved / non_pipe) * 100
    print(f"{stages:<10} {non_pipe:<12} {pipe:<12} {saved:<10} {impr:<10.1f}%")

print("=" * 70)
print("\n结论:")
print("- 流水线阶段数越多，效率提升越明显")
print("- 但阶段数过多会增加流水线冲突的开销")
print("- 现代CPU通常有10-20级流水线")
