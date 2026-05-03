#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命名实体识别实现：基于规则和词典查找的方法

本解决方案实现了简单的命名实体识别，使用预定义的实体词典
和基于模式的规则来识别文本中的人名、地名、组织名等实体。
"""

import re
from typing import List, Dict, Tuple, Set


class RuleBasedNER:
    """基于规则的命名实体识别器"""

    def __init__(self):
        # 预定义的实体词典（简化版）
        self.entity_dictionaries = {
            'PERSON': {
                '张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
                '李白', '杜甫', '苏轼', '鲁迅', '毛泽东', '邓小平', '习近平'
            },
            'LOCATION': {
                '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都',
                '中国', '美国', '日本', '韩国', '英国', '法国', '德国', '俄罗斯',
                '北京大学', '清华大学', '复旦大学', '浙江大学'
            },
            'ORGANIZATION': {
                '谷歌', '微软', '苹果', '阿里巴巴', '腾讯', '百度', '华为', '小米',
                '联合国', '世界银行', '国际货币基金组织', '世界卫生组织',
                '中国共产党', '中国政府', '美国政府', '欧盟'
            }
        }

        # 实体类型到标签的映射
        self.label_mapping = {
            'PERSON': 'PER',
            'LOCATION': 'LOC',
            'ORGANIZATION': 'ORG'
        }

        # 构建反向索引以加速查找
        self.word_to_entities = {}
        for entity_type, words in self.entity_dictionaries.items():
            for word in words:
                if word not in self.word_to_entities:
                    self.word_to_entities[word] = set()
                self.word_to_entities[word].add(entity_type)

    def find_entities_in_text(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        在文本中查找命名实体

        Args:
            text: 输入文本

        Returns:
            实体列表 [(实体文本, 实体类型, 起始位置, 结束位置), ...]
        """
        entities = []
        found_positions = set()  # 避免重复标记

        # 按长度降序排列词汇（优先匹配长词）
        all_words = sorted(self.word_to_entities.keys(), key=len, reverse=True)

        for word in all_words:
            start = 0
            while True:
                pos = text.find(word, start)
                if pos == -1:
                    break

                # 检查是否已被标记
                overlap = False
                for i in range(pos, pos + len(word)):
                    if i in found_positions:
                        overlap = True
                        break

                if not overlap:
                    # 找到实体
                    entity_types = self.word_to_entities[word]
                    for entity_type in entity_types:
                        entities.append((
                            word,
                            self.label_mapping[entity_type],
                            pos,
                            pos + len(word)
                        ))
                        # 标记已占用的位置
                        for i in range(pos, pos + len(word)):
                            found_positions.add(i)
                    break  # 找到最长匹配就停止

                start = pos + 1

        # 基于模式的规则（识别日期、数字等）
        entities.extend(self._find_pattern_entities(text, found_positions))

        # 按位置排序
        entities.sort(key=lambda x: x[2])

        return entities

    def _find_pattern_entities(self, text: str, occupied_positions: Set[int]) -> List[Tuple[str, str, int, int]]:
        """基于正则表达式的模式匹配"""
        pattern_entities = []

        # 日期模式 (YYYY-MM-DD, YYYY/MM/DD, YYYY年MM月DD日)
        date_patterns = [
            (r'\d{4}-\d{1,2}-\d{1,2}', 'DATE'),
            (r'\d{4}/\d{1,2}/\d{1,2}', 'DATE'),
            (r'\d{4}年\d{1,2}月\d{1,2}日', 'DATE')
        ]

        # 数字模式
        number_pattern = (r'\d+(?:\.\d+)?', 'NUMBER')

        all_patterns = date_patterns + [number_pattern]

        for pattern, entity_type in all_patterns:
            for match in re.finditer(pattern, text):
                start, end = match.span()
                # 检查是否与已有实体重叠
                overlap = False
                for i in range(start, end):
                    if i in occupied_positions:
                        overlap = True
                        break

                if not overlap:
                    pattern_entities.append((
                        match.group(),
                        entity_type,
                        start,
                        end
                    ))
                    # 标记位置
                    for i in range(start, end):
                        occupied_positions.add(i)

        return pattern_entities

    def annotate_text(self, text: str) -> str:
        """
        为文本添加实体标注

        Args:
            text: 输入文本

        Returns:
            带有实体标注的文本
        """
        entities = self.find_entities_in_text(text)
        if not entities:
            return text

        # 从后往前插入标注，避免位置偏移
        annotated_text = text
        offset = 0

        for entity_text, entity_type, start, end in reversed(entities):
            annotated_start = start + offset
            annotated_end = end + offset
            annotated_text = (
                annotated_text[:annotated_start] +
                f"[{entity_text}]({entity_type})" +
                annotated_text[annotated_end:]
            )
            offset += len(f"[{entity_text}]({entity_type})") - len(entity_text)

        return annotated_text


def create_ner_system() -> RuleBasedNER:
    """创建NER系统"""
    return RuleBasedNER()


if __name__ == "__main__":
    print("=== 命名实体识别演示 ===")

    # 创建NER系统
    ner = create_ner_system()

    # 测试文本
    test_texts = [
        "张三在北京的谷歌公司工作",
        "李四是清华大学的学生，他住在杭州",
        "联合国在2023年发布了重要报告",
        "习近平主席访问了美国和法国",
        "阿里巴巴集团成立于1999年"
    ]

    print("\n=== 实体识别结果 ===")
    for text in test_texts:
        entities = ner.find_entities_in_text(text)
        annotated = ner.annotate_text(text)

        print(f"原文: {text}")
        print(f"实体: {entities}")
        print(f"标注: {annotated}")
        print("-" * 50)