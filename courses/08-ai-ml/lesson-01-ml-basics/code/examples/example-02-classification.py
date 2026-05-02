#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: 分类（邮件垃圾邮件过滤）
展示如何使用朴素贝叶斯算法进行文本分类
"""

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer

def main():
    # 模拟邮件数据
    emails = [
        "免费赢取iPhone大奖", "会议安排明天上午10点",
        "点击链接领取现金奖励", "项目进度报告已发送",
        "限时优惠最后一天", "团队建设活动通知",
        "银行账户异常请验证", "代码审查已完成"
    ]
    labels = [1, 0, 1, 0, 1, 0, 1, 0]  # 1=垃圾邮件, 0=正常邮件

    # 使用简单的词频特征提取（实际中会用更复杂的方法）
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(emails).toarray()

    # 创建并训练朴素贝叶斯分类器
    clf = GaussianNB()
    clf.fit(X, labels)

    # 预测新邮件
    new_emails = ["免费领取奖金", "下周项目会议"]
    X_new = vectorizer.transform(new_emails).toarray()
    predictions = clf.predict(X_new)

    print("邮件分类结果:")
    for email, pred in zip(new_emails, predictions):
        result = "垃圾邮件" if pred == 1 else "正常邮件"
        print(f"'{email}' -> {result}")

    # 在原始数据上评估（实际中应该用更大的数据集）
    train_predictions = clf.predict(X)
    accuracy = accuracy_score(labels, train_predictions)
    print(f"\n训练准确率: {accuracy:.3f}")
    print("\n详细分类报告:")
    print(classification_report(labels, train_predictions, target_names=['正常邮件', '垃圾邮件']))

if __name__ == "__main__":
    main()