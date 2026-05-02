#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：提示工程（Prompt Engineering）实践

这个脚本演示不同的提示工程技术，
展示如何通过精心设计的提示来引导大模型产生更好的输出。
"""

import sys


def demonstrate_prompt_techniques():
    """演示不同的提示工程技术"""
    print("🚀 示例3：提示工程（Prompt Engineering）实践\n")
    print("=" * 60)

    # 模拟大语言模型的响应函数
    def mock_llm_response(prompt):
        """
        模拟大语言模型对提示的响应
        在真实场景中，这里会调用实际的API
        """
        # 简单的规则-based模拟
        prompt_lower = prompt.lower()

        if "总结" in prompt_lower or "摘要" in prompt_lower:
            return "这是一段关于人工智能发展的文本摘要。AI技术在过去十年取得了显著进步，特别是在深度学习和大语言模型方面。"

        elif "翻译" in prompt_lower:
            return "Artificial Intelligence is transforming our world in profound ways."

        elif "分类" in prompt_lower or "情感" in prompt_lower:
            return "情感分析结果：正面情感 (置信度: 0.85)"

        elif "问答" in prompt_lower or "?" in prompt:
            return "根据您的问题，Transformer架构于2017年由Google提出，其核心创新是自注意力机制。"

        elif "创意" in prompt_lower or "故事" in prompt_lower:
            return "从前，在一个充满数据的数字王国里，有一个名叫Transformer的英雄..."

        else:
            return "感谢您的输入！这是一个通用的AI响应示例。在实际应用中，精心设计的提示会产生更具体、更有用的输出。"

    # 不同类型的提示示例
    prompt_examples = [
        {
            "type": "基础提示",
            "prompt": "人工智能是什么？"
        },
        {
            "type": "角色扮演提示",
            "prompt": "你是一位AI专家，请用通俗易懂的语言解释Transformer架构的工作原理。"
        },
        {
            "type": "结构化提示",
            "prompt": """请完成以下任务：
1. 总结下面这段文字的主要观点
2. 提取3个关键术语
3. 用一句话说明其实际应用价值

文本：Transformer模型通过自注意力机制处理序列数据，允许并行计算并捕获长距离依赖关系。"""
        },
        {
            "type": "少样本提示（Few-shot）",
            "prompt": """示例1：
输入：这部电影太棒了！
输出：正面情感

示例2：
输入：服务很差，完全不推荐。
输出：负面情感

现在请分类：
输入：产品功能很全面，但价格有点贵。
输出："""
        },
        {
            "type": "思维链提示（Chain-of-Thought）",
            "prompt": """让我们一步一步思考这个问题：
如果一个模型有1750亿参数，每个参数需要4字节存储，
那么这个模型需要多少GB的内存？

步骤1：计算总字节数
步骤2：转换为GB
步骤3：给出最终答案

请按上述步骤详细解答。"""
        }
    ]

    # 演示每个提示的效果
    for i, example in enumerate(prompt_examples, 1):
        print(f"提示 {i}: {example['type']}")
        print(f"内容: \"{example['prompt']}\"")
        print("模型响应:")
        response = mock_llm_response(example['prompt'])
        print(f"\"{response}\"\n")
        print("-" * 50)

    print("✅ 提示工程演示完成！")
    print("\n关键要点:")
    print("1. 提示的质量直接影响模型输出的质量")
    print("2. 角色扮演提示可以让模型更好地适应特定场景")
    print("3. 结构化提示帮助模型理解复杂的多步骤任务")
    print("4. 少样本提示提供了明确的输出格式示例")
    print("5. 思维链提示鼓励模型展示推理过程")


def main():
    """主函数"""
    try:
        # 尝试导入openai库（用于真实API调用）
        import openai
        print("💡 检测到openai库，可以使用真实API！")
        print("要使用真实API，请设置OPENAI_API_KEY环境变量。\n")
    except ImportError:
        print("ℹ️  openai库未安装，将使用模拟演示。")
        print("要使用真实API，请运行: pip install openai\n")

    demonstrate_prompt_techniques()

    print("\n" + "=" * 60)
    print("🎯 提示工程最佳实践:")
    print("• 明确指定任务类型和期望的输出格式")
    print("• 提供具体的上下文和约束条件")
    print("• 使用示例来指导模型理解期望的输出风格")
    print("• 对于复杂任务，分解为多个简单步骤")
    print("• 测试不同的提示变体并选择效果最好的")


if __name__ == "__main__":
    main()