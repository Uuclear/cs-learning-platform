# 挑战1：手写数字识别入门

## 难度
⭐⭐

## 描述
使用sklearn的KNN算法实现简单的手写数字识别。

要求：
1. 使用sklearn内置的digits数据集
2. 将数据分为训练集和测试集（80/20）
3. 使用KNeighborsClassifier训练模型
4. 输出测试集准确率

## 提示
- 使用 `from sklearn.datasets import load_digits`
- 使用 `train_test_split` 分割数据
- K值可以尝试5或7
