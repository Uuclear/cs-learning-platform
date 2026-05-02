#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: 诊断和优化 5 种常见慢查询模式

本脚本提供了诊断和优化常见慢查询模式的完整解决方案，
包括自动化分析工具和优化建议。
"""

import sqlite3
import time
import re
from typing import List, Dict, Tuple, Optional


class QueryAnalyzer:
    """查询分析器 - 用于诊断慢查询问题"""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create_test_data(self) -> None:
        """创建测试数据用于演示"""
        # 创建表结构
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER,
                city TEXT,
                department_id INTEGER
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_name TEXT,
                amount REAL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 检查是否已有数据
        self.cursor.execute("SELECT COUNT(*) FROM users")
        if self.cursor.fetchone()[0] > 0:
            return

        # 生成大量测试数据
        print("正在生成测试数据...")
        users_data = [(f"用户{i:04d}", f"user{i:04d}@example.com",
                      i % 60 + 18, f"城市{i % 10}", i % 20) for i in range(10000)]
        self.cursor.executemany(
            "INSERT INTO users (name, email, age, city, department_id) VALUES (?, ?, ?, ?, ?)",
            users_data
        )

        orders_data = [(i % 10000 + 1, f"产品{i}", i * 10.5,
                       ["pending", "shipped", "delivered"][i % 3]) for i in range(50000)]
        self.cursor.executemany(
            "INSERT INTO orders (user_id, product_name, amount, status) VALUES (?, ?, ?, ?)",
            orders_data
        )

        # 创建一些索引用于对比
        self.cursor.execute("CREATE INDEX idx_users_email ON users(email)")
        self.cursor.execute("CREATE INDEX idx_orders_user_id ON orders(user_id)")
        self.cursor.execute("CREATE INDEX idx_orders_status ON orders(status)")

        self.conn.commit()
        print("测试数据生成完成!")

    def analyze_query_plan(self, query: str) -> Dict:
        """分析查询执行计划"""
        try:
            self.cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            plan_rows = self.cursor.fetchall()

            plan_info = {
                'full_table_scans': [],
                'index_scans': [],
                'search_details': []
            }

            for row in plan_rows:
                detail = row[3].lower()
                if 'scan table' in detail:
                    table_name = detail.split('table')[1].split()[0].strip()
                    plan_info['full_table_scans'].append(table_name)
                elif 'search table' in detail and 'using index' in detail:
                    plan_info['index_scans'].append(detail)
                plan_info['search_details'].append(detail)

            return plan_info
        except Exception as e:
            return {'error': str(e)}

    def measure_performance(self, query: str, iterations: int = 3) -> float:
        """测量查询性能"""
        total_time = 0.0
        for _ in range(iterations):
            start = time.time()
            self.cursor.execute(query)
            self.cursor.fetchall()
            total_time += (time.time() - start) * 1000
        return total_time / iterations

    def detect_slow_patterns(self, query: str) -> List[str]:
        """检测慢查询模式"""
        patterns = []

        # 模式 1: SELECT *
        if re.search(r'\bselect\s+\*\b', query, re.IGNORECASE):
            patterns.append("使用 SELECT * - 应该只选择需要的列")

        # 模式 2: 函数在 WHERE 子句中导致索引失效
        if re.search(r'\bwhere\s+.*\b(?:upper|lower|substr|concat)\s*\(', query, re.IGNORECASE):
            patterns.append("WHERE 子句中使用函数 - 可能导致索引失效")

        # 模式 3: LIKE 以通配符开头
        if re.search(r"\blike\s+'%\w+", query, re.IGNORECASE):
            patterns.append("LIKE 以 % 开头 - 无法使用索引")

        # 模式 4: 缺少 JOIN 条件
        if re.search(r'\bjoin\b', query, re.IGNORECASE) and not re.search(r'\bon\b', query, re.IGNORECASE):
            patterns.append("JOIN 缺少 ON 条件 - 可能产生笛卡尔积")

        # 模式 5: 子查询可以转换为 JOIN
        if query.lower().count('select') > 1 and 'in (' in query.lower():
            patterns.append("使用 IN 子查询 - 考虑转换为 JOIN")

        return patterns

    def optimize_query(self, original_query: str) -> str:
        """提供查询优化建议"""
        query = original_query.strip()

        # 优化 1: SELECT * -> 具体列名（这里简化处理）
        if re.search(r'\bselect\s+\*\b', query, re.IGNORECASE):
            # 在实际应用中，需要分析表结构来确定具体列名
            pass

        # 优化 2: IN 子查询转 JOIN
        in_subquery_pattern = r'select\s+(.*?)\s+from\s+(\w+)\s+where\s+(\w+)\s+in\s*\(\s*select\s+(\w+)\s+from\s+(\w+)'
        match = re.search(in_subquery_pattern, query, re.IGNORECASE | re.DOTALL)
        if match:
            select_part = match.group(1)
            main_table = match.group(2)
            main_col = match.group(3)
            sub_col = match.group(4)
            sub_table = match.group(5)
            optimized = f"SELECT DISTINCT {select_part} FROM {main_table} m JOIN {sub_table} s ON m.{main_col} = s.{sub_col}"
            return optimized

        return query

    def diagnose_and_optimize(self, slow_query: str) -> Dict:
        """完整的诊断和优化流程"""
        result = {
            'original_query': slow_query,
            'detected_patterns': self.detect_slow_patterns(slow_query),
            'execution_plan': self.analyze_query_plan(slow_query),
            'original_performance': self.measure_performance(slow_query),
            'optimized_query': self.optimize_query(slow_query)
        }

        # 测试优化后的查询（如果不同）
        if result['optimized_query'] != slow_query:
            try:
                result['optimized_performance'] = self.measure_performance(result['optimized_query'])
                result['improvement_percent'] = (
                    (result['original_performance'] - result['optimized_performance']) /
                    result['original_performance'] * 100
                ) if result['original_performance'] > 0 else 0
            except:
                result['optimized_performance'] = None
                result['improvement_percent'] = 0
        else:
            result['optimized_performance'] = None
            result['improvement_percent'] = 0

        return result

    def close(self):
        """关闭数据库连接"""
        self.conn.close()


def demonstrate_five_common_patterns():
    """演示 5 种常见慢查询模式的诊断和优化"""
    print("🔍 解决方案 1: 诊断和优化 5 种常见慢查询模式")
    print("=" * 60)

    analyzer = QueryAnalyzer()
    analyzer.create_test_data()

    # 5 种常见的慢查询模式
    slow_queries = [
        # 模式 1: SELECT *
        "SELECT * FROM users WHERE email = 'user1234@example.com'",

        # 模式 2: 函数导致索引失效
        "SELECT * FROM users WHERE UPPER(email) = 'USER1234@EXAMPLE.COM'",

        # 模式 3: 缺少 LIMIT 的分页查询
        "SELECT u.name, o.product_name FROM users u JOIN orders o ON u.id = o.user_id ORDER BY o.created_at DESC",

        # 模式 4: IN 子查询
        "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE status = 'delivered')",

        # 模式 5: 复合条件缺少复合索引
        "SELECT * FROM users WHERE age > 30 AND city = '北京'"
    ]

    for i, query in enumerate(slow_queries, 1):
        print(f"\n📊 慢查询模式 {i}:")
        print(f"查询: {query}")

        result = analyzer.diagnose_and_optimize(query)

        print(f"检测到的问题: {', '.join(result['detected_patterns']) if result['detected_patterns'] else '无'}")

        if result['execution_plan'].get('full_table_scans'):
            print(f"全表扫描表: {', '.join(result['execution_plan']['full_table_scans'])}")

        print(f"原始执行时间: {result['original_performance']:.2f} ms")

        if result['optimized_query'] != query:
            print(f"优化后查询: {result['optimized_query']}")
            if result['optimized_performance']:
                print(f"优化后时间: {result['optimized_performance']:.2f} ms")
                print(f"性能提升: {result['improvement_percent']:.1f}%")

    print("\n💡 通用优化建议:")
    print("1. 总是使用 EXPLAIN 分析执行计划")
    print("2. 为常用查询条件创建合适的索引")
    print("3. 避免在 WHERE 子句中对列使用函数")
    print("4. 使用 JOIN 替代子查询")
    print("5. 只选择需要的列，避免 SELECT *")
    print("6. 合理使用 LIMIT 进行分页")
    print("7. 定期更新表统计信息")

    analyzer.close()


if __name__ == "__main__":
    demonstrate_five_common_patterns()