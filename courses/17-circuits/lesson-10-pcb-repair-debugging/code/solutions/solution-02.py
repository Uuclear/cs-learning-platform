#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2：示波器波形参数提取与异常检测 - 完整版

这个完整的解决方案包含了更精确的频率估计、
多种波形类型识别和详细的异常分类。
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy import signal
from scipy.fft import fft, fftfreq


class WaveformAnalyzer:
    """高级波形分析器"""

    def __init__(self):
        self.supported_waveforms = ["sine", "square", "triangle", "sawtooth", "noise"]

    def analyze_waveform(self, samples: List[float], sample_rate: float,
                        expected_frequency: Optional[float] = None) -> Dict:
        """全面分析示波器采集的波形数据

        Args:
            samples: 采样点列表
            sample_rate: 采样率（Hz）
            expected_frequency: 期望频率（用于偏差计算），可选

        Returns:
            包含详细波形参数和异常信息的字典
        """
        if len(samples) < 10:
            return {"error": "样本数量不足，至少需要10个采样点"}

        # 基本统计参数
        basic_stats = self._calculate_basic_statistics(samples)

        # 频域分析
        frequency_analysis = self._frequency_domain_analysis(samples, sample_rate)

        # 波形类型识别
        waveform_type = self._identify_waveform_type(samples)

        # 异常检测
        anomalies = self._detect_comprehensive_anomalies(samples, basic_stats, frequency_analysis)

        # 频率偏差计算（如果提供了期望频率）
        frequency_deviation = None
        if expected_frequency is not None and frequency_analysis["dominant_frequency"] > 0:
            frequency_deviation = abs(frequency_analysis["dominant_frequency"] - expected_frequency) / expected_frequency * 100

        result = {
            "basic_statistics": basic_stats,
            "frequency_analysis": frequency_analysis,
            "waveform_type": waveform_type,
            "anomalies": anomalies,
            "frequency_deviation_percent": round(frequency_deviation, 2) if frequency_deviation is not None else None,
            "overall_quality": self._assess_overall_quality(anomalies, basic_stats)
        }

        return result

    def _calculate_basic_statistics(self, samples: List[float]) -> Dict:
        """计算基本统计参数"""
        samples_array = np.array(samples)
        return {
            "mean": round(np.mean(samples_array), 6),
            "std": round(np.std(samples_array), 6),
            "min": round(np.min(samples_array), 6),
            "max": round(np.max(samples_array), 6),
            "peak_to_peak": round(np.ptp(samples_array), 6),
            "rms": round(np.sqrt(np.mean(samples_array**2)), 6),
            "crest_factor": round(np.max(np.abs(samples_array)) / np.sqrt(np.mean(samples_array**2)), 3) if np.sqrt(np.mean(samples_array**2)) > 1e-10 else float('inf')
        }

    def _frequency_domain_analysis(self, samples: List[float], sample_rate: float) -> Dict:
        """频域分析 - 使用FFT"""
        samples_array = np.array(samples)
        n = len(samples_array)

        # 计算FFT
        yf = fft(samples_array - np.mean(samples_array))  # 去除直流分量
        xf = fftfreq(n, 1/sample_rate)[:n//2]

        # 找到主导频率
        magnitude = 2.0/n * np.abs(yf[:n//2])
        if len(magnitude) > 1:
            dominant_freq_idx = np.argmax(magnitude[1:]) + 1  # 跳过DC分量
            dominant_frequency = xf[dominant_freq_idx]
            dominant_magnitude = magnitude[dominant_freq_idx]
        else:
            dominant_frequency = 0.0
            dominant_magnitude = 0.0

        # 计算THD（总谐波失真）- 简化版本
        thd = self._calculate_thd(magnitude, dominant_freq_idx) if dominant_freq_idx > 0 else 0.0

        return {
            "dominant_frequency": round(dominant_frequency, 2),
            "dominant_magnitude": round(dominant_magnitude, 6),
            "thd_percent": round(thd * 100, 2),
            "frequency_resolution": round(sample_rate / n, 2)
        }

    def _calculate_thd(self, magnitude: np.ndarray, fundamental_idx: int) -> float:
        """计算总谐波失真（简化版）"""
        if fundamental_idx <= 0 or len(magnitude) <= fundamental_idx * 5:
            return 0.0

        # 取前5个谐波
        harmonic_indices = [fundamental_idx * i for i in range(2, 6) if fundamental_idx * i < len(magnitude)]
        if not harmonic_indices:
            return 0.0

        fundamental_power = magnitude[fundamental_idx] ** 2
        harmonic_powers = sum(magnitude[idx] ** 2 for idx in harmonic_indices)

        return np.sqrt(harmonic_powers / fundamental_power) if fundamental_power > 1e-12 else 0.0

    def _identify_waveform_type(self, samples: List[float]) -> str:
        """识别波形类型"""
        samples_array = np.array(samples)
        samples_normalized = (samples_array - np.mean(samples_array)) / (np.std(samples_array) + 1e-10)

        # 正弦波特征：高斯分布
        _, p_value_sine = signal.normaltest(samples_normalized)

        # 方波特征：双峰分布
        unique_values, counts = np.unique(np.round(samples_normalized, 1), return_counts=True)
        is_square_like = len(unique_values) <= 3 and np.max(counts) / len(samples) > 0.3

        # 三角波/锯齿波特征：线性变化
        diff_signs = np.sign(np.diff(samples_normalized))
        sign_changes = np.sum(diff_signs[:-1] != diff_signs[1:])
        is_triangle_like = sign_changes <= 2 and len(samples) > 20

        if is_square_like:
            return "square"
        elif is_triangle_like:
            # 区分三角波和锯齿波
            rising_time = np.sum(diff_signs > 0)
            falling_time = np.sum(diff_signs < 0)
            if abs(rising_time - falling_time) / (rising_time + falling_time) < 0.3:
                return "triangle"
            else:
                return "sawtooth"
        elif p_value_sine > 0.05:  # 通过正态性检验
            return "sine"
        elif np.std(samples_normalized) > 0.5:  # 高噪声
            return "noise"
        else:
            return "unknown"

    def _detect_comprehensive_anomalies(self, samples: List[float],
                                      basic_stats: Dict,
                                      freq_analysis: Dict) -> List[Dict]:
        """综合异常检测"""
        anomalies = []
        samples_array = np.array(samples)

        # 1. 削波检测
        clipping_anomalies = self._detect_clipping(samples_array, basic_stats)
        anomalies.extend(clipping_anomalies)

        # 2. 噪声水平检测
        noise_anomaly = self._detect_noise_level(basic_stats)
        if noise_anomaly:
            anomalies.append(noise_anomaly)

        # 3. 频率相关异常
        freq_anomalies = self._detect_frequency_anomalies(freq_analysis)
        anomalies.extend(freq_anomalies)

        # 4. 波形失真检测
        distortion_anomaly = self._detect_distortion(basic_stats, freq_analysis)
        if distortion_anomaly:
            anomalies.append(distortion_anomaly)

        return anomalies

    def _detect_clipping(self, samples: np.ndarray, stats: Dict) -> List[Dict]:
        """检测削波"""
        anomalies = []
        peak_val = max(abs(stats["min"]), abs(stats["max"]))

        if peak_val == 0:
            return anomalies

        # 检查顶部削波
        top_threshold = 0.98 * peak_val
        bottom_threshold = -0.98 * peak_val

        top_clipped_points = np.sum(samples >= top_threshold)
        bottom_clipped_points = np.sum(samples <= bottom_threshold)

        total_points = len(samples)
        clipped_ratio = (top_clipped_points + bottom_clipped_points) / total_points

        if clipped_ratio > 0.05:  # 超过5%的点被削波
            anomaly_type = "positive_clipping" if top_clipped_points > bottom_clipped_points else "negative_clipping"
            if top_clipped_points > 0 and bottom_clipped_points > 0:
                anomaly_type = "both_clipping"

            anomalies.append({
                "type": anomaly_type,
                "severity": "high" if clipped_ratio > 0.1 else "medium",
                "description": f"信号削波: {clipped_ratio*100:.1f}% 的采样点达到极限值"
            })

        return anomalies

    def _detect_noise_level(self, stats: Dict) -> Optional[Dict]:
        """检测噪声水平"""
        if abs(stats["mean"]) < 1e-6:  # 接近零的信号
            if stats["std"] > 0.1:
                return {
                    "type": "high_noise",
                    "severity": "high",
                    "description": f"高噪声水平: σ = {stats['std']:.3f}"
                }
        else:
            noise_ratio = stats["std"] / abs(stats["mean"])
            if noise_ratio > 0.5:
                return {
                    "type": "high_noise",
                    "severity": "high" if noise_ratio > 1.0 else "medium",
                    "description": f"高噪声水平: 噪声/信号比 = {noise_ratio:.2f}"
                }
        return None

    def _detect_frequency_anomalies(self, freq_analysis: Dict) -> List[Dict]:
        """检测频率相关异常"""
        anomalies = []

        if freq_analysis["dominant_frequency"] == 0:
            anomalies.append({
                "type": "no_signal",
                "severity": "high",
                "description": "未检测到有效信号频率"
            })
        elif freq_analysis["thd_percent"] > 10:
            severity = "high" if freq_analysis["thd_percent"] > 20 else "medium"
            anomalies.append({
                "type": "high_harmonic_distortion",
                "severity": severity,
                "description": f"高谐波失真: THD = {freq_analysis['thd_percent']:.1f}%"
            })

        return anomalies

    def _detect_distortion(self, stats: Dict, freq_analysis: Dict) -> Optional[Dict]:
        """检测波形失真"""
        if stats["crest_factor"] > 3.0 and freq_analysis["dominant_frequency"] > 0:
            return {
                "type": "waveform_distortion",
                "severity": "medium",
                "description": f"波形失真: 峰值因数 = {stats['crest_factor']:.2f}"
            }
        return None

    def _assess_overall_quality(self, anomalies: List[Dict], stats: Dict) -> str:
        """评估整体波形质量"""
        if not anomalies:
            return "excellent"

        high_severity_count = sum(1 for a in anomalies if a.get("severity") == "high")
        medium_severity_count = sum(1 for a in anomalies if a.get("severity") == "medium")

        if high_severity_count > 0:
            return "poor"
        elif medium_severity_count > 2:
            return "fair"
        elif medium_severity_count > 0:
            return "good"
        else:
            return "excellent"


# 使用示例
def main():
    """主函数 - 演示完整功能"""
    import math
    import random

    analyzer = WaveformAnalyzer()

    # 生成测试信号：带噪声的正弦波
    sample_rate = 10000  # 10kHz
    duration = 0.02      # 20ms (2个周期的100Hz信号)
    t = [i / sample_rate for i in range(int(duration * sample_rate))]

    # 100Hz 正弦波 + 噪声 + 轻微削波
    base_signal = [math.sin(2 * math.pi * 100 * ti) for ti in t]
    noisy_signal = [s + random.gauss(0, 0.05) for s in base_signal]
    # 添加轻微削波
    clipped_signal = [max(-0.95, min(0.95, s)) for s in noisy_signal]

    # 分析波形
    result = analyzer.analyze_waveform(clipped_signal, sample_rate, expected_frequency=100.0)

    print("📊 高级波形分析结果:")
    print("=" * 50)

    if "error" in result:
        print(f"❌ 错误: {result['error']}")
        return

    # 基本统计
    stats = result["basic_statistics"]
    print(f"基本统计:")
    print(f"  平均值: {stats['mean']:.4f}")
    print(f"  标准差: {stats['std']:.4f}")
    print(f"  峰峰值: {stats['peak_to_peak']:.4f}")
    print(f"  RMS值: {stats['rms']:.4f}")
    print(f"  峰值因数: {stats['crest_factor']:.2f}")

    # 频域分析
    freq = result["frequency_analysis"]
    print(f"\n频域分析:")
    print(f"  主导频率: {freq['dominant_frequency']} Hz")
    print(f"  THD: {freq['thd_percent']}%")
    if result["frequency_deviation_percent"] is not None:
        print(f"  频率偏差: {result['frequency_deviation_percent']}%")

    # 波形类型
    print(f"\n波形类型: {result['waveform_type']}")

    # 异常检测
    anomalies = result["anomalies"]
    print(f"\n异常检测 ({len(anomalies)} 个异常):")
    if anomalies:
        for i, anomaly in enumerate(anomalies, 1):
            print(f"  {i}. {anomaly['type']} [{anomaly['severity']}] - {anomaly['description']}")
    else:
        print("  ✅ 未检测到异常")

    # 整体质量
    print(f"\n整体质量: {result['overall_quality'].upper()}")


if __name__ == "__main__":
    main()