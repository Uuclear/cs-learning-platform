# 挑战1：实现简单的卷积操作

## 难度：⭐⭐⭐

## 任务描述

在本挑战中，你需要从零开始实现一个完整的2D卷积操作，支持以下功能：

- 基本的卷积计算（无填充、步长为1）
- 边界填充（padding）支持
- 自定义步长（stride）支持

## 要求

1. 创建函数 `conv2d_with_padding_stride(image, kernel, padding=0, stride=1)`
2. 支持任意大小的输入图像和卷积核
3. 正确处理边界填充（在图像周围添加零值）
4. 正确处理自定义步长
5. 返回正确的输出尺寸

## 输出尺寸计算公式

当使用填充 `p` 和步长 `s` 时，输出尺寸为：
```
output_size = (input_size + 2*p - kernel_size) // s + 1
```

## 测试用例

你的实现应该能够通过以下测试：

```python
# 测试1：基本卷积（无填充，步长1）
image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
kernel = np.array([[1, 0], [0, -1]])
result = conv2d_with_padding_stride(image, kernel)
# 期望输出形状: (2, 2)

# 测试2：带填充的卷积
result_padded = conv2d_with_padding_stride(image, kernel, padding=1)
# 期望输出形状: (3, 3)

# 测试3：自定义步长
result_strided = conv2d_with_padding_stride(image, kernel, stride=2)
# 期望输出形状: (1, 1)
```

## 提示

- 先实现基本的卷积操作（参考example-01-cnn-basics.py）
- 然后添加填充功能：使用 `np.pad()` 函数
- 最后添加步长支持：调整循环的步进
- 注意边界条件和数组索引

## 评估标准

- ✅ 功能正确性（60%）
- ✅ 代码可读性和注释（20%）
- ✅ 处理边界情况（20%）

完成后，将你的解决方案保存为 `challenge-01-solution.py` 并与提供的参考解决方案进行比较。