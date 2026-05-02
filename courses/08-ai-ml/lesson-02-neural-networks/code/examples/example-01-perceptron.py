import numpy as np

class Perceptron:
    """感知机：最简单的神经网络"""

    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """训练感知机"""
        n_samples, n_features = X.shape

        # 初始化权重和偏置
        self.weights = np.zeros(n_features)
        self.bias = 0

        # 训练过程
        for _ in range(self.n_iterations):
            for idx, x_i in enumerate(X):
                # 线性输出
                linear_output = np.dot(x_i, self.weights) + self.bias
                # 预测输出 (使用阶跃激活函数)
                y_predicted = self._unit_step_function(linear_output)

                # 更新规则
                update = self.learning_rate * (y[idx] - y_predicted)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        """预测"""
        linear_output = np.dot(X, self.weights) + self.bias
        return self._unit_step_function(linear_output)

    def _unit_step_function(self, x):
        """阶跃激活函数"""
        return np.where(x >= 0, 1, 0)

# 测试感知机
if __name__ == "__main__":
    # 创建简单的AND逻辑门数据
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])  # AND逻辑

    perceptron = Perceptron(learning_rate=0.1, n_iterations=1000)
    perceptron.fit(X, y)

    predictions = perceptron.predict(X)
    print("输入 -> 预测")
    for i in range(len(X)):
        print(f"{X[i]} -> {predictions[i]}")