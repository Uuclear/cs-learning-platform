# 为电商系统设计索引

## 难度：⭐⭐⭐

## 描述

你是一家大型电商平台的数据库工程师。平台有数百万用户和商品，每天处理数十万订单。随着业务增长，数据库查询性能开始下降，特别是在以下场景：

1. **用户订单查询**：用户查看自己的订单历史，按时间倒序排列
2. **商品搜索**：用户按分类、价格范围、品牌等条件筛选商品
3. **管理员报表**：生成各种统计报表，如按状态分组的订单数量、热门商品排行等
4. **实时库存查询**：检查特定商品的库存状态

## 表结构

```sql
-- 用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP,
    last_login TIMESTAMP
);

-- 商品表
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name VARCHAR(200),
    brand VARCHAR(100),
    category_id BIGINT,
    price DECIMAL(10,2),
    stock_quantity INT,
    rating DECIMAL(2,1),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 分类表
CREATE TABLE categories (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    parent_id BIGINT,
    level INT
);

-- 订单表
CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    status VARCHAR(20), -- 'pending', 'paid', 'shipped', 'delivered', 'cancelled'
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    payment_method VARCHAR(20)
);

-- 订单商品表
CREATE TABLE order_items (
    id BIGINT PRIMARY KEY,
    order_id BIGINT,
    product_id BIGINT,
    quantity INT,
    price DECIMAL(10,2)
);
```

## 要求

1. **分析查询模式**：列出至少8种典型的查询场景
2. **设计索引策略**：为每个表设计最优的索引（包括复合索引）
3. **考虑覆盖索引**：识别可以使用覆盖索引的查询场景
4. **权衡读写性能**：考虑到电商系统写操作相对较少，但查询非常频繁
5. **提供SQL语句**：写出创建所有推荐索引的SQL语句

## 提示

- 使用`EXPLAIN`或`EXPLAIN QUERY PLAN`来验证索引使用情况
- 考虑复合索引的列顺序（高选择性列在前，排序列在后）
- 对于范围查询，注意最左前缀原则的限制
- 考虑是否需要函数索引（如日期函数）
- 监控实际的查询性能，而不仅仅是理论分析

## 扩展挑战（可选）

- 如何处理全文搜索需求（商品名称、描述搜索）？
- 如果引入缓存层，索引策略是否需要调整？
- 如何监控和维护索引的健康状态？