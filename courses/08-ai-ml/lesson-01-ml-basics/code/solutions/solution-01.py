#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 简单线性回归（学生成绩预测）
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def main():
    # 生成100个学生的数据：学习时间(1-20小时)和成绩(0-100分)
    np.random.seed(42)
    study_hours = np.random.randint(1, 21, 100)  # 1-20小时

    # 成绩与学习时间成正比，但有噪声，且限制在0-100范围内
    scores = study_hours * 4 + np.random.normal(0, 8, 100)
    scores = np.clip(scores, 0, 100)  # 确保成绩在0-100之间

    # 准备数据
    X = study_hours.reshape(-1, 1)
    y = scores

    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练线性回归模型
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 评估性能
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"训练集R²分数: {train_score:.3f}")
    print(f"测试集R²分数: {test_score:.3f}")
    print(f"模型斜率: {model.coef_[0]:.2f} 分/小时")
    print(f"模型截距: {model.intercept_:.2f} 分")

    # 可视化结果
    plt.figure(figsize=(10, 6))
    plt.scatter(X_train, y_train, alpha=0.6, label='训练数据')
    plt.scatter(X_test, y_test, color='red', alpha=0.8, label='测试数据')
    plt.plot(X, model.predict(X), color='green', linewidth=2, label='预测线')
    plt.xlabel('学习时间 (小时)')
    plt.ylabel('考试成绩 (分)')
    plt.title('线性回归：学生成绩预测')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    main()