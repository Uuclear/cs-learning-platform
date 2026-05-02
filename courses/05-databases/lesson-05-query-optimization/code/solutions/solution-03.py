#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: SQL 查询性能测试框架

本脚本实现了一个完整的 SQL 查询性能测试框架，
可以用于基准测试、回归测试和性能监控。
"""

import sqlite3
import time
import json
import statistics
import argparse
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import os


@dataclass
class QueryTestResult:
    """查询测试结果"""
    query_name: str
    query_text: str
    execution_times: List[float]  # 毫秒
    average_time: float
    median_time: float
    min_time: float
    max_time: float
    std_deviation: float
    row_count: int
    timestamp: str
    database_size: int  # 字节


@dataclass
class PerformanceReport:
    """性能测试报告"""
    test_suite_name: str
    results: List[QueryTestResult]
    total_queries: int
    total_execution_time: float
    generated_at: str


class SQLPerformanceTester:
    """SQL 查询性能测试框架"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.results: List[QueryTestResult] = []

    def get_database_size(self) -> int:
        """获取数据库文件大小"""
        if self.db_path == ":memory:":
            return 0
        try:
            return os.path.getsize(self.db_path)
        except:
            return 0

    def execute_query_multiple_times(self, query: str, iterations: int = 5) -> tuple:
        """多次执行查询并返回时间和结果数量"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        execution_times = []
        row_count = 0

        for _ in range(iterations):
            start_time = time.time()
            cursor.execute(query)
            results = cursor.fetchall()
            end_time = time.time()

            execution_time_ms = (end_time - start_time) * 1000
            execution_times.append(execution_time_ms)

            if _ == 0:  # 只在第一次获取行数
                row_count = len(results)

        conn.close()
        return execution_times, row_count

    def analyze_execution_plan(self, query: str) -> Dict[str, Any]:
        """分析查询执行计划"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            plan_rows = cursor.fetchall()
            plan_info = {
                'operations': [row[3] for row in plan_rows],
                'full_table_scans': sum(1 for row in plan_rows if 'SCAN TABLE' in row[3]),
                'index_usage': sum(1 for row in plan_rows if 'USING INDEX' in row[3])
            }
        except Exception as e:
            plan_info = {'error': str(e), 'operations': []}

        conn.close()
        return plan_info

    def test_single_query(self, query_name: str, query_text: str,
                         iterations: int = 5) -> QueryTestResult:
        """测试单个查询的性能"""
        print(f"正在测试查询 '{query_name}'...")

        # 执行查询多次
        execution_times, row_count = self.execute_query_multiple_times(query_text, iterations)

        # 计算统计信息
        avg_time = statistics.mean(execution_times)
        median_time = statistics.median(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        std_dev = statistics.stdev(execution_times) if len(execution_times) > 1 else 0.0

        result = QueryTestResult(
            query_name=query_name,
            query_text=query_text,
            execution_times=execution_times,
            average_time=avg_time,
            median_time=median_time,
            min_time=min_time,
            max_time=max_time,
            std_deviation=std_dev,
            row_count=row_count,
            timestamp=datetime.now().isoformat(),
            database_size=self.get_database_size()
        )

        self.results.append(result)
        return result

    def test_query_suite(self, query_suite: Dict[str, str], iterations: int = 5) -> PerformanceReport:
        """测试整个查询套件"""
        print(f"开始测试查询套件，包含 {len(query_suite)} 个查询...")

        total_time = 0.0
        for query_name, query_text in query_suite.items():
            result = self.test_single_query(query_name, query_text, iterations)
            total_time += result.average_time

        report = PerformanceReport(
            test_suite_name="Query Performance Test Suite",
            results=self.results,
            total_queries=len(self.results),
            total_execution_time=total_time,
            generated_at=datetime.now().isoformat()
        )

        return report

    def save_report_to_json(self, report: PerformanceReport, filename: str) -> None:
        """保存报告到 JSON 文件"""
        report_dict = asdict(report)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, ensure_ascii=False, indent=2)
        print(f"报告已保存到: {filename}")

    def compare_with_baseline(self, current_report: PerformanceReport,
                            baseline_file: str) -> Dict[str, Any]:
        """与基线报告比较"""
        try:
            with open(baseline_file, 'r', encoding='utf-8') as f:
                baseline_data = json.load(f)

            baseline_results = {r['query_name']: r for r in baseline_data['results']}
            current_results = {r.query_name: r for r in current_report.results}

            comparison = {
                'regressions': [],
                'improvements': [],
                'unchanged': []
            }

            for query_name, current_result in current_results.items():
                if query_name in baseline_results:
                    baseline_avg = baseline_results[query_name]['average_time']
                    current_avg = current_result.average_time
                    change_percent = ((current_avg - baseline_avg) / baseline_avg) * 100

                    if change_percent > 10:  # 性能下降超过 10%
                        comparison['regressions'].append({
                            'query_name': query_name,
                            'baseline_time': baseline_avg,
                            'current_time': current_avg,
                            'change_percent': change_percent
                        })
                    elif change_percent < -10:  # 性能提升超过 10%
                        comparison['improvements'].append({
                            'query_name': query_name,
                            'baseline_time': baseline_avg,
                            'current_time': current_avg,
                            'change_percent': change_percent
                        })
                    else:
                        comparison['unchanged'].append(query_name)

            return comparison
        except FileNotFoundError:
            print(f"基线文件 {baseline_file} 不存在，跳过比较")
            return {}

    def generate_html_report(self, report: PerformanceReport, filename: str) -> None:
        """生成 HTML 报告"""
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL 查询性能测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .slow {{ background-color: #ffe6e6; }}
        .fast {{ background-color: #e6ffe6; }}
        .summary {{ background-color: #f9f9f9; padding: 15px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>SQL 查询性能测试报告</h1>
    <div class="summary">
        <h2>测试概要</h2>
        <p><strong>测试套件:</strong> {report.test_suite_name}</p>
        <p><strong>查询总数:</strong> {report.total_queries}</p>
        <p><strong>总执行时间:</strong> {report.total_execution_time:.2f} ms</p>
        <p><strong>生成时间:</strong> {report.generated_at}</p>
    </div>

    <h2>详细结果</h2>
    <table>
        <thead>
            <tr>
                <th>查询名称</th>
                <th>平均时间 (ms)</th>
                <th>中位数 (ms)</th>
                <th>最小值 (ms)</th>
                <th>最大值 (ms)</th>
                <th>标准差</th>
                <th>返回行数</th>
            </tr>
        </thead>
        <tbody>
"""

        for result in report.results:
            # 根据执行时间着色
            avg_time = result.average_time
            row_class = ""
            if avg_time > 100:
                row_class = "slow"
            elif avg_time < 10:
                row_class = "fast"

            html_content += f"""
            <tr class="{row_class}">
                <td>{result.query_name}</td>
                <td>{avg_time:.2f}</td>
                <td>{result.median_time:.2f}</td>
                <td>{result.min_time:.2f}</td>
                <td>{result.max_time:.2f}</td>
                <td>{result.std_deviation:.2f}</td>
                <td>{result.row_count}</td>
            </tr>
"""

        html_content += """
        </tbody>
    </table>
</body>
</html>
"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML 报告已生成: {filename}")


def create_sample_test_data(db_path: str) -> None:
    """创建示例测试数据"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            customer_id INTEGER,
            amount REAL,
            status TEXT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    print("正在生成测试数据...")

    # 生成产品数据
    products = [(i, f"Product {i}", f"Category {i % 10}", i * 10.5) for i in range(10000)]
    cursor.executemany("INSERT INTO products (id, name, category, price) VALUES (?, ?, ?, ?)", products)

    # 生成订单数据
    orders = [(i, i % 10000 + 1, i % 5000 + 1, i * 5.5,
               ["pending", "shipped", "delivered"][i % 3]) for i in range(50000)]
    cursor.executemany("INSERT INTO orders (id, product_id, customer_id, amount, status) VALUES (?, ?, ?, ?, ?)", orders)

    # 创建索引
    cursor.execute("CREATE INDEX idx_products_category ON products(category)")
    cursor.execute("CREATE INDEX idx_orders_product_id ON orders(product_id)")
    cursor.execute("CREATE INDEX idx_orders_status ON orders(status)")

    conn.commit()
    conn.close()
    print("测试数据生成完成!")


def demonstrate_performance_framework():
    """演示性能测试框架"""
    print("📊 解决方案 3: SQL 查询性能测试框架")
    print("=" * 60)

    # 使用内存数据库进行演示
    db_path = ":memory:"
    create_sample_test_data(db_path)

    # 定义测试查询套件
    test_queries = {
        "simple_select": "SELECT * FROM products WHERE id = 1234",
        "indexed_select": "SELECT * FROM products WHERE category = 'Category 5'",
        "join_query": "SELECT p.name, o.amount FROM products p JOIN orders o ON p.id = o.product_id WHERE o.status = 'delivered' LIMIT 100",
        "full_table_scan": "SELECT * FROM products WHERE price > 50000",
        "aggregate_query": "SELECT category, COUNT(*), AVG(price) FROM products GROUP BY category",
        "subquery_slow": "SELECT * FROM products WHERE id IN (SELECT product_id FROM orders WHERE status = 'delivered')"
    }

    # 初始化测试器
    tester = SQLPerformanceTester(db_path)

    # 执行测试
    report = tester.test_query_suite(test_queries, iterations=3)

    # 显示结果摘要
    print(f"\n📈 测试结果摘要:")
    print(f"总查询数: {report.total_queries}")
    print(f"总执行时间: {report.total_execution_time:.2f} ms")

    print(f"\n🔍 各查询性能详情:")
    for result in report.results:
        print(f"- {result.query_name}: {result.average_time:.2f} ms (返回 {result.row_count} 行)")

    # 保存报告
    tester.save_report_to_json(report, "performance_report.json")
    tester.generate_html_report(report, "performance_report.html")

    # 分析最慢的查询
    slowest = max(report.results, key=lambda r: r.average_time)
    print(f"\n🐢 最慢的查询: {slowest.query_name} ({slowest.average_time:.2f} ms)")

    fastest = min(report.results, key=lambda r: r.average_time)
    print(f"🚀 最快的查询: {fastest.query_name} ({fastest.average_time:.2f} ms)")

    print("\n💡 使用建议:")
    print("- 定期运行性能测试以监控查询性能变化")
    print("- 在代码变更前后对比性能差异")
    print("- 重点关注执行时间超过 100ms 的查询")
    print("- 结合 EXPLAIN 分析慢查询的根本原因")
    print("- 建立性能基线用于回归测试")


if __name__ == "__main__":
    demonstrate_performance_framework()