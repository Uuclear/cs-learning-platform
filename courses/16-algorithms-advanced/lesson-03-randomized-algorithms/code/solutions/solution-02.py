#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：Monte Carlo π估算完整实现

这个文件提供了Monte Carlo方法估算π的完整实现，
包括置信区间计算、收敛性分析和误差分析。
"""

import random
import math
import time
import statistics

class MonteCarloPiEstimator:
    """
    Monte Carlo π估算器类

    Attributes:
        results_history (list): 历史估算结果
    """

    def __init__(self):
        """初始化估算器"""
        self.results_history = []

    def estimate_pi(self, num_samples):
        """
        使用Monte Carlo方法估算π

        Args:
            num_samples (int): 随机采样点的数量

        Returns:
            dict: 包含估算结果和统计信息的字典
        """
        if num_samples <= 0:
            raise ValueError("采样点数必须大于0")

        start_time = time.time()
        points_in_circle = 0

        # 生成随机点并统计圆内点数
        for _ in range(num_samples):
            x = random.random()
            y = random.random()

            # 检查点是否在单位圆内（避免sqrt计算）
            if x * x + y * y <= 1.0:
                points_in_circle += 1

        # 计算π的估算值
        pi_estimate = 4.0 * points_in_circle / num_samples

        # 计算统计信息
        p_hat = points_in_circle / num_samples  # 圆内点的比例
        standard_error_p = math.sqrt(p_hat * (1 - p_hat) / num_samples)

        # 95%置信区间（z-score = 1.96）
        z_score = 1.96
        margin_of_error_p = z_score * standard_error_p
        confidence_interval_p = (
            p_hat - margin_of_error_p,
            p_hat + margin_of_error_p
        )

        # 转换为π的置信区间
        confidence_interval_pi = (
            4.0 * confidence_interval_p[0],
            4.0 * confidence_interval_p[1]
        )

        # 计算绝对误差
        true_pi = math.pi
        absolute_error = abs(pi_estimate - true_pi)
        relative_error = absolute_error / true_pi

        end_time = time.time()
        execution_time = end_time - start_time

        result = {
            'pi_estimate': pi_estimate,
            'num_samples': num_samples,
            'points_in_circle': points_in_circle,
            'confidence_interval': confidence_interval_pi,
            'absolute_error': absolute_error,
            'relative_error': relative_error,
            'execution_time': execution_time,
            'standard_error': 4.0 * standard_error_p,
            'true_pi': true_pi
        }

        # 保存到历史记录
        self.results_history.append(result)

        return result

    def multiple_estimates(self, num_samples, num_trials):
        """
        进行多次估算以分析稳定性

        Args:
            num_samples (int): 每次估算的采样点数
            num_trials (int): 估算次数

        Returns:
            dict: 多次估算的统计摘要
        """
        estimates = []
        errors = []
        execution_times = []

        for i in range(num_trials):
            result = self.estimate_pi(num_samples)
            estimates.append(result['pi_estimate'])
            errors.append(result['absolute_error'])
            execution_times.append(result['execution_time'])

        # 计算统计摘要
        mean_estimate = statistics.mean(estimates)
        std_estimate = statistics.stdev(estimates) if len(estimates) > 1 else 0

        mean_error = statistics.mean(errors)
        std_error = statistics.stdev(errors) if len(errors) > 1 else 0

        summary = {
            'num_samples': num_samples,
            'num_trials': num_trials,
            'mean_estimate': mean_estimate,
            'std_estimate': std_estimate,
            'mean_error': mean_error,
            'std_error': std_error,
            'mean_execution_time': statistics.mean(execution_times),
            'all_estimates': estimates,
            'all_errors': errors
        }

        return summary

def analyze_convergence():
    """分析收敛性"""
    print("=== Monte Carlo π估算收敛性分析 ===\n")

    estimator = MonteCarloPiEstimator()
    sample_sizes = [100, 1000, 10000, 100000, 1000000, 10000000]

    for n in sample_sizes:
        result = estimator.estimate_pi(n)
        ci_width = result['confidence_interval'][1] - result['confidence_interval'][0]
        theoretical_error = 1 / math.sqrt(n)  # 理论收敛率

        print(f"样本数: {n:>10}")
        print(f"  π估算值:     {result['pi_estimate']:>12.6f}")
        print(f"  真实值:       {result['true_pi']:>12.6f}")
        print(f"  绝对误差:     {result['absolute_error']:>12.6f}")
        print(f"  相对误差:     {result['relative_error']:>12.6f}")
        print(f"  置信区间宽度: {ci_width:>12.6f}")
        print(f"  理论误差界:   {theoretical_error:>12.6f}")
        print(f"  执行时间:     {result['execution_time']:>12.4f}s")
        print()

def analyze_stability():
    """分析估算稳定性"""
    print("=== 估算稳定性分析 ===\n")

    estimator = MonteCarloPiEstimator()
    sample_size = 100000
    num_trials = 100

    print(f"进行 {num_trials} 次估算，每次 {sample_size} 个样本点\n")

    summary = estimator.multiple_estimates(sample_size, num_trials)

    print(f"平均估算值: {summary['mean_estimate']:.6f}")
    print(f"估算标准差: {summary['std_estimate']:.6f}")
    print(f"平均绝对误差: {summary['mean_error']:.6f}")
    print(f"误差标准差: {summary['std_error']:.6f}")
    print(f"平均执行时间: {summary['mean_execution_time']:.4f}s")

    # 计算95%置信区间的实际覆盖率
    true_pi = math.pi
    covered_count = 0
    for estimate in summary['all_estimates']:
        error = abs(estimate - true_pi)
        # 理论95%置信区间的半宽
        theoretical_margin = 1.96 / math.sqrt(sample_size)
        if error <= theoretical_margin:
            covered_count += 1

    coverage_rate = covered_count / num_trials
    print(f"95%置信区间实际覆盖率: {coverage_rate:.3f}")

def main():
    """主函数"""
    analyze_convergence()
    print()
    analyze_stability()

if __name__ == "__main__":
    main()

# 预期输出示例:
# === Monte Carlo π估算收敛性分析 ===
#
# 样本数:        100
#   π估算值:         3.160000
#   真实值:          3.141593
#   绝对误差:        0.018407
#   相对误差:        0.005859
#   置信区间宽度:    0.552800
#   理论误差界:      0.100000
#   执行时间:           0.0001s