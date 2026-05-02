#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：服务间通信模式

这个脚本演示了微服务架构中两种主要的服务间通信模式：
1. 同步HTTP通信（请求-响应模式）
2. 异步消息传递（发布-订阅模式）

使用Python标准库实现，无需外部依赖。
"""

import json
import threading
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse


class UserServiceHandler(BaseHTTPRequestHandler):
    """用户服务 - 处理用户相关的请求"""

    def do_GET(self):
        if self.path == '/users/123':
            # 模拟获取用户信息
            response = {
                'id': '123',
                'name': '张三',
                'email': 'zhangsan@example.com'
            }
            self._send_response(200, response)
        else:
            self._send_response(404, {'error': '用户未找到'})

    def _send_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


class OrderServiceHandler(BaseHTTPRequestHandler):
    """订单服务 - 处理订单相关的请求"""

    def do_POST(self):
        if self.path == '/orders':
            # 读取请求体
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            order_request = json.loads(post_data.decode('utf-8'))

            # 模拟创建订单逻辑
            user_id = order_request.get('user_id')
            product_id = order_request.get('product_id')
            quantity = order_request.get('quantity', 1)

            # 这里会调用用户服务验证用户是否存在（同步调用）
            try:
                user_info = self._call_user_service(user_id)
                if user_info:
                    # 创建订单成功
                    order_response = {
                        'order_id': f'ORD-{int(time.time())}',
                        'user_id': user_id,
                        'product_id': product_id,
                        'quantity': quantity,
                        'status': 'created',
                        'timestamp': time.time()
                    }
                    self._send_response(201, order_response)

                    # 异步发送消息到消息队列（模拟）
                    self._publish_message('order.created', order_response)
                else:
                    self._send_response(400, {'error': '用户不存在'})
            except Exception as e:
                print(f"调用用户服务失败: {e}")
                self._send_response(500, {'error': '内部服务器错误'})

    def _call_user_service(self, user_id):
        """同步调用用户服务"""
        try:
            url = f'http://localhost:8001/users/{user_id}'
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f"✅ 成功从用户服务获取用户信息: {data['name']}")
                    return data
        except urllib.error.URLError as e:
            print(f"❌ 用户服务调用失败: {e}")
            return None

    def _publish_message(self, event_type, data):
        """异步发布消息到消息队列（模拟）"""
        message = {
            'event_type': event_type,
            'data': data,
            'timestamp': time.time()
        }
        print(f"📨 异步发布消息: {event_type}")
        # 在真实系统中，这里会发送到Kafka、RabbitMQ等消息队列

        # 模拟异步处理 - 在后台线程中处理
        def async_handler():
            time.sleep(1)  # 模拟处理延迟
            print(f"📬 消息处理完成: {event_type} -> 更新库存、发送通知等")

        thread = threading.Thread(target=async_handler)
        thread.daemon = True
        thread.start()

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


def test_communication():
    """测试服务间通信"""
    print("\n" + "="*50)
    print("🧪 测试服务间通信")
    print("="*50)

    # 测试同步调用
    print("\n1. 测试同步HTTP调用 (获取用户信息):")
    try:
        req = urllib.request.Request('http://localhost:8001/users/123')
        with urllib.request.urlopen(req) as response:
            user_data = json.loads(response.read().decode('utf-8'))
            print(f"   ✅ 成功获取用户: {user_data['name']}")
    except Exception as e:
        print(f"   ❌ 同步调用失败: {e}")

    # 测试创建订单（包含同步调用和异步消息）
    print("\n2. 测试创建订单 (包含同步验证和异步消息):")
    try:
        order_data = {
            'user_id': '123',
            'product_id': 'PROD-456',
            'quantity': 2
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
            print(f"   ✅ 订单创建成功: {order_response['order_id']}")
            print(f"   📧 异步消息已发布，稍后处理...")
    except Exception as e:
        print(f"   ❌ 订单创建失败: {e}")


if __name__ == '__main__':
    print("📚 微服务通信模式演示")
    print("本示例展示了同步HTTP调用和异步消息传递两种通信模式")

    # 在后台线程中启动服务
    user_thread = threading.Thread(target=start_user_service)
    order_thread = threading.Thread(target=start_order_service)

    user_thread.daemon = True
    order_thread.daemon = True

    user_thread.start()
    order_thread.start()

    # 等待服务启动
    time.sleep(2)

    # 运行测试
    test_communication()

    print("\n💡 观察输出，理解两种通信模式的区别：")
    print("   • 同步调用：立即得到响应，但会阻塞调用方")
    print("   • 异步消息：立即返回，后续在后台处理，提高系统响应性")

    # 保持程序运行一段时间以便观察异步消息处理
    time.sleep(3)
    print("\n👋 演示结束")