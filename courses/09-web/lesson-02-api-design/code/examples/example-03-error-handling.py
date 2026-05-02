#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: API错误处理和验证

这个示例演示了如何在Flask API中实现完善的错误处理、
输入验证和标准化的错误响应格式。

运行方法:
1. 安装Flask: pip install flask
2. 运行脚本: python3 example-03-error-handling.py
3. 测试各种错误场景

示例请求和预期响应:
=====================

# 1. 正常创建用户 (POST /users)
curl -X POST http://localhost:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "张三", "email": "zhangsan@example.com", "age": 25}'
响应: {"message": "用户创建成功", "user": {...}} (状态码: 201)

# 2. 输入验证错误 (缺少必需字段)
curl -X POST http://localhost:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "张三"}'
响应: {"error": {"code": "VALIDATION_ERROR", "message": "缺少必需字段: email", ...}} (状态码: 400)

# 3. 输入验证错误 (邮箱格式无效)
curl -X POST http://localhost:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "张三", "email": "invalid-email", "age": 25}'
响应: {"error": {"code": "VALIDATION_ERROR", "message": "邮箱格式无效", ...}} (状态码: 400)

# 4. 资源不存在错误 (GET /users/999)
curl http://localhost:5000/users/999
响应: {"error": {"code": "RESOURCE_NOT_FOUND", "message": "用户ID 999 不存在", ...}} (状态码: 404)

# 5. 服务器内部错误 (触发异常)
curl http://localhost:5000/users/crash
响应: {"error": {"code": "INTERNAL_ERROR", "message": "服务器内部错误", ...}} (状态码: 500)
"""

import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# 尝试导入Flask
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

# 模拟用户数据库
users_db: List[Dict] = [
    {
        "id": 1,
        "name": "管理员",
        "email": "admin@example.com",
        "age": 30,
        "created_at": "2026-05-01T10:00:00Z"
    }
]

next_user_id = 2


class ValidationError(Exception):
    """自定义验证错误异常"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)


def validate_email(email: str) -> bool:
    """
    验证邮箱格式

    参数:
        email (str): 要验证的邮箱地址

    返回:
        bool: 邮箱格式是否有效
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_user_data(data: Dict) -> None:
    """
    验证用户数据

    参数:
        data (dict): 用户数据字典

    抛出:
        ValidationError: 当验证失败时
    """
    # 检查必需字段
    required_fields = ['name', 'email', 'age']
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"缺少必需字段: {field}", field=field)

    # 验证姓名
    if not isinstance(data['name'], str) or len(data['name'].strip()) == 0:
        raise ValidationError("姓名不能为空", field='name', value=data.get('name'))

    if len(data['name']) > 50:
        raise ValidationError("姓名长度不能超过50个字符", field='name', value=data.get('name'))

    # 验证邮箱
    if not isinstance(data['email'], str):
        raise ValidationError("邮箱必须是字符串", field='email', value=data.get('email'))

    if not validate_email(data['email']):
        raise ValidationError("邮箱格式无效", field='email', value=data.get('email'))

    # 验证年龄
    if not isinstance(data['age'], int):
        raise ValidationError("年龄必须是整数", field='age', value=data.get('age'))

    if data['age'] < 0 or data['age'] > 150:
        raise ValidationError("年龄必须在0-150之间", field='age', value=data.get('age'))


def find_user_by_id(user_id: int) -> Optional[Dict]:
    """
    根据ID查找用户

    参数:
        user_id (int): 用户ID

    返回:
        dict 或 None: 找到的用户或None
    """
    for user in users_db:
        if user['id'] == user_id:
            return user
    return None


def create_error_response(code: str, message: str, status_code: int,
                         details: Dict = None) -> tuple:
    """
    创建标准化的错误响应

    参数:
        code (str): 错误代码
        message (str): 错误消息
        status_code (int): HTTP状态码
        details (dict): 额外的错误详情（可选）

    返回:
        tuple: (JSON响应, 状态码)
    """
    error_data = {
        "error": {
            "code": code,
            "message": message
        }
    }

    if details:
        error_data["error"]["details"] = details

    return jsonify(error_data), status_code


@app.route('/users', methods=['POST'])
def create_user():
    """
    创建新用户 - 包含完整的输入验证

    HTTP方法: POST
    URL: /users
    请求体: JSON { "name": "姓名", "email": "邮箱", "age": 年龄 }
    返回: 创建成功的用户信息或标准化错误响应
    状态码: 201 (成功) 或 400 (验证错误)
    """
    try:
        # 获取并验证请求数据
        data = request.get_json()
        if not data:
            return create_error_response(
                "INVALID_REQUEST",
                "请求体必须是有效的JSON格式",
                400
            )

        # 验证用户数据
        validate_user_data(data)

        # 检查邮箱是否已存在
        for existing_user in users_db:
            if existing_user['email'] == data['email']:
                return create_error_response(
                    "EMAIL_ALREADY_EXISTS",
                    f"邮箱 {data['email']} 已被注册",
                    400,
                    {"email": data['email']}
                )

        # 创建新用户
        global next_user_id
        new_user = {
            "id": next_user_id,
            "name": data['name'],
            "email": data['email'],
            "age": data['age'],
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
        users_db.append(new_user)
        next_user_id += 1

        return jsonify({
            "message": "用户创建成功",
            "user": new_user
        }), 201

    except ValidationError as e:
        return create_error_response(
            "VALIDATION_ERROR",
            e.message,
            400,
            {
                "field": e.field,
                "value": e.value
            } if e.field else None
        )
    except Exception as e:
        # 捕获其他意外错误
        app.logger.error(f"创建用户时发生未知错误: {str(e)}")
        return create_error_response(
            "INTERNAL_ERROR",
            "服务器内部错误，请稍后再试",
            500
        )


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    """
    获取单个用户信息

    HTTP方法: GET
    URL: /users/<user_id>
    返回: 用户信息或标准化错误响应
    状态码: 200 (成功) 或 404 (用户不存在)
    """
    try:
        user = find_user_by_id(user_id)
        if not user:
            return create_error_response(
                "RESOURCE_NOT_FOUND",
                f"用户ID {user_id} 不存在",
                404,
                {"resource_id": user_id, "resource_type": "user"}
            )

        return jsonify({
            "user": user
        }), 200

    except Exception as e:
        app.logger.error(f"获取用户时发生未知错误: {str(e)}")
        return create_error_response(
            "INTERNAL_ERROR",
            "服务器内部错误，请稍后再试",
            500
        )


@app.route('/users', methods=['GET'])
def get_users():
    """
    获取用户列表 - 支持分页和过滤

    HTTP方法: GET
    URL: /users?limit=10&offset=0&name=张
    查询参数:
        limit (int): 每页数量，默认10，最大100
        offset (int): 偏移量，默认0
        name (str): 按姓名过滤（模糊匹配）
    返回: 用户列表和分页信息
    状态码: 200
    """
    try:
        # 解析查询参数
        limit = request.args.get('limit', default=10, type=int)
        offset = request.args.get('offset', default=0, type=int)
        name_filter = request.args.get('name', default='', type=str)

        # 验证分页参数
        if limit < 1 or limit > 100:
            return create_error_response(
                "INVALID_PARAMETER",
                "limit参数必须在1-100之间",
                400,
                {"parameter": "limit", "value": limit}
            )

        if offset < 0:
            return create_error_response(
                "INVALID_PARAMETER",
                "offset参数不能为负数",
                400,
                {"parameter": "offset", "value": offset}
            )

        # 过滤用户
        filtered_users = users_db
        if name_filter:
            filtered_users = [
                user for user in users_db
                if name_filter.lower() in user['name'].lower()
            ]

        # 分页
        total = len(filtered_users)
        paginated_users = filtered_users[offset:offset + limit]

        return jsonify({
            "users": paginated_users,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total
            }
        }), 200

    except ValueError as e:
        # 参数类型转换错误
        return create_error_response(
            "INVALID_PARAMETER",
            "查询参数类型错误，请检查参数格式",
            400
        )
    except Exception as e:
        app.logger.error(f"获取用户列表时发生未知错误: {str(e)}")
        return create_error_response(
            "INTERNAL_ERROR",
            "服务器内部错误，请稍后再试",
            500
        )


@app.route('/users/crash', methods=['GET'])
def crash_endpoint():
    """
    故意触发服务器错误的端点 - 用于测试错误处理

    HTTP方法: GET
    URL: /users/crash
    返回: 标准化的500错误响应
    状态码: 500
    """
    # 故意引发异常来测试错误处理
    raise Exception("这是一个故意触发的服务器错误，用于测试错误处理机制")


@app.errorhandler(404)
def handle_404(error):
    """全局404错误处理"""
    return create_error_response(
        "ENDPOINT_NOT_FOUND",
        "请求的API端点不存在",
        404
    )


@app.errorhandler(405)
def handle_405(error):
    """全局405错误处理（方法不允许）"""
    return create_error_response(
        "METHOD_NOT_ALLOWED",
        "该端点不支持此HTTP方法",
        405
    )


@app.errorhandler(500)
def handle_500(error):
    """全局500错误处理"""
    app.logger.error(f"服务器内部错误: {str(error)}")
    return create_error_response(
        "INTERNAL_ERROR",
        "服务器内部错误，请稍后再试",
        500
    )


if __name__ == '__main__':
    print("🛡️  启动错误处理API服务器...")
    print("📝 可用的API端点:")
    print("   POST /users           - 创建用户 (包含完整验证)")
    print("   GET  /users           - 获取用户列表 (支持分页和过滤)")
    print("   GET  /users/<id>      - 获取单个用户")
    print("   GET  /users/crash     - 触发服务器错误 (测试用)")
    print("\n💡 测试建议:")
    print("   1. 测试正常创建用户")
    print("   2. 测试各种验证错误场景")
    print("   3. 测试资源不存在错误")
    print("   4. 测试服务器内部错误处理")
    print("   5. 注意观察标准化的错误响应格式")
    print("\n🌐 服务器运行在: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止服务器\n")

    app.run(debug=True, host='0.0.0.0', port=5000)