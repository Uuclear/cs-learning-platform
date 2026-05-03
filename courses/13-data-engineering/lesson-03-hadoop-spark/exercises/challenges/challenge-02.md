# 挑战 2: 实现简化版的 Spark DataFrame

⭐⭐⭐⭐ 难度 | 预计时间：30分钟

## 背景
Spark DataFrame 是 Spark SQL 的核心抽象，提供了类似 SQL 的操作接口。你需要实现一个简化的 DataFrame 类，支持基本的数据操作。

## 要求
1. 创建一个名为 `simple_dataframe.py` 的文件
2. 实现 `SimpleDataFrame` 类，构造函数接受一个字典列表作为数据：
   ```python
   data = [
       {"name": "Alice", "age": 25, "city": "Beijing"},
       {"name": "Bob", "age": 30, "city": "Shanghai"},
       {"name": "Charlie", "age": 35, "city": "Beijing"}
   ]
   df = SimpleDataFrame(data)
   ```
3. 实现以下方法：
   - `select(*columns)`: 选择指定列，返回新的 DataFrame
   - `filter(condition_func)`: 根据条件函数过滤行，返回新的 DataFrame
   - `group_by(column)`: 按指定列分组，返回 GroupBy 对象
   - `count()`: 返回行数（行动操作）
   - `collect()`: 返回所有数据（行动操作）

4. 实现 `GroupBy` 类，支持：
   - `count()`: 返回每个分组的计数
   - `avg(column)`: 返回指定列的平均值
   - `sum(column)`: 返回指定列的总和

5. 所有转换操作（select, filter, group_by）必须是惰性求值的
6. 行动操作（count, collect）必须触发实际计算
7. 添加完整的中文注释说明设计思路和实现细节

## 示例用法
```python
# 创建 DataFrame
df = SimpleDataFrame(data)

# 链式操作
result = (df
    .filter(lambda row: row["age"] > 25)
    .select("name", "city")
    .collect())

# 分组聚合
city_counts = df.group_by("city").count()
```

## 验证标准
- 代码结构清晰，符合面向对象设计原则
- 惰性求值机制正确实现
- 所有方法都能正确处理边界情况（空数据、无效列名等）
- 包含详细的中文注释和文档字符串
- 时间和空间复杂度合理