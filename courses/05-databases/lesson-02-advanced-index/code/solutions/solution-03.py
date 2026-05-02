#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3: 博客系统索引策略分析
分析博客系统的查询模式并推荐最优的索引策略。
"""

import sqlite3
from typing import List, Dict, Any


def analyze_blog_query_patterns() -> Dict[str, List[str]]:
    """
    分析博客系统的典型查询模式

    Returns:
        查询模式字典
    """
    patterns = {
        "post_retrieval": [
            # 按ID获取文章（主键查询）
            "SELECT * FROM posts WHERE id = ?",
            # 按URL slug获取文章
            "SELECT * FROM posts WHERE slug = ?",
            # 获取最新文章
            "SELECT * FROM posts ORDER BY created_at DESC LIMIT ?"
        ],
        "category_browsing": [
            # 按分类获取文章
            "SELECT * FROM posts WHERE category_id = ? ORDER BY created_at DESC",
            # 按分类和状态获取文章
            "SELECT * FROM posts WHERE category_id = ? AND status = 'published' ORDER BY created_at DESC"
        ],
        "search_functionality": [
            # 标题搜索
            "SELECT * FROM posts WHERE title LIKE ? AND status = 'published'",
            # 标签搜索
            "SELECT p.* FROM posts p JOIN post_tags pt ON p.id = pt.post_id JOIN tags t ON pt.tag_id = t.id WHERE t.name = ? AND p.status = 'published'"
        ],
        "author_operations": [
            # 按作者获取文章
            "SELECT * FROM posts WHERE author_id = ? ORDER BY created_at DESC",
            # 按作者和状态获取文章
            "SELECT * FROM posts WHERE author_id = ? AND status = 'published' ORDER BY created_at DESC"
        ],
        "archive_views": [
            # 按年月归档
            "SELECT * FROM posts WHERE strftime('%Y-%m', created_at) = ? AND status = 'published' ORDER BY created_at DESC",
            # 按年归档
            "SELECT * FROM posts WHERE strftime('%Y', created_at) = ? AND status = 'published' ORDER BY created_at DESC"
        ],
        "popular_content": [
            # 热门文章（按浏览量）
            "SELECT * FROM posts WHERE status = 'published' ORDER BY view_count DESC LIMIT ?",
            # 最新热门文章
            "SELECT * FROM posts WHERE status = 'published' AND created_at >= ? ORDER BY view_count DESC LIMIT ?"
        ]
    }

    return patterns


def recommend_blog_indexes() -> List[Dict[str, Any]]:
    """
    为博客系统推荐索引策略

    Returns:
        索引推荐列表
    """
    recommendations = [
        {
            "table": "posts",
            "columns": ["id"],
            "type": "PRIMARY KEY",
            "reason": "主键，自动创建聚簇索引"
        },
        {
            "table": "posts",
            "columns": ["slug"],
            "type": "UNIQUE INDEX",
            "reason": "URL slug需要唯一且频繁查询"
        },
        {
            "table": "posts",
            "columns": ["created_at DESC"],
            "type": "INDEX",
            "reason": "支持最新文章查询和时间排序"
        },
        {
            "table": "posts",
            "columns": ["category_id", "status", "created_at DESC"],
            "type": "COMPOSITE INDEX",
            "reason": "支持分类浏览，包含状态过滤和时间排序"
        },
        {
            "table": "posts",
            "columns": ["author_id", "status", "created_at DESC"],
            "type": "COMPOSITE INDEX",
            "reason": "支持作者文章查询，包含状态过滤和时间排序"
        },
        {
            "table": "posts",
            "columns": ["status", "view_count DESC"],
            "type": "COMPOSITE INDEX",
            "reason": "支持热门文章查询，状态过滤和浏览量排序"
        },
        {
            "table": "posts",
            "columns": ["status", "created_at DESC", "view_count DESC"],
            "type": "COMPOSITE INDEX",
            "reason": "支持最新热门文章查询"
        },
        {
            "table": "posts",
            "columns": ["title"],
            "type": "FULLTEXT INDEX (if supported)",
            "reason": "支持标题搜索，但在SQLite中使用普通索引"
        },
        {
            "table": "post_tags",
            "columns": ["tag_id", "post_id"],
            "type": "COMPOSITE INDEX",
            "reason": "支持标签搜索，优化JOIN操作"
        },
        {
            "table": "tags",
            "columns": ["name"],
            "type": "UNIQUE INDEX",
            "reason": "标签名称需要唯一且用于搜索"
        }
    ]

    return recommendations


def create_blog_schema_with_indexes(conn: sqlite3.Connection) -> None:
    """
    创建博客系统表结构和推荐的索引

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    print("🔧 创建博客系统表结构...")

    # 创建文章表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            excerpt TEXT,
            status TEXT NOT NULL DEFAULT 'draft',
            author_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            view_count INTEGER DEFAULT 0,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP,
            published_at TIMESTAMP
        )
    ''')

    # 创建分类表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')

    # 创建标签表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            slug TEXT UNIQUE NOT NULL
        )
    ''')

    # 创建文章-标签关联表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS post_tags (
            post_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (post_id, tag_id)
        )
    ''')

    # 创建作者表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL
        )
    ''')

    print("✅ 表结构创建完成")
    print("\n🔧 创建推荐索引...")

    # 创建推荐的索引
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC)",
        "CREATE INDEX IF NOT EXISTS idx_posts_category_status_created ON posts(category_id, status, created_at DESC)",
        "CREATE INDEX IF NOT EXISTS idx_posts_author_status_created ON posts(author_id, status, created_at DESC)",
        "CREATE INDEX IF NOT EXISTS idx_posts_status_viewcount ON posts(status, view_count DESC)",
        "CREATE INDEX IF NOT EXISTS idx_posts_status_created_viewcount ON posts(status, created_at DESC, view_count DESC)",
        "CREATE INDEX IF NOT EXISTS idx_posts_title ON posts(title)",
        "CREATE INDEX IF NOT EXISTS idx_post_tags_tag_post ON post_tags(tag_id, post_id)",
        "CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name)"
    ]

    for idx_sql in indexes:
        cursor.execute(idx_sql)

    conn.commit()
    print("✅ 所有推荐索引创建完成")


def demonstrate_index_effectiveness(conn: sqlite3.Connection) -> None:
    """
    演示索引的有效性

    Args:
        conn: 数据库连接
    """
    cursor = conn.cursor()

    print("\n🔍 索引有效性演示:")

    # 插入一些测试数据
    cursor.execute("INSERT INTO authors (username, email, display_name) VALUES ('john_doe', 'john@example.com', 'John Doe')")
    cursor.execute("INSERT INTO categories (name, slug, description) VALUES ('Technology', 'tech', 'Tech articles')")
    cursor.execute("INSERT INTO tags (name, slug) VALUES ('python', 'python')")

    # 插入多篇文章
    for i in range(100):
        cursor.execute('''
            INSERT INTO posts (title, slug, content, status, author_id, category_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            f"Article {i}",
            f"article-{i}",
            f"Content of article {i}",
            "published" if i % 2 == 0 else "draft",
            1,
            1,
            f"2026-04-{20 + (i % 10):02d} 12:00:00"
        ))

    cursor.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (1, 1)")
    conn.commit()

    # 测试各种查询的执行计划
    test_queries = [
        ("按分类获取已发布文章", "SELECT * FROM posts WHERE category_id = 1 AND status = 'published' ORDER BY created_at DESC"),
        ("按作者获取文章", "SELECT * FROM posts WHERE author_id = 1 ORDER BY created_at DESC"),
        ("热门已发布文章", "SELECT * FROM posts WHERE status = 'published' ORDER BY view_count DESC LIMIT 10"),
        ("标题搜索", "SELECT * FROM posts WHERE title LIKE '%Article 50%' AND status = 'published'")
    ]

    for desc, query in test_queries:
        print(f"\n{desc}:")
        cursor.execute(f"EXPLAIN QUERY PLAN {query}")
        plan = cursor.fetchall()
        print(f"  执行计划: {plan}")


def evaluate_index_strategy() -> None:
    """
    评估索引策略
    """
    print("\n📊 索引策略评估:")
    print("覆盖的查询场景:")
    print("  ✅ 文章检索（ID、slug、最新）")
    print("  ✅ 分类浏览（带状态过滤和排序）")
    print("  ✅ 作者文章（带状态过滤和排序）")
    print("  ✅ 热门内容（按浏览量排序）")
    print("  ✅ 标签搜索（通过关联表优化）")

    print("\n优化考虑:")
    print("  🔹 复合索引顺序：高选择性列在前，排序列在后")
    print("  🔹 覆盖常用查询模式，避免过度索引")
    print("  🔹 考虑写操作频率（博客主要是读多写少）")
    print("  🔹 为JOIN操作优化关联表索引")

    print("\n潜在改进:")
    print("  ⚠️ 对于全文搜索，可能需要专门的搜索引擎（如Elasticsearch）")
    print("  ⚠️ 如果标签搜索非常频繁，可以考虑反规范化")
    print("  ⚠️ 监控实际查询性能，根据使用模式调整索引")


def main():
    """主函数：运行博客索引策略分析"""
    print("📝 博客系统索引策略分析")
    print("=" * 50)

    # 分析查询模式
    patterns = analyze_blog_query_patterns()
    print("📋 识别的查询模式:")
    total_queries = 0
    for category, queries in patterns.items():
        print(f"  {category}: {len(queries)} 个查询模式")
        total_queries += len(queries)
    print(f"  总计: {total_queries} 个查询模式")

    # 推荐索引策略
    recommendations = recommend_blog_indexes()
    print(f"\n🎯 推荐 {len(recommendations)} 个索引:")

    for i, rec in enumerate(recommendations, 1):
        columns_str = ", ".join(rec["columns"])
        print(f"  {i}. {rec['table']}.{columns_str} ({rec['type']})")
        print(f"     原因: {rec['reason']}")

    # 创建数据库并演示
    conn = sqlite3.connect(':memory:')
    try:
        create_blog_schema_with_indexes(conn)
        demonstrate_index_effectiveness(conn)
        evaluate_index_strategy()
    finally:
        conn.close()

    print("\n💡 结论:")
    print("博客系统作为典型的读多写少应用，合理的索引设计可以显著提升用户体验。")
    print("关键是在查询性能和维护开销之间找到平衡点。")


if __name__ == "__main__":
    main()