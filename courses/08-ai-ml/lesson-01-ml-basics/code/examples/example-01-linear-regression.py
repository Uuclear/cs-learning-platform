#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 线性回归（房价预测）
展示如何使用线性回归模型预测房屋价格
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def main():
    # 创建模拟数据：房屋面积（平方米）和价格（万元）
    np.random.seed(42)
    area = np.random.randint(50, 200, 100)  # 50-200平方米的房子
    # 真实关系：价格 = 面积 * 2 + 噪声
    price = area * 2 + np.random.normal(0, 10, 100)

    # 准备数据：sklearn要求输入是二维数组
    X = area.reshape(-1, 1)  # 特征：面积
    y = price                # 目标：价格

    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 创建并训练线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = model.predict(X_test)

    # 输出模型参数和性能
    print(f"模型斜率（每平方米价格）: {model.coef_[0]:.2f} 万元/平方米")
    print(f"模型截距: {model.intercept_:.2f} 万元")
    print(f"模型在测试集上的R²分数: {model.score(X_test, y_test):.3f}")

    # 可视化结果
    plt.figure(figsize=(10, 6))
    plt.scatter(X_train, y_train, alpha=0.6, label='训练数据')
    plt.scatter(X_test, y_test, color='red', alpha=0.8, label='测试数据')
    plt.plot(X, model.predict(X), color='green', linewidth=2, label='预测线')
    plt.xlabel('房屋面积 (平方米)')
    plt.ylabel('价格 (万元)')
    plt.title('线性回归：房价预测')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    main()