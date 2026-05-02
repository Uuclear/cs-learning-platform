#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习3解答: 客户流失预测
"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt

def main():
    # 创建模拟客户数据
    np.random.seed(42)
    n_customers = 1000

    # 特征：使用时长(月)、月消费(元)、客服呼叫次数
    tenure = np.random.exponential(24, n_customers)  # 使用时长，指数分布
    monthly_charges = np.random.normal(70, 20, n_customers)  # 月消费
    customer_service_calls = np.random.poisson(2, n_customers)  # 客服呼叫次数

    # 确保数值合理
    tenure = np.clip(tenure, 1, 72)  # 1-72个月
    monthly_charges = np.clip(monthly_charges, 20, 150)  # 20-150元
    customer_service_calls = np.clip(customer_service_calls, 0, 10)  # 0-10次

    # 定义流失标签：使用时长短、客服呼叫多的客户更容易流失
    churn_probability = (
        0.7 * (1 - tenure / 72) +  # 使用时间越短，流失概率越高
        0.2 * (customer_service_calls / 10) +  # 客服呼叫越多，流失概率越高
        0.1 * np.random.random(n_customers)  # 随机噪声
    )
    churn = (churn_probability > 0.5).astype(int)

    # 准备特征矩阵
    X = np.column_stack([tenure, monthly_charges, customer_service_calls])
    y = churn

    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 处理不平衡数据：计算类别权重
    class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
    class_weight_dict = {0: class_weights[0], 1: class_weights[1]}

    # 训练随机森林分类器
    clf = RandomForestClassifier(
        n_estimators=100,
        class_weight=class_weight_dict,
        random_state=42
    )
    clf.fit(X_train, y_train)

    # 预测
    y_pred = clf.predict(X_test)
    y_pred_proba = clf.predict_proba(X_test)[:, 1]  # 正类概率

    # 评估性能
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba)

    print(f"准确率: {accuracy:.4f}")
    print(f"AUC分数: {auc_score:.4f}")
    print(f"流失客户比例: {np.mean(y):.3f}")

    # 绘制ROC曲线
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC曲线 (AUC = {auc_score:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='随机分类器')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('假正率 (False Positive Rate)')
    plt.ylabel('真正率 (True Positive Rate)')
    plt.title('客户流失预测 - ROC曲线')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.show()

    # 显示特征重要性
    feature_names = ['使用时长(月)', '月消费(元)', '客服呼叫次数']
    importance = clf.feature_importances_
    plt.figure(figsize=(8, 6))
    plt.barh(feature_names, importance)
    plt.xlabel('特征重要性')
    plt.title('客户流失预测 - 特征重要性')
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    main()