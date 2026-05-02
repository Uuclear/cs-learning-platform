#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 基础索引创建

创建学生表并测试索引性能。
"""

import sqlite3
import time
import random

def create_students_table():
    """创建学生表并插入测试数据"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建学生表
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            grade TEXT,
            class TEXT
        )
    ''')

    # 生成1000条测试数据
    names = [f"student_{i}" for i in range(1000)]
    grades = ['A', 'B', 'C', 'D']
    classes = ['math', 'english', 'science', 'history']

    students_data = []
    for i in range(1000):
        student = (
            i + 1,
            names[i],
            random.randint(15, 25),
            random.choice(grades),
            random.choice(classes)
        )
        students_data.append(student)

    cursor.executemany('INSERT INTO students VALUES (?, ?, ?, ?, ?)', students_data)
    conn.commit()

    return conn, cursor

def test_index_performance():
    """测试索引性能"""
    conn, cursor = create_students_table()

    # 测试无索引查询
    print("=== 无索引查询测试 ===")
    start_time = time.time()
    cursor.execute("SELECT * FROM students WHERE name = 'student_500'")
    result = cursor.fetchone()
    no_index_time = time.time() - start_time
    print(f"查询结果: {result}")
    print(f"无索引耗时: {no_index_time * 1000:.2f} 毫秒")

    # 创建索引
    cursor.execute('CREATE INDEX idx_student_name ON students(name)')

    # 测试有索引查询
    print("\n=== 有索引查询测试 ===")
    start_time = time.time()
    cursor.execute("SELECT * FROM students WHERE name = 'student_500'")
    result = cursor.fetchone()
    with_index_time = time.time() - start_time
    print(f"查询结果: {result}")
    print(f"有索引耗时: {with_index_time * 1000:.2f} 毫秒")

    if with_index_time > 0:
        speedup = no_index_time / with_index_time
        print(f"\n🎉 性能提升: {speedup:.1f} 倍!")

    conn.close()

if __name__ == "__main__":
    test_index_performance()