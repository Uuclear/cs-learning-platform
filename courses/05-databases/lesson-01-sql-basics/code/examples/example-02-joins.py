#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: SQL JOIN连接查询
演示不同类型的JOIN操作，理解表间关联查询
"""

import sqlite3

def main():
    # 创建内存数据库
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建部门表
    cursor.execute('''
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    # 创建员工表（包含部门ID外键）
    cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department_id INTEGER,
            salary REAL
        )
    ''')

    # 插入部门数据
    departments_data = [
        (1, "技术部"),
        (2, "销售部"),
        (3, "人事部"),
        (4, "市场部")
    ]
    cursor.executemany("INSERT INTO departments VALUES (?, ?)", departments_data)

    # 插入员工数据（注意：有些员工没有分配部门，模拟LEFT JOIN场景）
    employees_data = [
        (1, "张三", 1, 8000.0),
        (2, "李四", 1, 9000.0),
        (3, "王五", 2, 7000.0),
        (4, "赵六", 2, 7500.0),
        (5, "钱七", None, 6000.0),  # 没有部门的员工
        (6, "孙八", 3, 6500.0)
    ]
    cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?)", employees_data)
    conn.commit()

    print("✅ 部门和员工表创建成功！")

    # INNER JOIN - 内连接（只返回两个表都有匹配的记录）
    print("\n🔍 INNER JOIN (内连接) - 只显示有部门的员工:")
    cursor.execute('''
        SELECT e.name AS 员工姓名, d.name AS 部门名称, e.salary AS 薪资
        FROM employees e
        INNER JOIN departments d ON e.department_id = d.id
        ORDER BY d.name, e.name
    ''')
    inner_join_results = cursor.fetchall()
    for row in inner_join_results:
        print(f"  {row[0]} - {row[1]} - ¥{row[2]:,.2f}")

    # LEFT JOIN - 左连接（返回左表所有记录，右表没有匹配的显示NULL）
    print("\n🔍 LEFT JOIN (左连接) - 显示所有员工，包括没有部门的:")
    cursor.execute('''
        SELECT e.name AS 员工姓名,
               COALESCE(d.name, '未分配') AS 部门名称,
               e.salary AS 薪资
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        ORDER BY e.name
    ''')
    left_join_results = cursor.fetchall()
    for row in left_join_results:
        print(f"  {row[0]} - {row[1]} - ¥{row[2]:,.2f}")

    # RIGHT JOIN 模拟 - SQLite不直接支持RIGHT JOIN，但可以用LEFT JOIN交换表顺序实现
    print("\n🔍 RIGHT JOIN (右连接模拟) - 显示所有部门，包括没有员工的:")
    cursor.execute('''
        SELECT COALESCE(e.name, '暂无员工') AS 员工姓名,
               d.name AS 部门名称
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        ORDER BY d.name, e.name
    ''')
    right_join_results = cursor.fetchall()
    current_dept = ""
    for row in right_join_results:
        if row[1] != current_dept:
            current_dept = row[1]
            print(f"\n  🏢 {current_dept}:")
        print(f"    👤 {row[0]}")

    # CROSS JOIN - 笛卡尔积（每个员工与每个部门组合）
    print("\n🔍 CROSS JOIN (笛卡尔积) - 所有可能的员工部门组合:")
    cursor.execute('''
        SELECT e.name AS 员工姓名, d.name AS 部门名称
        FROM employees e
        CROSS JOIN departments d
        LIMIT 10  -- 限制显示数量避免太多输出
    ''')
    cross_join_results = cursor.fetchall()
    for i, row in enumerate(cross_join_results):
        print(f"  {row[0]} - {row[1]}")
    print(f"  ... (共{len(cross_join_results)}条记录，已限制显示)")

    # 关闭连接
    conn.close()
    print("\n🔒 数据库连接已关闭")

if __name__ == "__main__":
    main()