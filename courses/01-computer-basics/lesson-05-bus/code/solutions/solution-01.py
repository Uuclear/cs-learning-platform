# 练习1解答：简单总线带宽计算器


def calculate_bandwidth(frequency_mhz, bus_width_bits, ddr=False):
    """
    计算总线带宽

    参数:
        frequency_mhz: 总线频率（MHz）
        bus_width_bits: 总线位宽（位）
        ddr: 是否启用DDR双数据速率

    返回:
        包含mbps和gbps的字典
    """
    # 基础传输率：每秒传输次数
    transfers_per_second = frequency_mhz * 1_000_000

    # DDR模式：每个时钟周期传输两次
    if ddr:
        transfers_per_second *= 2

    # 每次传输的字节数
    bytes_per_transfer = bus_width_bits / 8

    # 带宽（字节每秒）
    bandwidth_bytes = transfers_per_second * bytes_per_transfer

    # 转换为MB/s（1 MB = 10^6 字节，带宽常用十进制）
    bandwidth_mbps = bandwidth_bytes / 1_000_000

    # 转换为Gbps（1 Gbps = 10^9 bps）
    bandwidth_bps = bandwidth_bytes * 8  # 字节转位
    bandwidth_gbps = bandwidth_bps / 1_000_000_000

    return {
        "mbps": bandwidth_mbps,
        "gbps": bandwidth_gbps,
    }


def main():
    """测试各种总线带宽"""
    print("=== 总线带宽计算器 ===\n")

    test_cases = [
        # (频率MHz, 位宽, DDR, 说明)
        (1600, 64, True, "DDR4-3200内存总线"),
        (3000, 64, True, "DDR5-6000内存总线"),
        (8000, 16, False, "PCIe 3.0 x16"),
        (16000, 16, False, "PCIe 4.0 x16"),
        (32000, 16, False, "PCIe 5.0 x16"),
        (5000, 1, False, "USB 3.0"),
        (6000, 1, False, "SATA 3.0"),
        (33, 32, False, "PCI 32位/33MHz"),
    ]

    for freq, width, is_ddr, desc in test_cases:
        result = calculate_bandwidth(freq, width, is_ddr)
        ddr_tag = " (DDR)" if is_ddr else ""
        print(f"{desc}{ddr_tag}:")
        print(f"  频率={freq}MHz, 位宽={width}位")
        print(f"  带宽={result['mbps']:,.2f} MB/s, {result['gbps']:.2f} Gbps")
        print()


if __name__ == "__main__":
    main()

# 预期输出:
# === 总线带宽计算器 ===
#
# DDR4-3200内存总线 (DDR):
#   频率=1600MHz, 位宽=64位
#   带宽=25,600.00 MB/s, 204.80 Gbps
#
# DDR5-6000内存总线 (DDR):
#   频率=3000MHz, 位宽=64位
#   带宽=48,000.00 MB/s, 384.00 Gbps
#
# PCIe 3.0 x16:
#   频率=8000MHz, 位宽=16位
#   带宽=16,000.00 MB/s, 128.00 Gbps
# ...
