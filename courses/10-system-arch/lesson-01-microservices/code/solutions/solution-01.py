#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：简单API网关实现

这个脚本实现了一个基本的API网关，演示了微服务架构中的统一入口点模式。
功能包括：
- 请求路由到后端服务
- 基本的错误处理和重试
- 简单的限流机制
- 健康检查集成
"""

import json
import threading
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from collections import defaultdict, deque


class RateLimiter:
    """简单的令牌桶限流器"""

    def __init__(self, rate=10, capacity=20):
        """
        :param rate: 每秒生成的令牌数
        :param capacity: 令牌桶容量
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_time = time.time()
        self.lock = threading.Lock()

    def allow_request(self):
        """检查是否允许请求通过"""
        with self.lock:
            current_time = time.time()
            # 添加新令牌
            new_tokens = int((current_time - self.last_time) * self.rate)
            if new_tokens > 0:
                self.tokens = min(self.capacity, self.tokens + new_tokens)
                self.last_time = current_time

            # 检查是否有足够令牌
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False


class HealthChecker:
    """服务健康检查器"""

    def __init__(self):
        self.service_health = {}
        self.lock = threading.Lock()

    def check_service_health(self, service_name, url):
        """检查单个服务的健康状态"""
        try:
            req = urllib.request.Request(f"{url}/health")
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    health_data = json.loads(response.read().decode('utf-8'))
                    return health_data.get('status') == 'healthy'
        except Exception as e:
            print(f"健康检查失败 {service_name}: {e}")
            return False

    def update_all_health(self, services):
        """更新所有服务的健康状态"""
        with self.lock:
            for service_name, service_info in services.items():
                healthy = self.check_service_health(service_name, service_info['url'])
                self.service_health[service_name] = {
                    'healthy': healthy,
                    'last_check': time.time()
                }
                status = "✅" if healthy else "❌"
                print(f"   {status} {service_name}: {'健康' if healthy else '不健康'}")

    def is_service_healthy(self, service_name):
        """检查服务是否健康"""
        with self.lock:
            health_info = self.service_health.get(service_name)
            if health_info:
                return health_info['healthy']
            return True  # 默认认为健康（如果未检查过）


class APIGatewayHandler(BaseHTTPRequestHandler):
    """API网关处理器"""

    # 服务路由配置
    ROUTES = {
        '/api/users': {'service': 'user-service', 'path': '/users'},
        '/api/users/<id>': {'service': 'user-service', 'path': '/users/<id>'},
        '/api/orders': {'service': 'order-service', 'path': '/orders'},
        '/api/products': {'service': 'product-service', 'path': '/products'},
        '/api/products/<id>': {'service': 'product-service', 'path': '/products/<id>'}
    }

    # 后端服务配置
    SERVICES = {
        'user-service': {'url': 'http://localhost:8001', 'retries': 2},
        'order-service': {'url': 'http://localhost:8002', 'retries': 2},
        'product-service': {'url': 'http://localhost:8003', 'retries': 2}
    }

    # 限流器（按客户端IP）
    rate_limiters = defaultdict(lambda: RateLimiter(rate=5, capacity=10))

    # 健康检查器
    health_checker = HealthChecker()

    def do_GET(self):
        self._handle_request('GET')

    def do_POST(self):
        self._handle_request('POST')

    def do_PUT(self):
        self._handle_request('PUT')

    def do_DELETE(self):
        self._handle_request('DELETE')

    def _handle_request(self, method):
        """处理所有HTTP请求"""
        client_ip = self.client_address[0]

        # 1. 限流检查
        if not self.rate_limiters[client_ip].allow_request():
            self._send_error(429, "请求过于频繁，请稍后再试")
            return

        # 2. 路由匹配
        route_info = self._match_route(self.path)
        if not route_info:
            self._send_error(404, "API端点不存在")
            return

        service_name = route_info['service']
        target_path = route_info['path']

        # 3. 健康检查
        if not self.health_checker.is_service_healthy(service_name):
            self._send_error(503, f"服务 {service_name} 暂时不可用")
            return

        # 4. 转发请求到后端服务
        service_config = self.SERVICES[service_name]
        backend_url = service_config['url'] + target_path

        success = False
        last_error = None

        # 5. 重试机制
        for attempt in range(service_config['retries'] + 1):
            try:
                response = self._forward_request(method, backend_url)
                if response:
                    # 成功响应
                    self.send_response(response.status)
                    for header, value in response.headers.items():
                        if header.lower() not in ['connection', 'transfer-encoding']:
                            self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.read())
                    success = True
                    break
            except Exception as e:
                last_error = str(e)
                if attempt < service_config['retries']:
                    print(f"⚠️  请求失败，第{attempt + 1}次重试: {backend_url}")
                    time.sleep(0.5 * (attempt + 1))  # 指数退避

        if not success:
            self._send_error(502, f"后端服务调用失败: {last_error}")

    def _match_route(self, path):
        """匹配请求路径到服务路由"""
        # 处理带参数的路径（如 /api/users/123）
        path_parts = path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] == 'api':
            # 构建基础路径用于匹配
            base_path = f"/{'/'.join(path_parts[:2])}"
            if base_path in self.ROUTES:
                route_info = self.ROUTES[base_path].copy()
                # 替换路径参数
                if '<id>' in route_info['path']:
                    if len(path_parts) >= 3:
                        route_info['path'] = route_info['path'].replace('<id>', path_parts[2])
                    else:
                        return None
                return route_info

        # 直接匹配完整路径
        if path in self.ROUTES:
            return self.ROUTES[path]

        return None

    def _forward_request(self, method, url):
        """转发请求到后端服务"""
        # 准备请求数据
        data = None
        if method in ['POST', 'PUT'] and 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)

        # 创建请求对象
        req = urllib.request.Request(url, data=data, method=method)

        # 复制原始请求头（除了Host）
        for header, value in self.headers.items():
            if header.lower() != 'host':
                req.add_header(header, value)

        # 发送请求
        return urllib.request.urlopen(req, timeout=10)

    def _send_error(self, status_code, message):
        """发送错误响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        error_response = {
            'error': message,
            'code': status_code,
            'timestamp': time.time()
        }
        self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"🌐 [{time.strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def start_api_gateway():
    """启动API网关"""
    server = HTTPServer(('localhost', 8080), APIGatewayHandler)
    print("🚀 API网关启动在 http://localhost:8080")
    print("   支持的路由:")
    for route, info in APIGatewayHandler.ROUTES.items():
        print(f"   • {route} -> {info['service']}")
    server.serve_forever()


def start_health_check_loop():
    """启动健康检查循环"""
    while True:
        print("\n🏥 执行服务健康检查...")
        APIGatewayHandler.health_checker.update_all_health(APIGatewayHandler.SERVICES)
        time.sleep(10)  # 每10秒检查一次


def simulate_backend_services():
    """模拟后端服务（用于演示）"""

    class MockBackendHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/health':
                self._send_response(200, {'status': 'healthy', 'timestamp': time.time()})
            elif self.path.startswith('/users'):
                user_id = self.path.split('/')[-1] if '/' in self.path else 'list'
                response = {'data': f'用户 {user_id} 的信息'}
                self._send_response(200, response)
            elif self.path.startswith('/products'):
                product_id = self.path.split('/')[-1] if '/' in self.path else 'list'
                response = {'data': f'商品 {product_id} 的信息'}
                self._send_response(200, response)
            else:
                self._send_response(404, {'error': 'Not Found'})

        def do_POST(self):
            if self.path == '/orders':
                self._send_response(201, {'message': '订单创建成功', 'order_id': 'ORD-123'})

        def _send_response(self, status_code, data):
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    # 启动模拟服务
    ports = [8001, 8002, 8003]
    for port in ports:
        thread = threading.Thread(
            target=lambda p=port: HTTPServer(('localhost', p), MockBackendHandler).serve_forever()
        )
        thread.daemon = True
        thread.start()
        print(f"🧪 模拟后端服务启动在 http://localhost:{port}")


if __name__ == '__main__':
    print("📚 API网关解决方案演示")
    print("本示例展示了API网关的核心功能：路由、限流、健康检查、错误处理")

    # 启动模拟后端服务
    simulate_backend_services()
    time.sleep(1)

    # 启动健康检查循环
    health_thread = threading.Thread(target=start_health_check_loop)
    health_thread.daemon = True
    health_thread.start()

    # 启动API网关
    start_api_gateway()