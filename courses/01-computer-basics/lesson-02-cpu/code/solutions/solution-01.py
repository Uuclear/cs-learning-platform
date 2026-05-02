# 练习1解答：设计一个简单指令集
# 设计4条指令：LOAD、ADD、SUB、HALT，并计算 15 + 27 - 10

class SimpleCPU:
    """
    简易CPU模拟器
    实现4条基本指令：LOAD、ADD、SUB、HALT
    """
    
    def __init__(self):
        # 初始化寄存器
        self.registers = {'R0': 0, 'R1': 0, 'R2': 0}
        # 程序计数器
        self.pc = 0
        # 运行状态
        self.running = True
    
    def execute_program(self, program):
        """执行程序"""
        print("程序代码:")
        for i, instr in enumerate(program):
            print(f"  [{i}] {instr}")
        print("\n执行过程:")
        
        step = 1
        while self.running and self.pc < len(program):
            print(f"\n>>> 步骤 {step}:")
            instruction = program[self.pc]
            print(f"  [取指] PC={self.pc}, 指令='{instruction}'")
            self.pc += 1
            
            # 解码和执行
            parts = instruction.split()
            op = parts[0]
            
            if op == 'LOAD':
                # LOAD R, value - 将立即数加载到寄存器
                reg = parts[1].replace(',', '')
                value = int(parts[2])
                old_val = self.registers[reg]
                self.registers[reg] = value
                print(f"  [解码] 操作: LOAD, 目标寄存器: {reg}, 值: {value}")
                print(f"  [执行] {reg}: {old_val} → {value}")
            
            elif op == 'ADD':
                # ADD R1, R2 - R1 = R1 + R2
                reg1 = parts[1].replace(',', '')
                reg2 = parts[2]
                old_val = self.registers[reg1]
                self.registers[reg1] += self.registers[reg2]
                print(f"  [解码] 操作: ADD, {reg1} = {reg1} + {reg2}")
                print(f"  [执行] {reg1}: {old_val} + {self.registers[reg2]} = {self.registers[reg1]}")
            
            elif op == 'SUB':
                # SUB R1, R2 - R1 = R1 - R2
                reg1 = parts[1].replace(',', '')
                reg2 = parts[2]
                old_val = self.registers[reg1]
                self.registers[reg1] -= self.registers[reg2]
                print(f"  [解码] 操作: SUB, {reg1} = {reg1} - {reg2}")
                print(f"  [执行] {reg1}: {old_val} - {self.registers[reg2]} = {self.registers[reg1]}")
            
            elif op == 'HALT':
                # HALT - 停止执行
                print(f"  [解码] 操作: HALT")
                print(f"  [执行] 停止执行")
                self.running = False
            
            print(f"  [寄存器状态] {self.registers}")
            step += 1
        
        print(f"\n{'='*50}")
        print(f"最终结果: R0 = {self.registers['R0']}")
        print(f"验证: 15 + 27 - 10 = {15 + 27 - 10}")
        print(f"{'='*50}")


# 测试程序：计算 15 + 27 - 10
program = [
    "LOAD R0, 15",    # R0 = 15
    "LOAD R1, 27",    # R1 = 27
    "ADD R0, R1",     # R0 = R0 + R1 = 15 + 27 = 42
    "LOAD R1, 10",    # R1 = 10 (复用R1作为临时寄存器)
    "SUB R0, R1",     # R0 = R0 - R1 = 42 - 10 = 32
    "HALT"            # 停止
]

print("=" * 50)
print("练习1解答：简单指令集模拟")
print("=" * 50)

cpu = SimpleCPU()
cpu.execute_program(program)
