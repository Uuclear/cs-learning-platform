# 实现TF-IDF文本相似度计算

## 难度：⭐⭐⭐

## 任务描述

在这个挑战中，你需要实现一个完整的TF-IDF文本相似度计算系统。你的实现应该能够：

1. 接受多个文档作为输入
2. 构建词汇表并计算每个文档的TF-IDF向量
3. 计算任意两个文档之间的余弦相似度
4. 找出与给定查询文档最相似的文档

## 具体要求

### 输入格式
- 文档集合：一个字符串列表，每个字符串代表一个文档
- 查询文档：一个字符串

### 输出格式
- 相似度矩阵：显示所有文档对之间的相似度
- 最相似文档：返回与查询文档最相似的文档及其相似度分数

### 实现细节

你需要实现以下函数：

```python
def calculate_tf(doc_tokens: List[str]) -> Dict[str, float]:
    """计算词频"""
    pass

def calculate_idf(documents: List[List[str]]) -> Dict[str, float]:
    """计算逆文档频率"""
    pass

def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    """计算余弦相似度"""
    pass

def find_most_similar_document(documents: List[str], query: str) -> Tuple[str, float]:
    """找出与查询最相似的文档"""
    pass
```

## 测试用例

使用以下文档集合进行测试：

```python
documents = [
    "机器学习是人工智能的重要分支",
    "深度学习使用神经网络进行模式识别", 
    "自然语言处理让计算机理解人类语言",
    "机器学习算法可以从数据中学习规律",
    "人工智能包含机器学习和深度学习"
]
```

查询文档："机器学习和人工智能的关系"

## 提示

- 注意处理中文分词（可以简单按空格分割）
- 确保正确实现TF和IDF的计算公式
- 余弦相似度的范围应该是[0, 1]
- 考虑边界情况（如空文档、未登录词等）

## 扩展挑战（可选）

- 实现向量化的TF-IDF表示（使用numpy数组而不是字典）
- 添加文档长度归一化
- 支持不同的相似度度量方法（如欧氏距离、Jaccard相似度等）