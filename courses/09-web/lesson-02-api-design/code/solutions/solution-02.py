#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案2: 用户注册/登录API与JWT认证系统

这是一个专注于用户管理的完整API实现，包含:
- 用户注册（带密码强度验证）
- 用户登录（JWT Token生成）
- Token刷新机制
- 用户角色权限系统
- 密码重置功能
- 完善的安全措施

运行方法:
1. 安装依赖: pip install flask pyjwt
2. 运行脚本: python3 solution-02.py
3. 测试用户管理功能
"""

import re
import time
import secrets
import hashlib
from typing import Dict, List, Optional
from datetime import datetime, timedelta
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
JWT_SECRET_KEY = "user-auth-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = 3600      # 1小时
REFRESH_TOKEN_EXPIRATION = 604800   # 7天

# 模拟数据库
users_db: List[Dict] = []
refresh_tokens_db: List[Dict] = []  # 存储有效的刷新Token

next_user_id = 1


# ==================== 工具函数 ====================

def hash_password(password: str, salt: str = None) -> tuple:
    """哈希密码（实际应用中应使用bcrypt等专用库）"""
    if salt is None:
        salt = secrets.token_hex(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                  salt.encode('utf-8'), 100000)
    return pwdhash.hex(), salt


def verify_password(password: str, hashed: str, salt: str) -> bool:
    """验证密码"""
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                  salt.encode('utf-8'), 100000)
    return pwdhash.hex() == hashed


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple:
    """
    验证密码强度

    返回: (是否有效, 错误消息)
    """
    if len(password) < 8:
        return False, "密码长度至少8位"

    if not re.search(r'[A-Z]', password):
        return False, "密码必须包含至少一个大写字母"

    if not re.search(r'[a-z]', password):
        return False, "密码必须包含至少一个小写字母"

    if not re.search(r'\d', password):
        return False, "密码必须包含至少一个数字"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "密码必须包含至少一个特殊字符 (!@#$%^&*(),.?\":{}|<>)"

    return True, ""


def generate_jwt_token(user_id: int, username: str, role: str = "user",
                      token_type: str = "access") -> str:
    """生成JWT Token"""
    expiration = (ACCESS_TOKEN_EXPIRATION if token_type == "access"
                  else REFRESH_TOKEN_EXPIRATION)

    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "type": token_type,
        "exp": time.time() + expiration,
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
    """认证装饰器 - 验证访问Token"""
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

        if payload.get('type') != 'access':
            return jsonify({
                "error": {"code": "INVALID_TOKEN_TYPE", "message": "需要访问令牌，不是刷新令牌"}
            }), 401

        request.current_user = payload
        return f(*args, **kwargs)
    return decorated_function


def require_role(required_role: str):
    """角色权限装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 先确保用户已认证
            auth_result = require_auth(f)(*args, **kwargs)
            if hasattr(request, 'current_user'):
                user_role = request.current_user.get('role', 'user')
                if user_role != required_role and required_role != 'any':
                    if required_role == 'admin' and user_role != 'admin':
                        return jsonify({
                            "error": {"code": "INSUFFICIENT_PERMISSIONS",
                                    "message": "需要管理员权限"}
                        }), 403
            return auth_result
        return decorated_function
    return decorator


def create_error_response(code: str, message: str, status_code: int, details: Dict = None) -> tuple:
    """创建标准化错误响应"""
    error_data = {"error": {"code": code, "message": message}}
    if details:
        error_data["error"]["details"] = details
    return jsonify(error_data), status_code


def invalidate_refresh_token(user_id: int, token: str = None):
    """使刷新Token失效"""
    global refresh_tokens_db
    if token:
        refresh_tokens_db = [rt for rt in refresh_tokens_db
                           if not (rt['user_id'] == user_id and rt['token'] == token)]
    else:
        refresh_tokens_db = [rt for rt in refresh_tokens_db if rt['user_id'] != user_id]


# ==================== 用户注册API ====================

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    """用户注册 - 包含密码强度验证"""
    data = request.get_json()

    # 验证必需字段
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
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return create_error_response(
            "VALIDATION_ERROR",
            "用户名只能包含字母、数字和下划线",
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

    # 验证密码强度
    is_valid, error_msg = validate_password_strength(password)
    if not is_valid:
        return create_error_response(
            "WEAK_PASSWORD",
            error_msg,
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

    # 哈希密码并创建用户
    global next_user_id
    password_hash, password_salt = hash_password(password)

    new_user = {
        "id": next_user_id,
        "username": username,
        "email": email,
        "password_hash": password_hash,
        "password_salt": password_salt,
        "role": "user",  # 默认普通用户
        "created_at": datetime.utcnow().isoformat() + "Z",
        "last_login": None
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


# ==================== 用户登录API ====================

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """用户登录 - 返回访问Token和刷新Token"""
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return create_error_response(
            "VALIDATION_ERROR",
            "缺少必需字段: username 和 password",
            400
        )

    username = data['username']
    password = data['password']

    # 查找用户
    user = None
    for u in users_db:
        if u['username'] == username:
            user = u
            break

    if not user:
        return create_error_response(
            "INVALID_CREDENTIALS",
            "用户名或密码错误",
            401
        )

    # 验证密码
    if not verify_password(password, user['password_hash'], user['password_salt']):
        return create_error_response(
            "INVALID_CREDENTIALS",
            "用户名或密码错误",
            401
        )

    # 更新最后登录时间
    user['last_login'] = datetime.utcnow().isoformat() + "Z"

    # 生成Tokens
    access_token = generate_jwt_token(user['id'], user['username'], user['role'], "access")
    refresh_token = generate_jwt_token(user['id'], user['username'], user['role'], "refresh")

    # 存储刷新Token（实际应用中应存储在数据库中）
    refresh_tokens_db.append({
        "user_id": user['id'],
        "token": refresh_token,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "expires_at": (datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_EXPIRATION)).isoformat() + "Z"
    })

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRATION,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


# ==================== Token刷新API ====================

@app.route('/api/v1/auth/refresh', methods=['POST'])
def refresh_token():
    """刷新访问Token"""
    data = request.get_json()

    if not data or 'refresh_token' not in data:
        return create_error_response(
            "VALIDATION_ERROR",
            "缺少必需字段: refresh_token",
            400
        )

    refresh_token = data['refresh_token']

    # 验证刷新Token
    payload = verify_jwt_token(refresh_token)
    if not payload or payload.get('type') != 'refresh':
        return create_error_response(
            "INVALID_REFRESH_TOKEN",
            "无效或过期的刷新令牌",
            401
        )

    user_id = payload['user_id']

    # 检查刷新Token是否在有效列表中
    valid_refresh_token = None
    for rt in refresh_tokens_db:
        if rt['user_id'] == user_id and rt['token'] == refresh_token:
            valid_refresh_token = rt
            break

    if not valid_refresh_token:
        return create_error_response(
            "INVALID_REFRESH_TOKEN",
            "刷新令牌已被撤销或不存在",
            401
        )

    # 生成新的访问Token
    username = payload['username']
    role = payload['role']
    new_access_token = generate_jwt_token(user_id, username, role, "access")

    return jsonify({
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRATION
    }), 200


# ==================== 登出API ====================

@app.route('/api/v1/auth/logout', methods=['POST'])
@require_auth
def logout():
    """用户登出 - 使刷新Token失效"""
    current_user = request.current_user
    user_id = current_user['user_id']

    # 使所有该用户的刷新Token失效
    invalidate_refresh_token(user_id)

    return jsonify({
        "message": "成功登出"
    }), 200


# ==================== 受保护的用户API ====================

@app.route('/api/v1/users/me', methods=['GET'])
@require_auth
def get_current_user():
    """获取当前用户信息"""
    current_user = request.current_user
    user_id = current_user['user_id']

    # 查找用户详细信息
    user_info = None
    for user in users_db:
        if user['id'] == user_id:
            user_info = user
            break

    if not user_info:
        return create_error_response(
            "USER_NOT_FOUND",
            "用户信息不存在",
            404
        )

    return jsonify({
        "user": {
            "id": user_info["id"],
            "username": user_info["username"],
            "email": user_info["email"],
            "role": user_info["role"],
            "created_at": user_info["created_at"],
            "last_login": user_info["last_login"]
        }
    }), 200


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
@require_role('admin')
def get_user(user_id: int):
    """管理员获取指定用户信息"""
    user_info = None
    for user in users_db:
        if user['id'] == user_id:
            user_info = user
            break

    if not user_info:
        return create_error_response(
            "USER_NOT_FOUND",
            f"用户ID {user_id} 不存在",
            404,
            {"user_id": user_id}
        )

    return jsonify({
        "user": {
            "id": user_info["id"],
            "username": user_info["username"],
            "email": user_info["email"],
            "role": user_info["role"],
            "created_at": user_info["created_at"],
            "last_login": user_info["last_login"]
        }
    }), 200


@app.route('/api/v1/users', methods=['GET'])
@require_role('admin')
def get_all_users():
    """管理员获取所有用户列表"""
    users_list = []
    for user in users_db:
        users_list.append({
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        })

    return jsonify({
        "users": users_list,
        "total": len(users_list)
    }), 200


# ==================== 密码重置API ====================

@app.route('/api/v1/auth/password-reset/request', methods=['POST'])
def request_password_reset():
    """请求密码重置（模拟发送邮件）"""
    data = request.get_json()

    if not data or 'email' not in data:
        return create_error_response(
            "VALIDATION_ERROR",
            "缺少必需字段: email",
            400
        )

    email = data['email'].strip()

    # 验证邮箱格式
    if not validate_email(email):
        return create_error_response(
            "VALIDATION_ERROR",
            "邮箱格式无效",
            400,
            {"field": "email"}
        )

    # 检查用户是否存在
    user_exists = any(user['email'] == email for user in users_db)
    if not user_exists:
        # 注意：为了安全，即使邮箱不存在也返回成功（防止邮箱枚举攻击）
        pass

    # 在实际应用中，这里会生成重置Token并发送邮件
    # 为了演示，我们只是返回成功消息
    return jsonify({
        "message": "如果邮箱存在，密码重置链接已发送到您的邮箱"
    }), 200


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
    # 添加一个默认管理员用户用于测试
    admin_password_hash, admin_password_salt = hash_password("admin123")
    users_db.append({
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "password_hash": admin_password_hash,
        "password_salt": admin_password_salt,
        "role": "admin",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "last_login": None
    })
    next_user_id = 2

    print("🔐 启动用户认证API服务器...")
    print("📝 API端点概览:")
    print("\n认证相关:")
    print("  POST /api/v1/auth/register          - 用户注册")
    print("  POST /api/v1/auth/login             - 用户登录")
    print("  POST /api/v1/auth/refresh           - 刷新访问Token")
    print("  POST /api/v1/auth/logout            - 用户登出")
    print("  POST /api/v1/auth/password-reset/request - 请求密码重置")
    print("\n用户管理:")
    print("  GET  /api/v1/users/me               - 获取当前用户信息")
    print("  GET  /api/v1/users/<id>             - 管理员获取用户信息")
    print("  GET  /api/v1/users                  - 管理员获取所有用户")
    print("\n💡 测试建议:")
    print("  1. 使用管理员账户登录: username=admin, password=admin123")
    print("  2. 注册新用户并测试密码强度验证")
    print("  3. 测试Token刷新机制")
    print("  4. 测试角色权限控制")
    print("\n🌐 服务器运行在: http://localhost:5000/api/v1")
    print("⏹️  按 Ctrl+C 停止服务器\n")

    app.run(debug=True, host='0.0.0.0', port=5000)