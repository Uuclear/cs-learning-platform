# 挑战 01：实现模型版本比较工具 ⭐⭐⭐

## 背景
你已经学习了基本的模型版本控制概念。现在需要构建一个更实用的工具来帮助数据科学家比较不同模型版本的性能。

## 任务要求
1. 扩展 `ModelRegistry` 类，添加以下功能：
   - 支持按时间范围查询模型版本（例如：过去7天的所有版本）
   - 实现模型版本的 A/B 测试比较功能
   - 添加导出功能，将比较结果保存为 CSV 格式

2. 创建一个命令行界面，支持以下操作：
   ```bash
   # 列出指定模型的所有版本
   python model_compare.py list --model-id sentiment_classifier
   
   # 比较两个特定版本
   python model_compare.py compare --model-id sentiment_classifier --versions v1.0 v2.0
   
   # 导出最近30天的所有版本到CSV
   python model_compare.py export --model-id sentiment_classifier --days 30 --output results.csv
   ```

## 提示
- 使用 `argparse` 模块处理命令行参数
- 时间范围查询需要解析 `timestamp` 字段
- CSV 导出应包含所有相关字段：版本、指标、参数、时间戳等
- 确保代码有适当的错误处理和用户友好的错误消息

## 验证标准
- 所有功能都能正常工作
- 代码包含完整的中文注释
- 命令行界面直观易用
- 处理边界情况（如模型不存在、版本不存在等）