#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：分布式追踪实现

这个脚本演示了分布式系统中的请求追踪机制，展示了如何在多个服务间传递
追踪上下文（Trace Context），以便构建完整的调用链路。

关键概念：
- Trace ID: 标识整个请求链路的唯一ID
- Span ID: 标识单个服务内的操作
- Parent Span ID: 标识父操作，建立调用树结构
"""

import json
import threading
import time
import uuid
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class Tracer:
    """分布式追踪器 - 生成和管理追踪上下文"""

    @staticmethod
    def generate_trace_id():
        """生成全局唯一的Trace ID"""
        return str(uuid.uuid4())

    @staticmethod
    def generate_span_id():
        """生成Span ID"""
        return str(uuid.uuid4())[:8]  # 使用较短的ID便于显示

    @staticmethod
    def extract_context(headers):
        """从HTTP头中提取追踪上下文"""
        trace_id = headers.get('X-Trace-ID')
        span_id = headers.get('X-Span-ID')
        parent_span_id = headers.get('X-Parent-Span-ID')
        return {
            'trace_id': trace_id,
            'span_id': span_id,
            'parent_span_id': parent_span_id
        }

    @staticmethod
    def inject_context(request, context):
        """将追踪上下文注入到HTTP请求头中"""
        if context.get('trace_id'):
            request.add_header('X-Trace-ID', context['trace_id'])
        if context.get('span_id'):
            request.add_header('X-Span-ID', context['span_id'])
        if context.get('parent_span_id'):
            request.add_header('X-Parent-Span-ID', context['parent_span_id'])


class TracingHandler(BaseHTTPRequestHandler):
    """支持追踪的HTTP处理器基类"""

    def log_request_info(self, operation, context=None):
        """记录请求信息和追踪上下文"""
        trace_id = context.get('trace_id', 'N/A') if context else 'N/A'
        span_id = context.get('span_id', 'N/A') if context else 'N/A'
        parent_span_id = context.get('parent_span_id', 'N/A') if context else 'N/A'

        print(f"🔍 [{self.__class__.__name__}] {operation}")
        print(f"   Trace ID: {trace_id}")
        print(f"   Span ID: {span_id}")
        print(f"   Parent Span ID: {parent_span_id}")


class UserServiceHandler(TracingHandler):
    """用户服务 - 处理用户相关的请求"""

    def do_GET(self):
        if self.path.startswith('/users/'):
            # 提取追踪上下文
            context = self.extract_context_from_headers()

            # 如果没有Trace ID，说明这是入口请求
            if not context.get('trace_id'):
                context['trace_id'] = self.generate_trace_id()
                context['parent_span_id'] = None

            # 为当前操作生成新的Span ID
            current_span_id = self.generate_span_id()
            context['span_id'] = current_span_id

            self.log_request_info("处理用户信息请求", context)

            # 模拟业务逻辑
            user_id = self.path.split('/')[-1]
            time.sleep(0.1)  # 模拟处理时间

            response = {
                'id': user_id,
                'name': f'用户{user_id}',
                'email': f'user{user_id}@example.com',
                'trace_context': context  # 在响应中包含追踪上下文（仅用于演示）
            }

            self._send_response(200, response)

    def extract_context_from_headers(self):
        """从请求头中提取追踪上下文"""
        headers = {}
        for header_name in ['X-Trace-ID', 'X-Span-ID', 'X-Parent-Span-ID']:
            header_value = self.headers.get(header_name)
            if header_value:
                headers[header_name.replace('X-', '').replace('-', '_').lower()] = header_value
        return headers

    def _send_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


class OrderServiceHandler(TracingHandler):
    """订单服务 - 处理订单相关的请求"""

    def do_POST(self):
        if self.path == '/orders':
            # 提取追踪上下文
            context = self.extract_context_from_headers()

            # 如果没有Trace ID，说明这是入口请求
            if not context.get('trace_id'):
                context['trace_id'] = self.generate_trace_id()
                context['parent_span_id'] = None

            # 为当前操作生成新的Span ID
            current_span_id = self.generate_span_id()
            context['span_id'] = current_span_id

            self.log_request_info("处理创建订单请求", context)

            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            order_request = json.loads(post_data.decode('utf-8'))

            # 调用用户服务（传递追踪上下文）
            user_id = order_request.get('user_id')
            user_info = self._call_user_service(user_id, context)

            if user_info:
                # 创建订单成功
                order_response = {
                    'order_id': f'ORD-{int(time.time())}',
                    'user_id': user_id,
                    'status': 'created',
                    'timestamp': time.time(),
                    'trace_context': context
                }
                self._send_response(201, order_response)
            else:
                self._send_response(400, {'error': '用户验证失败'})

    def extract_context_from_headers(self):
        """从请求头中提取追踪上下文"""
        headers = {}
        for header_name in ['X-Trace-ID', 'X-Span-ID', 'X-Parent-Span-ID']:
            header_value = self.headers.get(header_name)
            if header_value:
                headers[header_name.replace('X-', '').replace('-', '_').lower()] = header_value
        return headers

    def _call_user_service(self, user_id, parent_context):
        """调用用户服务，并传递追踪上下文"""
        try:
            url = f'http://localhost:8001/users/{user_id}'
            req = urllib.request.Request(url)

            # 注入追踪上下文到请求头
            tracer = Tracer()
            child_context = {
                'trace_id': parent_context['trace_id'],
                'span_id': tracer.generate_span_id(),  # 新的Span ID
                'parent_span_id': parent_context['span_id']  # 父Span ID
            }
            tracer.inject_context(req, child_context)

            print(f"   📡 调用用户服务 (Span: {child_context['span_id']})")

            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f"   ✅ 用户服务调用成功")
                    return data
        except Exception as e:
            print(f"   ❌ 用户服务调用失败: {e}")
            return None

    def _send_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


class ProductServiceHandler(TracingHandler):
    """商品服务 - 处理商品相关的请求"""

    def do_GET(self):
        if self.path.startswith('/products/'):
            # 提取追踪上下文
            context = self.extract_context_from_headers()

            # 如果没有Trace ID，说明这是入口请求
            if not context.get('trace_id'):
                context['trace_id'] = self.generate_trace_id()
                context['parent_span_id'] = None

            # 为当前操作生成新的Span ID
            current_span_id = self.generate_span_id()
            context['span_id'] = current_span_id

            self.log_request_info("处理商品信息请求", context)

            # 模拟业务逻辑
            product_id = self.path.split('/')[-1]
            time.sleep(0.15)  # 模拟处理时间

            response = {
                'id': product_id,
                'name': f'商品{product_id}',
                'price': 99.99,
                'stock': 100,
                'trace_context': context
            }

            self._send_response(200, response)

    def extract_context_from_headers(self):
        """从请求头中提取追踪上下文"""
        headers = {}
        for header_name in ['X-Trace-ID', 'X-Span-ID', 'X-Parent-Span-ID']:
            header_value = self.headers.get(header_name)
            if header_value:
                headers[header_name.replace('X-', '').replace('-', '_').lower()] = header_value
        return headers

    def _send_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


def start_user_service():
    """启动用户服务"""
    server = HTTPServer(('localhost', 8001), UserServiceHandler)
    print("🚀 用户服务启动在 http://localhost:8001")
    server.serve_forever()


def start_order_service():
    """启动订单服务"""
    server = HTTPServer(('localhost', 8002), OrderServiceHandler)
    print("🚀 订单服务启动在 http://localhost:8002")
    server.serve_forever()


def start_product_service():
    """启动商品服务"""
    server = HTTPServer(('localhost', 8003), ProductServiceHandler)
    print("🚀 商品服务启动在 http://localhost:8003")
    server.serve_forever()


def test_distributed_tracing():
    """测试分布式追踪"""
    print("\n" + "="*60)
    print("🧪 测试分布式追踪")
    print("="*60)

    # 测试1: 直接调用用户服务（入口请求）
    print("\n1. 直接调用用户服务（入口请求）:")
    try:
        req = urllib.request.Request('http://localhost:8001/users/123')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"   ✅ 获取用户信息成功")
            print(f"   Trace ID: {data['trace_context']['trace_id']}")
    except Exception as e:
        print(f"   ❌ 调用失败: {e}")

    # 测试2: 创建订单（涉及多个服务调用）
    print("\n2. 创建订单（跨服务调用链）:")
    try:
        order_data = {
            'user_id': '456',
            'product_id': '789',
            'quantity': 1
        }
        data = json.dumps(order_data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(
            'http://localhost:8002/orders',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        req.get_method = lambda: 'POST'

        with urllib.request.urlopen(req) as response:
            order_response = json.loads(response.read().decode('utf-8'))
            print(f"   ✅ 订单创建成功")
            print(f"   Trace ID: {order_response['trace_context']['trace_id']}")
            print(f"   🔗 完整的调用链路可以通过这个Trace ID追踪")
    except Exception as e:
        print(f"   ❌ 订单创建失败: {e}")

    # 测试3: 直接调用商品服务（另一个入口请求）
    print("\n3. 直接调用商品服务（独立入口请求）:")
    try:
        req = urllib.request.Request('http://localhost:8003/products/ABC')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"   ✅ 获取商品信息成功")
            print(f"   Trace ID: {data['trace_context']['trace_id']}")
    except Exception as e:
        print(f"   ❌ 调用失败: {e}")


if __name__ == '__main__':
    print("📚 分布式追踪机制演示")
    print("本示例展示了如何在多个服务间传递追踪上下文，构建完整的调用链路")

    # 在后台线程中启动所有服务
    services = [
        threading.Thread(target=start_user_service),
        threading.Thread(target=start_order_service),
        threading.Thread(target=start_product_service)
    ]

    for service in services:
        service.daemon = True
        service.start()

    # 等待服务启动
    time.sleep(2)

    # 运行测试
    test_distributed_tracing()

    print("\n💡 关键概念理解:")
    print("   • Trace ID: 贯穿整个请求链路的唯一标识")
    print("   • Span ID: 标识单个服务内的具体操作")
    print("   • Parent Span ID: 建立调用树结构，显示父子关系")
    print("   • 上下文传播: 通过HTTP头在服务间传递追踪信息")

    # 保持程序运行一段时间
    time.sleep(3)
    print("\n👋 演示结束")