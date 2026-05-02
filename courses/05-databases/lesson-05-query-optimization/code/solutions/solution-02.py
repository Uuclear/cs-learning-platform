#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: 简单查询优化器

本脚本实现了一个简单的查询优化器，能够为给定的查询选择最佳执行计划。
虽然简化了很多细节，但展示了查询优化器的核心概念。
"""

import sqlite3
import time
import random
import math
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class JoinAlgorithm(Enum):
    """连接算法类型"""
    NESTED_LOOP = "nested_loop"
    INDEX_JOIN = "index_join"
    HASH_JOIN = "hash_join"


@dataclass
class TableStats:
    """表统计信息"""
    table_name: str
    row_count: int
    columns: Dict[str, 'ColumnStats']


@dataclass
class ColumnStats:
    """列统计信息"""
    column_name: str
    distinct_values: int
    min_value: Any
    max_value: Any
    histogram: Optional[List[int]] = None


@dataclass
class QueryPlan:
    """查询计划"""
    plan_id: str
    operations: List[str]
    estimated_cost: float
    join_algorithm: Optional[JoinAlgorithm] = None


class SimpleQueryOptimizer:
    """简单查询优化器"""

    def __init__(self, db_connection: sqlite3.Connection):
        self.conn = db_connection
        self.cursor = db_connection.cursor()
        self.table_stats: Dict[str, TableStats] = {}
        self._collect_statistics()

    def _collect_statistics(self) -> None:
        """收集表和列的统计信息"""
        # 获取所有表名
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.cursor.fetchall()]

        for table in tables:
            # 获取行数
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = self.cursor.fetchone()[0]

            # 获取列信息
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns_info = self.cursor.fetchall()
            columns = {}

            for col_info in columns_info:
                col_name = col_info[1]
                # 获取唯一值数量（简化版）
                self.cursor.execute(f"SELECT COUNT(DISTINCT {col_name}) FROM {table}")
                distinct_count = self.cursor.fetchone()[0] or 1

                # 获取最小/最大值（仅对数值列）
                try:
                    self.cursor.execute(f"SELECT MIN({col_name}), MAX({col_name}) FROM {table}")
                    min_val, max_val = self.cursor.fetchone()
                except:
                    min_val, max_val = None, None

                columns[col_name] = ColumnStats(
                    column_name=col_name,
                    distinct_values=distinct_count,
                    min_value=min_val,
                    max_value=max_val
                )

            self.table_stats[table] = TableStats(
                table_name=table,
                row_count=row_count,
                columns=columns
            )

    def estimate_selectivity(self, table_name: str, condition: str) -> float:
        """估算选择性（返回行数占总行数的比例）"""
        if table_name not in self.table_stats:
            return 0.1  # 默认选择性

        stats = self.table_stats[table_name]
        total_rows = stats.row_count

        # 简化的选择性估算
        if '=' in condition:
            # 等值查询 - 假设均匀分布
            col_name = condition.split('=')[0].strip()
            if col_name in stats.columns:
                distinct_vals = stats.columns[col_name].distinct_values
                return 1.0 / max(distinct_vals, 1)
        elif 'BETWEEN' in condition or ('>' in condition or '<' in condition):
            # 范围查询 - 粗略估算为 30%
            return 0.3
        elif 'LIKE' in condition:
            if condition.endswith("'%"):
                # 前缀匹配 - 估算为 10%
                return 0.1
            else:
                # 通配符开头 - 全表扫描
                return 1.0

        return 0.1  # 默认选择性

    def calculate_table_scan_cost(self, table_name: str) -> float:
        """计算全表扫描成本"""
        if table_name not in self.table_stats:
            return 1000.0

        stats = self.table_stats[table_name]
        # 成本与行数成正比
        return stats.row_count * 0.1

    def calculate_index_scan_cost(self, table_name: str, index_selectivity: float) -> float:
        """计算索引扫描成本"""
        if table_name not in self.table_stats:
            return 500.0

        stats = self.table_stats[table_name]
        # 索引查找成本 + 回表成本
        lookup_cost = math.log2(max(stats.row_count, 1)) * 2
        rows_to_fetch = stats.row_count * index_selectivity
        fetch_cost = rows_to_fetch * 0.5
        return lookup_cost + fetch_cost

    def calculate_join_cost(self, left_table: str, right_table: str,
                           join_condition: str, algorithm: JoinAlgorithm) -> float:
        """计算连接操作成本"""
        if left_table not in self.table_stats or right_table not in self.table_stats:
            return 10000.0

        left_stats = self.table_stats[left_table]
        right_stats = self.table_stats[right_table]

        if algorithm == JoinAlgorithm.NESTED_LOOP:
            # 嵌套循环: 外表每行都要扫描内表
            return left_stats.row_count * self.calculate_table_scan_cost(right_table)
        elif algorithm == JoinAlgorithm.INDEX_JOIN:
            # 索引连接: 外表每行通过索引查找内表
            selectivity = self.estimate_selectivity(right_table, join_condition)
            return left_stats.row_count * self.calculate_index_scan_cost(right_table, selectivity)
        elif algorithm == JoinAlgorithm.HASH_JOIN:
            # 哈希连接: 构建哈希表 + 探测
            build_cost = right_stats.row_count * 0.3
            probe_cost = left_stats.row_count * 0.2
            return build_cost + probe_cost

        return 10000.0

    def generate_single_table_plans(self, table_name: str, where_clause: str = "") -> List[QueryPlan]:
        """为单表查询生成执行计划"""
        plans = []

        # 计划 1: 全表扫描
        scan_cost = self.calculate_table_scan_cost(table_name)
        if where_clause:
            selectivity = self.estimate_selectivity(table_name, where_clause)
            scan_cost *= selectivity
        plans.append(QueryPlan(
            plan_id=f"{table_name}_scan",
            operations=[f"SCAN TABLE {table_name}"],
            estimated_cost=scan_cost
        ))

        # 计划 2: 索引扫描（如果有合适的索引）
        # 这里简化处理 - 假设有索引可用
        if where_clause and "=" in where_clause:
            col_name = where_clause.split("=")[0].strip()
            # 检查是否有索引（简化 - 假设有）
            index_cost = self.calculate_index_scan_cost(table_name,
                                                      self.estimate_selectivity(table_name, where_clause))
            plans.append(QueryPlan(
                plan_id=f"{table_name}_index",
                operations=[f"SEARCH TABLE {table_name} USING INDEX idx_{table_name}_{col_name}"],
                estimated_cost=index_cost
            ))

        return plans

    def generate_join_plans(self, tables: List[str], join_conditions: List[str]) -> List[QueryPlan]:
        """为多表连接生成执行计划"""
        if len(tables) != 2:
            return []  # 简化处理，只支持两表连接

        left_table, right_table = tables
        join_condition = join_conditions[0] if join_conditions else ""

        plans = []

        # 尝试不同的连接算法
        for algorithm in JoinAlgorithm:
            cost = self.calculate_join_cost(left_table, right_table, join_condition, algorithm)
            operations = [
                f"JOIN {left_table} AND {right_table}",
                f"USING {algorithm.value.upper()} JOIN"
            ]
            plans.append(QueryPlan(
                plan_id=f"{left_table}_{right_table}_{algorithm.value}",
                operations=operations,
                estimated_cost=cost,
                join_algorithm=algorithm
            ))

        return plans

    def choose_best_plan(self, query_type: str, **kwargs) -> QueryPlan:
        """选择最佳执行计划"""
        if query_type == "single_table":
            plans = self.generate_single_table_plans(kwargs['table_name'], kwargs.get('where_clause', ''))
        elif query_type == "join":
            plans = self.generate_join_plans(kwargs['tables'], kwargs.get('join_conditions', []))
        else:
            raise ValueError(f"Unsupported query type: {query_type}")

        if not plans:
            raise ValueError("No plans generated")

        # 选择成本最低的计划
        best_plan = min(plans, key=lambda p: p.estimated_cost)
        return best_plan

    def optimize_query(self, sql_query: str) -> QueryPlan:
        """优化 SQL 查询并返回最佳执行计划"""
        # 简化的 SQL 解析
        sql_lower = sql_query.lower().strip()

        if 'join' in sql_lower:
            # 处理 JOIN 查询
            # 提取表名（简化）
            from_pos = sql_lower.find('from')
            join_pos = sql_lower.find('join')
            where_pos = sql_lower.find('where')

            if from_pos != -1 and join_pos != -1:
                # 提取两个表名
                from_part = sql_query[from_pos+4:join_pos].strip()
                join_part = sql_query[join_pos+4:where_pos if where_pos != -1 else len(sql_query)].strip()

                # 简化：假设表名是第一个单词
                table1 = from_part.split()[0]
                table2 = join_part.split()[0]

                # 提取 JOIN 条件（简化）
                on_pos = sql_lower.find('on')
                if on_pos != -1:
                    join_cond = sql_query[on_pos+2:where_pos if where_pos != -1 else len(sql_query)].strip()
                    join_conditions = [join_cond]
                else:
                    join_conditions = []

                return self.choose_best_plan("join", tables=[table1, table2], join_conditions=join_conditions)

        else:
            # 处理单表查询
            from_pos = sql_lower.find('from')
            where_pos = sql_lower.find('where')

            if from_pos != -1:
                table_part = sql_query[from_pos+4:where_pos if where_pos != -1 else len(sql_query)].strip()
                table_name = table_part.split()[0]
                where_clause = sql_query[where_pos+5:].strip() if where_pos != -1 else ""
                return self.choose_best_plan("single_table", table_name=table_name, where_clause=where_clause)

        # 默认返回一个简单计划
        return QueryPlan(
            plan_id="default",
            operations=["UNKNOWN QUERY PATTERN"],
            estimated_cost=1000.0
        )


def demonstrate_simple_optimizer():
    """演示简单查询优化器"""
    print("🧠 解决方案 2: 简单查询优化器")
    print("=" * 60)

    # 创建测试数据库
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # 创建测试表
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            age INTEGER,
            city TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            status TEXT
        )
    """)

    # 插入测试数据
    users_data = [(i, f"user{i}", f"user{i}@example.com", i % 60 + 18, f"city{i%10}") for i in range(1000)]
    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users_data)

    orders_data = [(i, i % 1000, i * 10.5, ["pending", "shipped", "delivered"][i % 3]) for i in range(5000)]
    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders_data)

    conn.commit()

    # 创建索引
    cursor.execute("CREATE INDEX idx_users_email ON users(email)")
    cursor.execute("CREATE INDEX idx_orders_user_id ON orders(user_id)")

    # 初始化优化器
    optimizer = SimpleQueryOptimizer(conn)

    # 测试查询
    test_queries = [
        "SELECT * FROM users WHERE email = 'user123@example.com'",
        "SELECT * FROM users WHERE age > 30",
        "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id WHERE o.status = 'delivered'"
    ]

    for query in test_queries:
        print(f"\n🔍 查询: {query}")
        best_plan = optimizer.optimize_query(query)
        print(f"最佳执行计划: {best_plan.plan_id}")
        print(f"估算成本: {best_plan.estimated_cost:.2f}")
        print("执行步骤:")
        for op in best_plan.operations:
            print(f"  - {op}")

        # 实际执行时间对比
        start_time = time.time()
        cursor.execute(query)
        cursor.fetchall()
        actual_time = (time.time() - start_time) * 1000
        print(f"实际执行时间: {actual_time:.2f} ms")

    print("\n💡 优化器说明:")
    print("- 这是一个简化的查询优化器，展示了核心概念")
    print("- 实际数据库优化器要复杂得多，考虑更多因素")
    print("- 成本模型基于统计信息和启发式规则")
    print("- 优化器的目标是找到成本最低的执行计划")
    print("- 统计信息的准确性对优化效果至关重要")

    conn.close()


if __name__ == "__main__":
    demonstrate_simple_optimizer()