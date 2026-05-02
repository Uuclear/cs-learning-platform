# 总线通信模拟
# 演示地址线、数据线、控制线如何协同工作

class BusLine:
    """模拟一根总线线路"""
    def __init__(self, name, direction):
        self.name = name          # 线路名称
        self.direction = direction # 方向：单向或双向
        self.data = None          # 当前传输的数据

    def send(self, data):
        """发送数据"""
        self.data = data
        print(f"  [{self.name}] 发送: {data}")

    def receive(self):
        """接收数据"""
        return self.data


class SimpleBus:
    """
    简化的总线模拟器
    包含地址线、数据线和控制线
    """
    def __init__(self, address_bits=32, data_bits=64):
        # 地址线：32位，单向（CPU→内存）
        self.address_bus = BusLine("地址线(32位)", "单向: CPU->内存")
        # 数据线：64位，双向
        self.data_bus = BusLine("数据线(64位)", "双向")
        # 控制线：发送读/写信号
        self.control_bus = BusLine("控制线", "双向")

    def read_memory(self, cpu, memory, address):
        """CPU从内存读取数据（模拟总线操作）"""
        print(f"\n读操作: CPU从内存地址 {hex(address)} 读取数据")
        print("-" * 50)

        # 第1步：地址线传输地址
        self.address_bus.send(hex(address))

        # 第2步：控制线发送"读"信号
        self.control_bus.send("READ")

        # 第3步：内存读取数据，通过数据线返回
        data = memory.read(address)
        self.data_bus.send(data)

        # 第4步：CPU接收数据
        cpu.receive(data)
        print(f"  CPU收到数据: {data}")

    def write_memory(self, cpu, memory, address, data):
        """CPU向内存写入数据（模拟总线操作）"""
        print(f"\n写操作: CPU向内存地址 {hex(address)} 写入 {data}")
        print("-" * 50)

        # 第1步：地址线传输地址
        self.address_bus.send(hex(address))

        # 第2步：数据线传输要写入的数据
        self.data_bus.send(data)

        # 第3步：控制线发送"写"信号
        self.control_bus.send("WRITE")

        # 第4步：内存接收数据
        memory.write(address, data)
        print(f"  数据已写入内存")


class SimpleMemory:
    """简易内存"""
    def __init__(self):
        self.data = {}

    def read(self, address):
        return self.data.get(address, 0)

    def write(self, address, value):
        self.data[address] = value

    def dump(self):
        print("  当前内存内容:")
        for addr, val in sorted(self.data.items()):
            print(f"    {hex(addr)}: {val}")


class SimpleCPU:
    """简易CPU"""
    def __init__(self):
        self.register = None  # 寄存器

    def receive(self, data):
        self.register = data


def main():
    """主程序：演示总线读写操作"""
    print("=== 总线通信模拟 ===\n")

    # 创建组件
    bus = SimpleBus()
    cpu = SimpleCPU()
    memory = SimpleMemory()

    # 先写入一些数据
    bus.write_memory(cpu, memory, 0x1000, 42)
    bus.write_memory(cpu, memory, 0x1004, 256)
    bus.write_memory(cpu, memory, 0x1008, 1024)

    memory.dump()

    # 再从内存读取数据
    bus.read_memory(cpu, memory, 0x1000)
    print(f"  CPU寄存器当前值: {cpu.register}")

    bus.read_memory(cpu, memory, 0x1008)
    print(f"  CPU寄存器当前值: {cpu.register}")


if __name__ == "__main__":
    main()
