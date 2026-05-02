#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：将学生注册表规范化到3NF
原始表包含冗余数据和各种异常，需要分解为符合3NF的表结构
"""

import sqlite3

def create_original_denormalized_table(conn):
    """创建原始的非规范化学生注册表"""
    cursor = conn.cursor()

    # 原始表包含所有信息在一个表中
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_registration_raw (
            student_id INTEGER,
            student_name TEXT,
            student_email TEXT,
            course_id INTEGER,
            course_name TEXT,
            course_instructor TEXT,
            instructor_office TEXT,
            grade REAL,
            semester TEXT,
            PRIMARY KEY (student_id, course_id, semester)
        )
    ''')

    # 插入示例数据（包含冗余）
    sample_data = [
        (1, '张三', 'zhang@example.com', 101, '数据库系统', '王教授', 'A101', 95.0, '2023-Fall'),
        (1, '张三', 'zhang@example.com', 102, '算法设计', '李教授', 'B202', 88.0, '2023-Fall'),
        (2, '李四', 'li@example.com', 101, '数据库系统', '王教授', 'A101', 92.0, '2023-Fall'),
        (2, '李四', 'li@example.com', 103, '操作系统', '赵教授', 'C303', 85.0, '2023-Fall'),
        (3, '王五', 'wang@example.com', 102, '算法设计', '李教授', 'B202', 90.0, '2023-Fall'),
        (3, '王五', 'wang@example.com', 101, '数据库系统', '王教授', 'A101', 87.0, '2023-Spring')
    ]

    cursor.executemany(
        "INSERT INTO student_registration_raw VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        sample_data
    )
    conn.commit()

def normalize_to_3nf(conn):
    """将表规范化到3NF"""
    cursor = conn.cursor()

    # 步骤1：识别函数依赖
    # student_id → student_name, student_email
    # course_id → course_name, course_instructor
    # course_instructor → instructor_office
    # (student_id, course_id, semester) → grade

    # 步骤2：分解为3NF表

    # 学生表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL UNIQUE
        )
    ''')

    # 课程表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            course_instructor TEXT NOT NULL
        )
    ''')

    # 教师表（解决传递依赖：course_instructor → instructor_office）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructors (
            instructor_name TEXT PRIMARY KEY,
            instructor_office TEXT NOT NULL
        )
    ''')

    # 注册表（关联表）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            student_id INTEGER,
            course_id INTEGER,
            semester TEXT,
            grade REAL,
            PRIMARY KEY (student_id, course_id, semester),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
    ''')

    # 步骤3：迁移数据

    # 迁移学生数据（去重）
    cursor.execute('''
        INSERT OR IGNORE INTO students (student_id, student_name, student_email)
        SELECT DISTINCT student_id, student_name, student_email
        FROM student_registration_raw
    ''')

    # 迁移课程数据（去重）
    cursor.execute('''
        INSERT OR IGNORE INTO courses (course_id, course_name, course_instructor)
        SELECT DISTINCT course_id, course_name, course_instructor
        FROM student_registration_raw
    ''')

    # 迁移教师数据（去重）
    cursor.execute('''
        INSERT OR IGNORE INTO instructors (instructor_name, instructor_office)
        SELECT DISTINCT course_instructor, instructor_office
        FROM student_registration_raw
    ''')

    # 迁移注册数据
    cursor.execute('''
        INSERT OR IGNORE INTO registrations (student_id, course_id, semester, grade)
        SELECT student_id, course_id, semester, grade
        FROM student_registration_raw
    ''')

    conn.commit()

def verify_normalization(conn):
    """验证规范化结果"""
    cursor = conn.cursor()

    print("✅ 规范化后的3NF表结构：")
    print("=" * 50)

    # 显示学生表
    print("\n👥 学生表 (students):")
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    for student in students:
        print(f"   {student}")

    # 显示课程表
    print("\n📚 课程表 (courses):")
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    for course in courses:
        print(f"   {course}")

    # 显示教师表
    print("\n👨‍🏫 教师表 (instructors):")
    cursor.execute("SELECT * FROM instructors")
    instructors = cursor.fetchall()
    for instructor in instructors:
        print(f"   {instructor}")

    # 显示注册表
    print("\n📝 注册表 (registrations):")
    cursor.execute("SELECT * FROM registrations")
    registrations = cursor.fetchall()
    for registration in registrations[:5]:  # 只显示前5条
        print(f"   {registration}")
    if len(registrations) > 5:
        print(f"   ... 还有 {len(registrations) - 5} 条记录")

    # 验证3NF特性
    print("\n🔍 3NF验证：")
    print("✅ 消除了数据冗余：每个实体只存储一次")
    print("✅ 消除了更新异常：更新教师办公室只需修改instructors表")
    print("✅ 消除了插入异常：可以单独添加新学生或新课程")
    print("✅ 消除了删除异常：删除注册记录不会丢失学生/课程信息")

def demonstrate_anomaly_fix():
    """演示如何修复原始表中的异常"""
    print("🔧 解决方案1：学生注册表规范化到3NF")
    print("=" * 60)

    conn = sqlite3.connect(':memory:')

    try:
        # 创建原始非规范化表
        create_original_denormalized_table(conn)

        # 显示原始表的问题
        cursor = conn.cursor()
        print("\n❌ 原始非规范化表的问题：")
        print("- 数据冗余：学生信息、课程信息、教师信息重复存储")
        print("- 更新异常：如果王教授换了办公室，需要更新多行")
        print("- 插入异常：无法添加没有学生的课程")
        print("- 删除异常：删除最后一个选课学生会丢失课程信息")

        # 执行规范化
        normalize_to_3nf(conn)

        # 验证结果
        verify_normalization(conn)

        # 演示更新操作的简化
        print("\n✨ 更新操作演示：")
        print("在规范化设计中，更新'王教授'的办公室：")
        cursor.execute("UPDATE instructors SET instructor_office = 'A202' WHERE instructor_name = '王教授'")
        conn.commit()
        print("✅ 只需更新一行，所有相关记录自动保持一致！")

    finally:
        conn.close()

if __name__ == "__main__":
    demonstrate_anomaly_fix()