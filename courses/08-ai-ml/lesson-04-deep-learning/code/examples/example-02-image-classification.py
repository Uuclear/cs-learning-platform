# 示例2：使用简单神经网络进行MNIST手写数字分类
import numpy as np

class SimpleNeuralNetwork:
    """简单的神经网络用于MNIST分类"""

    def __init__(self, input_size=784, hidden_size=128, output_size=10):
        # 初始化权重和偏置
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))

    def relu(self, x):
        """ReLU激活函数"""
        return np.maximum(0, x)

    def softmax(self, x):
        """Softmax函数用于多分类"""
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, X):
        """前向传播"""
        # 第一层
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.relu(self.z1)

        # 输出层
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.softmax(self.z2)

        return self.a2

# 模拟MNIST数据（实际使用时会加载真实数据）
np.random.seed(42)
X_sample = np.random.rand(5, 784)  # 5个28x28的图像展平
y_sample = np.array([0, 1, 2, 3, 4])  # 对应标签

# 创建并运行网络
nn = SimpleNeuralNetwork()
predictions = nn.forward(X_sample)

print("预测概率分布:")
for i in range(5):
    pred_class = np.argmax(predictions[i])
    confidence = np.max(predictions[i])
    print(f"样本 {i}: 预测为 {pred_class}, 置信度 {confidence:.3f}")