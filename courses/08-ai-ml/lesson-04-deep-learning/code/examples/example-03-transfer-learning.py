# 示例3：迁移学习概念演示
import numpy as np

def extract_features(images, feature_extractor_type="simulated"):
    """
    模拟特征提取过程（实际中会使用预训练模型）
    :param images: 输入图像列表
    :param feature_extractor_type: 特征提取器类型
    :return: 提取的特征向量
    """
    if feature_extractor_type == "simulated":
        # 模拟从预训练模型提取的特征
        num_images = len(images)
        feature_dim = 128  # 假设特征维度为128
        features = np.random.rand(num_images, feature_dim)
        return features
    else:
        raise NotImplementedError("仅支持模拟特征提取")

def classify_with_extracted_features(features, labels, new_labels):
    """
    使用提取的特征进行分类
    :param features: 提取的特征
    :param labels: 原始标签
    :param new_labels: 新任务的标签
    :return: 分类结果
    """
    # 简单的最近邻分类器
    try:
        from scipy.spatial.distance import cdist
    except ImportError:
        # 如果没有scipy，使用numpy实现简单距离计算
        def simple_distance(a, b):
            return np.sqrt(np.sum((a - b) ** 2))

        predictions = []
        for i in range(len(new_labels)):
            # 模拟新特征
            new_feature = np.random.rand(features.shape[1])
            distances = [simple_distance(new_feature, feat) for feat in features[:2]]
            nearest_idx = np.argmin(distances)
            predictions.append(labels[nearest_idx])
        return predictions, np.random.rand(len(new_labels), features.shape[1])

    # 为新样本生成特征（模拟）
    new_features = np.random.rand(len(new_labels), features.shape[1])

    # 计算距离
    distances = cdist(new_features, features, metric='euclidean')
    predictions = []

    for i in range(len(new_labels)):
        nearest_idx = np.argmin(distances[i])
        predictions.append(labels[nearest_idx])

    return predictions, new_features

# 演示迁移学习
original_images = [np.random.rand(224, 224, 3) for _ in range(10)]
original_labels = ["cat", "dog", "bird", "car", "plane", "cat", "dog", "bird", "car", "plane"]

# 提取特征
features = extract_features(original_images)
print(f"提取的特征形状: {features.shape}")

# 新任务：区分动物和交通工具
new_task_labels = ["animal", "vehicle"]
predictions, _ = classify_with_extracted_features(features[:2], original_labels[:2], new_task_labels)

print(f"\n迁移学习预测结果: {predictions}")
print("这展示了如何重用预训练模型的特征提取能力！")