# 练习3解答：扩展CPU
# 添加JUMP和JUMP_IF_ZERO指令，实现循环计算1+2+3+...+10

class ExtendedCPU:
    """扩展的CPU模拟器，支持跳转指令"""

    def __init__(self):
        self.pc = 0          # 程序计数器
        self.accumulator = 0 # 累加器
        self.running = True
        self.cycle_count = 0

        # 扩展的指令集
        self.instructions = {
            'LOAD': 0x01,
            'ADD': 0x02,
            'SUB': 0x03,
            'STORE': 0x04,
            'MUL': 0x05,
            'JUMP': 0x06,          # 无条件跳转
            'JUMP_IF_ZERO': 0x07,  # 如果累加器为0则跳转
            'HALT': 0x0F,
        }

    def fetch(self, memory):
        """取指令"""
        instruction = memory[self.pc]
        self.pc += 1
        return instruction

    def decode_execute(self, instruction, memory):
        """译码和执行"""
        opcode = (instruction >> 4) & 0x0F
        operand = instruction & 0x0F

        # LOAD
        if opcode == 0x01:
            self.accumulator = memory[operand]
            print(f"   LOAD {operand}: ACC = {self.accumulator}")

        # ADD
        elif opcode == 0x02:
            old = self.accumulator
            self.accumulator += memory[operand]
            print(f"   ADD {operand}: {old} + {memory[operand]} = {self.accumulator}")

        # SUB
        elif opcode == 0x03:
            old = self.accumulator
            self.accumulator -= memory[operand]
            print(f"   SUB {operand}: {old} - {memory[operand]} = {self.accumulator}")

        # STORE
        elif opcode == 0x04:
            memory[operand] = self.accumulator
            print(f"   STORE {operand}: 内存[{operand}] = {self.accumulator}")

        # MUL
        elif opcode == 0x05:
            old = self.accumulator
            self.accumulator *= memory[operand]
            print(f"   MUL {operand}: {old} * {memory[operand]} = {self.accumulator}")

        # JUMP (无条件跳转)
        elif opcode == 0x06:
            self.pc = operand
            print(f"   JUMP {operand}: PC跳转到 {operand}")

        # JUMP_IF_ZERO (条件跳转)
        elif opcode == 0x07:
            if self.accumulator == 0:
                self.pc = operand
                print(f"   JUMP_IF_ZERO {operand}: ACC=0，跳转到 {operand}")
            else:
                print(f"   JUMP_IF_ZERO {operand}: ACC={self.accumulator}≠0，不跳转")

        # HALT
        elif opcode == 0x0F:
            self.running = False
            print(f"   HALT: 程序结束")

        else:
            print(f"   未知指令: 0x{instruction:02X}")
            self.running = False

    def run(self, memory, max_cycles=100):
        """运行CPU"""
        print(f"   PC初始值: {self.pc}")

        while self.running and self.cycle_count < max_cycles:
            self.cycle_count += 1
            print(f"\n--- 周期 {self.cycle_count} (PC={self.pc-1}) ---")

            instruction = self.fetch(memory)
            print(f"   取出指令: 0x{instruction:02X}")

            self.decode_execute(instruction, memory)
            print(f"   状态: PC={self.pc}, ACC={self.accumulator}")

        return self.cycle_count


def create_sum_program():
    """
    创建计算 1+2+3+...+10 的程序

    算法思路：
    - 内存[10]: 计数器（从10递减到0）
    - 内存[11]: 累加和
    - 循环：
        1. 加载计数器
        2. 加到累加和
        3. 计数器减1
        4. 如果计数器不为0，跳回步骤1
    """
    memory = [0] * 32

    # 数据区
    memory[10] = 10   # 计数器初始值
    memory[11] = 0    # 累加和
    memory[12] = 1    # 常量1（用于减1）

    # 程序代码区
    # 地址0: LOAD 10 - 加载计数器
    memory[0] = 0x1A  # LOAD 10

    # 地址1: ADD 11 - 加到累加和
    memory[1] = 0x2B  # ADD 11

    # 地址2: STORE 11 - 保存累加和
    memory[2] = 0x4B  # STORE 11

    # 地址3: LOAD 10 - 重新加载计数器
    memory[3] = 0x1A  # LOAD 10

    # 地址4: SUB 12 - 计数器减1
    memory[4] = 0x3C  # SUB 12

    # 地址5: STORE 10 - 保存计数器
    memory[5] = 0x4A  # STORE 10

    # 地址6: JUMP_IF_ZERO 8 - 如果计数器为0，跳到结束（地址8）
    memory[6] = 0x78  # JUMP_IF_ZERO 8

    # 地址7: JUMP 0 - 否则跳回循环开始（地址0）
    memory[7] = 0x60  # JUMP 0

    # 地址8: LOAD 11 - 加载最终结果
    memory[8] = 0x1B  # LOAD 11

    # 地址9: HALT - 停止
    memory[9] = 0xF0  # HALT

    return memory


def main():
    print("=" * 60)
    print("练习3解答：扩展CPU实现循环")
    print("=" * 60)
    print("\n目标：计算 1+2+3+...+10")
    print("预期结果: 55\n")

    # 创建程序
    memory = create_sum_program()

    print("📋 程序代码:")
    print("   地址0: LOAD 10   (加载计数器)")
    print("   地址1: ADD 11    (加到累加和)")
    print("   地址2: STORE 11  (保存累加和)")
    print("   地址3: LOAD 10   (重新加载计数器)")
    print("   地址4: SUB 12    (计数器减1)")
    print("   地址5: STORE 10  (保存计数器)")
    print("   地址6: JUMP_IF_ZERO 8  (如果为0则结束)")
    print("   地址7: JUMP 0    (跳回循环开始)")
    print("   地址8: LOAD 11   (加载结果)")
    print("   地址9: HALT      (停止)")

    print("\n📦 初始内存状态:")
    print(f"   内存[10] (计数器) = {memory[10]}")
    print(f"   内存[11] (累加和) = {memory[11]}")
    print(f"   内存[12] (常量1)  = {memory[12]}")

    # 创建CPU并运行
    cpu = ExtendedCPU()

    print("\n" + "=" * 60)
    print("开始执行")
    print("=" * 60)

    cycles = cpu.run(memory)

    print("\n" + "=" * 60)
    print("执行完成")
    print("=" * 60)

    print(f"\n✅ 总执行周期: {cycles}")
    print(f"✅ 内存[11] (累加和) = {memory[11]}")
    print(f"✅ 内存[10] (计数器) = {memory[10]}")
    print(f"✅ 累加器 = {cpu.accumulator}")
    print(f"✅ 预期结果: 1+2+3+...+10 = 55")
    print(f"✅ 验证: {'通过！' if memory[11] == 55 else '失败！'}")

    # 验证数学公式
    expected = 10 * 11 // 2  # n*(n+1)/2
    print(f"\n📐 数学验证: n*(n+1)/2 = 10*11/2 = {expected}")

    return memory[11]


if __name__ == "__main__":
    result = main()

    print("\n" + "=" * 60)
    print("💡 关键洞察")
    print("=" * 60)
    print("""
1. JUMP指令让程序可以"回头"执行，形成循环
2. JUMP_IF_ZERO让程序可以根据条件决定是否跳转
3. 这两种指令的组合，让计算机可以执行任意复杂的逻辑
4. 这就是现代编程语言中 while/for/if 的底层实现！

在真实CPU中：
- JUMP 对应汇编指令 JMP
- JUMP_IF_ZERO 对应 JZ 或 JE (Jump if Zero/Equal)
- 所有高级语言的循环和条件，最终都编译成这些跳转指令
    """)
