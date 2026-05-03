#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 01: 模型版本控制完整实现
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, List


class ModelVersion:
    def __init__(self, model_id: str, version: str, metrics: Dict[str, float],
                 parameters: Dict[str, Any], timestamp: str = None):
        self.model_id = model_id
        self.version = version
        self.metrics = metrics
        self.parameters = parameters
        self.timestamp = timestamp or datetime.now().isoformat()
        self.model_hash = self._calculate_hash()

    def _calculate_hash(self) -> str:
        model_data = {
            'model_id': self.model_id,
            'version': self.version,
            'metrics': self.metrics,
            'parameters': self.parameters
        }
        return hashlib.md5(json.dumps(model_data, sort_keys=True).encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_id': self.model_id,
            'version': self.version,
            'metrics': self.metrics,
            'parameters': self.parameters,
            'timestamp': self.timestamp,
            'model_hash': self.model_hash
        }


class ModelRegistry:
    def __init__(self, registry_path: str = "model_registry.json"):
        self.registry_path = registry_path
        self.models = self._load_registry()

    def _load_registry(self) -> Dict[str, List[Dict]]:
        if os.path.exists(self.registry_path):
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_registry(self):
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.models, f, indent=2, ensure_ascii=False)

    def log_model(self, model_version: ModelVersion):
        model_id = model_version.model_id
        if model_id not in self.models:
            self.models[model_id] = []

        existing_hashes = [m['model_hash'] for m in self.models[model_id]]
        if model_version.model_hash not in existing_hashes:
            self.models[model_id].append(model_version.to_dict())
            self._save_registry()

    def get_best_model(self, model_id: str, metric: str = 'accuracy') -> Dict:
        if model_id not in self.models:
            raise ValueError(f"模型 {model_id} 不存在")

        versions = self.models[model_id]
        best_version = max(versions, key=lambda x: x['metrics'].get(metric, 0))
        return best_version

    def compare_models(self, model_id: str) -> None:
        if model_id not in self.models:
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


def main():
    registry = ModelRegistry()

    # 创建多个模型版本进行测试
    models_data = [
        ("recommendation_model", "v1.0", {"precision": 0.75, "recall": 0.70}, {"algorithm": "collaborative_filtering"}),
        ("recommendation_model", "v1.1", {"precision": 0.78, "recall": 0.72}, {"algorithm": "matrix_factorization"}),
        ("recommendation_model", "v2.0", {"precision": 0.82, "recall": 0.75}, {"algorithm": "deep_learning"}),
    ]

    for model_id, version, metrics, params in models_data:
        model_version = ModelVersion(model_id, version, metrics, params)
        registry.log_model(model_version)

    # 获取最佳模型
    best = registry.get_best_model("recommendation_model", "precision")
    print(f"最佳模型: {best['version']} (Precision: {best['metrics']['precision']})")

    # 比较所有版本
    registry.compare_models("recommendation_model")


if __name__ == "__main__":
    main()