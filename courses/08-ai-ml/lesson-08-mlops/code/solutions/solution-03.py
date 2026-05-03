#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 03: 模型服务完整实现
"""

import json
from typing import Dict, Any


class SimpleModel:
    def __init__(self):
        self.version = "1.0.0"

    def predict(self, features: Dict[str, float]) -> Dict[str, Any]:
        score = sum(features.values()) / len(features) if features else 0.0

        if score > 0.5:
            prediction = "positive"
            confidence = min(score, 0.99)
        else:
            prediction = "negative"
            confidence = max(1 - score, 0.01)

        return {
            "prediction": prediction,
            "confidence": confidence,
            "score": score,
            "model_version": self.version
        }


class ModelMetrics:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0

    def record_request(self, success: bool):
        self.total_requests += 1
        if success:
            self.successful_requests += 1

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0.0
        }


def main():
    # 测试模型和指标
    model = SimpleModel()
    metrics = ModelMetrics()

    # 测试预测
    test_features = {"feature1": 0.6, "feature2": 0.7}
    result = model.predict(test_features)
    metrics.record_request(True)

    print("预测结果:", result)
    print("指标:", metrics.get_metrics())


if __name__ == "__main__":
    main()