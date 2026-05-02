# 模拟ALU（算术逻辑单元）的工作原理
# ALU是CPU的计算核心，负责执行算术和逻辑运算

class SimpleALU:
    """
    简易ALU模拟器
    就像工厂里的数控机床，专门负责计算
    """
    
    def __init__(self):
        # ALU内部有两个输入寄存器和一个输出寄存器
        self.input_a = 0
        self.input_b = 0
        self.output = 0
        self.operation = None
    
    def load(self, a, b, op):
        """
        加载数据和操作指令
        就像把原材料放到机床的进料口
        """
        self.input_a = a
        self.input_b = b
        self.operation = op
        print(f"[ALU] 加载数据: A={a}, B={b}, 操作={op}")
    
    def execute(self):
        """
        执行运算
        就像机床开始加工
        """
        if self.operation == "ADD":
            self.output = self.input_a + self.input_b
            print(f"[ALU] 执行加法: {self.input_a} + {self.input_b} = {self.output}")
        elif self.operation == "SUB":
            self.output = self.input_a - self.input_b
            print(f"[ALU] 执行减法: {self.input_a} - {self.input_b} = {self.output}")
        elif self.operation == "AND":
            self.output = self.input_a & self.input_b
            print(f"[ALU] 执行与运算: {self.input_a} & {self.input_b} = {self.output}")
        elif self.operation == "OR":
            self.output = self.input_a | self.input_b
            print(f"[ALU] 执行或运算: {self.input_a} | {self.input_b} = {self.output}")
        elif self.operation == "CMP":
            # 比较运算，设置标志位
            if self.input_a > self.input_b:
                self.output = 1  # 大于
                print(f"[ALU] 比较: {self.input_a} > {self.input_b}, 结果=大于")
            elif self.input_a < self.input_b:
                self.output = -1  # 小于
                print(f"[ALU] 比较: {self.input_a} < {self.input_b}, 结果=小于")
            else:
                self.output = 0  # 等于
                print(f"[ALU] 比较: {self.input_a} = {self.input_b}, 结果=等于")
        else:
            print(f"[ALU] 未知操作: {self.operation}")
        
        return self.output


# 演示ALU的工作
print("=" * 50)
print("ALU运算演示 - CPU的计算心脏")
print("=" * 50)

alu = SimpleALU()

# 测试各种运算
print("\n--- 算术运算 ---")
alu.load(15, 27, "ADD")
alu.execute()

alu.load(100, 42, "SUB")
alu.execute()

print("\n--- 逻辑运算 ---")
alu.load(5, 3, "AND")  # 5(101) & 3(011) = 1(001)
alu.execute()

alu.load(5, 3, "OR")   # 5(101) | 3(011) = 7(111)
alu.execute()

print("\n--- 比较运算 ---")
alu.load(10, 5, "CMP")
alu.execute()

alu.load(5, 10, "CMP")
alu.execute()

alu.load(7, 7, "CMP")
alu.execute()

print("\n" + "=" * 50)
print("ALU演示完成！")
print("=" * 50)
