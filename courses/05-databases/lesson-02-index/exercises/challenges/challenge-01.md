# 挑战1: 索引性能调优专家

## 背景
你是一家电商公司的数据库工程师，需要优化一个慢查询问题。用户反馈商品搜索功能非常慢，特别是按分类和价格范围筛选时。

## 任务
1. 创建一个`products`表，包含以下字段：
   - id (INTEGER, 主键)
   - name (TEXT)
   - category (TEXT) 
   - sub_category (TEXT)
   - price (REAL)
   - brand (TEXT)
   - created_at (TEXT)

2. 插入5000条测试数据（使用随机生成的数据）

3. 分析并解决以下查询的性能问题：
   ```sql
   SELECT * FROM products 
   WHERE category = 'electronics' 
     AND sub_category = 'smartphones'
     AND price BETWEEN 100 AND 1000
   ORDER BY price DESC
   LIMIT 20;
   ```

4. 使用EXPLAIN命令验证索引是否被正确使用

## 要求
- 实现完整的Python脚本
- 包含性能对比（有无索引）
- 使用合适的复合索引设计
- 在代码中添加详细的中文注释

## 评分标准
- 功能完整性（40%）
- 性能优化效果（30%）  
- 代码质量与注释（20%）
- EXPLAIN分析报告（10%）