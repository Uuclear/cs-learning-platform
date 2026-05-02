# 模拟CPU流水线的工作原理
# 流水线让CPU可以同时处理多条指令的不同阶段，提高效率

class PipelineCPU:
    """
    简易流水线CPU模拟器
    就像工厂的生产流水线，每个阶段同时处理不同的产品
    """
    
    def __init__(self):
        # 流水线的四个阶段
        self.stages = {
            'FETCH': None,    # 取指令阶段
            'DECODE': None,   # 解码阶段
            'EXECUTE': None,  # 执行阶段
            'WRITEBACK': None # 写回阶段
        }
        
        # 指令内存
        self.memory = []
        # 寄存器
        self.registers = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0}
        # 程序计数器
        self.pc = 0
        # 时钟周期计数
        self.cycle = 0
        # 完成的指令数
        self.completed = 0
        
    def load_program(self, program):
        """加载程序到内存"""
        self.memory = program
        print(f"[系统] 程序加载完成，共{len(program)}条指令")
    
    def fetch(self):
        """取指令阶段 - 从内存中取出指令"""
        if self.pc < len(self.memory):
            instruction = self.memory[self.pc]
            self.pc += 1
            return {'stage': 'FETCH', 'instruction': instruction, 'pc': self.pc - 1}
        return None
    
    def decode(self, instruction_data):
        """解码阶段 - 理解指令的含义"""
        instr = instruction_data['instruction']
        parts = instr.split()
        
        decoded = {
            'stage': 'DECODE',
            'instruction': instr,
            'pc': instruction_data['pc'],
            'op': parts[0],
            'operands': parts[1:] if len(parts) > 1 else []
        }
        return decoded
    
    def execute(self, decoded_data):
        """执行阶段 - ALU进行计算"""
        op = decoded_data['op']
        operands = decoded_data['operands']
        result = None
        
        if op == 'ADD':
            # ADD R0, R1 -> R0 = R0 + R1
            reg1 = operands[0].replace(',', '')
            reg2 = operands[1]
            result = self.registers[reg1] + self.registers[reg2]
        elif op == 'SUB':
            reg1 = operands[0].replace(',', '')
            reg2 = operands[1]
            result = self.registers[reg1] - self.registers[reg2]
        elif op == 'LOAD':
            # LOAD R0, 10
            reg = operands[0].replace(',', '')
            value = int(operands[1])
            result = value
        elif op == 'MUL':
            reg1 = operands[0].replace(',', '')
            reg2 = operands[1]
            result = self.registers[reg1] * self.registers[reg2]
        
        decoded_data['result'] = result
        decoded_data['stage'] = 'EXECUTE'
        return decoded_data
    
    def writeback(self, execute_data):
        """写回阶段 - 将结果写回寄存器"""
        op = execute_data['op']
        result = execute_data.get('result')
        operands = execute_data['operands']
        
        if op in ['ADD', 'SUB', 'MUL']:
            reg = operands[0].replace(',', '')
            self.registers[reg] = result
        elif op == 'LOAD':
            reg = operands[0].replace(',', '')
            self.registers[reg] = result
        
        execute_data['stage'] = 'WRITEBACK'
        self.completed += 1
        return execute_data
    
    def run_cycle(self):
        """运行一个时钟周期"""
        self.cycle += 1
        print(f"\n{'='*60}")
        print(f"时钟周期 {self.cycle}")
        print(f"{'='*60}")
        
        # 流水线推进（从后往前，避免覆盖）
        # WRITEBACK阶段完成
        if self.stages['WRITEBACK']:
            completed = self.stages['WRITEBACK']
            print(f"[WRITEBACK] 完成指令: {completed['instruction']}")
            self.stages['WRITEBACK'] = None
        
        # EXECUTE -> WRITEBACK
        if self.stages['EXECUTE']:
            self.stages['WRITEBACK'] = self.writeback(self.stages['EXECUTE'])
            print(f"[EXECUTE] 执行指令: {self.stages['EXECUTE']['instruction']} -> 结果: {self.stages['EXECUTE'].get('result')}")
            self.stages['EXECUTE'] = None
        
        # DECODE -> EXECUTE
        if self.stages['DECODE']:
            self.stages['EXECUTE'] = self.execute(self.stages['DECODE'])
            print(f"[DECODE] 解码指令: {self.stages['DECODE']['instruction']}")
            self.stages['DECODE'] = None
        
        # FETCH -> DECODE
        if self.stages['FETCH']:
            self.stages['DECODE'] = self.decode(self.stages['FETCH'])
            print(f"[FETCH] 取出指令: {self.stages['FETCH']['instruction']}")
            self.stages['FETCH'] = None
        
        # 新的FETCH
        new_instr = self.fetch()
        if new_instr:
            self.stages['FETCH'] = new_instr
            print(f"[FETCH] 从内存取出新指令")
        
        # 显示当前流水线状态
        self.show_pipeline()
    
    def show_pipeline(self):
        """显示当前流水线状态"""
        print("\n当前流水线状态:")
        for stage, data in self.stages.items():
            if data:
                print(f"  {stage:10}: {data['instruction']}")
            else:
                print(f"  {stage:10}: [空闲]")
        print(f"\n寄存器状态: {self.registers}")
    
    def run(self):
        """运行整个程序"""
        print(f"\n{'#'*60}")
        print("开始流水线执行")
        print(f"{'#'*60}")
        
        # 持续运行直到所有指令完成
        while (self.pc < len(self.memory) or 
               any(self.stages.values())):
            self.run_cycle()
        
        print(f"\n{'#'*60}")
        print("流水线执行完成！")
        print(f"总时钟周期: {self.cycle}")
        print(f"完成指令数: {self.completed}")
        print(f"平均每条指令周期 (CPI): {self.cycle / self.completed:.2f}")
        print(f"最终寄存器状态: {self.registers}")
        print(f"{'#'*60}")


# 测试程序
program = [
    "LOAD R0, 5",     # R0 = 5
    "LOAD R1, 3",     # R1 = 3
    "ADD R0, R1",     # R0 = R0 + R1 = 8
    "LOAD R2, 2",     # R2 = 2
    "MUL R0, R2",     # R0 = R0 * R2 = 16
]

print("=" * 60)
print("流水线CPU模拟 - 让CPU一心多用")
print("=" * 60)
print("\n程序代码:")
for i, instr in enumerate(program):
    print(f"  [{i}] {instr}")

# 创建CPU并运行
cpu = PipelineCPU()
cpu.load_program(program)
cpu.run()

print("\n" + "=" * 60)
print("对比说明:")
print("=" * 60)
print("非流水线执行: 5条指令 × 4个阶段 = 20个周期")
print(f"流水线执行:   {cpu.cycle}个周期")
print(f"效率提升:     约{20/cpu.cycle:.1f}倍！")
print("=" * 60)
