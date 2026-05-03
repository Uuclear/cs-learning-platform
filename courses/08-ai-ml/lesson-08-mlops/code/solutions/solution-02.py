#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 02: 数据漂移检测完整实现
"""

import json
import math
from typing import List, Dict, Any


def calculate_mean(data: List[float]) -> float:
    return sum(data) / len(data) if data else 0.0


def calculate_std(data: List[float]) -> float:
    if len(data) < 2:
        return 0.0
    mean = calculate_mean(data)
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)


def calculate_ks_statistic(sample1: List[float], sample2: List[float]) -> float:
    if not sample1 or not sample2:
        return 0.0

    combined = sorted(set(sample1 + sample2))
    max_diff = 0.0
    n1, n2 = len(sample1), len(sample2)

    for value in combined:
        cdf1 = sum(1 for x in sample1 if x <= value) / n1
        cdf2 = sum(1 for x in sample2 if x <= value) / n2
        diff = abs(cdf1 - cdf2)
        max_diff = max(max_diff, diff)

    return max_diff


def detect_data_drift(training_data: Dict[str, List[float]],
                     production_data: Dict[str, List[float]],
                     threshold: float = 0.3) -> Dict[str, Any]:
    results = {
        'drift_detected': False,
        'features_with_drift': [],
        'feature_statistics': {},
        'overall_assessment': ''
    }

    all_features = set(training_data.keys()) | set(production_data.keys())

    for feature in all_features:
        train_values = training_data.get(feature, [])
        prod_values = production_data.get(feature, [])

        if not train_values or not prod_values:
            continue

        train_mean = calculate_mean(train_values)
        train_std = calculate_std(train_values)
        prod_mean = calculate_mean(prod_values)
        prod_std = calculate_std(prod_values)
        ks_stat = calculate_ks_statistic(train_values, prod_values)
        has_drift = ks_stat > threshold

        results['feature_statistics'][feature] = {
            'training_mean': train_mean,
            'training_std': train_std,
            'production_mean': prod_mean,
            'production_std': prod_std,
            'ks_statistic': ks_stat,
            'has_drift': has_drift
        }

        if has_drift:
            results['features_with_drift'].append(feature)
            results['drift_detected'] = True

    if results['drift_detected']:
        results['overall_assessment'] = f"检测到数据漂移！影响特征: {', '.join(results['features_with_drift'])}"
    else:
        results['overall_assessment'] = "未检测到显著的数据漂移"

    return results


def main():
    # 测试数据
    training_data = {
        'temperature': [20.0, 22.5, 18.0, 25.0, 21.0],
        'humidity': [60.0, 65.0, 55.0, 70.0, 62.0]
    }

    production_data = {
        'temperature': [28.0, 30.5, 26.0, 32.0, 29.0],  # 明显偏移
        'humidity': [61.0, 66.0, 56.0, 71.0, 63.0]      # 轻微变化
    }

    results = detect_data_drift(training_data, production_data, threshold=0.2)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()