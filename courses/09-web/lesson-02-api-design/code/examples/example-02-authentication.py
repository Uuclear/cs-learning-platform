#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2: JWT认证API

这个示例演示了如何在Flask API中实现JWT(JSON Web Token)认证，
保护敏感的API端点，确保只有经过身份验证的用户才能访问。

运行方法:
1. 安装依赖: pip install flask pyjwt
2. 运行脚本: python3 example-02-authentication.py
3. 测试认证流程

示例请求和预期响应:
=====================

# 1. 用户注册 (POST /auth/register)
curl -X POST http://localhost:5000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "alice", "password": "secret123"}'
响应: {"message": "用户注册成功", "user": {"username": "alice"}}

# 2. 用户登录获取Token (POST /auth/login)
curl -X POST http://localhost:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "alice", "password": "secret123"}'
响应: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}

# 3. 使用Token访问受保护的资源 (GET /protected)
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     http://localhost:5000/protected
响应: {"message": "欢迎, alice! 这是受保护的内容。"}

# 4. 无Token访问受保护资源 (应该失败)
curl http://localhost:5000/protected
响应: {"error": "认证失败: 缺少访问令牌"} (状态码: 401)
"""

import json
import time
from typing import Dict, Optional
from functools import wraps

# 尝试导入必要的库
try:
    from flask import Flask, request, jsonify
    import jwt  # PyJWT库用于处理JWT
except ImportError as e:
    missing_package = "pyjwt" if "jwt" in str(e) else "flask"
    print(f"❌ 错误: {missing_package} 未安装！")
    print("请运行以下命令安装所有依赖:")
    print("pip install flask pyjwt")
    print("\n安装完成后重新运行此脚本。")
    exit(1)

# 创建Flask应用实例
app = Flask(__name__)

# 密钥用于JWT签名 - 在生产环境中应该使用更安全的密钥管理
JWT_SECRET_KEY = "your-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = 3600  # Token有效期1小时 (秒)

# 模拟用户数据库 - 实际应用中应使用真正的数据库和密码哈希
users_db: Dict[str, str] = {
    "admin": "admin123",  # username: password
}

# 模拟受保护的数据
protected_data = {
    "secret_info": "这是只有认证用户才能看到的秘密信息！"
}


def generate_jwt_token(username: str) -> str:
    """
    生成JWT Token

    参数:
        username (str): 用户名

    返回:
        str: JWT Token字符串
    """
    payload = {
        "username": username,
        "exp": time.time() + JWT_EXPIRATION_DELTA,  # 过期时间
        "iat": time.time()  # 签发时间
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt_token(token: str) -> Optional[Dict]:
    """
    验证JWT Token

    参数:
        token (str): JWT Token字符串

    返回:
        dict 或 None: 如果验证成功返回payload，否则返回None
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token已过期
    except jwt.InvalidTokenError:
        return None  # Token无效


def require_auth(f):
    """
    装饰器：保护需要认证的API端点

    使用方法: 在需要认证的路由函数上添加 @require_auth
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从Authorization头中获取Token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                "error": "认证失败: 缺少访问令牌"
            }), 401

        # 验证Bearer Token格式
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": "认证失败: 无效的令牌格式，应为 'Bearer <token>'"
            }), 401

        token = auth_header.split(' ')[1]  # 提取Token部分

        # 验证Token
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({
                "error": "认证失败: 无效或过期的访问令牌"
            }), 401

        # 将用户名添加到请求上下文中（可选）
        request.current_user = payload['username']

        return f(*args, **kwargs)

    return decorated_function


@app.route('/auth/register', methods=['POST'])
def register():
    """
    用户注册端点

    HTTP方法: POST
    URL: /auth/register
    请求体: { "username": "用户名", "password": "密码" }
    返回: 注册结果
    状态码: 201 (成功) 或 400 (用户名已存在/输入错误)
    """
    data = request.get_json()

    # 验证输入
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "error": "缺少必需字段: username 和 password"
        }), 400

    username = data['username']
    password = data['password']

    # 检查用户名是否已存在
    if username in users_db:
        return jsonify({
            "error": "用户名已存在，请选择其他用户名"
        }), 400

    # 保存用户（实际应用中应该哈希密码）
    users_db[username] = password

    return jsonify({
        "message": "用户注册成功",
        "user": {"username": username}
    }), 201


@app.route('/auth/login', methods=['POST'])
def login():
    """
    用户登录端点 - 返回JWT Token

    HTTP方法: POST
    URL: /auth/login
    请求体: { "username": "用户名", "password": "密码" }
    返回: JWT Token
    状态码: 200 (成功) 或 401 (认证失败)
    """
    data = request.get_json()

    # 验证输入
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({
            "error": "缺少必需字段: username 和 password"
        }), 400

    username = data['username']
    password = data['password']

    # 验证用户凭据
    if username not in users_db or users_db[username] != password:
        return jsonify({
            "error": "用户名或密码错误"
        }), 401

    # 生成JWT Token
    access_token = generate_jwt_token(username)

    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": JWT_EXPIRATION_DELTA
    }), 200


@app.route('/protected', methods=['GET'])
@require_auth
def protected_resource():
    """
    受保护的资源端点 - 需要有效的JWT Token才能访问

    HTTP方法: GET
    URL: /protected
    头部: Authorization: Bearer <token>
    返回: 受保护的数据
    状态码: 200 (成功) 或 401 (认证失败)
    """
    current_user = getattr(request, 'current_user', 'unknown')

    return jsonify({
        "message": f"欢迎, {current_user}! 这是受保护的内容。",
        "data": protected_data
    }), 200


@app.route('/public', methods=['GET'])
def public_resource():
    """
    公共资源端点 - 不需要认证即可访问

    HTTP方法: GET
    URL: /public
    返回: 公共信息
    状态码: 200
    """
    return jsonify({
        "message": "这是公共内容，任何人都可以访问！",
        "info": "要访问受保护的内容，请先登录获取Token。"
    }), 200


@app.errorhandler(404)
def not_found(error):
    """处理404错误"""
    return jsonify({
        "error": "API端点不存在"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """处理500错误"""
    return jsonify({
        "error": "服务器内部错误"
    }), 500


if __name__ == '__main__':
    print("🔐 启动JWT认证API服务器...")
    print("📝 可用的API端点:")
    print("   POST /auth/register  - 用户注册")
    print("   POST /auth/login     - 用户登录 (获取Token)")
    print("   GET  /public         - 公共资源 (无需认证)")
    print("   GET  /protected      - 受保护资源 (需要Token)")
    print("\n💡 使用说明:")
    print("   1. 先注册用户: POST /auth/register")
    print("   2. 登录获取Token: POST /auth/login")
    print("   3. 使用Token访问受保护资源: GET /protected")
    print("   4. Token格式: Authorization: Bearer <your-token>")
    print("\n🌐 服务器运行在: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止服务器\n")

    app.run(debug=True, host='0.0.0.0', port=5000)