# 解决方案1：边缘计算与云计算的延迟和带宽对比模拟（优化版）
import time
import random
import math

def simulate_cloud_processing(data_size_mb, distance_km, network_conditions=None):
    """
    模拟云计算处理：包括传输延迟和处理延迟

    :param data_size_mb: 数据大小（MB）
    :param distance_km: 到数据中心的距离（公里）
    :param network_conditions: 网络条件字典 {'bandwidth_mbps': int, 'latency_factor': float}
    :return: 总延迟（毫秒）
    """
    if network_conditions is None:
        network_conditions = {'bandwidth_mbps': 100, 'latency_factor': 1.0}

    # 光速传输延迟（光在光纤中的速度约为200,000 km/s）
    transmission_delay_ms = (distance_km * 2) / 200 * network_conditions['latency_factor']

    # 网络传输时间
    bandwidth_mbps = network_conditions['bandwidth_mbps']
    transfer_time_ms = (data_size_mb * 8) / bandwidth_mbps * 1000

    # 云端处理时间（根据数据大小动态调整）
    processing_time_ms = 50 + data_size_mb * 0.5

    total_delay = transmission_delay_ms + transfer_time_ms + processing_time_ms
    return total_delay

def simulate_edge_processing(data_size_mb, local_processing_power, edge_conditions=None):
    """
    模拟边缘计算处理：本地处理，无传输延迟

    :param data_size_mb: 数据大小（MB）
    :param local_processing_power: 本地处理能力（1.0表示标准能力）
    :param edge_conditions: 边缘条件字典 {'startup_overhead': float}
    :return: 总延迟（毫秒）
    """
    if edge_conditions is None:
        edge_conditions = {'startup_overhead': 10.0}

    # 本地处理时间
    base_processing_time = 100
    processing_time_ms = base_processing_time / local_processing_power

    # 启动开销
    if data_size_mb < 1:
        processing_time_ms += edge_conditions['startup_overhead']

    return processing_time_ms

def compare_edge_vs_cloud_detailed():
    """详细的边缘计算与云计算对比"""
    scenarios = [
        {"name": "智能摄像头", "data_size": 5, "distance": 1000, "edge_power": 0.5},
        {"name": "工业传感器", "data_size": 0.1, "distance": 500, "edge_power": 0.8},
        {"name": "自动驾驶", "data_size": 50, "distance": 2000, "edge_power": 2.0},
        {"name": "AR/VR设备", "data_size": 20, "distance": 1500, "edge_power": 1.5},
    ]

    network_variants = [
        {'name': '理想网络', 'bandwidth_mbps': 1000, 'latency_factor': 0.8},
        {'name': '普通网络', 'bandwidth_mbps': 100, 'latency_factor': 1.0},
        {'name': '拥堵网络', 'bandwidth_mbps': 10, 'latency_factor': 2.0},
    ]

    print("详细边缘计算 vs 云计算性能对比")
    print("=" * 80)

    for scenario in scenarios:
        print(f"\n场景: {scenario['name']}")
        print("-" * 50)

        for net_variant in network_variants:
            edge_delay = simulate_edge_processing(
                scenario["data_size"],
                scenario["edge_power"]
            )
            cloud_delay = simulate_cloud_processing(
                scenario["data_size"],
                scenario["distance"],
                net_variant
            )

            advantage = "边缘" if edge_delay < cloud_delay else "云端"
            ratio = cloud_delay / edge_delay if edge_delay > 0 else float('inf')

            print(f"{net_variant['name']}: 边缘={edge_delay:.1f}ms, 云={cloud_delay:.1f}ms, "
                  f"优势={advantage}, 云/边={ratio:.1f}x")

if __name__ == "__main__":
    compare_edge_vs_cloud_detailed()