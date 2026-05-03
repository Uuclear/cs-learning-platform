#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：列式存储概念演示

本示例演示列式存储与行式存储的概念差异，并展示查询性能对比。
虽然SQLite是行式存储，但我们可以通过Python数据结构模拟列式存储的优势。
"""

import time
import random
from collections import defaultdict

class RowStore:
    """行式存储模拟"""
    def __init__(self):
        self.data = []  # 存储为列表的列表 [[id, name, age, salary], ...]

    def insert(self, record):
        """插入记录"""
        self.data.append(record)

    def query_by_column(self, column_index, condition_func):
        """按列查询（模拟分析查询）"""
        results = []
        for row in self.data:
            if condition_func(row[column_index]):
                results.append(row)
        return results

    def aggregate_column(self, column_index, agg_func):
        """聚合指定列"""
        values = [row[column_index] for row in self.data]
        return agg_func(values)

class ColumnStore:
    """列式存储模拟"""
    def __init__(self):
        self.columns = defaultdict(list)  # 存储为字典的列表 {'id': [1,2,3...], 'name': [...]}
        self.column_names = []

    def set_schema(self, column_names):
        """设置列名"""
        self.column_names = column_names
        for name in column_names:
            self.columns[name] = []

    def insert(self, record):
        """插入记录"""
        for i, value in enumerate(record):
            self.columns[self.column_names[i]].append(value)

    def query_by_column(self, column_name, condition_func):
        """按列查询（高效！）"""
        target_column = self.columns[column_name]
        matching_indices = []
        for i, value in enumerate(target_column):
            if condition_func(value):
                matching_indices.append(i)

        # 只返回需要的列数据
        return matching_indices

    def aggregate_column(self, column_name, agg_func):
        """聚合指定列（高效！）"""
        return agg_func(self.columns[column_name])

def generate_test_data(n_records=100000):
    """生成测试数据"""
    data = []
    names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十']
    departments = ['销售部', '技术部', '市场部', '人事部', '财务部']

    for i in range(n_records):
        record = [
            i + 1,  # id
            random.choice(names),  # name
            random.randint(20, 60),  # age
            random.choice(departments),  # department
            round(random.uniform(3000, 20000), 2)  # salary
        ]
        data.append(record)

    return data

def performance_comparison():
    """性能对比测试"""
    print("=== 列式存储 vs 行式存储性能对比 ===\n")

    # 生成测试数据
    test_data = generate_test_data(50000)
    print(f"生成 {len(test_data)} 条测试记录")

    # 测试行式存储
    print("1. 行式存储测试:")
    row_store = RowStore()

    # 插入数据
    start_time = time.time()
    for record in test_data:
        row_store.insert(record)
    insert_time_row = time.time() - start_time
    print(f"   插入耗时: {insert_time_row * 1000:.2f} 毫秒")

    # 聚合查询：计算平均工资
    start_time = time.time()
    avg_salary_row = row_store.aggregate_column(4, lambda x: sum(x) / len(x))
    query_time_row = time.time() - start_time
    print(f"   平均工资查询耗时: {query_time_row * 1000:.2f} 毫秒")
    print(f"   平均工资: ¥{avg_salary_row:.2f}")

    # 测试列式存储
    print("\n2. 列式存储测试:")
    column_store = ColumnStore()
    column_store.set_schema(['id', 'name', 'age', 'department', 'salary'])

    # 插入数据
    start_time = time.time()
    for record in test_data:
        column_store.insert(record)
    insert_time_col = time.time() - start_time
    print(f"   插入耗时: {insert_time_col * 1000:.2f} 毫秒")

    # 聚合查询：计算平均工资
    start_time = time.time()
    avg_salary_col = column_store.aggregate_column('salary', lambda x: sum(x) / len(x))
    query_time_col = time.time() - start_time
    print(f"   平均工资查询耗时: {query_time_col * 1000:.2f} 毫秒")
    print(f"   平均工资: ¥{avg_salary_col:.2f}")

    # 性能对比
    print("\n=== 性能对比总结 ===")
    print(f"插入性能: 行式 {insert_time_row*1000:.2f}ms vs 列式 {insert_time_col*1000:.2f}ms")
    print(f"查询性能: 行式 {query_time_row*1000:.2f}ms vs 列式 {query_time_col*1000:.2f}ms")

    if query_time_col > 0:
        speedup = query_time_row / query_time_col
        print(f"查询加速比: {speedup:.2f}x")

    print("\n列式存储优势说明:")
    print("- 分析查询通常只访问少数列，减少I/O")
    print("- 同一列数据类型相同，压缩效率高")
    print("- CPU缓存友好，向量化计算更高效")
    print("- 适合OLAP场景，不适合OLTP场景")

def main():
    """主函数"""
    print("列式存储概念演示")
    print("=" * 30)

    performance_comparison()

    print("\n实际应用:")
    print("现代数据仓库如Apache Parquet、Amazon Redshift、Google BigQuery")
    print("都采用列式存储来优化分析查询性能。")

if __name__ == "__main__":
    main()