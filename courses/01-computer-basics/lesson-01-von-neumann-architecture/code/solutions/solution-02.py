# 练习2解答：设计指令
# 实现 A * B + C 的计算

def design_instructions():
    """
    设计指令集实现 A * B + C
    假设 A=3, B=4, C=5
    """
    print("=" * 60)
    print("练习2解答：设计指令实现 A * B + C")
    print("=" * 60)

    # 定义指令集
    instructions = {
        'LOAD': 0x01,   # 从内存加载到累加器
        'ADD': 0x02,    # 加法
        'MUL': 0x04,    # 乘法
        'STORE': 0x05,  # 存储到内存
        'HALT': 0x0F,   # 停止
    }

    print("\n📋 指令集设计:")
    for name, code in instructions.items():
        print(f"   {name}: 0x0{code:X} (操作码)")

    # 内存布局设计
    print("\n📦 内存布局:")
    print("   地址0-4:  程序代码区")
    print("   地址10:   数据 A = 3")
    print("   地址11:   数据 B = 4")
    print("   地址12:   数据 C = 5")
    print("   地址20:   结果存储区")

    # 初始化内存
    memory = [0] * 32

    # 数据区
    memory[10] = 3   # A = 3
    memory[11] = 4   # B = 4
    memory[12] = 5   # C = 5

    # 程序代码区（地址0-4）
    # LOAD 10 -> 0x1A (操作码0x01, 操作数0x0A=10)
    memory[0] = 0x1A

    # MUL 11 -> 0x4B (操作码0x04, 操作数0x0B=11)
    memory[1] = 0x4B

    # ADD 12 -> 0x2C (操作码0x02, 操作数0x0C=12)
    memory[2] = 0x2C

    # STORE 20 -> 0x54 (操作码0x05, 操作数0x14=20)
    memory[3] = 0x54

    # HALT -> 0xF0 (操作码0x0F, 操作数0x00)
    memory[4] = 0xF0

    print("\n📝 机器码程序:")
    print("   地址0: 0x1A  (LOAD 10)")
    print("   地址1: 0x4B  (MUL 11)")
    print("   地址2: 0x2C  (ADD 12)")
    print("   地址3: 0x54  (STORE 20)")
    print("   地址4: 0xF0  (HALT)")

    # 内存布局图
    print("\n🗺️  内存布局图:")
    print("""
    ┌─────────────────────────────────────┐
    │  地址   │  内容      │  说明         │
    ├─────────────────────────────────────┤
    │   0     │  0x1A      │  LOAD 10      │
    │   1     │  0x4B      │  MUL 11       │
    │   2     │  0x2C      │  ADD 12       │
    │   3     │  0x54      │  STORE 20     │
    │   4     │  0xF0      │  HALT         │
    │  ...    │  ...       │  ...          │
    │  10     │  3         │  数据 A       │
    │  11     │  4         │  数据 B       │
    │  12     │  5         │  数据 C       │
    │  ...    │  ...       │  ...          │
    │  20     │  ?         │  结果 (3*4+5) │
    └─────────────────────────────────────┘
    """)

    # 执行程序
    print("\n🚀 执行程序...")
    pc = 0
    accumulator = 0
    running = True

    while running and pc < len(memory):
        instruction = memory[pc]
        pc += 1

        opcode = (instruction >> 4) & 0x0F
        operand = instruction & 0x0F

        if opcode == 0x01:  # LOAD
            accumulator = memory[operand]
            print(f"   LOAD {operand}: 累加器 = {accumulator}")

        elif opcode == 0x02:  # ADD
            old = accumulator
            accumulator += memory[operand]
            print(f"   ADD {operand}: {old} + {memory[operand]} = {accumulator}")

        elif opcode == 0x04:  # MUL
            old = accumulator
            accumulator *= memory[operand]
            print(f"   MUL {operand}: {old} * {memory[operand]} = {accumulator}")

        elif opcode == 0x05:  # STORE
            memory[operand] = accumulator
            print(f"   STORE {operand}: 内存[{operand}] = {accumulator}")

        elif opcode == 0x0F:  # HALT
            running = False
            print(f"   HALT: 程序结束")

    print("\n" + "=" * 60)
    print("执行结果")
    print("=" * 60)
    print(f"\n✅ 内存[20] = {memory[20]}")
    print(f"✅ 预期结果: A * B + C = 3 * 4 + 5 = 17")
    print(f"✅ 验证: {'通过！' if memory[20] == 17 else '失败！'}")

    return memory[20]


if __name__ == "__main__":
    result = design_instructions()

    print("\n" + "=" * 60)
    print("💡 扩展思考")
    print("=" * 60)
    print("""
问题：如果要计算 (A + B) * C，需要如何修改程序？

答案：
只需要交换 LOAD 和 MUL 的顺序：

原程序（A * B + C）：
  1. LOAD A      -> ACC = A
  2. MUL B       -> ACC = A * B
  3. ADD C       -> ACC = A * B + C

新程序（(A + B) * C）：
  1. LOAD A      -> ACC = A
  2. ADD B       -> ACC = A + B
  3. MUL C       -> ACC = (A + B) * C

关键洞察：冯诺依曼计算机按照指令顺序执行，
改变指令顺序就改变了计算逻辑！
    """)
