#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贪心算法解决方案 02: 霍夫曼编码实现
用于数据压缩的最优前缀编码
"""

import heapq
from collections import defaultdict


class HuffmanNode:
    """霍夫曼树节点类"""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char      # 字符（叶子节点）
        self.freq = freq      # 频率
        self.left = left      # 左子树
        self.right = right    # 右子树

    def __lt__(self, other):
        """用于堆排序的比较函数"""
        return self.freq < other.freq


def build_huffman_tree(char_freq):
    """
    构建霍夫曼树

    参数:
        char_freq: 字典，字符到频率的映射

    返回:
        霍夫曼树的根节点
    """
    # 创建最小堆（优先队列）
    heap = []
    for char, freq in char_freq.items():
        node = HuffmanNode(char, freq)
        heapq.heappush(heap, node)

    # 贪心策略：每次取频率最小的两个节点合并
    while len(heap) > 1:
        # 取出频率最小的两个节点
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # 创建新节点，频率为两者之和
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    # 堆中只剩一个节点，即霍夫曼树的根
    return heap[0] if heap else None


def generate_huffman_codes(root):
    """
    从霍夫曼树生成编码表

    参数:
        root: 霍夫曼树根节点

    返回:
        编码字典，字符到编码字符串的映射
    """
    if not root:
        return {}

    codes = {}

    def traverse(node, code):
        """深度优先遍历生成编码"""
        if node.char is not None:
            # 叶子节点，存储编码
            codes[node.char] = code if code else "0"  # 处理只有一个字符的情况
        else:
            # 内部节点，继续遍历
            if node.left:
                traverse(node.left, code + "0")
            if node.right:
                traverse(node.right, code + "1")

    traverse(root, "")
    return codes


def huffman_encode(text, codes):
    """
    使用霍夫曼编码压缩文本

    参数:
        text: 原始文本
        codes: 霍夫曼编码表

    返回:
        编码后的二进制字符串
    """
    encoded = ""
    for char in text:
        encoded += codes[char]
    return encoded


def huffman_decode(encoded_text, root):
    """
    使用霍夫曼树解码文本

    参数:
        encoded_text: 编码后的二进制字符串
        root: 霍夫曼树根节点

    返回:
        解码后的原始文本
    """
    if not root or not encoded_text:
        return ""

    # 特殊情况：只有一个字符
    if root.char is not None:
        return root.char * len(encoded_text)

    decoded = []
    current = root

    for bit in encoded_text:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        # 到达叶子节点
        if current.char is not None:
            decoded.append(current.char)
            current = root  # 重置到根节点

    return "".join(decoded)


def calculate_compression_ratio(original, encoded):
    """
    计算压缩率

    参数:
        original: 原始文本
        encoded: 编码后的二进制字符串

    返回:
        压缩率百分比
    """
    original_bits = len(original) * 8  # 假设ASCII编码，每个字符8位
    encoded_bits = len(encoded)
    ratio = (1 - encoded_bits / original_bits) * 100
    return ratio


def main():
    """主函数：演示霍夫曼编码的完整流程"""
    print("=== 霍夫曼编码贪心算法实现 ===\n")

    # 示例1：英文文本压缩
    print("1. 英文文本压缩示例:")
    text1 = "this is an example of a huffman tree"
    print(f"   原始文本: '{text1}'")
    print(f"   文本长度: {len(text1)} 字符")

    # 统计字符频率
    char_freq1 = defaultdict(int)
    for char in text1:
        char_freq1[char] += 1

    print("   字符频率:")
    for char, freq in sorted(char_freq1.items()):
        display_char = repr(char) if char == ' ' else char
        print(f"     {display_char}: {freq}")

    # 构建霍夫曼树和编码
    root1 = build_huffman_tree(char_freq1)
    codes1 = generate_huffman_codes(root1)

    print("\n   霍夫曼编码:")
    for char, code in sorted(codes1.items()):
        display_char = repr(char) if char == ' ' else char
        print(f"     {display_char}: {code}")

    # 编码和解码
    encoded1 = huffman_encode(text1, codes1)
    decoded1 = huffman_decode(encoded1, root1)
    compression_ratio1 = calculate_compression_ratio(text1, encoded1)

    print(f"\n   编码结果: {encoded1}")
    print(f"   解码结果: '{decoded1}'")
    print(f"   压缩率: {compression_ratio1:.1f}%")
    print(f"   正确性: {'✓' if decoded1 == text1 else '✗'}\n")

    # 示例2：中文文本压缩
    print("2. 中文文本压缩示例:")
    text2 = "动态规划很有趣贪心算法也很有用"
    print(f"   原始文本: '{text2}'")
    print(f"   文本长度: {len(text2)} 字符")

    # 统计字符频率
    char_freq2 = defaultdict(int)
    for char in text2:
        char_freq2[char] += 1

    # 构建霍夫曼树和编码
    root2 = build_huffman_tree(char_freq2)
    codes2 = generate_huffman_codes(root2)

    print("   霍夫曼编码:")
    for char, code in sorted(codes2.items()):
        print(f"     '{char}': {code}")

    # 编码和解码
    encoded2 = huffman_encode(text2, codes2)
    decoded2 = huffman_decode(encoded2, root2)
    compression_ratio2 = calculate_compression_ratio(text2, encoded2)

    print(f"\n   编码结果: {encoded2}")
    print(f"   解码结果: '{decoded2}'")
    print(f"   压缩率: {compression_ratio2:.1f}%")
    print(f"   正确性: {'✓' if decoded2 == text2 else '✗'}\n")

    # 示例3：极端情况 - 所有字符相同
    print("3. 极端情况测试（所有字符相同）:")
    text3 = "aaaaaa"
    char_freq3 = defaultdict(int)
    for char in text3:
        char_freq3[char] += 1

    root3 = build_huffman_tree(char_freq3)
    codes3 = generate_huffman_codes(root3)
    encoded3 = huffman_encode(text3, codes3)
    decoded3 = huffman_decode(encoded3, root3)

    print(f"   原始文本: '{text3}'")
    print(f"   编码: {codes3}")
    print(f"   编码结果: {encoded3}")
    print(f"   解码结果: '{decoded3}'")
    print(f"   正确性: {'✓' if decoded3 == text3 else '✗'}")


if __name__ == "__main__":
    main()