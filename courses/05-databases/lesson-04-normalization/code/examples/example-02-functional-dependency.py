#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
函数依赖分析器：检测表中的函数依赖关系
帮助识别范式违反和规范化机会
"""

import sqlite3
from collections import defaultdict
from itertools import combinations

def create_sample_table(conn):
    """创建示例表用于分析"""
    cursor = conn.cursor()

    # 创建一个可能包含函数依赖的表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee_data (
            emp_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            dept_manager TEXT NOT NULL,
            salary_grade TEXT NOT NULL,
            salary_range TEXT NOT NULL
        )
    ''')

    # 插入示例数据
    sample_data = [
        (1, '张三', 'IT部门', '李经理', 'A级', '10000-20000'),
        (2, '李四', 'IT部门', '李经理', 'B级', '8000-15000'),
        (3, '王五', 'HR部门', '赵经理', 'A级', '10000-20000'),
        (4, '赵六', 'IT部门', '李经理', 'C级', '6000-12000'),
        (5, '钱七', 'HR部门', '赵经理', 'B级', '8000-15000'),
        (6, '孙八', '财务部', '周经理', 'A级', '10000-20000')
    ]

    cursor.executemany(
        "INSERT INTO employee_data VALUES (?, ?, ?, ?, ?, ?)",
        sample_data
    )
    conn.commit()

def get_column_names(conn, table_name):
    """获取表的列名"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [col[1] for col in cursor.fetchall()]

def get_all_rows(conn, table_name):
    """获取表的所有行数据"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()

def find_functional_dependencies(conn, table_name):
    """
    分析表中的函数依赖关系
    返回字典：{决定因素: [被决定因素]}
    """
    columns = get_column_names(conn, table_name)
    rows = get_all_rows(conn, table_name)

    if not rows:
        return {}

    dependencies = defaultdict(list)
    num_columns = len(columns)

    # 检查所有可能的决定因素组合
    for r in range(1, num_columns + 1):
        for determinant_cols in combinations(range(num_columns), r):
            # 获取决定因素的列名
            determinant_names = [columns[i] for i in determinant_cols]

            # 检查每个非决定因素列是否函数依赖于决定因素
            for dependent_col in range(num_columns):
                if dependent_col in determinant_cols:
                    continue

                dependent_name = columns[dependent_col]

                # 检查函数依赖是否成立
                value_map = {}
                is_functional_dependency = True

                for row in rows:
                    # 获取决定因素的值元组
                    determinant_values = tuple(row[i] for i in determinant_cols)
                    dependent_value = row[dependent_col]

                    if determinant_values in value_map:
                        if value_map[determinant_values] != dependent_value:
                            is_functional_dependency = False
                            break
                    else:
                        value_map[determinant_values] = dependent_value

                if is_functional_dependency and len(value_map) > 0:
                    dependencies[tuple(determinant_names)].append(dependent_name)

    return dict(dependencies)

def analyze_normalization_violations(conn, table_name, dependencies):
    """分析范式违反情况"""
    columns = get_column_names(conn, table_name)
    primary_key = get_primary_key(conn, table_name)

    print(f"\n📊 表 '{table_name}' 的函数依赖分析结果：")
    print("-" * 50)

    if not dependencies:
        print("未发现明显的函数依赖关系")
        return

    # 显示所有函数依赖
    for determinant, dependents in dependencies.items():
        determinant_str = ", ".join(determinant)
        dependents_str = ", ".join(dependents)
        print(f"{determinant_str} → {dependents_str}")

    print(f"\n🔑 主键: {', '.join(primary_key) if primary_key else '未知'}")

    # 分析范式违反
    violations = []

    # 检查1NF（这里假设输入数据已经是1NF）
    violations.append("✅ 假设已满足1NF（原子性）")

    # 检查2NF违反（部分依赖）
    if primary_key and len(primary_key) > 1:
        partial_dependencies = []
        for determinant, dependents in dependencies.items():
            if set(determinant).issubset(set(primary_key)) and set(determinant) != set(primary_key):
                # 这是部分依赖
                partial_dependencies.extend([(determinant, dep) for dep in dependents])

        if partial_dependencies:
            violations.append("❌ 发现2NF违反：存在部分函数依赖")
            for det, dep in partial_dependencies:
                violations.append(f"   {' ,'.join(det)} → {dep}")
        else:
            violations.append("✅ 满足2NF（无部分依赖）")
    else:
        violations.append("✅ 单列主键，自动满足2NF")

    # 检查3NF违反（传递依赖）
    transitive_dependencies = []
    for determinant, dependents in dependencies.items():
        det_set = set(determinant)
        if not det_set.issubset(set(primary_key)):
            # 决定因素不是主键的子集，检查是否传递依赖
            for dep in dependents:
                if dep not in primary_key:
                    transitive_dependencies.append((determinant, dep))

    if transitive_dependencies:
        violations.append("❌ 发现3NF违反：存在传递函数依赖")
        for det, dep in transitive_dependencies:
            violations.append(f"   {' ,'.join(det)} → {dep}")
    else:
        violations.append("✅ 满足3NF（无传递依赖）")

    print("\n🔍 范式分析结果：")
    for violation in violations:
        print(violation)

def get_primary_key(conn, table_name):
    """获取表的主键列"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    primary_key_cols = []

    for col in columns:
        if col[5] == 1:  # pk 列为1表示是主键
            primary_key_cols.append(col[1])

    # 如果没有显式主键，检查是否有复合主键约束
    if not primary_key_cols:
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()
        for idx in indexes:
            if idx[2] == 1:  # unique 为1且是主键索引
                cursor.execute(f"PRAGMA index_info({idx[1]})")
                idx_info = cursor.fetchall()
                primary_key_cols = [info[2] for info in idx_info]
                break

    return primary_key_cols

def main():
    """主函数：演示函数依赖分析"""
    print("🔍 函数依赖分析器：识别数据库范式违反")
    print("=" * 60)

    # 创建内存数据库
    conn = sqlite3.connect(':memory:')

    try:
        # 创建示例表
        create_sample_table(conn)

        # 显示原始数据
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee_data")
        columns = get_column_names(conn, 'employee_data')
        print(f"\n📋 原始表结构: {', '.join(columns)}")
        print("📋 示例数据:")
        for row in cursor.fetchall():
            print(row)

        # 分析函数依赖
        dependencies = find_functional_dependencies(conn, 'employee_data')

        # 分析范式违反
        analyze_normalization_violations(conn, 'employee_data', dependencies)

        print("\n💡 分析建议：")
        print("基于函数依赖分析，建议将表分解为：")
        print("1. 员工表 (emp_id, name, department, salary_grade)")
        print("2. 部门表 (department, dept_manager)")
        print("3. 薪资等级表 (salary_grade, salary_range)")

    finally:
        conn.close()

if __name__ == "__main__":
    main()