#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 02: 数据漂移检测
检测训练数据和生产数据之间的分布差异
仅使用标准库实现（使用基本统计方法）
"""

import json
import math
from typing import List, Dict, Any
import random


def calculate_mean(data: List[float]) -> float:
    """计算均值"""
    return sum(data) / len(data) if data else 0.0


def calculate_std(data: List[float]) -> float:
    """计算标准差"""
    if len(data) < 2:
        return 0.0
    mean = calculate_mean(data)
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)


def calculate_ks_statistic(sample1: List[float], sample2: List[float]) -> float:
    """
    计算 Kolmogorov-Smirnov 统计量的简化版本
    用于检测两个样本分布的差异
    """
    if not sample1 or not sample2:
        return 0.0

    # 合并并排序所有值
    combined = sorted(set(sample1 + sample2))

    max_diff = 0.0
    n1, n2 = len(sample1), len(sample2)

    # 计算累积分布函数的差异
    for value in combined:
        cdf1 = sum(1 for x in sample1 if x <= value) / n1
        cdf2 = sum(1 for x in sample2 if x <= value) / n2
        diff = abs(cdf1 - cdf2)
        max_diff = max(max_diff, diff)

    return max_diff


def detect_data_drift(training_data: Dict[str, List[float]],
                     production_data: Dict[str, List[float]],
                     threshold: float = 0.3) -> Dict[str, Any]:
    """
    检测数据漂移

    Args:
        training_data: 训练数据字典 {特征名: 值列表}
        production_data: 生产数据字典 {特征名: 值列表}
        threshold: 漂移阈值，KS统计量超过此值认为存在漂移

    Returns:
        包含漂移检测结果的字典
    """
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

        # 计算基本统计信息
        train_mean = calculate_mean(train_values)
        train_std = calculate_std(train_values)
        prod_mean = calculate_mean(prod_values)
        prod_std = calculate_std(prod_values)

        # 计算 KS 统计量
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
        results['overall_assessment'] = f"⚠️  检测到数据漂移！影响特征: {', '.join(results['features_with_drift'])}"
    else:
        results['overall_assessment'] = "✅ 未检测到显著的数据漂移"

    return results


def generate_sample_data():
    """生成示例数据用于演示"""
    # 模拟训练数据（正常分布）
    training_data = {
        'age': [random.gauss(35, 10) for _ in range(1000)],
        'income': [random.gauss(50000, 15000) for _ in range(1000)],
        'click_rate': [random.betavariate(2, 5) for _ in range(1000)]
    }

    # 模拟生产数据（部分特征有漂移）
    production_data = {
        'age': [random.gauss(40, 12) for _ in range(500)],  # 年龄分布偏移
        'income': [random.gauss(50000, 15000) for _ in range(500)],  # 收入正常
        'click_rate': [random.betavariate(1.5, 6) for _ in range(500)]  # 点击率偏移
    }

    return training_data, production_data


def main():
    """主函数：演示数据漂移检测"""
    print("🔍 开始数据漂移检测演示...")

    # 生成示例数据
    training_data, production_data = generate_sample_data()

    # 执行漂移检测
    results = detect_data_drift(training_data, production_data, threshold=0.2)

    # 输出结果
    print(f"\n{results['overall_assessment']}")
    print("\n📊 特征详细分析:")
    print("-" * 80)

    for feature, stats in results['feature_statistics'].items():
        status = "🚨" if stats['has_drift'] else "✅"
        print(f"{status} {feature}:")
        print(f"   训练集 - 均值: {stats['training_mean']:.2f}, 标准差: {stats['training_std']:.2f}")
        print(f"   生产集 - 均值: {stats['production_mean']:.2f}, 标准差: {stats['production_std']:.2f}")
        print(f"   KS 统计量: {stats['ks_statistic']:.3f} ({'漂移' if stats['has_drift'] else '正常'})")
        print()

    # 保存结果到文件
    with open('data_drift_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("💾 结果已保存到 data_drift_results.json")


if __name__ == "__main__":
    main()