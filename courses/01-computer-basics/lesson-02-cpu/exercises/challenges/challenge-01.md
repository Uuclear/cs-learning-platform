# 挑战1：设计一个简单指令集

## 难度
⭐

## 描述

设计一个包含4条指令的简单指令集，并用Python模拟执行。通过这个挑战，你将理解CPU是如何一步步执行程序指令的。

## 要求

1. 设计4条指令：
   - `LOAD R, value` - 将立即数加载到寄存器R
   - `ADD R1, R2` - 将寄存器R2的值加到R1上
   - `SUB R1, R2` - 从寄存器R1中减去R2的值
   - `HALT` - 停止执行

2. 编写一个程序，计算 `15 + 27 - 10` 的结果

3. 模拟CPU执行这个程序，输出每一步的状态变化

## 输入

无需输入，程序内置测试代码。

## 输出

程序执行过程中的详细日志，包括：
- 每条指令的取指、解码、执行过程
- 寄存器状态的变化
- 最终计算结果

## 示例

```
程序代码:
  [0] LOAD R0, 15
  [1] LOAD R1, 27
  [2] ADD R0, R1
  [3] LOAD R1, 10
  [4] SUB R0, R1
  [5] HALT

执行过程:
>>> 步骤 1: 取指令 [LOAD R0, 15] -> 解码 -> 执行 -> R0 = 15
>>> 步骤 2: 取指令 [LOAD R1, 27] -> 解码 -> 执行 -> R1 = 27
...

最终结果: R0 = 32
```

## 提示

1. 参考课件中的寄存器示例代码，设计一个简单的CPU类
2. 使用字典存储寄存器状态
3. 使用列表存储程序指令（模拟内存）
4. 使用PC（程序计数器）跟踪当前执行位置

## 进阶思考

- 如果要添加乘法指令，应该如何修改代码？
- 如何添加条件跳转指令（如JUMP）？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

1. 创建一个SimpleCPU类，包含寄存器和PC
2. 实现execute_program方法，循环取指令、解码、执行
3. 根据指令类型执行相应操作
4. 直到遇到HALT指令停止

### 代码

```python
class SimpleCPU:
    def __init__(self):
        self.registers = {'R0': 0, 'R1': 0, 'R2': 0}
        self.pc = 0
        self.running = True
    
    def execute_program(self, program):
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
                reg = parts[1].replace(',', '')
                value = int(parts[2])
                self.registers[reg] = value
                print(f"  [执行] {reg} = {value}")
            
            elif op == 'ADD':
                reg1 = parts[1].replace(',', '')
                reg2 = parts[2]
                old_val = self.registers[reg1]
                self.registers[reg1] += self.registers[reg2]
                print(f"  [执行] {reg1} = {old_val} + {self.registers[reg2]} = {self.registers[reg1]}")
            
            elif op == 'SUB':
                reg1 = parts[1].replace(',', '')
                reg2 = parts[2]
                old_val = self.registers[reg1]
                self.registers[reg1] -= self.registers[reg2]
                print(f"  [执行] {reg1} = {old_val} - {self.registers[reg2]} = {self.registers[reg1]}")
            
            elif op == 'HALT':
                print(f"  [执行] 停止执行")
                self.running = False
            
            print(f"  [寄存器状态] {self.registers}")
            step += 1
        
        print(f"\n最终结果: R0 = {self.registers['R0']}")


# 测试程序：计算 15 + 27 - 10
program = [
    "LOAD R0, 15",
    "LOAD R1, 27",
    "ADD R0, R1",
    "LOAD R1, 10",
    "SUB R0, R1",
    "HALT"
]

cpu = SimpleCPU()
cpu.execute_program(program)
```

### 复杂度分析

- 时间复杂度: O(n)，n为指令数，每条指令执行一次
- 空间复杂度: O(1)，使用固定数量的寄存器

</details>
