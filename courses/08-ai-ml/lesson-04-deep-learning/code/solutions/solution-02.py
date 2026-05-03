# 解决方案2：图像增强管道（旋转、翻转、缩放）
import numpy as np
from math import cos, sin, radians

def rotate_image(image, angle_degrees):
    """
    旋转图像
    :param image: 输入图像 (H, W) 或 (H, W, C)
    :param angle_degrees: 旋转角度（度）
    :return: 旋转后的图像
    """
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
        image_3d = image.reshape(height, width, 1)
    else:
        height, width, channels = image.shape
        image_3d = image

    # 转换为弧度
    angle_rad = radians(angle_degrees)

    # 计算旋转后的边界框
    cos_val = abs(cos(angle_rad))
    sin_val = abs(sin(angle_rad))
    new_width = int((height * sin_val) + (width * cos_val))
    new_height = int((height * cos_val) + (width * sin_val))

    # 创建输出图像
    rotated = np.zeros((new_height, new_width, channels))

    # 计算中心点
    center_x, center_y = width // 2, height // 2
    new_center_x, new_center_y = new_width // 2, new_height // 2

    # 执行旋转
    for x in range(new_width):
        for y in range(new_height):
            # 转换到原坐标系
            orig_x = (x - new_center_x) * cos_val + (y - new_center_y) * sin_val + center_x
            orig_y = -(x - new_center_x) * sin_val + (y - new_center_y) * cos_val + center_y

            # 检查边界
            if 0 <= orig_x < width - 1 and 0 <= orig_y < height - 1:
                # 双线性插值
                x1, y1 = int(orig_x), int(orig_y)
                x2, y2 = x1 + 1, y1 + 1

                dx = orig_x - x1
                dy = orig_y - y1

                for c in range(channels):
                    val = (image_3d[y1, x1, c] * (1 - dx) * (1 - dy) +
                           image_3d[y1, x2, c] * dx * (1 - dy) +
                           image_3d[y2, x1, c] * (1 - dx) * dy +
                           image_3d[y2, x2, c] * dx * dy)
                    rotated[y, x, c] = val

    if channels == 1:
        return rotated.reshape(new_height, new_width)
    else:
        return rotated.astype(np.uint8)

def flip_image(image, flip_type='horizontal'):
    """
    翻转图像
    :param image: 输入图像
    :param flip_type: 'horizontal' 或 'vertical'
    :return: 翻转后的图像
    """
    if flip_type == 'horizontal':
        return np.fliplr(image)
    elif flip_type == 'vertical':
        return np.flipud(image)
    else:
        raise ValueError("flip_type 必须是 'horizontal' 或 'vertical'")

def zoom_image(image, zoom_factor):
    """
    缩放图像
    :param image: 输入图像
    :param zoom_factor: 缩放因子 (>1 放大, <1 缩小)
    :return: 缩放后的图像
    """
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
        image_3d = image.reshape(height, width, 1)
    else:
        height, width, channels = image.shape
        image_3d = image

    new_height = int(height * zoom_factor)
    new_width = int(width * zoom_factor)

    # 创建输出图像
    zoomed = np.zeros((new_height, new_width, channels))

    # 计算缩放映射
    for x in range(new_width):
        for y in range(new_height):
            orig_x = x / zoom_factor
            orig_y = y / zoom_factor

            if 0 <= orig_x < width - 1 and 0 <= orig_y < height - 1:
                # 双线性插值
                x1, y1 = int(orig_x), int(orig_y)
                x2, y2 = min(x1 + 1, width - 1), min(y1 + 1, height - 1)

                dx = orig_x - x1
                dy = orig_y - y1

                for c in range(channels):
                    val = (image_3d[y1, x1, c] * (1 - dx) * (1 - dy) +
                           image_3d[y1, x2, c] * dx * (1 - dy) +
                           image_3d[y2, x1, c] * (1 - dx) * dy +
                           image_3d[y2, x2, c] * dx * dy)
                    zoomed[y, x, c] = val

    if channels == 1:
        return zoomed.reshape(new_height, new_width)
    else:
        return zoomed.astype(np.uint8)

def apply_random_augmentation(image):
    """
    应用随机增强
    :param image: 输入图像
    :return: 增强后的图像
    """
    augmented = image.copy()

    # 随机选择增强类型
    augmentation_type = np.random.choice(['rotate', 'flip', 'zoom', 'none'])

    if augmentation_type == 'rotate':
        angle = np.random.uniform(-30, 30)
        augmented = rotate_image(augmented, angle)
    elif augmentation_type == 'flip':
        flip_dir = np.random.choice(['horizontal', 'vertical'])
        augmented = flip_image(augmented, flip_dir)
    elif augmentation_type == 'zoom':
        zoom_factor = np.random.uniform(0.8, 1.2)
        augmented = zoom_image(augmented, zoom_factor)

    return augmented

# 测试图像增强
if __name__ == "__main__":
    # 创建测试图像
    test_image = np.random.randint(0, 256, (32, 32, 3), dtype=np.uint8)

    print("原始图像形状:", test_image.shape)

    # 测试各种增强
    rotated = rotate_image(test_image, 45)
    flipped_h = flip_image(test_image, 'horizontal')
    flipped_v = flip_image(test_image, 'vertical')
    zoomed = zoom_image(test_image, 1.5)
    random_aug = apply_random_augmentation(test_image)

    print("旋转后形状:", rotated.shape)
    print("水平翻转后形状:", flipped_h.shape)
    print("垂直翻转后形状:", flipped_v.shape)
    print("缩放后形状:", zoomed.shape)
    print("随机增强后形状:", random_aug.shape)

    print("\n图像增强管道工作正常！")