# 模拟CPU寄存器的工作原理
# 寄存器是CPU内部的高速存储空间，就像厂长办公桌上的便签纸

class CPURegisters:
    """
    简易寄存器组模拟器
    就像厂长办公桌上的各种便签和文件夹
    """
    
    def __init__(self):
        # 通用寄存器 - 用于存放临时数据
        self.general_registers = {
            'R0': 0,  # 就像便签纸1
            'R1': 0,  # 便签纸2
            'R2': 0,  # 便签纸3
            'R3': 0,  # 便签纸4
        }
        
        # 特殊寄存器 - 各有专门用途
        self.PC = 0   # Program Counter - 程序计数器，记录"下一条指令在哪里"
        self.IR = None  # Instruction Register - 指令寄存器，存放"当前正在执行的指令"
        self.SP = 100  # Stack Pointer - 栈指针，记录"栈顶在哪里"
        self.ACC = 0  # Accumulator - 累加器，专门用于存放计算结果
        
        print("[寄存器组] 初始化完成")
        print(f"  通用寄存器: {list(self.general_registers.keys())}")
        print(f"  特殊寄存器: PC(程序计数器), IR(指令寄存器), SP(栈指针), ACC(累加器)")
    
    def write(self, reg_name, value):
        """向寄存器写入数据"""
        if reg_name in self.general_registers:
            old_value = self.general_registers[reg_name]
            self.general_registers[reg_name] = value
            print(f"[寄存器] {reg_name}: {old_value} → {value}")
        elif reg_name == 'PC':
            old_value = self.PC
            self.PC = value
            print(f"[PC] 程序计数器: {old_value} → {value} (下一条指令地址)")
        elif reg_name == 'ACC':
            old_value = self.ACC
            self.ACC = value
            print(f"[ACC] 累加器: {old_value} → {value} (计算结果)")
        else:
            print(f"[错误] 未知寄存器: {reg_name}")
    
    def read(self, reg_name):
        """从寄存器读取数据"""
        if reg_name in self.general_registers:
            value = self.general_registers[reg_name]
            print(f"[寄存器] 读取 {reg_name} = {value}")
            return value
        elif reg_name == 'PC':
            print(f"[PC] 读取程序计数器 = {self.PC}")
            return self.PC
        elif reg_name == 'ACC':
            print(f"[ACC] 读取累加器 = {self.ACC}")
            return self.ACC
        else:
            print(f"[错误] 未知寄存器: {reg_name}")
            return None
    
    def fetch_instruction(self, memory):
        """
        取指令
        PC告诉我们要从内存的哪个位置取指令
        """
        address = self.PC
        if address < len(memory):
            self.IR = memory[address]
            self.PC += 1  # PC自动加1，指向下一条指令
            print(f"[取指令] 从地址{address}取出指令: '{self.IR}'")
            print(f"[PC更新] 现在指向下一个地址: {self.PC}")
            return self.IR
        else:
            print("[取指令] 到达程序末尾")
            return None
    
    def show_status(self):
        """显示所有寄存器的当前状态"""
        print("\n" + "-" * 40)
        print("当前寄存器状态:")
        print("-" * 40)
        print("通用寄存器:")
        for reg, value in self.general_registers.items():
            print(f"  {reg} = {value}")
        print("特殊寄存器:")
        print(f"  PC (程序计数器) = {self.PC}")
        print(f"  IR (指令寄存器) = {self.IR}")
        print(f"  SP (栈指针)     = {self.SP}")
        print(f"  ACC (累加器)    = {self.ACC}")
        print("-" * 40)


# 模拟一段简单的程序（存储在内存中）
program = [
    "LOAD R0, 10",    # 将10加载到R0
    "LOAD R1, 20",    # 将20加载到R1
    "ADD R0, R1",     # R0 + R1
    "STORE R2",       # 结果存到R2
    "HALT"            # 停止
]

print("=" * 50)
print("寄存器操作演示 - CPU的高速便签纸")
print("=" * 50)

# 创建寄存器组
regs = CPURegisters()

print("\n--- 模拟程序加载到内存 ---")
for i, instr in enumerate(program):
    print(f"  地址[{i}]: {instr}")

print("\n--- 开始执行程序 ---")
step = 1
while True:
    print(f"\n>>> 步骤 {step}:")
    instruction = regs.fetch_instruction(program)
    if instruction is None or instruction == "HALT":
        print("[程序] 执行完毕！")
        break
    
    # 模拟指令解码和执行
    if "LOAD" in instruction:
        parts = instruction.split()
        reg = parts[1].replace(",", "")
        value = int(parts[2])
        regs.write(reg, value)
    elif "ADD" in instruction:
        parts = instruction.split()
        reg1 = parts[1].replace(",", "")
        reg2 = parts[2]
        val1 = regs.read(reg1)
        val2 = regs.read(reg2)
        result = val1 + val2
        regs.write('ACC', result)
    elif "STORE" in instruction:
        reg = instruction.split()[1]
        regs.write(reg, regs.ACC)
    
    step += 1

# 显示最终状态
regs.show_status()

print("\n" + "=" * 50)
print("寄存器演示完成！")
print("=" * 50)
