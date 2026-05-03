# 挑战 02：构建数据质量监控框架

## 背景
你的公司正在构建一个金融数据分析平台，需要处理来自多个数据源的敏感财务数据。数据质量对业务决策至关重要，任何质量问题都可能导致重大的财务损失或合规风险。

当前的数据质量问题包括：
- 客户收入数据中存在负值和异常高值
- 交易日期格式不一致（有些是ISO格式，有些是MM/DD/YYYY格式）
- 产品分类信息缺失率高达30%
- 实时交易数据延迟超过15分钟
- 不同系统中的同一客户ID对应不同的基本信息

## 任务
使用Python标准库开发一个可扩展的数据质量监控框架。你的框架应该能够：

### 1. 数据质量维度实现
- **完整性检查**：验证必需字段是否存在且非空，计算缺失率
- **准确性检查**：实现多种验证规则（数值范围、日期格式、邮箱格式、自定义正则表达式等）
- **一致性检查**：检测同一实体在不同记录中的信息是否一致
- **及时性检查**：验证数据是否在预期时间窗口内到达

### 2. 框架设计要求
- 使用面向对象设计，确保代码可扩展和可维护
- 支持配置驱动的质量规则定义（可以使用字典或JSON格式）
- 提供详细的错误报告，包括问题位置、类型和建议修复方案
- 实现质量评分机制，为每个数据集生成综合质量分数
- 支持批量处理和单条记录处理两种模式

### 3. 具体实现
创建以下组件：
- `DataQualityChecker` 主类，负责协调各种检查
- `CompletenessChecker`、`AccuracyChecker`、`ConsistencyChecker`、`TimelinessChecker` 四个专门的检查器类
- `QualityReport` 类，用于生成和格式化质量报告
- 配置解析器，能够从字典配置中加载质量规则

### 4. 测试用例
使用提供的示例数据测试你的框架：
```python
test_data = [
    {"customer_id": "C001", "income": 50000, "transaction_date": "2023-05-01", "product_category": "Electronics"},
    {"customer_id": "C002", "income": -1000, "transaction_date": "05/02/2023", "product_category": None},
    {"customer_id": "C001", "income": 75000, "transaction_date": "2023-05-03", "product_category": "Electronics"}
]
```

配置示例：
```python
config = {
    "required_fields": ["customer_id", "income", "transaction_date"],
    "validation_rules": {
        "income": {"type": "range", "min": 0, "max": 1000000},
        "transaction_date": {"type": "date_format", "formats": ["%Y-%m-%d", "%m/%d/%Y"]},
        "product_category": {"type": "not_null"}
    },
    "consistency_fields": ["customer_id"],
    "timeliness_window_hours": 24
}
```

## 交付物
提交完整的Python代码实现，包括所有类和测试用例。代码必须包含详细的中文注释，说明每个组件的功能和使用方法。

## 评估标准
- 代码的正确性和完整性
- 架构设计的合理性和可扩展性
- 错误处理和边界情况的考虑
- 代码质量和注释质量
- 测试用例的覆盖度