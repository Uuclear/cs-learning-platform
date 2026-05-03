#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：简单OLAP查询引擎

实现一个支持ROLLUP和CUBE聚合的简单OLAP查询引擎。
使用SQLite作为后端，但通过Python逻辑实现高级聚合功能。
"""

import sqlite3
import itertools
from collections import defaultdict

class SimpleOLAPEngine:
    """简单的OLAP查询引擎"""

    def __init__(self, conn):
        self.conn = conn

    def create_sample_data(self):
        """创建示例销售数据"""
        cursor = self.conn.cursor()

        # 创建销售事实表
        cursor.execute('''
            CREATE TABLE sales (
                id INTEGER PRIMARY KEY,
                region TEXT NOT NULL,
                product_category TEXT NOT NULL,
                year INTEGER NOT NULL,
                quarter INTEGER NOT NULL,
                sales_amount REAL NOT NULL,
                units_sold INTEGER NOT NULL
            )
        ''')

        # 插入示例数据
        sample_data = [
            ('North', 'Electronics', 2023, 1, 150000, 120),
            ('North', 'Electronics', 2023, 2, 180000, 140),
            ('North', 'Clothing', 2023, 1, 80000, 200),
            ('North', 'Clothing', 2023, 2, 95000, 220),
            ('South', 'Electronics', 2023, 1, 120000, 95),
            ('South', 'Electronics', 2023, 2, 140000, 110),
            ('South', 'Clothing', 2023, 1, 60000, 150),
            ('South', 'Clothing', 2023, 2, 75000, 180),
        ]

        cursor.executemany('''
            INSERT INTO sales (region, product_category, year, quarter, sales_amount, units_sold)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_data)

        self.conn.commit()

    def execute_rollup(self, group_by_columns, aggregate_columns):
        """
        执行ROLLUP聚合

        ROLLUP生成从最详细到最汇总的所有可能组合
        例如：ROLLUP(region, category) 会生成：
        - (region, category)
        - (region, ALL)
        - (ALL, ALL)
        """
        print(f"=== ROLLUP 聚合: {group_by_columns} ===")

        # 获取所有可能的分组级别
        group_levels = []
        for i in range(len(group_by_columns), -1, -1):
            group_levels.append(group_by_columns[:i])

        all_results = []

        for level in group_levels:
            if not level:
                # 总计行
                sql = f"SELECT 'ALL' as dummy, SUM({aggregate_columns[0]}) as total"
                for agg_col in aggregate_columns[1:]:
                    sql += f", SUM({agg_col}) as {agg_col}"
                sql += " FROM sales"
                group_desc = "总计"
            else:
                # 分组查询
                select_clause = ", ".join(level)
                sql = f"SELECT {select_clause}, SUM({aggregate_columns[0]}) as total"
                for agg_col in aggregate_columns[1:]:
                    sql += f", SUM({agg_col}) as {agg_col}"
                sql += " FROM sales GROUP BY " + ", ".join(level)
                group_desc = " + ".join(level) if len(level) > 1 else level[0]

            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                if not level:
                    display_row = ["总计"] + list(row[1:])
                else:
                    # 将None值替换为'ALL'用于显示
                    display_values = []
                    for i, val in enumerate(row[:-len(aggregate_columns)]):
                        display_values.append(val if val is not None else 'ALL')
                    display_row = display_values + list(row[-len(aggregate_columns):])

                all_results.append((group_desc, display_row))

        # 显示结果
        headers = group_by_columns + aggregate_columns
        print(f"{'分组':<15} {' | '.join(headers)}")
        print("-" * 60)

        for group_desc, row in all_results:
            row_str = " | ".join(str(val) for val in row)
            print(f"{group_desc:<15} {row_str}")

        print()
        return all_results

    def execute_cube(self, group_by_columns, aggregate_columns):
        """
        执行CUBE聚合

        CUBE生成所有可能的分组组合
        例如：CUBE(region, category) 会生成：
        - (region, category)
        - (region, ALL)
        - (ALL, category)
        - (ALL, ALL)
        """
        print(f"=== CUBE 聚合: {group_by_columns} ===")

        # 获取所有可能的分组组合
        all_combinations = []
        for r in range(len(group_by_columns) + 1):
            combinations = list(itertools.combinations(group_by_columns, r))
            all_combinations.extend(combinations)

        # 去重并排序（按组合长度降序）
        all_combinations = list(set(all_combinations))
        all_combinations.sort(key=lambda x: (-len(x), x))

        all_results = []

        for combo in all_combinations:
            if not combo:
                # 总计行
                sql = f"SELECT 'ALL' as dummy, SUM({aggregate_columns[0]}) as total"
                for agg_col in aggregate_columns[1:]:
                    sql += f", SUM({agg_col}) as {agg_col}"
                sql += " FROM sales"
                group_desc = "总计"
            else:
                # 分组查询
                select_clause = ", ".join(combo)
                sql = f"SELECT {select_clause}, SUM({aggregate_columns[0]}) as total"
                for agg_col in aggregate_columns[1:]:
                    sql += f", SUM({agg_col}) as {agg_col}"
                sql += " FROM sales GROUP BY " + ", ".join(combo)
                group_desc = " + ".join(combo) if len(combo) > 1 else combo[0]

            cursor = self.conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                if not combo:
                    display_row = ["总计"] + list(row[1:])
                else:
                    display_values = []
                    for i, val in enumerate(row[:-len(aggregate_columns)]):
                        display_values.append(val if val is not None else 'ALL')
                    display_row = display_values + list(row[-len(aggregate_columns):])

                all_results.append((group_desc, display_row))

        # 显示结果
        headers = group_by_columns + aggregate_columns
        print(f"{'分组':<20} {' | '.join(headers)}")
        print("-" * 70)

        for group_desc, row in all_results:
            row_str = " | ".join(str(val) for val in row)
            print(f"{group_desc:<20} {row_str}")

        print()
        return all_results

def main():
    """主函数"""
    print("简单OLAP查询引擎演示")
    print("=" * 30)

    # 创建内存数据库
    conn = sqlite3.connect(':memory:')

    # 创建OLAP引擎
    olap_engine = SimpleOLAPEngine(conn)

    # 创建示例数据
    olap_engine.create_sample_data()
    print("✓ 示例销售数据创建完成\n")

    # 演示ROLLUP
    olap_engine.execute_rollup(
        ['region', 'product_category'],
        ['sales_amount', 'units_sold']
    )

    # 演示CUBE
    olap_engine.execute_cube(
        ['region', 'product_category'],
        ['sales_amount', 'units_sold']
    )

    # 关闭连接
    conn.close()

    print("OLAP聚合功能说明:")
    print("- ROLLUP: 生成层次化的汇总，适合有自然层次结构的维度")
    print("- CUBE: 生成所有可能的组合汇总，适合需要全面分析的场景")
    print("- 实际数据仓库系统（如Snowflake、Redshift）原生支持这些功能")
    print("- 本示例展示了这些聚合操作的基本原理")

if __name__ == "__main__":
    main()