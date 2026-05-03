# 示例1：边缘计算与云计算的延迟和带宽对比模拟
import time
import random
import math

def simulate_cloud_processing(data_size_mb, distance_km):
    """
    模拟云计算处理：包括传输延迟和处理延迟

    :param data_size_mb: 数据大小（MB）
    :param distance_km: 到数据中心的距离（公里）
    :return: 总延迟（毫秒）
    """
    # 光速传输延迟（光在光纤中的速度约为200,000 km/s）
    transmission_delay_ms = (distance_km * 2) / 200  # 往返延迟

    # 网络传输时间（假设带宽为100 Mbps）
    bandwidth_mbps = 100
    transfer_time_ms = (data_size_mb * 8) / bandwidth_mbps * 1000  # 转换为毫秒

    # 云端处理时间（假设处理能力强大，固定为50ms）
    processing_time_ms = 50

    total_delay = transmission_delay_ms + transfer_time_ms + processing_time_ms
    return total_delay

def simulate_edge_processing(data_size_mb, local_processing_power):
    """
    模拟边缘计算处理：本地处理，无传输延迟

    :param data_size_mb: 数据大小（MB）
    :param local_processing_power: 本地处理能力（1.0表示标准能力）
    :return: 总延迟（毫秒）
    """
    # 无网络传输延迟

    # 本地处理时间（受处理能力影响）
    base_processing_time = 100  # 基础处理时间（毫秒）
    processing_time_ms = base_processing_time / local_processing_power

    # 小量数据可能需要额外的启动开销
    if data_size_mb < 1:
        processing_time_ms += 10

    return processing_time_ms

def compare_edge_vs_cloud():
    """比较边缘计算和云计算在不同场景下的性能"""
    scenarios = [
        {"name": "智能摄像头", "data_size": 5, "distance": 1000, "edge_power": 0.5},
        {"name": "工业传感器", "data_size": 0.1, "distance": 500, "edge_power": 0.8},
        {"name": "自动驾驶", "data_size": 50, "distance": 2000, "edge_power": 2.0},
    ]

    print("边缘计算 vs 云计算性能对比")
    print("=" * 60)
    print(f"{'场景':<15} {'边缘延迟(ms)':<15} {'云延迟(ms)':<15} {'优势':<10}")
    print("-" * 60)

    for scenario in scenarios:
        edge_delay = simulate_edge_processing(scenario["data_size"], scenario["edge_power"])
        cloud_delay = simulate_cloud_processing(scenario["data_size"], scenario["distance"])

        advantage = "边缘" if edge_delay < cloud_delay else "云端"

        print(f"{scenario['name']:<15} {edge_delay:<15.1f} {cloud_delay:<15.1f} {advantage:<10}")

if __name__ == "__main__":
    compare_edge_vs_cloud()