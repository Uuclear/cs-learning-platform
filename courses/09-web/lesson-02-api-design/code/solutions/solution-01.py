#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1: 完整的博客API系统

这是一个功能完整的博客API实现，包含:
- 用户注册和登录 (JWT认证)
- 文章CRUD操作
- 评论功能
- 分页支持
- 完善的错误处理
- 输入验证

运行方法:
1. 安装依赖: pip install flask pyjwt
2. 运行脚本: python3 solution-01.py
3. 按照说明测试完整功能
"""

import re
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from functools import wraps

# 尝试导入必要的库
try:
    from flask import Flask, request, jsonify
    import jwt
except ImportError as e:
    missing_package = "pyjwt" if "jwt" in str(e) else "flask"
    print(f"❌ 错误: {missing_package} 未安装！")
    print("请运行以下命令安装所有依赖:")
    print("pip install flask pyjwt")
    exit(1)

# 创建Flask应用实例
app = Flask(__name__)

# JWT配置
JWT_SECRET_KEY = "blog-api-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = 7200  # 2小时

# 模拟数据库
users_db: List[Dict] = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123",  # 实际应用中应该哈希存储
        "role": "admin",
        "created_at": "2026-05-01T00:00:00Z"
    }
]

posts_db: List[Dict] = [
    {
        "id": 1,
        "title": "欢迎来到博客API",
        "content": "这是我们的第一篇博客文章，演示完整的API功能。",
        "author_id": 1,
        "created_at": "2026-05-01T10:00:00Z",
        "updated_at": "2026-05-01T10:00:00Z"
    }
]

comments_db: List[Dict] = [
    {
        "id": 1,
        "content": "很棒的文章！",
        "post_id": 1,
        "author_id": 1,
        "created_at": "2026-05-01T10:30:00Z"
    }
]

next_user_id = 2
next_post_id = 2
next_comment_id = 2


# ==================== 工具函数 ====================

def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def generate_jwt_token(user_id: int, username: str, role: str = "user") -> str:
    """生成JWT Token"""
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": time.time() + JWT_EXPIRATION_DELTA,
        "iat": time.time()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str) -> Optional[Dict]:
    """验证JWT Token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "error": {"code": "UNAUTHORIZED", "message": "需要有效的访问令牌"}
            }), 401

        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({
                "error": {"code": "INVALID_TOKEN", "message": "无效或过期的访问令牌"}
            }), 401

        request.current_user = payload
        return f(*args, **kwargs)
    return decorated_function


def require_admin(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 先确保用户已认证
        auth_result = require_auth(f)(*args, **kwargs)
        if hasattr(request, 'current_user'):
            if request.current_user.get('role') != 'admin':
                return jsonify({
                    "error": {"code": "FORBIDDEN", "message": "需要管理员权限"}
                }), 403
        return auth_result
    return decorated_function


def create_error_response(code: str, message: str, status_code: int, details: Dict = None) -> tuple:
    """创建标准化错误响应"""
    error_data = {"error": {"code": code, "message": message}}
    if details:
        error_data["error"]["details"] = details
    return jsonify(error_data), status_code


def paginate_list(items: List, limit: int, offset: int) -> Dict:
    """分页工具函数"""
    total = len(items)
    paginated_items = items[offset:offset + limit]
    return {
        "items": paginated_items,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total
        }
    }


# ==================== 用户相关API ====================

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()

    # 验证输入
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data or field not in data:
            return create_error_response(
                "VALIDATION_ERROR",
                f"缺少必需字段: {field}",
                400,
                {"field": field}
            )

    username = data['username'].strip()
    email = data['email'].strip()
    password = data['password']

    # 验证用户名
    if len(username) < 3 or len(username) > 20:
        return create_error_response(
            "VALIDATION_ERROR",
            "用户名长度必须在3-20个字符之间",
            400,
            {"field": "username"}
        )

    # 验证邮箱
    if not validate_email(email):
        return create_error_response(
            "VALIDATION_ERROR",
            "邮箱格式无效",
            400,
            {"field": "email", "value": email}
        )

    # 验证密码
    if len(password) < 6:
        return create_error_response(
            "VALIDATION_ERROR",
            "密码长度至少6位",
            400,
            {"field": "password"}
        )

    # 检查用户名和邮箱是否已存在
    for user in users_db:
        if user['username'] == username:
            return create_error_response(
                "USERNAME_EXISTS",
                "用户名已存在",
                400,
                {"field": "username", "value": username}
            )
        if user['email'] == email:
            return create_error_response(
                "EMAIL_EXISTS",
                "邮箱已被注册",
                400,
                {"field": "email", "value": email}
            )

    # 创建新用户
    global next_user_id
    new_user = {
        "id": next_user_id,
        "username": username,
        "email": email,
        "password": password,  # 实际应用中应哈希
        "role": "user",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    users_db.append(new_user)
    next_user_id += 1

    return jsonify({
        "message": "用户注册成功",
        "user": {
            "id": new_user["id"],
            "username": new_user["username"],
            "email": new_user["email"],
            "role": new_user["role"],
            "created_at": new_user["created_at"]
        }
    }), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return create_error_response(
            "VALIDATION_ERROR",
            "缺少必需字段: username 和 password",
            400
        )

    username = data['username']
    password = data['password']

    # 查找用户并验证密码
    user = None
    for u in users_db:
        if u['username'] == username and u['password'] == password:
            user = u
            break

    if not user:
        return create_error_response(
            "INVALID_CREDENTIALS",
            "用户名或密码错误",
            401
        )

    # 生成JWT Token
    access_token = generate_jwt_token(user['id'], user['username'], user['role'])

    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": JWT_EXPIRATION_DELTA,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


# ==================== 文章相关API ====================

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    """获取文章列表（支持分页和过滤）"""
    try:
        # 解析查询参数
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        author_id = request.args.get('author_id', default=None, type=int)

        # 验证分页参数
        if limit < 1 or limit > 50:
            return create_error_response(
                "INVALID_PARAMETER",
                "limit参数必须在1-50之间",
                400,
                {"parameter": "limit"}
            )
        if offset < 0:
            return create_error_response(
                "INVALID_PARAMETER",
                "offset参数不能为负数",
                400,
                {"parameter": "offset"}
            )

        # 过滤文章
        filtered_posts = posts_db
        if author_id:
            filtered_posts = [post for post in posts_db if post['author_id'] == author_id]

        # 分页
        result = paginate_list(filtered_posts, limit, offset)

        return jsonify({
            "posts": result["items"],
            "pagination": result["pagination"]
        }), 200

    except ValueError:
        return create_error_response(
            "INVALID_PARAMETER",
            "查询参数类型错误",
            400
        )


@app.route('/api/v1/posts', methods=['POST'])
@require_auth
def create_post():
    """创建新文章"""
    data = request.get_json()

    if not data or 'title' not in data or 'content' not in data:
        return create_error_response(
            "VALIDATION_ERROR",
            "缺少必需字段: title 和 content",
            400
        )

    title = data['title'].strip()
    content = data['content'].strip()

    if len(title) == 0 or len(title) > 100:
        return create_error_response(
            "VALIDATION_ERROR",
            "标题不能为空且长度不能超过100个字符",
            400,
            {"field": "title"}
        )

    if len(content) == 0:
        return create_error_response(
            "VALIDATION_ERROR",
            "内容不能为空",
            400,
            {"field": "content"}
        )

    # 创建新文章
    global next_post_id
    current_user = request.current_user
    new_post = {
        "id": next_post_id,
        "title": title,
        "content": content,
        "author_id": current_user['user_id'],
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    posts_db.append(new_post)
    next_post_id += 1

    return jsonify({
        "message": "文章创建成功",
        "post": new_post
    }), 201


@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def get_post(post_id: int):
    """获取单篇文章"""
    post = None
    for p in posts_db:
        if p['id'] == post_id:
            post = p
            break

    if not post:
        return create_error_response(
            "POST_NOT_FOUND",
            f"文章ID {post_id} 不存在",
            404,
            {"post_id": post_id}
        )

    return jsonify({"post": post}), 200


@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
@require_auth
def update_post(post_id: int):
    """更新文章"""
    # 查找文章
    post_index = None
    for i, p in enumerate(posts_db):
        if p['id'] == post_id:
            post_index = i
            break

    if post_index is None:
        return create_error_response(
            "POST_NOT_FOUND",
            f"文章ID {post_id} 不存在",
            404,
            {"post_id": post_id}
        )

    # 检查权限（只有作者或管理员可以编辑）
    current_user = request.current_user
    if (posts_db[post_index]['author_id'] != current_user['user_id'] and
        current_user['role'] != 'admin'):
        return create_error_response(
            "FORBIDDEN",
            "只能编辑自己的文章",
            403
        )

    # 验证输入
    data = request.get_json()
    if not data:
        return create_error_response(
            "VALIDATION_ERROR",
            "请求体不能为空",
            400
        )

    # 更新字段
    if 'title' in data:
        title = data['title'].strip()
        if len(title) == 0 or len(title) > 100:
            return create_error_response(
                "VALIDATION_ERROR",
                "标题不能为空且长度不能超过100个字符",
                400,
                {"field": "title"}
            )
        posts_db[post_index]['title'] = title

    if 'content' in data:
        content = data['content'].strip()
        if len(content) == 0:
            return create_error_response(
                "VALIDATION_ERROR",
                "内容不能为空",
                400,
                {"field": "content"}
            )
        posts_db[post_index]['content'] = content

    posts_db[post_index]['updated_at'] = datetime.utcnow().isoformat() + "Z"

    return jsonify({
        "message": "文章更新成功",
        "post": posts_db[post_index]
    }), 200


@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
@require_auth
def delete_post(post_id: int):
    """删除文章"""
    # 查找文章
    post_index = None
    for i, p in enumerate(posts_db):
        if p['id'] == post_id:
            post_index = i
            break

    if post_index is None:
        return create_error_response(
            "POST_NOT_FOUND",
            f"文章ID {post_id} 不存在",
            404,
            {"post_id": post_id}
        )

    # 检查权限（只有作者或管理员可以删除）
    current_user = request.current_user
    if (posts_db[post_index]['author_id'] != current_user['user_id'] and
        current_user['role'] != 'admin'):
        return create_error_response(
            "FORBIDDEN",
            "只能删除自己的文章",
            403
        )

    # 删除文章和相关评论
    deleted_post = posts_db.pop(post_index)
    global comments_db
    comments_db = [c for c in comments_db if c['post_id'] != post_id]

    return jsonify({
        "message": f"文章 '{deleted_post['title']}' 删除成功"
    }), 200


# ==================== 评论相关API ====================

@app.route('/api/v1/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id: int):
    """获取文章的评论列表"""
    # 验证文章是否存在
    post_exists = any(p['id'] == post_id for p in posts_db)
    if not post_exists:
        return create_error_response(
            "POST_NOT_FOUND",
            f"文章ID {post_id} 不存在",
            404,
            {"post_id": post_id}
        )

    # 获取该文章的评论
    post_comments = [c for c in comments_db if c['post_id'] == post_id]

    # 分页
    limit = request.args.get('limit', default=20, type=int)
    offset = request.args.get('offset', default=0, type=int)

    if limit < 1 or limit > 50:
        limit = 20
    if offset < 0:
        offset = 0

    result = paginate_list(post_comments, limit, offset)

    return jsonify({
        "comments": result["items"],
        "pagination": result["pagination"]
    }), 200


@app.route('/api/v1/posts/<int:post_id>/comments', methods=['POST'])
@require_auth
def create_comment(post_id: int):
    """创建评论"""
    # 验证文章是否存在
    post_exists = any(p['id'] == post_id for p in posts_db)
    if not post_exists:
        return create_error_response(
            "POST_NOT_FOUND",
            f"文章ID {post_id} 不存在",
            404,
            {"post_id": post_id}
        )

    data = request.get_json()
    if not data or 'content' not in data:
        return create_error_response(
            "VALIDATION_ERROR",
            "缺少必需字段: content",
            400
        )

    content = data['content'].strip()
    if len(content) == 0 or len(content) > 500:
        return create_error_response(
            "VALIDATION_ERROR",
            "评论内容不能为空且长度不能超过500个字符",
            400,
            {"field": "content"}
        )

    # 创建新评论
    global next_comment_id
    current_user = request.current_user
    new_comment = {
        "id": next_comment_id,
        "content": content,
        "post_id": post_id,
        "author_id": current_user['user_id'],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    comments_db.append(new_comment)
    next_comment_id += 1

    return jsonify({
        "message": "评论创建成功",
        "comment": new_comment
    }), 201


# ==================== 错误处理 ====================

@app.errorhandler(404)
def handle_404(error):
    return create_error_response(
        "ENDPOINT_NOT_FOUND",
        "API端点不存在",
        404
    )


@app.errorhandler(405)
def handle_405(error):
    return create_error_response(
        "METHOD_NOT_ALLOWED",
        "该端点不支持此HTTP方法",
        405
    )


@app.errorhandler(500)
def handle_500(error):
    app.logger.error(f"服务器内部错误: {str(error)}")
    return create_error_response(
        "INTERNAL_ERROR",
        "服务器内部错误，请稍后再试",
        500
    )


if __name__ == '__main__':
    print("📚 启动完整的博客API服务器...")
    print("📝 API端点概览:")
    print("\n用户认证:")
    print("  POST /api/v1/auth/register  - 用户注册")
    print("  POST /api/v1/auth/login     - 用户登录")
    print("\n文章管理:")
    print("  GET    /api/v1/posts         - 获取文章列表")
    print("  POST   /api/v1/posts         - 创建文章")
    print("  GET    /api/v1/posts/<id>    - 获取单篇文章")
    print("  PUT    /api/v1/posts/<id>    - 更新文章")
    print("  DELETE /api/v1/posts/<id>    - 删除文章")
    print("\n评论管理:")
    print("  GET  /api/v1/posts/<id>/comments - 获取评论列表")
    print("  POST /api/v1/posts/<id>/comments - 创建评论")
    print("\n💡 使用流程:")
    print("  1. 注册用户: POST /api/v1/auth/register")
    print("  2. 登录获取Token: POST /api/v1/auth/login")
    print("  3. 使用Token创建文章: POST /api/v1/posts")
    print("  4. 为文章添加评论: POST /api/v1/posts/1/comments")
    print("\n🌐 服务器运行在: http://localhost:5000/api/v1")
    print("⏹️  按 Ctrl+C 停止服务器\n")

    app.run(debug=True, host='0.0.0.0', port=5000)