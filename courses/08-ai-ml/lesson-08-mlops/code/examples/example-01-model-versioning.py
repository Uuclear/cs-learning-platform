#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 01: 模型版本控制
模拟使用类似 MLflow 的模式进行模型版本管理和比较
仅使用标准库实现，避免使用 pickle
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, List


class ModelVersion:
    """模型版本类，包含模型元数据和指标"""

    def __init__(self, model_id: str, version: str, metrics: Dict[str, float],
                 parameters: Dict[str, Any], timestamp: str = None):
        self.model_id = model_id
        self.version = version
        self.metrics = metrics
        self.parameters = parameters
        self.timestamp = timestamp or datetime.now().isoformat()
        self.model_hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        """计算模型的唯一哈希值"""
        model_data = {
            'model_id': self.model_id,
            'version': self.version,
            'metrics': self.metrics,
            'parameters': self.parameters
        }
        return hashlib.md5(json.dumps(model_data, sort_keys=True).encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'model_id': self.model_id,
            'version': self.version,
            'metrics': self.metrics,
            'parameters': self.parameters,
            'timestamp': self.timestamp,
            'model_hash': self.model_hash
        }


class ModelRegistry:
    """简单的模型注册表，用于存储和管理模型版本"""

    def __init__(self, registry_path: str = "model_registry.json"):
        self.registry_path = registry_path
        self.models = self._load_registry()

    def _load_registry(self) -> Dict[str, List[Dict]]:
        """从文件加载注册表"""
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_registry(self):
        """保存注册表到文件"""
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.models, f, indent=2, ensure_ascii=False)

    def log_model(self, model_version: ModelVersion):
        """记录新的模型版本"""
        model_id = model_version.model_id
        if model_id not in self.models:
            self.models[model_id] = []

        # 检查是否已存在相同哈希的版本
        existing_hashes = [m['model_hash'] for m in self.models[model_id]]
        if model_version.model_hash not in existing_hashes:
            self.models[model_id].append(model_version.to_dict())
            self._save_registry()
            print(f"✅ 模型 {model_id} 版本 {model_version.version} 已记录")
        else:
            print(f"⚠️  模型 {model_id} 版本 {model_version.version} 已存在，跳过记录")

    def get_best_model(self, model_id: str, metric: str = 'accuracy') -> Dict:
        """获取指定模型ID的最佳版本（基于指定指标）"""
        if model_id not in self.models:
            raise ValueError(f"模型 {model_id} 不存在")

        versions = self.models[model_id]
        best_version = max(versions, key=lambda x: x['metrics'].get(metric, 0))
        return best_version

    def compare_models(self, model_id: str) -> None:
        """比较同一模型的不同版本"""
        if model_id not in self.models:
            print(f"❌ 模型 {model_id} 不存在")
            return

        versions = self.models[model_id]
        print(f"\n📊 模型 {model_id} 版本比较:")
        print("-" * 60)
        print(f"{'版本':<10} {'准确率':<10} {'F1分数':<10} {'训练时间':<20}")
        print("-" * 60)

        for version in versions:
            metrics = version['metrics']
            print(f"{version['version']:<10} "
                  f"{metrics.get('accuracy', 0):<10.4f} "
                  f"{metrics.get('f1_score', 0):<10.4f} "
                  f"{version['timestamp'][:19]}")
        print("-" * 60)


def simulate_training_run():
    """模拟训练运行并记录模型版本"""
    registry = ModelRegistry()

    # 模拟第一个模型版本
    model_v1 = ModelVersion(
        model_id="sentiment_classifier",
        version="v1.0",
        metrics={"accuracy": 0.85, "f1_score": 0.83},
        parameters={"learning_rate": 0.01, "epochs": 10, "batch_size": 32}
    )
    registry.log_model(model_v1)

    # 模拟改进后的模型版本
    model_v2 = ModelVersion(
        model_id="sentiment_classifier",
        version="v2.0",
        metrics={"accuracy": 0.89, "f1_score": 0.87},
        parameters={"learning_rate": 0.005, "epochs": 15, "batch_size": 64}
    )
    registry.log_model(model_v2)

    # 获取最佳模型
    best_model = registry.get_best_model("sentiment_classifier", "accuracy")
    print(f"\n🏆 最佳模型版本: {best_model['version']} (准确率: {best_model['metrics']['accuracy']:.4f})")

    # 比较所有版本
    registry.compare_models("sentiment_classifier")


if __name__ == "__main__":
    print("🚀 开始模型版本控制演示...")
    simulate_training_run()
    print("\n📝 注册表已保存到 model_registry.json")