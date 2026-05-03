# 挑战2：Monte Carlo方法估算π ⭐⭐

## 问题描述

使用**Monte Carlo方法**估算圆周率π的值。通过在单位正方形内随机生成点，并统计落在单位圆内的比例来估算π。

这是一个经典的Monte Carlo算法应用，展示了如何用随机采样解决确定性数学问题。

## 输入/输出规格

### 函数定义
```python
def estimate_pi(num_samples):
    """
    使用Monte Carlo方法估算π
    
    Args:
        num_samples (int): 随机采样点的数量
        
    Returns:
        dict: 包含估算结果和统计信息的字典
    """
    pass
```

### 输出格式
返回字典包含以下键：
- `pi_estimate`: π的估算值
- `num_samples`: 采样点总数
- `points_in_circle`: 落在圆内的点数
- `confidence_interval`: 95%置信区间
- `error`: 与真实π值的绝对误差

### 示例
```python
result = estimate_pi(1000000)
print(f"π估算值: {result['pi_estimate']:.6f}")
print(f"置信区间: [{result['confidence_interval'][0]:.6f}, {result['confidence_interval'][1]:.6f}]")
print(f"绝对误差: {result['error']:.6f}")
```

## 约束条件

- 必须使用标准库的random模块
- 必须计算95%置信区间
- 采样点数必须可配置（至少支持1到10^7）
- 必须处理边界情况（如num_samples <= 0）
- 代码必须有详细的中文注释

## 提示

1. **几何关系**：单位圆面积 = π/4，单位正方形面积 = 1
2. **置信区间**：使用二项分布的正态近似计算
3. **效率优化**：避免使用sqrt函数，直接比较x² + y² ≤ 1
4. **统计分析**：计算标准误差和置信区间

<details>
<summary>参考解决方案</summary>

```python
import random
import math
import time

def estimate_pi(num_samples):
    """
    使用Monte Carlo方法估算圆周率π
    
    算法原理：
    - 在单位正方形[0,1]×[0,1]内随机生成点
    - 统计落在单位圆x²+y²≤1内的点的比例
    - 由于圆的面积是π/4，所以π ≈ 4 × (圆内点数 / 总点数)
    
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
    standard_error = math.sqrt(p_hat * (1 - p_hat) / num_samples)
    
    # 95%置信区间（z-score = 1.96）
    z_score = 1.96
    margin_of_error = z_score * standard_error
    confidence_interval = (
        4.0 * (p_hat - margin_of_error),
        4.0 * (p_hat + margin_of_error)
    )
    
    # 计算绝对误差
    true_pi = math.pi
    absolute_error = abs(pi_estimate - true_pi)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    return {
        'pi_estimate': pi_estimate,
        'num_samples': num_samples,
        'points_in_circle': points_in_circle,
        'confidence_interval': confidence_interval,
        'error': absolute_error,
        'execution_time': execution_time,
        'standard_error': 4.0 * standard_error
    }

def analyze_convergence():
    """分析收敛性"""
    print("=== Monte Carlo π估算收敛性分析 ===\n")
    
    sample_sizes = [100, 1000, 10000, 100000, 1000000]
    
    for n in sample_sizes:
        result = estimate_pi(n)
        ci_width = result['confidence_interval'][1] - result['confidence_interval'][0]
        
        print(f"样本数: {n:>8}")
        print(f"  π估算值: {result['pi_estimate']:>10.6f}")
        print(f"  真实值:   {math.pi:>10.6f}")
        print(f"  绝对误差: {result['error']:>10.6f}")
        print(f"  置信区间宽度: {ci_width:>10.6f}")
        print(f"  执行时间: {result['execution_time']:>10.4f}s")
        print()

def compare_with_theoretical_error():
    """与理论误差比较"""
    print("=== 误差分析 ===\n")
    
    n = 1000000
    theoretical_error = 1 / math.sqrt(n)  # 理论收敛率 O(1/√n)
    
    result = estimate_pi(n)
    empirical_error = result['error']
    
    print(f"样本数: {n}")
    print(f"理论误差界: {theoretical_error:.6f}")
    print(f"实际误差:   {empirical_error:.6f}")
    print(f"误差比率:   {empirical_error/theoretical_error:.2f}")

def main():
    """主函数"""
    analyze_convergence()
    compare_with_theoretical_error()

if __name__ == "__main__":
    main()
```

</details>