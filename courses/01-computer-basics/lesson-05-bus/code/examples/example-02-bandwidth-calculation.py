# 总线带宽计算演示
# 帮助理解频率、位宽和带宽的关系

def calculate_bandwidth(frequency_mhz, bus_width_bits, cycles_per_transfer=1, ddr=False):
    """
    计算总线带宽
    公式: 带宽 = 频率 × 位宽 / 8 / 每传输周期数
    单位: MB/s (兆字节每秒)

    参数:
        frequency_mhz: 总线频率（MHz）
        bus_width_bits: 总线位宽（位）
        cycles_per_transfer: 每次传输需要的周期数（默认1）
        ddr: 是否启用DDR双数据速率（默认False）
    """
    # 基础传输率
    transfers_per_second = frequency_mhz * 1_000_000 / cycles_per_transfer

    # DDR模式下翻倍
    if ddr:
        transfers_per_second *= 2

    # 每次传输的字节数
    bytes_per_transfer = bus_width_bits / 8

    # 带宽 = 传输次数 × 每次字节数
    bandwidth_bytes = transfers_per_second * bytes_per_transfer
    bandwidth_mbps = bandwidth_bytes / (1024 * 1024)  # 转换为MB/s
    bandwidth_gbps = bandwidth_mbps / 1024             # 转换为GB/s

    return bandwidth_mbps, bandwidth_gbps


def compare_bus_bandwidth():
    """对比各种常见总线的理论带宽"""
    print("=== 总线带宽对比 ===\n")

    # 定义各种总线：(名称, 频率MHz, 位宽, 每传输周期数, 是否DDR)
    buses = [
        ("PCIe 3.0 x1",     8000,   1,   1, False),   # 8GT/s，1位有效
        ("PCIe 3.0 x16",    8000,   16,  1, False),   # 16条lane
        ("PCIe 4.0 x16",    16000,  16,  1, False),   # 16GT/s，翻倍
        ("PCIe 5.0 x16",    32000,  16,  1, False),   # 32GT/s，再翻倍
        ("DDR4-3200",       1600,   64,  1, True),    # DDR=双数据传输
        ("DDR5-6000",       3000,   64,  1, True),    # 更快
        ("USB 3.0",         5000,   1,   1, False),   # 5Gbps
        ("USB 3.2 Gen2x2",  10000,  2,   1, False),   # 双通道
        ("SATA 3.0",        6000,   1,   1, False),   # 6Gbps
    ]

    print(f"{'总线名称':<20} {'频率(MHz)':>12} {'位宽':>6} {'带宽(MB/s)':>14} {'带宽(GB/s)':>12}")
    print("-" * 70)

    for name, freq, width, cycles, is_ddr in buses:
        mbps, gbps = calculate_bandwidth(freq, width, cycles, is_ddr)
        print(f"{name:<20} {freq:>12,} {width:>6} {mbps:>14,.0f} {gbps:>12,.2f}")

    print("\n关键发现:")
    print("  1. 带宽 = 频率 × 位宽，两者都很重要")
    print("  2. PCIe x16是x1的16倍速，所以显卡都要用x16插槽")
    print("  3. DDR的'Double Data Rate'让每个周期传2次数据，带宽翻倍")
    print("  4. 新一代PCIe每次迭代带宽翻倍！")


def bandwidth_bottle_neck_demo():
    """演示带宽瓶颈问题"""
    print("\n\n=== 带宽瓶颈演示 ===\n")

    # 假设场景：从SSD加载一个5GB的游戏到内存
    game_size_gb = 5
    game_size_mb = game_size_gb * 1024

    interfaces = [
        ("SATA 3.0 SSD", 600),       # ~600 MB/s 实际
        ("NVMe PCIe 3.0", 3500),     # ~3500 MB/s
        ("NVMe PCIe 4.0", 7000),     # ~7000 MB/s
        ("NVMe PCIe 5.0", 14000),    # ~14000 MB/s
    ]

    print(f"加载 {game_size_gb}GB 游戏所需时间:\n")
    for name, speed in interfaces:
        time_sec = game_size_mb / speed
        if time_sec < 1:
            time_str = f"{time_sec * 1000:.0f}毫秒"
        else:
            time_str = f"{time_sec:.2f}秒"
        bar_length = int(time_sec * 2)
        bar = "*" * max(bar_length, 1)
        print(f"  {name:<20} {speed:>6} MB/s -> {time_str:>10} {bar}")

    print("\n带宽就像公路的车道数：车道越多，同时通过的车越多！")


def interactive_calculator():
    """交互式带宽计算器"""
    print("\n\n=== 交互式带宽计算器 ===\n")

    test_cases = [
        # (频率MHz, 位宽, DDR, 说明)
        (2666, 64, True, "DDR4-2666内存"),
        (4800, 64, True, "DDR5-4800内存"),
        (8000, 16, False, "PCIe 3.0 x16"),
        (16000, 16, False, "PCIe 4.0 x16"),
        (32000, 16, False, "PCIe 5.0 x16"),
        (500, 32, False, "PCI 32位/33MHz（老古董）"),
    ]

    for freq, width, is_ddr, desc in test_cases:
        mbps, gbps = calculate_bandwidth(freq, width, ddr=is_ddr)
        ddr_label = " (DDR)" if is_ddr else ""
        print(f"  {desc}{ddr_label}:")
        print(f"    频率={freq}MHz, 位宽={width}位 -> 带宽={mbps:,.0f} MB/s ({gbps:.2f} GB/s)")


if __name__ == "__main__":
    compare_bus_bandwidth()
    bandwidth_bottle_neck_demo()
    interactive_calculator()
