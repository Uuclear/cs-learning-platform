# 解决方案3：构建简单的图像相似性搜索系统
import numpy as np
from typing import List, Tuple

class ImageSimilaritySearch:
    """
    简单的图像相似性搜索系统
    使用特征向量和余弦相似度进行图像检索
    """

    def __init__(self):
        self.image_features = {}  # 存储图像ID到特征向量的映射
        self.image_paths = {}     # 存储图像ID到路径的映射

    def extract_features(self, image: np.ndarray) -> np.ndarray:
        """
        提取图像特征（简化版）
        实际应用中会使用预训练CNN提取深度特征
        """
        if len(image.shape) == 3:
            # 对于彩色图像，计算每个通道的统计特征
            features = []
            for channel in range(image.shape[2]):
                channel_data = image[:, :, channel]
                features.extend([
                    np.mean(channel_data),
                    np.std(channel_data),
                    np.min(channel_data),
                    np.max(channel_data)
                ])
            return np.array(features)
        else:
            # 对于灰度图像
            return np.array([
                np.mean(image),
                np.std(image),
                np.min(image),
                np.max(image)
            ])

    def add_image(self, image_id: str, image: np.ndarray, image_path: str = ""):
        """
        添加图像到搜索系统
        :param image_id: 图像唯一标识符
        :param image: 图像数据
        :param image_path: 图像路径（可选）
        """
        features = self.extract_features(image)
        self.image_features[image_id] = features
        self.image_paths[image_id] = image_path

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        计算余弦相似度
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def search_similar(self, query_image: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        搜索相似图像
        :param query_image: 查询图像
        :param top_k: 返回前K个最相似的结果
        :return: [(image_id, similarity_score), ...]
        """
        if not self.image_features:
            return []

        query_features = self.extract_features(query_image)
        similarities = []

        for image_id, features in self.image_features.items():
            similarity = self.cosine_similarity(query_features, features)
            similarities.append((image_id, similarity))

        # 按相似度降序排序
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def batch_add_images(self, image_dict: dict):
        """
        批量添加图像
        :param image_dict: {image_id: (image_array, image_path)}
        """
        for image_id, (image, path) in image_dict.items():
            self.add_image(image_id, image, path)

# 创建测试数据并演示相似性搜索
def create_test_images():
    """创建测试图像"""
    np.random.seed(42)

    # 创建一些具有不同特征的测试图像
    images = {}

    # 红色主导的图像
    red_image = np.random.rand(64, 64, 3)
    red_image[:, :, 0] += 0.5  # 增加红色通道
    images['red_01'] = (np.clip(red_image, 0, 1), "red_image_01.jpg")

    # 蓝色主导的图像
    blue_image = np.random.rand(64, 64, 3)
    blue_image[:, :, 2] += 0.5  # 增加蓝色通道
    images['blue_01'] = (np.clip(blue_image, 0, 1), "blue_image_01.jpg")

    # 高对比度图像
    high_contrast = np.random.choice([0, 1], size=(64, 64, 3), p=[0.3, 0.7])
    images['contrast_01'] = (high_contrast.astype(float), "contrast_01.jpg")

    # 低对比度图像
    low_contrast = np.full((64, 64, 3), 0.5) + np.random.normal(0, 0.1, (64, 64, 3))
    low_contrast = np.clip(low_contrast, 0, 1)
    images['low_contrast_01'] = (low_contrast, "low_contrast_01.jpg")

    # 另一个红色图像（应该与red_01相似）
    red_image_2 = np.random.rand(64, 64, 3)
    red_image_2[:, :, 0] += 0.4  # 类似的红色增强
    images['red_02'] = (np.clip(red_image_2, 0, 1), "red_image_02.jpg")

    return images

# 主程序
if __name__ == "__main__":
    # 创建相似性搜索系统
    search_system = ImageSimilaritySearch()

    # 添加测试图像
    test_images = create_test_images()
    search_system.batch_add_images(test_images)

    print("已添加图像到搜索系统:")
    for img_id in test_images.keys():
        print(f"  - {img_id}")

    # 创建查询图像（类似于red_01）
    query_red = np.random.rand(64, 64, 3)
    query_red[:, :, 0] += 0.45

    print(f"\n查询图像特征: 红色主导")

    # 执行相似性搜索
    results = search_system.search_similar(query_red, top_k=3)

    print("\n最相似的图像:")
    for i, (img_id, similarity) in enumerate(results, 1):
        print(f"{i}. {img_id} (相似度: {similarity:.4f})")

    # 测试另一个查询（蓝色主导）
    query_blue = np.random.rand(64, 64, 3)
    query_blue[:, :, 2] += 0.6

    print(f"\n\n查询图像特征: 蓝色主导")
    results_blue = search_system.search_similar(query_blue, top_k=3)

    print("\n最相似的图像:")
    for i, (img_id, similarity) in enumerate(results_blue, 1):
        print(f"{i}. {img_id} (相似度: {similarity:.4f})")

    print("\n图像相似性搜索系统演示完成！")