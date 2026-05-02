#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3: 带速率限制和分页的API

这是一个展示高级API功能的实现，包含:
- 速率限制（Rate Limiting）
- 高级分页（游标分页）
- 过滤和排序
- 缓存机制
- 完整的错误处理

运行方法:
1. 安装依赖: pip install flask
2. 运行脚本: python3 solution-03.py
3. 测试速率限制和分页功能
"""

import time
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from functools import wraps

# 尝试导入Flask
try:
    from flask import Flask, request, jsonify
except ImportError:
    print("❌ 错误: Flask 未安装！")
    print("请运行以下命令安装Flask:")
    print("pip install flask")
    exit(1)

# 创建Flask应用实例
app = Flask(__name__)

# 速率限制配置
RATE_LIMIT_WINDOW = 60  # 60秒窗口
RATE_LIMIT_MAX_REQUESTS = 10  # 最多10个请求

# 模拟数据库 - 产品数据
products_db: List[Dict] = []
for i in range(1, 101):  # 创建100个产品用于测试
    products_db.append({
        "id": i,
        "name": f"产品 {i}",
        "description": f"这是第{i}个产品的详细描述",
        "price": 10.0 + i * 5.5,
        "category": "electronics" if i % 3 == 0 else "clothing" if i % 3 == 1 else "books",
        "created_at": (datetime.utcnow() - timedelta(days=i)).isoformat() + "Z",
        "updated_at": (datetime.utcnow() - timedelta(hours=i)).isoformat() + "Z"
    })

# 速率限制存储 - 实际应用中应使用Redis等
rate_limit_store: Dict[str, List[float]] = defaultdict(list)

# 缓存存储 - 实际应用中应使用Redis或Memcached
cache_store: Dict[str, Tuple[Any, float]] = {}
CACHE_TTL = 300  # 5分钟缓存


# ==================== 工具函数 ====================

def get_client_ip():
    """获取客户端IP地址"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or '127.0.0.1'


def check_rate_limit(client_id: str) -> tuple:
    """
    检查速率限制

    返回: (是否允许, 重置时间戳, 当前请求数)
    """
    current_time = time.time()
    window_start = current_time - RATE_LIMIT_WINDOW

    # 清理过期的请求记录
    rate_limit_store[client_id] = [
        req_time for req_time in rate_limit_store[client_id]
        if req_time >= window_start
    ]

    current_requests = len(rate_limit_store[client_id])

    if current_requests >= RATE_LIMIT_MAX_REQUESTS:
        reset_time = rate_limit_store[client_id][0] + RATE_LIMIT_WINDOW
        return False, reset_time, current_requests
    else:
        rate_limit_store[client_id].append(current_time)
        return True, current_time + RATE_LIMIT_WINDOW, current_requests + 1


def rate_limit(f):
    """速率限制装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_id = get_client_ip()
        allowed, reset_time, current_requests = check_rate_limit(client_id)

        if not allowed:
            return jsonify({
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": "请求过于频繁，请稍后再试"
                }
            }), 429, {
                'X-RateLimit-Limit': RATE_LIMIT_MAX_REQUESTS,
                'X-RateLimit-Remaining': 0,
                'X-RateLimit-Reset': int(reset_time)
            }

        # 添加速率限制头信息
        response = f(*args, **kwargs)
        if isinstance(response, tuple) and len(response) == 2:
            resp, status_code = response
            headers = {
                'X-RateLimit-Limit': RATE_LIMIT_MAX_REQUESTS,
                'X-RateLimit-Remaining': RATE_LIMIT_MAX_REQUESTS - current_requests,
                'X-RateLimit-Reset': int(reset_time)
            }
            return resp, status_code, headers
        elif isinstance(response, tuple) and len(response) == 3:
            resp, status_code, existing_headers = response
            existing_headers.update({
                'X-RateLimit-Limit': RATE_LIMIT_MAX_REQUESTS,
                'X-RateLimit-Remaining': RATE_LIMIT_MAX_REQUESTS - current_requests,
                'X-RateLimit-Reset': int(reset_time)
            })
            return resp, status_code, existing_headers
        else:
            headers = {
                'X-RateLimit-Limit': RATE_LIMIT_MAX_REQUESTS,
                'X-RateLimit-Remaining': RATE_LIMIT_MAX_REQUESTS - current_requests,
                'X-RateLimit-Reset': int(reset_time)
            }
            return response, 200, headers

    return decorated_function


def cache_get(key: str) -> Optional[Any]:
    """从缓存获取数据"""
    if key in cache_store:
        data, timestamp = cache_store[key]
        if time.time() - timestamp < CACHE_TTL:
            return data
        else:
            del cache_store[key]
    return None


def cache_set(key: str, data: Any):
    """设置缓存数据"""
    cache_store[key] = (data, time.time())


def create_error_response(code: str, message: str, status_code: int, details: Dict = None) -> tuple:
    """创建标准化错误响应"""
    error_data = {"error": {"code": code, "message": message}}
    if details:
        error_data["error"]["details"] = details
    return jsonify(error_data), status_code


def apply_filters_and_sort(items: List[Dict], filters: Dict, sort_by: str = None,
                          sort_order: str = 'asc') -> List[Dict]:
    """应用过滤和排序"""
    filtered_items = items[:]

    # 应用过滤
    for field, value in filters.items():
        if field == 'category':
            filtered_items = [item for item in filtered_items if item.get(field) == value]
        elif field == 'min_price':
            filtered_items = [item for item in filtered_items if item.get('price', 0) >= float(value)]
        elif field == 'max_price':
            filtered_items = [item for item in filtered_items if item.get('price', 0) <= float(value)]
        elif field == 'search':
            search_term = value.lower()
            filtered_items = [
                item for item in filtered_items
                if (search_term in item.get('name', '').lower() or
                    search_term in item.get('description', '').lower())
            ]

    # 应用排序
    if sort_by and sort_by in ['id', 'name', 'price', 'created_at']:
        reverse = sort_order.lower() == 'desc'
        filtered_items.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)

    return filtered_items


def cursor_paginate(items: List[Dict], limit: int, cursor: str = None,
                   sort_field: str = 'id') -> Dict:
    """
    游标分页实现

    参数:
        items: 已排序的项目列表
        limit: 每页数量
        cursor: 游标值（基于sort_field）
        sort_field: 排序字段

    返回:
        包含items、has_next、next_cursor的字典
    """
    if cursor is None:
        # 第一页
        paginated_items = items[:limit]
        if len(paginated_items) == limit:
            next_cursor = str(paginated_items[-1][sort_field])
            has_next = True
        else:
            next_cursor = None
            has_next = False
    else:
        # 找到游标位置
        cursor_value = type(items[0][sort_field])(cursor) if items else cursor
        start_index = None
        for i, item in enumerate(items):
            if item[sort_field] > cursor_value:
                start_index = i
                break

        if start_index is None:
            paginated_items = []
            has_next = False
            next_cursor = None
        else:
            paginated_items = items[start_index:start_index + limit]
            if len(paginated_items) == limit:
                next_cursor = str(paginated_items[-1][sort_field])
                has_next = True
            else:
                next_cursor = None
                has_next = False

    return {
        "items": paginated_items,
        "has_next": has_next,
        "next_cursor": next_cursor
    }


# ==================== 产品API端点 ====================

@app.route('/api/v1/products', methods=['GET'])
@rate_limit
def get_products():
    """
    获取产品列表 - 支持高级分页、过滤、排序和缓存

    查询参数:
        limit (int): 每页数量，默认20，最大50
        cursor (str): 游标值，用于分页
        category (str): 按分类过滤
        min_price (float): 最低价格
        max_price (float): 最高价格
        search (str): 搜索关键词
        sort_by (str): 排序字段 (id, name, price, created_at)
        sort_order (str): 排序顺序 (asc, desc)

    响应头:
        X-RateLimit-*: 速率限制信息
        X-Cache-Hit: 是否命中缓存 (true/false)
    """
    # 解析查询参数
    try:
        limit = min(max(int(request.args.get('limit', 20)), 1), 50)
        cursor = request.args.get('cursor')
        category = request.args.get('category')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'id')
        sort_order = request.args.get('sort_order', 'asc')

        # 构建缓存键
        cache_key = f"products:{limit}:{cursor}:{category}:{min_price}:{max_price}:{search}:{sort_by}:{sort_order}"
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result), 200, {'X-Cache-Hit': 'true'}

    except (ValueError, TypeError):
        return create_error_response(
            "INVALID_PARAMETER",
            "查询参数类型错误",
            400
        )

    # 准备过滤条件
    filters = {}
    if category:
        filters['category'] = category
    if min_price:
        filters['min_price'] = min_price
    if max_price:
        filters['max_price'] = max_price
    if search:
        filters['search'] = search

    # 应用过滤和排序
    try:
        filtered_products = apply_filters_and_sort(products_db, filters, sort_by, sort_order)
    except ValueError as e:
        return create_error_response(
            "INVALID_PARAMETER",
            f"参数值错误: {str(e)}",
            400
        )

    # 应用游标分页
    pagination_result = cursor_paginate(filtered_products, limit, cursor, sort_by)

    # 构建响应
    response_data = {
        "products": pagination_result["items"],
        "pagination": {
            "has_next": pagination_result["has_next"],
            "next_cursor": pagination_result["next_cursor"],
            "limit": limit
        },
        "filters": filters,
        "sort": {"by": sort_by, "order": sort_order}
    }

    # 缓存结果
    cache_set(cache_key, response_data)

    return jsonify(response_data), 200, {'X-Cache-Hit': 'false'}


@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
@rate_limit
def get_product(product_id: int):
    """获取单个产品详情"""
    # 尝试从缓存获取
    cache_key = f"product:{product_id}"
    cached_product = cache_get(cache_key)
    if cached_product:
        return jsonify({"product": cached_product}), 200, {'X-Cache-Hit': 'true'}

    # 查找产品
    product = None
    for p in products_db:
        if p['id'] == product_id:
            product = p
            break

    if not product:
        return create_error_response(
            "PRODUCT_NOT_FOUND",
            f"产品ID {product_id} 不存在",
            404,
            {"product_id": product_id}
        )

    # 缓存产品详情
    cache_set(cache_key, product)

    return jsonify({"product": product}), 200, {'X-Cache-Hit': 'false'}


# ==================== 统计API端点 ====================

@app.route('/api/v1/stats/products', methods=['GET'])
@rate_limit
def get_product_stats():
    """获取产品统计信息"""
    cache_key = "stats:products"
    cached_stats = cache_get(cache_key)
    if cached_stats:
        return jsonify({"stats": cached_stats}), 200, {'X-Cache-Hit': 'true'}

    # 计算统计信息
    total_products = len(products_db)
    categories = {}
    total_price = 0

    for product in products_db:
        category = product['category']
        categories[category] = categories.get(category, 0) + 1
        total_price += product['price']

    stats = {
        "total_products": total_products,
        "categories": categories,
        "average_price": round(total_price / total_products, 2) if total_products > 0 else 0,
        "most_expensive": max(products_db, key=lambda x: x['price'])['price'] if products_db else 0,
        "least_expensive": min(products_db, key=lambda x: x['price'])['price'] if products_db else 0
    }

    cache_set(cache_key, stats)

    return jsonify({"stats": stats}), 200, {'X-Cache-Hit': 'false'}


# ==================== 健康检查端点 ====================

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """健康检查端点 - 不受速率限制"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "rate_limit_store_size": len(rate_limit_store),
        "cache_store_size": len(cache_store)
    }), 200


# ==================== 调试端点 ====================

@app.route('/api/v1/debug/rate-limit', methods=['GET'])
def debug_rate_limit():
    """调试速率限制状态 - 不受速率限制"""
    client_id = get_client_ip()
    current_time = time.time()
    window_start = current_time - RATE_LIMIT_WINDOW
    requests_in_window = len([
        req_time for req_time in rate_limit_store.get(client_id, [])
        if req_time >= window_start
    ])

    return jsonify({
        "client_id": client_id,
        "requests_in_window": requests_in_window,
        "window_size": RATE_LIMIT_WINDOW,
        "max_requests": RATE_LIMIT_MAX_REQUESTS,
        "remaining_requests": max(0, RATE_LIMIT_MAX_REQUESTS - requests_in_window)
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


@app.errorhandler(429)
def handle_429(error):
    # 这个错误应该已经被rate_limit装饰器处理了
    return create_error_response(
        "RATE_LIMIT_EXCEEDED",
        "请求过于频繁，请稍后再试",
        429
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
    print("🚀 启动带速率限制和分页的API服务器...")
    print("📝 API端点概览:")
    print("\n产品管理:")
    print("  GET /api/v1/products             - 获取产品列表（支持分页/过滤/排序）")
    print("  GET /api/v1/products/<id>        - 获取产品详情")
    print("\n统计信息:")
    print("  GET /api/v1/stats/products       - 获取产品统计")
    print("\n系统监控:")
    print("  GET /api/v1/health               - 健康检查")
    print("  GET /api/v1/debug/rate-limit     - 调试速率限制状态")
    print("\n💡 测试建议:")
    print("  1. 测试游标分页: GET /api/v1/products?limit=5")
    print("  2. 使用返回的next_cursor继续获取下一页")
    print("  3. 测试过滤: GET /api/v1/products?category=electronics&min_price=50")
    print("  4. 测试排序: GET /api/v1/products?sort_by=price&sort_order=desc")
    print("  5. 快速连续请求测试速率限制（超过10次/分钟会触发429错误）")
    print("  6. 观察X-Cache-Hit头了解缓存命中情况")
    print("\n🌐 服务器运行在: http://localhost:5000/api/v1")
    print("⏹️  按 Ctrl+C 停止服务器\n")

    app.run(debug=True, host='0.0.0.0', port=5000)