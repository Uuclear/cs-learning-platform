# 指令周期可视化
# 展示CPU执行指令的完整周期

import time

class VisualCPU:
    """带可视化的CPU模拟器"""

    def __init__(self):
        self.pc = 0
        self.accumulator = 0
        self.ir = 0  # 指令寄存器：保存当前指令
        self.running = True
        self.cycle_count = 0

    def visualize_state(self, stage, memory):
        """可视化当前CPU状态"""
        print(f"\n  {'─' * 40}")
        print(f"  🔄 指令周期 {self.cycle_count} | 阶段: {stage}")
        print(f"  {'─' * 40}")
        print(f"  ┌─────────────────────────────────────┐")
        print(f"  │  📋 寄存器状态:                      │")
        print(f"  │     PC (程序计数器): {self.pc:3d}           │")
        print(f"  │     IR (指令寄存器): {self.ir:3d} (0x{self.ir:02x})    │")
        print(f"  │     ACC (累加器):    {self.accumulator:3d}           │")
        print(f"  └─────────────────────────────────────┘")

        # 显示内存中PC附近的内容
        print(f"  📦 内存快照 (PC附近):")
        start = max(0, self.pc - 1)
        for i in range(start, min(start + 4, len(memory))):
            marker = " <-- PC" if i == self.pc else ""
            print(f"     [{i:2d}]: {memory[i]:3d}{marker}")

    def fetch(self, memory):
        """取指令阶段"""
        self.ir = memory[self.pc]
        print(f"\n  📥 [取指令] 从内存[{self.pc}]取出指令: {self.ir}")
        self.pc += 1
        return self.ir

    def decode_execute(self, memory):
        """译码和执行阶段"""
        opcode = (self.ir >> 4) & 0x0F
        operand = self.ir & 0x0F

        operations = {
            0x01: ("LOAD", self.op_load),
            0x02: ("ADD", self.op_add),
            0x03: ("SUB", self.op_sub),
            0x04: ("MUL", self.op_mul),
            0x05: ("STORE", self.op_store),
            0x0F: ("HALT", self.op_halt),  # 0xF = 15
        }

        if opcode in operations:
            name, func = operations[opcode]
            print(f"  🔍 [译码] 操作码: {name}, 操作数: {operand}")
            print(f"  ⚡ [执行] ", end="")
            func(operand, memory)
        else:
            print(f"  ❌ [错误] 未知操作码: {opcode}")
            self.running = False

    def op_load(self, addr, memory):
        self.accumulator = memory[addr]
        print(f"LOAD: ACC = 内存[{addr}] = {self.accumulator}")

    def op_add(self, addr, memory):
        old = self.accumulator
        self.accumulator += memory[addr]
        print(f"ADD: {old} + 内存[{addr}]({memory[addr]}) = {self.accumulator}")

    def op_sub(self, addr, memory):
        old = self.accumulator
        self.accumulator -= memory[addr]
        print(f"SUB: {old} - 内存[{addr}]({memory[addr]}) = {self.accumulator}")

    def op_mul(self, addr, memory):
        old = self.accumulator
        self.accumulator *= memory[addr]
        print(f"MUL: {old} * 内存[{addr}]({memory[addr]}) = {self.accumulator}")

    def op_store(self, addr, memory):
        memory[addr] = self.accumulator
        print(f"STORE: 内存[{addr}] = ACC({self.accumulator})")

    def op_halt(self, operand, memory):
        print(f"HALT: CPU停止")
        self.running = False

    def run(self, memory, delay=0.5):
        """运行CPU，可选延迟以便观察"""
        print("=" * 60)
        print("🚀 冯诺依曼CPU启动！")
        print("=" * 60)
        print("\n💡 观察要点：")
        print("   1. PC如何一步步前进")
        print("   2. 指令如何从内存取出")
        print("   3. 累加器如何变化")
        print("   4. 程序和数据共享内存")

        while self.running and self.pc < len(memory):
            self.cycle_count += 1

            # 取指令
            self.visualize_state("取指令前", memory)
            self.fetch(memory)

            # 译码和执行
            self.visualize_state("执行后", memory)
            self.decode_execute(memory)

            if delay > 0:
                time.sleep(delay)

        print("\n" + "=" * 60)
        print(f"✅ 程序执行完毕！")
        print(f"   总周期数: {self.cycle_count}")
        print(f"   最终结果: {self.accumulator}")
        print("=" * 60)


# 创建CPU实例
cpu = VisualCPU()

# 准备内存（程序 + 数据）
memory = [0] * 32

# 编写程序：计算 (2 + 3) * 4
# 程序代码区
memory[0] = 0x1A   # LOAD 10: 加载地址10的值 (0001 1010)
memory[1] = 0x2B   # ADD 11: 加上地址11的值 (0010 1011)
memory[2] = 0x4D   # STORE 13: 存储中间结果到地址13 (0100 1101)
memory[3] = 0x1C   # LOAD 12: 加载地址12的值（乘数）(0001 1100)
memory[4] = 0x4D   # MUL 13: 乘以地址13的值（中间结果）(0100 1101)
memory[5] = 0x4E   # STORE 14: 存储最终结果 (0100 1110)
memory[6] = 0xF0   # HALT: 停止 (1111 0000)
# 数据区
memory[10] = 0x02   # 数据: 2
memory[11] = 0x03   # 数据: 3
memory[12] = 0x04   # 数据: 4
memory[13] = 0x00   # 中间结果存储位置
memory[14] = 0x00   # 最终结果存储位置

# 运行（无延迟，直接输出）
cpu.run(memory, delay=0)

print(f"\n📝 验证: (2 + 3) * 4 = {(2 + 3) * 4}")
print(f"   内存[6] = {memory[6]}")
