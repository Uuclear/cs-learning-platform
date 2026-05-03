# 解决方案2：边缘AI模型量化和优化
import random
import math

class QuantizedEdgeAIDevice:
    """支持量化模型的边缘AI设备"""

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

    def run_inference(self, model_name, input_data_size, quantization_level="fp32"):
        """
        运行推理任务（支持量化）

        :param model_name: 模型名称
        :param input_data_size: 输入数据大小
        :param quantization_level: 量化级别 ("fp32", "int8", "int4")
        :return: 推理结果和延迟
        """
        # 基础模型规格
        base_model_specs = {
            "tiny_cnn": {"size_mb": 2, "compute_factor": 0.3},
            "mobile_net": {"size_mb": 15, "compute_factor": 0.8},
            "efficient_net": {"size_mb": 30, "compute_factor": 1.5}
        }

        if model_name not in base_model_specs:
            return None, float('inf')

        base_spec = base_model_specs[model_name]

        # 应用量化
        quantization_factors = {
            "fp32": {"size_factor": 1.0, "compute_factor": 1.0, "accuracy_factor": 1.0},
            "int8": {"size_factor": 0.25, "compute_factor": 0.6, "accuracy_factor": 0.95},
            "int4": {"size_factor": 0.125, "compute_factor": 0.4, "accuracy_factor": 0.85}
        }

        if quantization_level not in quantization_factors:
            quantization_level = "fp32"

        q_factor = quantization_factors[quantization_level]
        model_size_mb = base_spec["size_mb"] * q_factor["size_factor"]
        compute_factor = base_spec["compute_factor"] * q_factor["compute_factor"]
        accuracy_factor = q_factor["accuracy_factor"]

        # 检查资源是否足够
        if not self.can_run_model(model_size_mb, compute_factor):
            return None, float('inf')

        # 消耗内存
        self.available_memory -= model_size_mb

        # 计算推理延迟
        base_latency = 50
        compute_latency = base_latency * (compute_factor / self.compute_capacity)
        data_latency = input_data_size * 0.1

        total_latency = compute_latency + data_latency

        # 模拟推理结果（考虑量化对准确性的影响）
        result = {
            "model": model_name,
            "quantization": quantization_level,
            "prediction": random.choice(["normal", "anomaly"]),
            "confidence": random.uniform(0.7, 0.95) * accuracy_factor,
            "latency_ms": total_latency,
            "model_size_mb": model_size_mb
        }

        return result, total_latency

def optimize_edge_ai_models():
    """优化边缘AI模型部署"""
    devices = [
        QuantizedEdgeAIDevice("smart_camera_01", 0.5, 100),
        QuantizedEdgeAIDevice("industrial_sensor_01", 0.8, 200),
        QuantizedEdgeAIDevice("autonomous_vehicle_01", 3.0, 1000)
    ]

    models_to_test = ["tiny_cnn", "mobile_net", "efficient_net"]
    quantization_levels = ["fp32", "int8", "int4"]
    input_sizes = [1, 5, 20]

    print("边缘AI模型量化优化模拟")
    print("=" * 100)
    print(f"{'设备':<20} {'模型':<15} {'量化':<8} {'输入(MB)':<10} {'大小(MB)':<10} {'延迟(ms)':<12} {'准确率':<10} {'状态':<10}")
    print("-" * 100)

    for device in devices:
        for model in models_to_test:
            for quant_level in quantization_levels:
                for input_size in input_sizes:
                    # 重置设备内存状态
                    device.available_memory = device.memory_capacity

                    result, latency = device.run_inference(model, input_size, quant_level)

                    if result is not None:
                        status = "成功"
                        size_mb = f"{result['model_size_mb']:.1f}"
                        accuracy = f"{result['confidence']:.2f}"
                    else:
                        status = "资源不足"
                        size_mb = "N/A"
                        accuracy = "N/A"
                        latency = "N/A"

                    print(f"{device.device_id:<20} {model:<15} {quant_level:<8} {input_size:<10} "
                          f"{size_mb:<10} {latency:<12} {accuracy:<10} {status:<10}")

if __name__ == "__main__":
    optimize_edge_ai_models()