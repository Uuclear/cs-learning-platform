# 挑战01：构建电商订单ETL管道 ⭐⭐⭐

## 背景
你是一家电商公司的数据工程师，需要为订单分析系统构建一个ETL管道。每天都有新的订单数据产生，需要定期处理并加载到数据仓库中。

## 任务要求

### 数据源格式
订单数据存储在CSV文件中，包含以下字段：
- `order_id`: 订单ID（字符串）
- `customer_id`: 客户ID（字符串）
- `order_date`: 订单日期（YYYY-MM-DD格式字符串）
- `total_amount`: 订单总金额（字符串，可能包含货币符号）
- `status`: 订单状态（"completed", "pending", "cancelled"）
- `items_count`: 商品数量（字符串）

### ETL要求

#### 提取阶段
- 从指定的CSV文件读取数据
- 处理文件不存在或格式错误的情况

#### 转换阶段
- 清洗数据：去除金额中的货币符号和逗号
- 验证必需字段（order_id, customer_id, total_amount）
- 将金额转换为浮点数，商品数量转换为整数
- 添加计算字段：`is_completed`（布尔值，基于status）
- 添加处理时间戳字段：`processed_at`

#### 加载阶段
- 将处理后的数据保存为JSON格式
- 实现基本的错误处理和日志记录

#### 质量检查
- 验证所有必需字段都存在且非空
- 验证金额和数量可以正确转换为数字
- 检查订单ID是否重复

## 输出
- 完整的Python脚本，包含中文注释
- 能够处理示例数据并生成正确的输出
- 包含基本的错误处理逻辑

## 示例数据
```csv
order_id,customer_id,order_date,total_amount,status,items_count
ORD001,CUST001,2026-05-01,$1,250.50,completed,3
ORD002,CUST002,2026-05-01,$899.99,pending,1
ORD003,CUST003,2026-05-02,$2,450.00,completed,5
```

## 提示
- 使用Python标准库（csv, json, datetime）
- 考虑数据类型转换的异常处理
- 实现简单的重复检测逻辑