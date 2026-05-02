# 练习1解答：指令模拟
# 手动模拟CPU执行过程

def simulate_cpu():
    """
    模拟CPU执行给定的程序
    程序：计算 10 + 3，结果存入地址6
    """
    # 内存内容
    memory = [0] * 16
    memory[0] = 0x15   # LOAD 5: 从地址5加载数据
    memory[1] = 0x22   # ADD 2: 加上地址2的数据
    memory[2] = 0x46   # STORE 6: 存储到地址6
    memory[3] = 0xFF   # HALT: 停止
    memory[4] = 0x00   # 数据: 0
    memory[5] = 0x0A   # 数据: 10
    memory[6] = 0x00   # （结果将存储在这里）
    memory[7] = 0x03   # 数据: 3
    memory[8] = 0x00   # 数据: 0

    # CPU状态
    pc = 0              # 程序计数器
    accumulator = 0     # 累加器
    running = True

    print("=" * 60)
    print("CPU执行模拟 - 练习1解答")
    print("=" * 60)
    print("\n程序：计算 10 + 3，结果存入地址6")
    print("预期结果：内存[6] = 13\n")

    cycle = 1
    execution_log = []  # 记录执行过程

    while running and pc < len(memory):
        print(f"--- 周期 {cycle} ---")
        print(f"PC = {pc}, 累加器 = {accumulator}")

        # 取指令
        instruction = memory[pc]
        pc += 1

        # 译码
        opcode = (instruction >> 4) & 0x0F
        operand = instruction & 0x0F

        # 执行
        if opcode == 0x01:  # LOAD
            accumulator = memory[operand]
            print(f"执行: LOAD {operand} -> 累加器 = {accumulator}")

        elif opcode == 0x02:  # ADD
            old_acc = accumulator
            accumulator += memory[operand]
            print(f"执行: ADD {operand} -> {old_acc} + {memory[operand]} = {accumulator}")

        elif opcode == 0x04:  # STORE
            memory[operand] = accumulator
            print(f"执行: STORE {operand} -> 内存[{operand}] = {accumulator}")

        elif opcode == 0x0F:  # HALT
            running = False
            print(f"执行: HALT -> CPU停止")

        else:
            print(f"未知指令: {hex(instruction)}")
            break

        execution_log.append({
            'cycle': cycle,
            'pc': pc,
            'accumulator': accumulator
        })

        cycle += 1

    print("\n" + "=" * 60)
    print("执行完成！")
    print("=" * 60)

    # 输出执行过程汇总表
    print("\n📊 执行过程汇总:")
    print("周期 | 指令执行前PC | 指令执行后累加器")
    print("-" * 40)
    for log in execution_log:
        print(f"{log['cycle']:4d} | {log['pc']:12d} | {log['accumulator']:16d}")

    print(f"\n✅ 最终内存[6]的值: {memory[6]}")
    print(f"✅ 预期结果: 13")
    print(f"✅ 验证: {'通过！' if memory[6] == 13 else '失败！'}")

    return memory[6]


if __name__ == "__main__":
    result = simulate_cpu()

    # 附加思考题
    print("\n" + "=" * 60)
    print("💡 思考题解答")
    print("=" * 60)
    print("""
问题：为什么程序计数器（PC）在执行完最后一条指令后，
      指向的是一个不存在指令的地址？

答案：
因为在执行HALT指令后，PC会自增1（这是取指令阶段的正常操作），
指向HALT之后的位置。但由于HALT停止了CPU，PC的值不再重要。

在真实计算机中，操作系统会接管控制权，
将PC设置为下一个程序的入口地址。
    """)
