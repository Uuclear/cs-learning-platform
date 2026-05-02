#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库范式演示：1NF、2NF、3NF 的违反与修复
使用 SQLite3 演示规范化过程
"""

import sqlite3
import os

def create_violating_tables(conn):
    """创建违反范式的表"""
    cursor = conn.cursor()

    # 1NF 违反示例：非原子字段（电话号码包含多个值）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students_1nf_violation (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone_numbers TEXT  -- 违反1NF：包含多个电话号码，用逗号分隔
        )
    ''')

    # 插入违反1NF的数据
    cursor.execute("INSERT INTO students_1nf_violation VALUES (1, '张三', '138****1234,139****5678')")
    cursor.execute("INSERT INTO students_1nf_violation VALUES (2, '李四', '136****9999')")

    # 2NF 违反示例：部分依赖（复合主键下非主属性只依赖部分主键）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollment_2nf_violation (
            student_id INTEGER,
            course_id INTEGER,
            student_name TEXT,      -- 只依赖 student_id，违反2NF
            course_name TEXT,       -- 只依赖 course_id，违反2NF
            grade REAL,
            PRIMARY KEY (student_id, course_id)
        )
    ''')

    # 插入违反2NF的数据
    cursor.execute("INSERT INTO enrollment_2nf_violation VALUES (1, 101, '张三', '数学', 95.0)")
    cursor.execute("INSERT INTO enrollment_2nf_violation VALUES (1, 102, '张三', '英语', 88.0)")
    cursor.execute("INSERT INTO enrollment_2nf_violation VALUES (2, 101, '李四', '数学', 92.0)")

    # 3NF 违反示例：传递依赖
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students_3nf_violation (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,    -- 学生属于某个系
            department_head TEXT NOT NULL -- 系主任，依赖于 department，违反3NF
        )
    ''')

    # 插入违反3NF的数据
    cursor.execute("INSERT INTO students_3nf_violation VALUES (1, '张三', '计算机系', '王教授')")
    cursor.execute("INSERT INTO students_3nf_violation VALUES (2, '李四', '计算机系', '王教授')")
    cursor.execute("INSERT INTO students_3nf_violation VALUES (3, '王五', '数学系', '李教授')")

    conn.commit()

def create_normalized_tables(conn):
    """创建规范化的表"""
    cursor = conn.cursor()

    # 1NF 修复：每个电话号码单独一行
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students_1nf_fixed (
            student_id INTEGER,
            name TEXT NOT NULL,
            phone_number TEXT,
            PRIMARY KEY (student_id, phone_number)
        )
    ''')

    cursor.execute("INSERT INTO students_1nf_fixed VALUES (1, '张三', '138****1234')")
    cursor.execute("INSERT INTO students_1nf_fixed VALUES (1, '张三', '139****5678')")
    cursor.execute("INSERT INTO students_1nf_fixed VALUES (2, '李四', '136****9999')")

    # 2NF 修复：分解为三个表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students_2nf_fixed (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses_2nf_fixed (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollment_2nf_fixed (
            student_id INTEGER,
            course_id INTEGER,
            grade REAL,
            PRIMARY KEY (student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students_2nf_fixed(student_id),
            FOREIGN KEY (course_id) REFERENCES courses_2nf_fixed(course_id)
        )
    ''')

    # 插入2NF修复后的数据
    cursor.execute("INSERT INTO students_2nf_fixed VALUES (1, '张三')")
    cursor.execute("INSERT INTO students_2nf_fixed VALUES (2, '李四')")
    cursor.execute("INSERT INTO courses_2nf_fixed VALUES (101, '数学')")
    cursor.execute("INSERT INTO courses_2nf_fixed VALUES (102, '英语')")
    cursor.execute("INSERT INTO enrollment_2nf_fixed VALUES (1, 101, 95.0)")
    cursor.execute("INSERT INTO enrollment_2nf_fixed VALUES (1, 102, 88.0)")
    cursor.execute("INSERT INTO enrollment_2nf_fixed VALUES (2, 101, 92.0)")

    # 3NF 修复：分离系信息
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students_3nf_fixed (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            FOREIGN KEY (department) REFERENCES departments_3nf_fixed(department)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments_3nf_fixed (
            department TEXT PRIMARY KEY,
            department_head TEXT NOT NULL
        )
    ''')

    # 插入3NF修复后的数据
    cursor.execute("INSERT INTO departments_3nf_fixed VALUES ('计算机系', '王教授')")
    cursor.execute("INSERT INTO departments_3nf_fixed VALUES ('数学系', '李教授')")
    cursor.execute("INSERT INTO students_3nf_fixed VALUES (1, '张三', '计算机系')")
    cursor.execute("INSERT INTO students_3nf_fixed VALUES (2, '李四', '计算机系')")
    cursor.execute("INSERT INTO students_3nf_fixed VALUES (3, '王五', '数学系')")

    conn.commit()

def display_table_data(conn, table_name, title):
    """显示表数据"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")

    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"列名: {', '.join(columns)}")

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def demonstrate_anomalies():
    """演示各种异常情况"""
    print("\n🔍 数据库范式演示：识别和修复范式违反")
    print("="*60)

    # 创建内存数据库
    conn = sqlite3.connect(':memory:')

    try:
        # 创建违反范式的表
        create_violating_tables(conn)

        # 显示违反范式的表
        display_table_data(conn, 'students_1nf_violation', '❌ 1NF 违反示例（非原子字段）')
        display_table_data(conn, 'enrollment_2nf_violation', '❌ 2NF 违反示例（部分依赖）')
        display_table_data(conn, 'students_3nf_violation', '❌ 3NF 违反示例（传递依赖）')

        # 创建规范化的表
        create_normalized_tables(conn)

        # 显示规范化的表
        display_table_data(conn, 'students_1nf_fixed', '✅ 1NF 修复后（原子字段）')
        display_table_data(conn, 'students_2nf_fixed', '✅ 2NF 修复 - 学生表')
        display_table_data(conn, 'courses_2nf_fixed', '✅ 2NF 修复 - 课程表')
        display_table_data(conn, 'enrollment_2nf_fixed', '✅ 2NF 修复 - 选课表')
        display_table_data(conn, 'students_3nf_fixed', '✅ 3NF 修复 - 学生表')
        display_table_data(conn, 'departments_3nf_fixed', '✅ 3NF 修复 - 系别表')

        # 演示更新异常的修复
        print("\n🔧 更新异常演示：")
        print("在违反3NF的表中，如果'计算机系'换了系主任，需要更新多行")
        print("在规范化的表中，只需要更新departments_3nf_fixed表中的一行！")

    finally:
        conn.close()

if __name__ == "__main__":
    demonstrate_anomalies()