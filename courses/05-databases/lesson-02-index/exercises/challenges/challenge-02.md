# 挑战2: 索引失效侦探

## 背景
你的团队发现一个原本很快的查询突然变慢了。经过初步调查，发现是某个开发人员修改了查询语句，导致索引失效。

## 任务
1. 创建一个`users`表，包含以下字段：
   - id (INTEGER, 主键)
   - username (TEXT)
   - email (TEXT)
   - phone (TEXT)
   - created_at (TEXT)  -- 格式: 'YYYY-MM-DD HH:MM:SS'
   - last_login (TEXT)  -- 格式: 'YYYY-MM-DD HH:MM:SS'

2. 为email和created_at字段创建索引

3. 创建5个会导致索引失效的查询示例，并解释为什么失效

4. 为每个失效的查询提供优化方案

5. 实现一个工具函数，能够自动检测SQL查询中可能导致索引失效的模式

## 具体要求
- 至少演示5种不同的索引失效场景（函数使用、类型转换、LIKE通配符等）
- 每种场景都要有对应的优化方案
- 工具函数应该能识别常见的索引失效模式
- 使用EXPLAIN验证优化前后的效果

## 示例场景
- `WHERE UPPER(username) = 'JOHN'`
- `WHERE created_at LIKE '%2026%'`
- `WHERE email = 12345` (email是TEXT类型)
- `WHERE SUBSTR(phone, 1, 3) = '123'`
- `WHERE created_at + 86400 > '2026-05-03'`

## 评分标准
- 索引失效场景的多样性（30%）
- 优化方案的有效性（30%）
- 自动检测工具的实用性（25%）
- 代码质量和文档（15%）