# 解决方案1：使用numpy实现完整的CNN进行MNIST分类
import numpy as np

class SimpleCNN:
    """
    简单的CNN实现，用于MNIST手写数字分类
    架构: 输入(28x28) -> 卷积层 -> ReLU -> 池化层 -> 全连接层 -> 输出(10类)
    """

    def __init__(self):
        # 卷积层参数 (假设使用5x5卷积核，6个输出通道)
        self.conv_weights = np.random.randn(6, 5, 5) * 0.1
        self.conv_bias = np.zeros(6)

        # 全连接层参数 (池化后尺寸为12x12，所以输入维度为6*12*12=864)
        self.fc_weights = np.random.randn(864, 10) * 0.01
        self.fc_bias = np.zeros(10)

        # 存储中间结果用于反向传播
        self.cache = {}

    def relu(self, x):
        """ReLU激活函数"""
        return np.maximum(0, x)

    def relu_derivative(self, x):
        """ReLU导数"""
        return (x > 0).astype(float)

    def max_pool_2d(self, x, pool_size=2):
        """2D最大池化"""
        batch_size, channels, height, width = x.shape
        out_height = height // pool_size
        out_width = width // pool_size

        output = np.zeros((batch_size, channels, out_height, out_width))

        for b in range(batch_size):
            for c in range(channels):
                for i in range(out_height):
                    for j in range(out_width):
                        region = x[b, c,
                                  i*pool_size:(i+1)*pool_size,
                                  j*pool_size:(j+1)*pool_size]
                        output[b, c, i, j] = np.max(region)

        return output

    def conv2d_forward(self, x, weights, bias):
        """2D卷积前向传播"""
        batch_size, height, width = x.shape
        num_filters, filter_h, filter_w = weights.shape

        out_height = height - filter_h + 1
        out_width = width - filter_w + 1

        output = np.zeros((batch_size, num_filters, out_height, out_width))

        for b in range(batch_size):
            for f in range(num_filters):
                for i in range(out_height):
                    for j in range(out_width):
                        region = x[b, i:i+filter_h, j:j+filter_w]
                        output[b, f, i, j] = np.sum(region * weights[f]) + bias[f]

        return output

    def forward(self, x):
        """前向传播"""
        # 假设输入x形状为(batch_size, 28, 28)
        batch_size = x.shape[0]

        # 卷积层
        conv_out = self.conv2d_forward(x, self.conv_weights, self.conv_bias)
        self.cache['conv_out'] = conv_out

        # ReLU激活
        relu_out = self.relu(conv_out)
        self.cache['relu_out'] = relu_out

        # 最大池化
        pool_out = self.max_pool_2d(relu_out)
        self.cache['pool_out'] = pool_out

        # 展平
        flat_out = pool_out.reshape(batch_size, -1)
        self.cache['flat_out'] = flat_out

        # 全连接层
        fc_out = np.dot(flat_out, self.fc_weights) + self.fc_bias
        self.cache['fc_out'] = fc_out

        # Softmax
        exp_out = np.exp(fc_out - np.max(fc_out, axis=1, keepdims=True))
        softmax_out = exp_out / np.sum(exp_out, axis=1, keepdims=True)

        return softmax_out

    def cross_entropy_loss(self, predictions, targets):
        """交叉熵损失"""
        batch_size = predictions.shape[0]
        correct_logprobs = -np.log(predictions[np.arange(batch_size), targets])
        return np.sum(correct_logprobs) / batch_size

# 创建模拟数据并测试
np.random.seed(42)
X_train = np.random.rand(10, 28, 28)  # 10个28x28图像
y_train = np.random.randint(0, 10, 10)  # 随机标签

# 创建CNN模型
cnn = SimpleCNN()
predictions = cnn.forward(X_train)

print("CNN预测结果:")
for i in range(min(5, len(predictions))):
    pred_class = np.argmax(predictions[i])
    confidence = np.max(predictions[i])
    true_class = y_train[i]
    print(f"样本 {i}: 预测={pred_class}(置信度={confidence:.3f}), 真实={true_class}")

# 计算损失
loss = cnn.cross_entropy_loss(predictions, y_train)
print(f"\n交叉熵损失: {loss:.4f}")
print("\n注意：这是一个简化的CNN实现，实际应用中建议使用PyTorch或TensorFlow等框架。")