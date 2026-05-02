#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1: 基础REST API - 博客文章管理

这个示例演示了如何使用Flask创建一个简单的RESTful API，
支持对博客文章的增删改查(CRUD)操作。

运行方法:
1. 安装Flask: pip install flask
2. 运行脚本: python3 example-01-rest-api-basics.py
3. 在另一个终端测试API调用

示例请求和预期响应:
=====================

# 1. 获取所有文章 (GET /posts)
curl http://localhost:5000/posts
响应: {"posts": [{"id": 1, "title": "第一篇文章", "content": "这是内容..."}]}

# 2. 创建新文章 (POST /posts)
curl -X POST http://localhost:5000/posts \
     -H "Content-Type: application/json" \
     -d '{"title": "新文章", "content": "新内容"}'
响应: {"message": "文章创建成功", "post": {"id": 2, "title": "新文章", "content": "新内容"}}

# 3. 获取单篇文章 (GET /posts/1)
curl http://localhost:5000/posts/1
响应: {"post": {"id": 1, "title": "第一篇文章", "content": "这是内容..."}}

# 4. 更新文章 (PUT /posts/1)
curl -X PUT http://localhost:5000/posts/1 \
     -H "Content-Type: application/json" \
     -d '{"title": "更新后的标题", "content": "更新后的内容"}'
响应: {"message": "文章更新成功", "post": {"id": 1, "title": "更新后的标题", "content": "更新后的内容"}}

# 5. 删除文章 (DELETE /posts/1)
curl -X DELETE http://localhost:5000/posts/1
响应: {"message": "文章删除成功"}
"""

import json
from typing import Dict, List, Optional

# 尝试导入Flask，如果未安装则显示友好错误信息
try:
    from flask import Flask, request, jsonify
except ImportError:
    print("❌ 错误: Flask 未安装！")
    print("请运行以下命令安装Flask:")
    print("pip install flask")
    print("\n安装完成后重新运行此脚本。")
    exit(1)

# 创建Flask应用实例
app = Flask(__name__)

# 模拟数据库 - 在实际应用中应该使用真正的数据库
posts_db: List[Dict] = [
    {
        "id": 1,
        "title": "第一篇文章",
        "content": "这是我们的第一篇博客文章，欢迎来到API世界！"
    },
    {
        "id": 2,
        "title": "API设计基础",
        "content": "好的API设计应该简洁、一致且易于理解。"
    }
]

# 全局ID计数器
next_id = 3


@app.route('/posts', methods=['GET'])
def get_posts():
    """
    获取所有文章列表

    HTTP方法: GET
    URL: /posts
    返回: 包含所有文章的JSON数组
    状态码: 200 OK
    """
    return jsonify({
        "posts": posts_db
    }), 200


@app.route('/posts', methods=['POST'])
def create_post():
    """
    创建新文章

    HTTP方法: POST
    URL: /posts
    请求体: JSON格式 { "title": "标题", "content": "内容" }
    返回: 创建成功的文章信息
    状态码: 201 Created (成功) 或 400 Bad Request (输入错误)
    """
    # 获取请求数据
    data = request.get_json()

    # 验证必需字段
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({
            "error": "缺少必需字段: title 和 content"
        }), 400

    # 创建新文章
    global next_id
    new_post = {
        "id": next_id,
        "title": data['title'],
        "content": data['content']
    }
    posts_db.append(new_post)
    next_id += 1

    return jsonify({
        "message": "文章创建成功",
        "post": new_post
    }), 201


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id: int):
    """
    获取单篇文章

    HTTP方法: GET
    URL: /posts/<post_id>
    参数: post_id (URL路径参数)
    返回: 单篇文章信息或错误信息
    状态码: 200 OK (找到) 或 404 Not Found (未找到)
    """
    # 查找文章
    post = None
    for p in posts_db:
        if p['id'] == post_id:
            post = p
            break

    if post is None:
        return jsonify({
            "error": f"文章 ID {post_id} 不存在"
        }), 404

    return jsonify({
        "post": post
    }), 200


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id: int):
    """
    更新文章

    HTTP方法: PUT
    URL: /posts/<post_id>
    请求体: JSON格式 { "title": "新标题", "content": "新内容" }
    返回: 更新后的文章信息或错误信息
    状态码: 200 OK (成功) 或 400/404 (错误)
    """
    # 查找文章
    post_index = None
    for i, p in enumerate(posts_db):
        if p['id'] == post_id:
            post_index = i
            break

    if post_index is None:
        return jsonify({
            "error": f"文章 ID {post_id} 不存在"
        }), 404

    # 获取请求数据
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "请求体不能为空"
        }), 400

    # 更新文章
    if 'title' in data:
        posts_db[post_index]['title'] = data['title']
    if 'content' in data:
        posts_db[post_index]['content'] = data['content']

    return jsonify({
        "message": "文章更新成功",
        "post": posts_db[post_index]
    }), 200


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id: int):
    """
    删除文章

    HTTP方法: DELETE
    URL: /posts/<post_id>
    返回: 成功消息或错误信息
    状态码: 200 OK (成功) 或 404 Not Found (未找到)
    """
    # 查找并删除文章
    post_index = None
    for i, p in enumerate(posts_db):
        if p['id'] == post_id:
            post_index = i
            break

    if post_index is None:
        return jsonify({
            "error": f"文章 ID {post_id} 不存在"
        }), 404

    # 删除文章
    deleted_post = posts_db.pop(post_index)

    return jsonify({
        "message": f"文章 '{deleted_post['title']}' 删除成功"
    }), 200


@app.errorhandler(404)
def not_found(error):
    """处理404错误 - 请求的端点不存在"""
    return jsonify({
        "error": "API端点不存在，请检查URL是否正确"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """处理500错误 - 服务器内部错误"""
    return jsonify({
        "error": "服务器内部错误，请稍后再试"
    }), 500


if __name__ == '__main__':
    print("🚀 启动博客API服务器...")
    print("📝 可用的API端点:")
    print("   GET    /posts          - 获取所有文章")
    print("   POST   /posts          - 创建新文章")
    print("   GET    /posts/<id>     - 获取单篇文章")
    print("   PUT    /posts/<id>     - 更新文章")
    print("   DELETE /posts/<id>     - 删除文章")
    print("\n💡 测试提示: 在另一个终端使用curl命令测试API")
    print("🌐 服务器运行在: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止服务器\n")

    # 启动开发服务器
    app.run(debug=True, host='0.0.0.0', port=5000)