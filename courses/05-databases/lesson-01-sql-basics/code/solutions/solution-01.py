#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
练习1解答: 创建学生表并进行基本查询
"""

import sqlite3

def create_student_database():
    """创建学生数据库并插入示例数据"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建学生表
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL,
            score REAL
        )
    ''')

    # 插入学生数据
    students_data = [
        (1, "小明", 18, "A", 95.5),
        (2, "小红", 17, "B", 88.0),
        (3, "小刚", 18, "A", 92.0),
        (4, "小丽", 17, "B", 85.5),
        (5, "小强", 19, "C", 78.0)
    ]
    cursor.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?)", students_data)
    conn.commit()

    return conn, cursor

def main():
    conn, cursor = create_student_database()

    print("✅ 学生数据库创建成功！")

    # 查询所有学生
    print("\n📋 所有学生信息:")
    cursor.execute("SELECT * FROM students ORDER BY id")
    students = cursor.fetchall()
    for student in students:
        print(f"  ID: {student[0]}, 姓名: {student[1]}, 年龄: {student[2]}, 班级: {student[3]}, 成绩: {student[4]}")

    # 查询成绩大于90的学生
    print("\n🏆 成绩大于90分的学生:")
    cursor.execute("SELECT name, score FROM students WHERE score > 90 ORDER BY score DESC")
    high_scorers = cursor.fetchall()
    for name, score in high_scorers:
        print(f"  {name}: {score}分")

    # 计算平均成绩
    cursor.execute("SELECT AVG(score) FROM students")
    avg_score = cursor.fetchone()[0]
    print(f"\n📊 全体平均成绩: {avg_score:.2f}分")

    conn.close()

if __name__ == "__main__":
    main()