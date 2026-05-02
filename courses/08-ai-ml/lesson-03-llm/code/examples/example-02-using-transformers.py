#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：使用HuggingFace Transformers进行文本生成

这个脚本演示如何使用HuggingFace的transformers库
加载预训练的语言模型并生成文本。
"""

import sys


def main():
    """主函数：演示使用transformers库"""
    print("🚀 示例2：使用HuggingFace Transformers进行文本生成\n")
    print("=" * 60)

    try:
        # 尝试导入必要的库
        from transformers import pipeline, set_seed

        print("✅ 成功导入transformers库！\n")

        # 设置随机种子以确保结果可重现
        set_seed(42)

        # 创建文本生成管道
        # 使用一个较小的预训练模型以减少资源消耗
        print("正在加载预训练模型...")
        generator = pipeline(
            'text-generation',
            model='distilgpt2',  # 轻量级GPT-2变体
            max_length=50,
            num_return_sequences=1,
            pad_token_id=50256  # GPT-2的eos_token_id
        )
        print("✅ 模型加载完成！\n")

        # 定义输入提示
        prompts = [
            "人工智能是",
            "机器学习的主要优势在于",
            "Transformer架构的核心思想是"
        ]

        # 为每个提示生成文本
        for i, prompt in enumerate(prompts, 1):
            print(f"提示 {i}: \"{prompt}\"")
            print("生成结果:")

            try:
                outputs = generator(prompt)
                generated_text = outputs[0]['generated_text']
                print(f"\"{generated_text}\"\n")
            except Exception as e:
                print(f"❌ 生成失败: {e}\n")
                continue

        print("=" * 60)
        print("✅ 文本生成演示完成！")
        print("\n关键要点:")
        print("1. HuggingFace提供了简单易用的API来使用预训练模型")
        print("2. 预训练模型可以快速适应各种文本生成任务")
        print("3. 提示（prompt）的设计对生成结果有很大影响")
        print("4. 不同的模型在质量和速度之间有不同的权衡")

    except ImportError as e:
        print(f"❌ 无法导入transformers库: {e}")
        print("\n请安装必要的依赖:")
        print("pip install transformers torch")
        print("\n或者运行这个简化版本的演示:")

        # 简化版演示（不依赖外部库）
        simple_demo()


def simple_demo():
    """简化版演示（不依赖transformers库）"""
    print("\n" + "=" * 40)
    print("简化版文本生成演示")
    print("=" * 40)

    # 模拟预训练模型的输出
    mock_responses = {
        "人工智能是": "人工智能是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。",
        "机器学习的主要优势在于": "机器学习的主要优势在于能够从数据中自动学习模式，而无需显式编程。",
        "Transformer架构的核心思想是": "Transformer架构的核心思想是使用注意力机制来处理序列数据，完全摒弃了循环和卷积结构。"
    }

    prompts = ["人工智能是", "机器学习的主要优势在于", "Transformer架构的核心思想是"]

    for prompt in prompts:
        print(f"提示: \"{prompt}\"")
        print(f"生成: \"{mock_responses[prompt]}\"\n")

    print("💡 这只是一个模拟演示。要体验真实的Transformer模型，请安装transformers库！")


if __name__ == "__main__":
    main()