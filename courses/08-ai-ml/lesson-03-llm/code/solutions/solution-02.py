#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2：使用预训练Transformer构建文本分类器

这个脚本演示如何使用预训练的Transformer模型
构建一个简单的文本分类器。
"""

import numpy as np


def simple_text_classifier(texts, labels=None):
    """
    简化的文本分类器实现

    在真实场景中，这会使用预训练的Transformer模型，
    但这里我们使用模拟的方式来演示概念。

    Args:
        texts: 输入文本列表
        labels: 真实标签（用于训练模式）

    Returns:
        预测结果或训练信息
    """
    # 模拟预训练模型的特征提取
    def extract_features(text):
        """模拟从文本中提取特征"""
        # 简单的基于关键词的特征提取
        positive_words = ['好', '优秀', '棒', '喜欢', '推荐', '满意']
        negative_words = ['差', '糟糕', '讨厌', '不喜欢', '失望', '垃圾']

        text_lower = text.lower()
        pos_score = sum(1 for word in positive_words if word in text_lower)
        neg_score = sum(1 for word in negative_words if word in text_lower)

        # 返回简单的特征向量
        return np.array([pos_score, neg_score, len(text)])

    # 模拟分类器
    def classify(features):
        """基于特征进行分类"""
        pos_score, neg_score, length = features

        if pos_score > neg_score:
            confidence = min(0.9, 0.5 + (pos_score - neg_score) * 0.1)
            return "正面", confidence
        elif neg_score > pos_score:
            confidence = min(0.9, 0.5 + (neg_score - pos_score) * 0.1)
            return "负面", confidence
        else:
            return "中性", 0.5

    # 处理输入文本
    results = []
    for text in texts:
        features = extract_features(text)
        prediction, confidence = classify(features)
        results.append({
            'text': text,
            'prediction': prediction,
            'confidence': confidence,
            'features': features
        })

    return results


def real_transformer_classifier(texts):
    """
    使用真实Transformer模型的文本分类器（如果可用）
    """
    try:
        from transformers import pipeline

        print("✅ 使用真实的Transformer模型进行分类...")

        # 创建情感分析管道
        classifier = pipeline(
            "sentiment-analysis",
            model="uer/roberta-base-finetuned-chinanews-chinese",  # 中文情感分析模型
            return_all_scores=True
        )

        results = []
        for text in texts:
            output = classifier(text)
            # 获取最高置信度的预测
            best_pred = max(output[0], key=lambda x: x['score'])
            results.append({
                'text': text,
                'prediction': best_pred['label'],
                'confidence': best_pred['score']
            })

        return results

    except ImportError:
        print("ℹ️  transformers库未安装，使用模拟分类器...")
        return None
    except Exception as e:
        print(f"⚠️  真实模型分类失败: {e}")
        print("使用模拟分类器...")
        return None


def main():
    """主函数：演示文本分类器"""
    print("🎯 解决方案2：构建文本分类器\n")
    print("=" * 60)

    # 测试文本
    test_texts = [
        "这部电影真是太棒了！演员表演出色，剧情紧凑。",
        "产品质量很差，完全不值得购买。",
        "今天天气不错，适合出去散步。",
        "这个餐厅的服务态度很好，食物也很美味。",
        "软件经常崩溃，用户体验非常糟糕。"
    ]

    print("测试文本:")
    for i, text in enumerate(test_texts, 1):
        print(f"{i}. {text}")
    print()

    # 尝试使用真实Transformer模型
    real_results = real_transformer_classifier(test_texts)

    if real_results is not None:
        print("真实Transformer模型结果:")
        for result in real_results:
            print(f"文本: {result['text'][:30]}...")
            print(f"预测: {result['prediction']} (置信度: {result['confidence']:.3f})\n")
    else:
        # 使用模拟分类器
        print("模拟分类器结果:")
        simulated_results = simple_text_classifier(test_texts)
        for result in simulated_results:
            print(f"文本: {result['text'][:30]}...")
            print(f"预测: {result['prediction']} (置信度: {result['confidence']:.3f})")
            print(f"特征: 正面词={int(result['features'][0])}, 负面词={int(result['features'][1])}, 长度={int(result['features'][2])}\n")

    print("=" * 60)
    print("✅ 文本分类器演示完成！")
    print("\n关键要点:")
    print("1. 预训练Transformer模型可以作为强大的特征提取器")
    print("2. 微调（fine-tuning）可以让模型适应特定的分类任务")
    print("3. 迁移学习大大减少了训练所需的数据和计算资源")
    print("4. 即使是简单的特征工程也能产生合理的分类结果")
    print("\n💡 实际应用建议:")
    print("- 对于中文文本，选择专门针对中文预训练的模型")
    print("- 根据具体任务选择合适的预训练模型")
    print("- 考虑使用few-shot learning减少标注数据需求")


if __name__ == "__main__":
    main()