#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：检索增强生成（RAG）管道演示

这个脚本演示如何构建一个简单的RAG系统，
结合信息检索和文本生成来回答问题。
"""

import numpy as np
from typing import List, Dict, Tuple


class SimpleVectorStore:
    """简单的向量存储实现"""

    def __init__(self):
        self.documents = []
        self.vectors = []

    def add_document(self, text: str, vector: np.ndarray):
        """添加文档和对应的向量"""
        self.documents.append(text)
        self.vectors.append(vector)

    def search(self, query_vector: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
        """基于向量相似度搜索最相关的文档"""
        if not self.vectors:
            return []

        # 计算余弦相似度
        similarities = []
        for vec in self.vectors:
            # 归一化向量
            query_norm = query_vector / np.linalg.norm(query_vector)
            doc_norm = vec / np.linalg.norm(vec)
            similarity = np.dot(query_norm, doc_norm)
            similarities.append(similarity)

        # 获取top-k最相似的文档
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = [(self.documents[i], similarities[i]) for i in top_indices]

        return results


class SimpleRAG:
    """简单的RAG系统实现"""

    def __init__(self):
        self.vector_store = SimpleVectorStore()

    def _text_to_vector(self, text: str) -> np.ndarray:
        """
        将文本转换为向量（模拟真实嵌入模型）

        在真实场景中，这里会使用预训练的嵌入模型如BERT、Sentence-BERT等
        """
        # 简单的基于字符的哈希向量（仅用于演示）
        np.random.seed(hash(text) % (2**32))
        return np.random.randn(128)

    def add_knowledge_base(self, documents: List[str]):
        """向知识库添加文档"""
        print(f"正在处理 {len(documents)} 个文档...")
        for doc in documents:
            vector = self._text_to_vector(doc)
            self.vector_store.add_document(doc, vector)
        print("✅ 知识库构建完成！")

    def generate_answer(self, question: str, retrieved_docs: List[str]) -> str:
        """
        基于检索到的文档生成答案（模拟大语言模型）

        在真实场景中，这里会调用实际的LLM API
        """
        if not retrieved_docs:
            return "抱歉，我没有找到相关信息来回答这个问题。"

        # 构建提示
        context = "\n".join([f"相关信息 {i+1}: {doc}" for i, doc in enumerate(retrieved_docs)])
        prompt = f"""基于以下相关信息回答问题：

{context}

问题: {question}

请基于上述信息给出简洁准确的回答。如果信息不足以回答问题，请说明无法确定。"""

        # 模拟LLM响应
        if "Transformer" in question or "注意力" in question:
            return "Transformer架构的核心是自注意力机制，它允许模型在处理序列时关注序列中的不同位置。"
        elif "大模型" in question or "LLM" in question:
            return "大语言模型通过在海量文本上预训练，学习了丰富的语言模式和世界知识。"
        elif "RAG" in question or "检索" in question:
            return "RAG（检索增强生成）结合了信息检索和文本生成，让模型能够基于最新、特定领域的知识回答问题。"
        else:
            # 通用响应
            return f"根据检索到的信息，{question}的答案涉及相关文档中提到的内容。具体的详细信息需要参考相关资料。"

    def query(self, question: str, top_k: int = 3) -> Dict:
        """查询RAG系统"""
        # 1. 将问题转换为向量
        query_vector = self._text_to_vector(question)

        # 2. 检索最相关的文档
        retrieved_docs = self.vector_store.search(query_vector, top_k)

        # 3. 提取文档文本
        doc_texts = [doc for doc, score in retrieved_docs]

        # 4. 生成答案
        answer = self.generate_answer(question, doc_texts)

        return {
            'question': question,
            'retrieved_documents': retrieved_docs,
            'answer': answer
        }


def main():
    """主函数：演示RAG系统"""
    print("🎯 解决方案3：RAG（检索增强生成）管道演示\n")
    print("=" * 60)

    # 创建知识库文档
    knowledge_base = [
        "Transformer是一种神经网络架构，完全基于注意力机制，摒弃了传统的循环和卷积结构。",
        "自注意力机制允许序列中的每个位置都能关注序列中的其他所有位置，计算它们之间的相关性权重。",
        "多头注意力通过并行使用多个注意力头，让模型能够同时关注不同位置的不同子空间信息。",
        "大语言模型的训练通常包括预训练、微调和人类反馈强化学习（RLHF）三个阶段。",
        "提示工程是与大语言模型有效交互的关键技能，好的提示能显著提升模型输出质量。",
        "RAG（Retrieval Augmented Generation）结合了信息检索和文本生成，解决了传统LLM的知识截止和幻觉问题。",
        "缩放定律表明，大语言模型的性能与模型参数数量、训练数据量和计算资源呈幂律关系。",
        "涌现能力是指当模型规模达到某个阈值时，出现的一些在小模型中完全不存在的能力。"
    ]

    # 初始化RAG系统
    rag_system = SimpleRAG()

    # 添加知识库
    rag_system.add_knowledge_base(knowledge_base)
    print()

    # 测试问题
    test_questions = [
        "Transformer架构的核心思想是什么？",
        "什么是RAG系统？",
        "大语言模型是如何训练的？",
        "为什么多头注意力很重要？"
    ]

    # 回答问题
    for i, question in enumerate(test_questions, 1):
        print(f"问题 {i}: {question}")
        result = rag_system.query(question)

        print(f"\n检索到的相关文档 (Top 2):")
        for j, (doc, score) in enumerate(result['retrieved_documents'][:2], 1):
            print(f"  {j}. 相似度: {score:.3f} - {doc[:60]}...")

        print(f"\n生成的答案:")
        print(f"  {result['answer']}\n")
        print("-" * 50)

    print("✅ RAG系统演示完成！")
    print("\n关键要点:")
    print("1. RAG解决了传统LLM的知识截止问题")
    print("2. 检索阶段确保模型基于最新、准确的信息回答")
    print("3. 生成阶段利用LLM的语言能力产生流畅的回答")
    print("4. 向量检索的质量直接影响最终答案的准确性")
    print("\n💡 实际应用建议:")
    print("- 使用专门的嵌入模型（如text-embedding-ada-002）进行向量化")
    print("- 考虑使用FAISS或Pinecone等高效的向量数据库")
    print("- 对检索结果进行重排序以提高相关性")


if __name__ == "__main__":
    main()