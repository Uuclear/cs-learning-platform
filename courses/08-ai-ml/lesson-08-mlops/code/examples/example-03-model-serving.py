#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 03: 模型服务模拟
模拟简单的模型服务 API，包含健康检查和指标收集
仅使用标准库实现（使用 http.server）
"""

import json
import time
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List


class SimpleModel:
    """简单的预测模型（用于演示）"""

    def __init__(self):
        self.version = "1.0.0"
        self.last_prediction_time = None

    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        """
        执行预测

        Args:
            features: 输入特征字典

        Returns:
            包含预测结果和元数据的字典
        """
        # 简单的线性组合预测（用于演示）
        score = sum(features.values()) / len(features) if features else 0.0

        # 分类逻辑
        if score > 0.5:
            prediction = "positive"
            confidence = min(score, 0.99)
        else:
            prediction = "negative"
            confidence = max(1 - score, 0.01)

        self.last_prediction_time = time.time()

        return {
            "prediction": prediction,
            "confidence": confidence,
            "score": score,
            "model_version": self.version,
            "timestamp": datetime.now().isoformat()
        }


class ModelMetrics:
    """模型服务指标收集器"""

    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_latency = 0.0
        self.predictions = []
        self.start_time = time.time()

    def record_request(self, success: bool, latency: float, prediction: str = None):
        """记录请求指标"""
        self.total_requests += 1
        if success:
            self.successful_requests += 1
            if prediction:
                self.predictions.append(prediction)
        else:
            self.failed_requests += 1
        self.total_latency += latency

    def get_metrics(self) -> Dict[str, Any]:
        """获取当前指标"""
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / self.total_requests if self.total_requests > 0 else 0.0

        # 计算预测分布
        pred_counts = {}
        for pred in self.predictions:
            pred_counts[pred] = pred_counts.get(pred, 0) + 1

        return {
            "uptime_seconds": uptime,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "average_latency_ms": avg_latency * 1000,
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0.0,
            "prediction_distribution": pred_counts
        }


class ModelServingHandler(BaseHTTPRequestHandler):
    """模型服务 HTTP 处理器"""

    # 类变量，所有实例共享
    model = SimpleModel()
    metrics = ModelMetrics()

    def _send_response(self, status_code: int, data: Dict[str, Any], content_type: str = "application/json"):
        """发送 HTTP 响应"""
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")  # 允许跨域（仅用于演示）
        self.end_headers()

        if content_type == "application/json":
            response_data = json.dumps(data, ensure_ascii=False, indent=2)
            self.wfile.write(response_data.encode('utf-8'))
        else:
            self.wfile.write(data.encode('utf-8'))

    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/health":
            self._handle_health_check()
        elif path == "/metrics":
            self._handle_metrics()
        elif path == "/":
            self._handle_root()
        else:
            self._send_response(404, {"error": "路径未找到"})

    def do_POST(self):
        """处理 POST 请求"""
        if self.path == "/predict":
            self._handle_predict()
        else:
            self._send_response(404, {"error": "路径未找到"})

    def _handle_health_check(self):
        """健康检查端点"""
        health_status = {
            "status": "healthy",
            "model_version": self.model.version,
            "uptime_seconds": time.time() - self.metrics.start_time,
            "last_prediction": self.model.last_prediction_time,
            "timestamp": datetime.now().isoformat()
        }
        self._send_response(200, health_status)

    def _handle_metrics(self):
        """指标端点"""
        metrics_data = self.metrics.get_metrics()
        self._send_response(200, metrics_data)

    def _handle_root(self):
        """根路径 - 提供使用说明"""
        instructions = """# 模型服务 API

## 端点

### GET /health
健康检查

### GET /metrics
服务指标

### POST /predict
执行预测

请求体格式:
{
    "features": {
        "feature1": 0.5,
        "feature2": 0.8,
        ...
    }
}

## 示例

curl -X POST http://localhost:8000/predict \\
     -H "Content-Type: application/json" \\
     -d '{"features": {"age": 0.7, "income": 0.6, "click_rate": 0.9}}'
"""
        self._send_response(200, instructions, "text/markdown")

    def _handle_predict(self):
        """预测端点"""
        start_time = time.time()

        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                raise ValueError("请求体为空")

            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))

            if 'features' not in request_data:
                raise ValueError("缺少 'features' 字段")

            features = request_data['features']
            if not isinstance(features, dict):
                raise ValueError("'features' 必须是字典")

            # 执行预测
            result = self.model.predict(features)

            # 记录成功请求
            latency = time.time() - start_time
            self.metrics.record_request(True, latency, result['prediction'])

            self._send_response(200, result)

        except Exception as e:
            # 记录失败请求
            latency = time.time() - start_time
            self.metrics.record_request(False, latency)

            error_response = {
                "error": str(e),
                "model_version": self.model.version,
                "timestamp": datetime.now().isoformat()
            }
            self._send_response(400, error_response)


def start_server(port: int = 8000):
    """启动模型服务"""
    server = HTTPServer(('localhost', port), ModelServingHandler)
    print(f"🚀 模型服务已启动在 http://localhost:{port}")
    print(f"📚 访问 http://localhost:{port} 查看使用说明")
    print(f"💚 健康检查: http://localhost:{port}/health")
    print(f"📊 指标监控: http://localhost:{port}/metrics")
    print(f"🔮 预测接口: POST http://localhost:{port}/predict")
    print("\n按 Ctrl+C 停止服务...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        server.shutdown()
        print("✅ 服务已停止")


def test_model_serving():
    """测试模型服务功能（不启动实际服务器）"""
    print("🧪 测试模型服务功能...")

    # 创建模型实例
    model = SimpleModel()
    metrics = ModelMetrics()

    # 测试预测
    test_features = {"feature1": 0.6, "feature2": 0.7, "feature3": 0.8}
    result = model.predict(test_features)

    print(f"✅ 预测结果: {result['prediction']} (置信度: {result['confidence']:.3f})")

    # 测试指标记录
    metrics.record_request(True, 0.05, result['prediction'])
    metrics.record_request(False, 0.02)

    final_metrics = metrics.get_metrics()
    print(f"📈 测试指标: {final_metrics['total_requests']} 请求, "
          f"{final_metrics['success_rate']:.1%} 成功率")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 运行测试模式
        test_model_serving()
    else:
        # 启动实际服务器
        start_server()