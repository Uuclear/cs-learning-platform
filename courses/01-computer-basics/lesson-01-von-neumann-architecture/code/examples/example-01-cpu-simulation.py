# 简单CPU模拟器
# 展示冯诺依曼架构的核心：取指令-译码-执行循环

class SimpleCPU:
    """模拟一个简单的CPU，包含控制器和ALU"""

    def __init__(self):
        # 寄存器（CPU内部的超高速存储）
        self.pc = 0          # 程序计数器：记录下一条指令的地址
        self.accumulator = 0 # 累加器：存储运算结果
        self.running = True  # CPU运行状态

        # 指令集定义
        self.instructions = {
            'LOAD': 0x01,   # 从内存加载数据到累加器
            'ADD': 0x02,    # 加法
            'SUB': 0x03,    # 减法
            'STORE': 0x04,  # 存储累加器到内存
            'HALT': 0xFF,   # 停止运行
        }

    def fetch(self, memory):
        """取指令阶段：从内存中取出指令"""
        instruction = memory[self.pc]
        print(f"  [取指令] 从地址 {self.pc} 取出: {hex(instruction)}")
        self.pc += 1  # 程序计数器+1，指向下一条指令
        return instruction

    def decode(self, instruction):
        """译码阶段：解析指令"""
        opcode = (instruction >> 4) & 0x0F  # 高4位是操作码
        operand = instruction & 0x0F        # 低4位是操作数

        for name, code in self.instructions.items():
            if code == opcode:
                print(f"  [译码] 指令: {name}, 操作数: {operand}")
                return name, operand

        return 'UNKNOWN', operand

    def execute(self, operation, operand, memory):
        """执行阶段：执行指令"""
        if operation == 'LOAD':
            self.accumulator = memory[operand]
            print(f"  [执行] LOAD: 从内存[{operand}]加载 {self.accumulator} 到累加器")

        elif operation == 'ADD':
            value = memory[operand]
            old_value = self.accumulator
            self.accumulator += value
            print(f"  [执行] ADD: {old_value} + {value} = {self.accumulator}")

        elif operation == 'SUB':
            value = memory[operand]
            old_value = self.accumulator
            self.accumulator -= value
            print(f"  [执行] SUB: {old_value} - {value} = {self.accumulator}")

        elif operation == 'STORE':
            memory[operand] = self.accumulator
            print(f"  [执行] STORE: 将累加器值 {self.accumulator} 存入内存[{operand}]")

        elif operation == 'HALT':
            self.running = False
            print(f"  [执行] HALT: CPU停止运行")

        else:
            print(f"  [执行] 未知指令！")

    def run(self, memory):
        """运行CPU：不断循环取指令-译码-执行"""
        print("=" * 50)
        print("CPU开始运行...")
        print("=" * 50)

        step = 1
        while self.running and self.pc < len(memory):
            print(f"\n--- 周期 {step} ---")

            # 冯诺依曼核心循环：取指令 -> 译码 -> 执行
            instruction = self.fetch(memory)
            operation, operand = self.decode(instruction)
            self.execute(operation, operand, memory)

            print(f"  [状态] PC={self.pc}, 累加器={self.accumulator}")
            step += 1

            if step > 20:  # 安全限制，防止无限循环
                print("达到最大周期数，强制停止")
                break

        print("\n" + "=" * 50)
        print("CPU运行结束")
        print(f"最终结果: 累加器 = {self.accumulator}")
        print("=" * 50)


# 测试程序：计算 5 + 3 - 2
# 程序存储在内存中（这就是"存储程序"的概念！）
memory = [0] * 16  # 16个存储单元

# 编写程序（数据和指令都存储在同一块内存中）
memory[0] = 0x15   # LOAD 5: 从地址5加载数据
memory[1] = 0x23   # ADD 3: 加上地址3的数据
memory[2] = 0x34   # SUB 4: 减去地址4的数据
memory[3] = 0x0A   # 数据: 10 (注意：程序和数据混合存储！)
memory[4] = 0x02   # 数据: 2
memory[5] = 0x05   # 数据: 5
memory[6] = 0x46   # STORE 6: 结果存入地址6
memory[7] = 0xFF0  # HALT: 停止

# 初始化CPU并运行
cpu = SimpleCPU()
cpu.run(memory)

print(f"\n内存[6]中的结果: {memory[6]}")
print(f"预期结果: 5 + 10 - 2 = 13")
