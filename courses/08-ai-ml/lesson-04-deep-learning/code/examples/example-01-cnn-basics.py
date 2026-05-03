# 示例1：卷积操作基础实现
import numpy as np

def convolution_2d(image, kernel):
    """
    手动实现2D卷积操作
    :param image: 输入图像 (H, W)
    :param kernel: 卷积核 (K, K)
    :return: 卷积结果
    """
    image_height, image_width = image.shape
    kernel_size = kernel.shape[0]
    output_height = image_height - kernel_size + 1
    output_width = image_width - kernel_size + 1

    output = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            # 提取图像的局部区域
            region = image[i:i+kernel_size, j:j+kernel_size]
            # 计算点积
            output[i, j] = np.sum(region * kernel)

    return output

# 创建测试图像和卷积核
test_image = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
])

# 边缘检测卷积核
edge_kernel = np.array([
    [-1, -1, -1],
    [-1, 8, -1],
    [-1, -1, -1]
])

result = convolution_2d(test_image, edge_kernel)
print("原始图像:")
print(test_image)
print("\n卷积核 (边缘检测):")
print(edge_kernel)
print("\n卷积结果:")
print(result)