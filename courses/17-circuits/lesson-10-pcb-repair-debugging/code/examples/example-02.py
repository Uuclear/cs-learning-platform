#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2：示波器波形参数提取与异常检测

这个脚本演示了如何分析示波器采集的波形数据，
包括频率估计、幅度计算和异常检测。
"""

import numpy as np
from typing import List, Tuple, Dict


def analyze_waveform(samples: List[float], sample_rate: float) -> Dict:
    """分析示波器采集的波形数据

    Args:
        samples: 采样点列表
        sample_rate: 采样率（Hz）

    Returns:
        包含波形参数和异常信息的字典
    """
    if len(samples) < 2:
        return {"error": "样本数量不足"}

    # 计算基本参数
    amplitude = (max(samples) - min(samples)) / 2
    dc_offset = np.mean(samples)
    frequency = estimate_frequency(samples, sample_rate)

    # 检测异常
    anomalies = detect_anomalies(samples)

    return {
        "amplitude": round(amplitude, 3),
        "dc_offset": round(dc_offset, 3),
        "frequency": round(frequency, 2),
        "anomalies": anomalies,
        "waveform_quality": "good" if len(anomalies) == 0 else "poor"
    }


def estimate_frequency(samples: List[float], sample_rate: float) -> float:
    """粗略估计信号频率（使用过零检测法）

    Args:
        samples: 采样点列表
        sample_rate: 采样率（Hz）

    Returns:
        估计的频率（Hz）
    """
    # 简化的过零检测
    zero_crossings = 0
    for i in range(1, len(samples)):
        if (samples[i-1] < 0 and samples[i] >= 0) or \
           (samples[i-1] >= 0 and samples[i] < 0):
            zero_crossings += 1

    if zero_crossings < 2:
        return 0.0

    # 频率 = 过零次数 / (2 * 时间)
    time_duration = len(samples) / sample_rate
    frequency = zero_crossings / (2 * time_duration)
    return frequency


def detect_anomalies(samples: List[float]) -> List[str]:
    """检测波形异常

    Args:
        samples: 采样点列表

    Returns:
        异常类型列表
    """
    anomalies = []

    # 检查是否有削波（信号达到最大/最小值）
    max_val, min_val = max(samples), min(samples)
    peak_to_peak = max_val - min_val
    if peak_to_peak > 0:  # 避免除零错误
        if max_val >= 0.95 * max(abs(max_val), abs(min_val)):
            anomalies.append("positive_clipping")
        if min_val <= -0.95 * max(abs(max_val), abs(min_val)):
            anomalies.append("negative_clipping")

    # 检查噪声水平
    std_dev = np.std(samples)
    mean_val = np.mean(samples)
    if abs(mean_val) > 0.001:  # 避免除零错误
        noise_ratio = std_dev / abs(mean_val)
        if noise_ratio > 0.3:  # 噪声超过平均值的30%
            anomalies.append("high_noise")
    elif std_dev > 0.1:  # 对于接近零的信号，直接检查标准差
        anomalies.append("high_noise")

    # 检查信号是否过于平缓（可能是直流或低频）
    if len(samples) > 10:
        derivative = np.diff(samples)
        if np.max(np.abs(derivative)) < 0.01 * max(abs(max_val), abs(min_val)):
            anomalies.append("low_frequency_or_dc")

    return anomalies


# 使用示例
if __name__ == "__main__":
    # 模拟一个正弦波（1kHz, 1Vpp, 0.5V DC offset）
    import math
    sample_rate = 10000  # 10kHz 采样率
    duration = 0.01  # 10ms
    t = [i / sample_rate for i in range(int(duration * sample_rate))]
    samples = [0.5 + 0.5 * math.sin(2 * math.pi * 1000 * ti) for ti in t]

    # 添加一些噪声模拟真实情况
    import random
    noisy_samples = [s + random.gauss(0, 0.02) for s in samples]

    # 分析波形
    result = analyze_waveform(noisy_samples, sample_rate)
    print("📊 波形分析结果:")
    print(f"  幅度: {result['amplitude']} V")
    print(f"  直流偏移: {result['dc_offset']} V")
    print(f"  频率: {result['frequency']} Hz")
    print(f"  波形质量: {result['waveform_quality']}")
    if result['anomalies']:
        print(f"  异常: {', '.join(result['anomalies'])}")