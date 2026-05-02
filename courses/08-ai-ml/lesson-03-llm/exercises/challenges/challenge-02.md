# 用大模型构建文本分类器

**难度**: ⭐⭐⭐⭐

## 描述

在这个挑战中，你需要构建一个完整的文本分类系统，利用预训练的大语言模型（LLM）或Transformer模型来对文本进行分类。文本分类是NLP中最基础也是最重要的任务之一，广泛应用于情感分析、垃圾邮件检测、新闻分类等场景。

你需要设计一个系统，能够处理中文文本，并在给定的分类任务上达到良好的性能。

## 要求

### 基本要求
1. 实现一个`TextClassifier`类，包含以下方法：
   - `__init__(self, model_name=None)`: 初始化分类器，可选择预训练模型
   - `prepare_data(self, texts, labels)`: 数据预处理和准备
   - `train(self, train_texts, train_labels, val_texts=None, val_labels=None)`: 训练分类器
   - `predict(self, texts)`: 对新文本进行预测
   - `evaluate(self, test_texts, test_labels)`: 评估模型性能

2. 支持至少两种分类任务（如情感分析、主题分类）
3. 处理中文文本，考虑中文分词和编码问题
4. 提供清晰的训练和预测接口

### 进阶要求（可选）
1. 实现few-shot learning支持，仅用少量样本进行分类
2. 添加模型微调（fine-tuning）功能
3. 实现模型集成（ensemble）提高准确性
4. 添加可视化功能展示分类结果和置信度

## 提示

### 技术选择
- **使用HuggingFace Transformers**: 可以直接加载预训练的中文BERT、RoBERTa等模型
- **特征提取方法**: 
  - 直接使用[CLS] token的表示
  - 对所有token的表示进行平均池化
  - 使用专门的分类头进行微调

### 数据预处理
```python
from transformers import AutoTokenizer

# 中文分词器
tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")

# 编码文本
encoded = tokenizer(
    texts,
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt"
)
```

### 模型架构
```python
from transformers import AutoModel
import torch.nn as nn

class TextClassifier(nn.Module):
    def __init__(self, model_name, num_classes):
        super().__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_classes)
    
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output  # [CLS] token representation
        output = self.dropout(pooled_output)
        return self.classifier(output)
```

### 测试数据集
你可以使用以下公开的中文数据集：
- **ChnSentiCorp**: 中文情感分析数据集
- **THUCNews**: 中文新闻分类数据集
- **自定义数据**: 创建简单的正面/负面情感标注数据

## 评估标准

- ✅ 正确实现文本分类pipeline
- ✅ 支持中文文本处理
- ✅ 提供清晰的API接口
- ✅ 在测试数据上达到合理准确率（>70%）
- 🌟 实现模型微调功能
- 🌟 支持few-shot learning
- 🌟 包含完整的文档和使用示例