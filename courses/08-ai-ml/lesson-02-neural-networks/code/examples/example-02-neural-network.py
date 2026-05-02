import numpy as np

class NeuralNetwork:
    """简单的多层神经网络"""

    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        # 随机初始化权重 (使用小的随机数)
        self.W1 = np.random.randn(self.input_size, self.hidden_size) * 0.01
        self.b1 = np.zeros((1, self.hidden_size))
        self.W2 = np.random.randn(self.hidden_size, self.output_size) * 0.01
        self.b2 = np.zeros((1, self.output_size))

    def sigmoid(self, x):
        """Sigmoid激活函数"""
        # 防止溢出
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        """Sigmoid的导数"""
        return x * (1 - x)

    def forward(self, X):
        """前向传播"""
        # 第一层
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)

        # 输出层
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)

        return self.a2

    def backward(self, X, y, output):
        """反向传播"""
        m = X.shape[0]

        # 输出层误差
        dZ2 = output - y
        dW2 = (1/m) * np.dot(self.a1.T, dZ2)
        db2 = (1/m) * np.sum(dZ2, axis=0, keepdims=True)

        # 隐藏层误差
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.sigmoid_derivative(self.a1)
        dW1 = (1/m) * np.dot(X.T, dZ1)
        db1 = (1/m) * np.sum(dZ1, axis=0, keepdims=True)

        # 更新权重
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1

    def train(self, X, y, epochs=1000):
        """训练网络"""
        for i in range(epochs):
            output = self.forward(X)
            self.backward(X, y, output)

            if i % 100 == 0:
                loss = np.mean(np.square(y - output))
                print(f"Epoch {i}, Loss: {loss:.4f}")

    def predict(self, X):
        """预测"""
        return self.forward(X)

# 测试XOR问题 (非线性可分)
if __name__ == "__main__":
    # XOR数据
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])  # XOR逻辑

    # 创建网络 (2输入, 4隐藏, 1输出)
    nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1, learning_rate=1.0)

    print("训练前的预测:")
    initial_pred = nn.predict(X)
    for i in range(len(X)):
        print(f"{X[i]} -> {initial_pred[i][0]:.2f}")

    print("\n开始训练...")
    nn.train(X, y, epochs=1000)

    print("\n训练后的预测:")
    final_pred = nn.predict(X)
    for i in range(len(X)):
        print(f"{X[i]} -> {final_pred[i][0]:.2f} (目标: {y[i][0]})")