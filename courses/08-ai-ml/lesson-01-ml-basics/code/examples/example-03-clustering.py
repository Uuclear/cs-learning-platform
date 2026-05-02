#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: 聚类（客户分群）
展示如何使用K-means算法进行无监督学习的客户分群
"""

import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def main():
    # 创建模拟客户数据：年消费金额和访问频率
    np.random.seed(42)
    # 高价值客户：高消费、高频率
    high_value = np.random.multivariate_normal([80, 15], [[20, 5], [5, 3]], 30)
    # 中等价值客户：中等消费、中等频率
    medium_value = np.random.multivariate_normal([50, 8], [[15, 3], [3, 2]], 40)
    # 低价值客户：低消费、低频率
    low_value = np.random.multivariate_normal([20, 3], [[10, 2], [2, 1]], 30)

    # 合并所有客户数据
    customers = np.vstack([high_value, medium_value, low_value])
    np.random.shuffle(customers)  # 打乱顺序

    # 使用K-means聚类，假设我们知道有3个客户群体
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(customers)

    # 可视化聚类结果
    plt.figure(figsize=(10, 6))
    colors = ['red', 'blue', 'green']
    for i in range(3):
        cluster_points = customers[clusters == i]
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                   c=colors[i], label=f'群体 {i+1}', alpha=0.7)

    # 标记聚类中心
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', marker='x', s=200, linewidths=3, label='聚类中心')

    plt.xlabel('年消费金额 (千元)')
    plt.ylabel('年访问频率')
    plt.title('客户聚类分析')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

    # 输出聚类中心信息
    print("各客户群体特征:")
    for i, center in enumerate(centers):
        print(f"群体 {i+1}: 年消费 {center[0]:.1f}千元, 年访问 {center[1]:.1f}次")

if __name__ == "__main__":
    main()