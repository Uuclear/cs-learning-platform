# 实现简单注意力机制

**难度**: ⭐⭐⭐

## 描述

在这个挑战中，你需要从零开始实现一个完整的自注意力机制。注意力机制是Transformer架构的核心组件，理解其实现原理对于深入掌握大语言模型至关重要。

你需要实现的注意力机制应该能够处理任意长度的输入序列，并正确计算Query、Key、Value之间的注意力权重。

## 要求

### 基本要求
1. 实现一个`SimpleAttention`类，包含以下方法：
   - `__init__(self, d_model, d_k=None, d_v=None)`: 初始化注意力层
   - `softmax(self, x, axis=-1)`: 实现数值稳定的softmax函数
   - `forward(self, x)`: 执行前向传播计算注意力

2. 输入张量形状为 `[batch_size, seq_len, d_model]`
3. 输出张量形状应为 `[batch_size, seq_len, d_v]`
4. 返回注意力权重矩阵，形状为 `[batch_size, seq_len, seq_len]`

### 进阶要求（可选）
1. 实现多头注意力机制的简化版本
2. 添加掩码注意力支持（用于处理变长序列）
3. 优化计算效率，避免不必要的内存分配

## 提示

### 关键公式
- **线性变换**: Q = X·W_q, K = X·W_k, V = X·W_v
- **注意力分数**: Attention(Q,K,V) = softmax(Q·K^T / √d_k) · V
- **缩放因子**: 除以√d_k防止梯度消失

### 实现步骤
1. 首先实现数值稳定的softmax函数
2. 初始化随机权重矩阵 W_q, W_k, W_v
3. 在forward方法中执行线性变换得到Q, K, V
4. 计算注意力分数并应用softmax
5. 使用注意力权重对Value进行加权求和

### 测试用例
```python
# 创建测试数据
np.random.seed(42)
x = np.random.randn(2, 4, 8)  # batch_size=2, seq_len=4, d_model=8

# 初始化注意力层
attention = SimpleAttention(d_model=8, d_k=8, d_v=8)

# 执行前向传播
output, weights = attention.forward(x)

# 验证输出形状
assert output.shape == (2, 4, 8)
assert weights.shape == (2, 4, 4)
```

## 评估标准

- ✅ 正确实现注意力机制的核心计算
- ✅ 处理任意批次大小和序列长度
- ✅ 数值稳定性（不会出现NaN或无穷大）
- ✅ 代码结构清晰，注释完整
- 🌟 实现多头注意力（进阶）
- 🌟 添加单元测试验证正确性