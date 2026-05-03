# 挑战2：构建图像分类器

## 难度：⭐⭐⭐⭐

## 任务描述

在这个高级挑战中，你需要构建一个完整的图像分类系统，能够对CIFAR-10数据集中的图像进行分类。由于我们限制只使用numpy，你将需要实现一个简化的CNN架构。

## 要求

1. **数据准备**：创建模拟的CIFAR-10数据（32x32x3彩色图像，10个类别）
2. **网络架构**：实现以下组件
   - 卷积层（支持多个卷积核）
   - ReLU激活函数
   - 最大池化层
   - 全连接层
   - Softmax输出层
3. **训练过程**：实现简单的前向传播和损失计算
4. **评估**：计算分类准确率

## 网络架构建议

```
输入 (32, 32, 3)
↓
卷积层1 (6个5x5卷积核) → ReLU
↓
最大池化 (2x2)
↓
卷积层2 (16个5x5卷积核) → ReLU  
↓
最大池化 (2x2)
↓
展平 → 全连接层 (120神经元) → ReLU
↓
全连接层 (84神经元) → ReLU
↓
输出层 (10神经元) → Softmax
```

## 实现步骤

### 步骤1：数据模拟
```python
# 创建模拟CIFAR-10数据
def create_cifar10_simulation(num_samples=100):
    # 返回: X_train (num_samples, 32, 32, 3), y_train (num_samples,)
    pass
```

### 步骤2：CNN组件实现
- `Conv2DLayer`: 卷积层类
- `MaxPool2D`: 最大池化类  
- `FullyConnectedLayer`: 全连接层类
- `ReLU`, `Softmax`: 激活函数

### 步骤3：完整网络集成
```python
class SimpleCIFAR10CNN:
    def __init__(self):
        # 初始化所有层
        pass
    
    def forward(self, x):
        # 前向传播
        pass
    
    def compute_loss(self, predictions, targets):
        # 交叉熵损失
        pass
```

### 步骤4：训练和评估
```python
# 创建数据
X_train, y_train = create_cifar10_simulation(100)

# 创建模型
model = SimpleCIFAR10CNN()

# 前向传播
predictions = model.forward(X_train)

# 计算损失和准确率
loss = model.compute_loss(predictions, y_train)
accuracy = compute_accuracy(predictions, y_train)

print(f"损失: {loss:.4f}, 准确率: {accuracy:.2%}")
```

## 额外挑战（可选）

- 实现简单的梯度下降更新（不需要完整的反向传播）
- 添加Dropout层防止过拟合
- 实现数据增强功能

## 提示

- 参考 `solution-01.py` 中的简化CNN实现
- 使用面向对象的方式组织代码
- 先实现单个组件，再逐步集成
- 注意内存效率，避免不必要的数组复制

## 评估标准

- ✅ 网络架构完整性（30%）
- ✅ 功能正确性（40%）
- ✅ 代码结构和可读性（20%）
- ✅ 创新性和扩展性（10%）

完成后，将你的解决方案保存为 `challenge-02-solution.py` 并测试其在模拟数据上的性能。