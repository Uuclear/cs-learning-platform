#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习2解答: 手写数字分类
"""

import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt

def main():
    # 加载手写数字数据集
    digits = load_digits()
    X, y = digits.data, digits.target

    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 使用SVM分类器
    clf = SVC(kernel='rbf', gamma='scale', random_state=42)
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_test)

    # 评估性能
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"准确率: {accuracy:.4f}")
    print("\n混淆矩阵:")
    print(cm)
    print("\n详细分类报告:")
    print(classification_report(y_test, y_pred))

    # 可视化预测错误的例子
    errors = y_test != y_pred
    error_indices = np.where(errors)[0]

    if len(error_indices) > 0:
        plt.figure(figsize=(12, 8))
        for i, idx in enumerate(error_indices[:8]):  # 显示前8个错误
            plt.subplot(2, 4, i+1)
            plt.imshow(X_test[idx].reshape(8, 8), cmap='gray')
            plt.title(f'真实: {y_test[idx]}, 预测: {y_pred[idx]}')
            plt.axis('off')
        plt.suptitle('预测错误的例子')
        plt.tight_layout()
        plt.show()
    else:
        print("模型在测试集上没有预测错误！")

if __name__ == "__main__":
    main()