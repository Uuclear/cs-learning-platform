# 示例2：边缘AI - 在边缘设备上运行轻量级机器学习模型
import random
import math

class EdgeAIDevice:
    """模拟边缘AI设备"""

    def __init__(self, device_id, compute_capacity, memory_capacity):
        """
        初始化边缘AI设备

        :param device_id: 设备ID
        :param compute_capacity: 计算能力（相对值，1.0为基准）
        :param memory_capacity: 内存容量（MB）
        """
        self.device_id = device_id
        self.compute_capacity = compute_capacity
        self.memory_capacity = memory_capacity
        self.current_load = 0.0
        self.available_memory = memory_capacity

    def can_run_model(self, model_size_mb, required_compute):
        """
        检查设备是否能够运行指定模型

        :param model_size_mb: 模型大小（MB）
        :param required_compute: 所需计算能力
        :return: 是否可以运行
        """
        if model_size_mb > self.available_memory:
            return False
        if required_compute > self.compute_capacity:
            return False
        return True

    def run_inference(self, model_name, input_data_size):
        """
        运行推理任务

        :param model_name: 模型名称
        :param input_data_size: 输入数据大小
        :return: 推理结果和延迟
        """
        # 模拟不同模型的资源需求
        model_specs = {
            "tiny_cnn": {"size_mb": 2, "compute_factor": 0.3},
            "mobile_net": {"size_mb": 15, "compute_factor": 0.8},
            "efficient_net": {"size_mb": 30, "compute_factor": 1.5}
        }

        if model_name not in model_specs:
            return None, float('inf')

        spec = model_specs[model_name]

        # 检查资源是否足够
        if not self.can_run_model(spec["size_mb"], spec["compute_factor"]):
            return None, float('inf')

        # 消耗内存
        self.available_memory -= spec["size_mb"]

        # 计算推理延迟（受计算能力和输入数据大小影响）
        base_latency = 50  # 基础延迟（毫秒）
        compute_latency = base_latency * (spec["compute_factor"] / self.compute_capacity)
        data_latency = input_data_size * 0.1  # 数据处理延迟

        total_latency = compute_latency + data_latency

        # 模拟推理结果（随机分类结果）
        result = {
            "model": model_name,
            "prediction": random.choice(["normal", "anomaly"]),
            "confidence": random.uniform(0.7, 0.95),
            "latency_ms": total_latency
        }

        return result, total_latency

def simulate_edge_ai_scenario():
    """模拟边缘AI应用场景"""
    # 创建不同类型的边缘设备
    devices = [
        EdgeAIDevice("smart_camera_01", 0.5, 100),   # 智能摄像头
        EdgeAIDevice("industrial_sensor_01", 0.8, 200),  # 工业传感器
        EdgeAIDevice("autonomous_vehicle_01", 3.0, 1000)  # 自动驾驶车辆
    ]

    models_to_test = ["tiny_cnn", "mobile_net", "efficient_net"]
    input_sizes = [1, 5, 20]  # 不同输入数据大小（MB）

    print("边缘AI模型部署模拟")
    print("=" * 80)
    print(f"{'设备':<20} {'模型':<15} {'输入(MB)':<10} {'延迟(ms)':<12} {'状态':<10}")
    print("-" * 80)

    for device in devices:
        for model in models_to_test:
            for input_size in input_sizes:
                # 重置设备内存状态
                device.available_memory = device.memory_capacity

                result, latency = device.run_inference(model, input_size)

                if result is not None:
                    status = "成功"
                else:
                    status = "资源不足"
                    latency = "N/A"

                print(f"{device.device_id:<20} {model:<15} {input_size:<10} {latency:<12} {status:<10}")

if __name__ == "__main__":
    simulate_edge_ai_scenario()