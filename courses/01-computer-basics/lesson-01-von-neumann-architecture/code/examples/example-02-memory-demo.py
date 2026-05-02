# 内存读写演示
# 展示冯诺依曼架构中存储器的工作原理

class Memory:
    """模拟计算机内存"""

    def __init__(self, size=256):
        """初始化内存，size是存储单元数量"""
        self.size = size
        self.cells = [0] * size  # 所有存储单元初始化为0
        self.access_count = 0    # 记录访问次数

    def read(self, address):
        """
        从指定地址读取数据
        参数: address - 内存地址（0到size-1）
        返回: 该地址存储的数据
        """
        if 0 <= address < self.size:
            self.access_count += 1
            value = self.cells[address]
            print(f"  [内存读] 地址 {address:3d} -> 值 {value:3d}")
            return value
        else:
            raise IndexError(f"地址 {address} 超出范围！有效范围: 0-{self.size-1}")

    def write(self, address, value):
        """
        向指定地址写入数据
        参数: address - 内存地址
              value - 要写入的数据
        """
        if 0 <= address < self.size:
            self.access_count += 1
            old_value = self.cells[address]
            self.cells[address] = value
            print(f"  [内存写] 地址 {address:3d} <- 值 {value:3d} (原值: {old_value})")
        else:
            raise IndexError(f"地址 {address} 超出范围！有效范围: 0-{self.size-1}")

    def dump(self, start=0, end=None):
        """显示内存内容，就像调试器一样"""
        if end is None:
            end = min(start + 16, self.size)

        print(f"\n  [内存快照] 地址 {start} 到 {end-1}:")
        print("  地址 | 值(十进制) | 值(十六进制)")
        print("  " + "-" * 35)
        for i in range(start, end):
            marker = " <-- PC" if i == getattr(self, '_highlight', -1) else ""
            print(f"  {i:4d} | {self.cells[i]:10d} | 0x{self.cells[i]:08x}{marker}")


# 演示内存操作
print("=" * 60)
print("内存操作演示")
print("=" * 60)

# 创建256个单元的内存
mem = Memory(256)

print("\n1. 写入一些数据到内存...")
mem.write(0, 100)      # 地址0写入100
mem.write(1, 200)      # 地址1写入200
mem.write(10, 0x55)    # 地址10写入十六进制55
mem.write(11, 0xAA)    # 地址11写入十六进制AA

print("\n2. 从内存读取数据...")
val1 = mem.read(0)
val2 = mem.read(1)
print(f"   读取结果: {val1} + {val2} = {val1 + val2}")

print("\n3. 查看内存快照...")
mem.dump(0, 16)

print("\n4. 模拟程序存储...")
# 在冯诺依曼架构中，程序和数据都存储在内存中！
program = [
    ("LOAD", 10),   # 从地址10加载
    ("ADD", 11),    # 加上地址11的值
    ("STORE", 20),  # 存储到地址20
]

# 将"程序"编码为数字存入内存（简化编码）
mem.write(100, 1)   # 1 表示 LOAD
mem.write(101, 10)  # 操作数：地址10
mem.write(102, 2)   # 2 表示 ADD
mem.write(103, 11)  # 操作数：地址11
mem.write(104, 4)   # 4 表示 STORE
mem.write(105, 20)  # 操作数：地址20

print("\n5. 程序存储区快照（地址100-110）:")
mem.dump(100, 110)

print(f"\n6. 统计信息:")
print(f"   内存总大小: {mem.size} 单元")
print(f"   访问次数: {mem.access_count}")
print(f"   利用率: {mem.access_count / mem.size * 100:.1f}%")

print("\n" + "=" * 60)
print("关键洞察：程序和数据都以数字形式存储在内存中！")
print("这就是冯诺依曼架构的核心创新——存储程序概念。")
print("=" * 60)
