#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例2：服务发现实现

这个脚本实现了一个简单的服务注册中心，演示了微服务架构中的服务发现机制。
包含服务注册、心跳检测、服务发现和健康检查功能。

使用Python标准库实现，无需外部依赖。
"""

import json
import threading
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import defaultdict


class ServiceRegistry:
    """服务注册中心 - 管理所有注册的服务实例"""

    def __init__(self):
        self.services = defaultdict(list)  # 服务名 -> 实例列表
        self.heartbeat_timeout = 10  # 心跳超时时间（秒）
        self.lock = threading.Lock()

    def register_service(self, service_name, host, port, metadata=None):
        """注册服务实例"""
        with self.lock:
            service_instance = {
                'host': host,
                'port': port,
                'last_heartbeat': time.time(),
                'metadata': metadata or {}
            }

            # 检查是否已存在相同的实例
            existing = False
            for instance in self.services[service_name]:
                if instance['host'] == host and instance['port'] == port:
                    instance['last_heartbeat'] = time.time()
                    existing = True
                    break

            if not existing:
                self.services[service_name].append(service_instance)
                print(f"✅ 服务注册: {service_name} @ {host}:{port}")

    def heartbeat(self, service_name, host, port):
        """服务心跳 - 更新最后心跳时间"""
        with self.lock:
            for instance in self.services[service_name]:
                if instance['host'] == host and instance['port'] == port:
                    instance['last_heartbeat'] = time.time()
                    return True
            return False

    def discover_services(self, service_name):
        """发现服务 - 返回可用的服务实例列表"""
        with self.lock:
            current_time = time.time()
            available_instances = []

            # 清理过期的实例
            alive_instances = []
            for instance in self.services[service_name]:
                if current_time - instance['last_heartbeat'] <= self.heartbeat_timeout:
                    alive_instances.append(instance)
                    available_instances.append(f"{instance['host']}:{instance['port']}")
                else:
                    print(f"❌ 服务实例超时移除: {service_name} @ {instance['host']}:{instance['port']}")

            self.services[service_name] = alive_instances
            return available_instances

    def get_all_services(self):
        """获取所有服务信息"""
        with self.lock:
            result = {}
            current_time = time.time()
            for service_name, instances in self.services.items():
                alive_instances = []
                for instance in instances:
                    if current_time - instance['last_heartbeat'] <= self.heartbeat_timeout:
                        alive_instances.append(instance)
                if alive_instances:
                    result[service_name] = alive_instances
            return result


# 全局服务注册中心实例
registry = ServiceRegistry()


class RegistryHandler(BaseHTTPRequestHandler):
    """注册中心HTTP接口处理器"""

    def do_POST(self):
        if self.path == '/register':
            # 处理服务注册请求
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            register_data = json.loads(post_data.decode('utf-8'))

            service_name = register_data.get('service_name')
            host = register_data.get('host')
            port = register_data.get('port')
            metadata = register_data.get('metadata', {})

            if service_name and host and port:
                registry.register_service(service_name, host, port, metadata)
                self._send_response(200, {'status': 'registered'})
            else:
                self._send_response(400, {'error': '缺少必要参数'})

        elif self.path == '/heartbeat':
            # 处理心跳请求
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            heartbeat_data = json.loads(post_data.decode('utf-8'))

            service_name = heartbeat_data.get('service_name')
            host = heartbeat_data.get('host')
            port = heartbeat_data.get('port')

            if service_name and host and port:
                success = registry.heartbeat(service_name, host, port)
                if success:
                    self._send_response(200, {'status': 'heartbeat received'})
                else:
                    self._send_response(404, {'error': '服务实例未找到'})
            else:
                self._send_response(400, {'error': '缺少必要参数'})

    def do_GET(self):
        if self.path == '/discover':
            # 处理服务发现请求
            query = self.path.split('?')[1] if '?' in self.path else ''
            params = {}
            for param in query.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value

            service_name = params.get('service')
            if service_name:
                instances = registry.discover_services(service_name)
                self._send_response(200, {'instances': instances})
            else:
                self._send_response(400, {'error': '缺少service参数'})

        elif self.path == '/services':
            # 获取所有服务信息
            services = registry.get_all_services()
            self._send_response(200, services)

    def _send_response(self, status_code, data):
        """发送JSON响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


class MockService:
    """模拟的微服务 - 用于演示注册和心跳"""

    def __init__(self, name, host, port, registry_host='localhost', registry_port=8000):
        self.name = name
        self.host = host
        self.port = port
        self.registry_url = f'http://{registry_host}:{registry_port}'
        self.running = True

    def register(self):
        """向注册中心注册自己"""
        register_data = {
            'service_name': self.name,
            'host': self.host,
            'port': self.port,
            'metadata': {
                'version': '1.0.0',
                'environment': 'demo'
            }
        }

        try:
            data = json.dumps(register_data, ensure_ascii=False).encode('utf-8')
            req = urllib.request.Request(
                f'{self.registry_url}/register',
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    print(f"✅ {self.name} 注册成功")
                    return True
        except Exception as e:
            print(f"❌ {self.name} 注册失败: {e}")
        return False

    def send_heartbeat(self):
        """发送心跳到注册中心"""
        heartbeat_data = {
            'service_name': self.name,
            'host': self.host,
            'port': self.port
        }

        try:
            data = json.dumps(heartbeat_data, ensure_ascii=False).encode('utf-8')
            req = urllib.request.Request(
                f'{self.registry_url}/heartbeat',
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    return True
        except Exception as e:
            print(f"❌ {self.name} 心跳失败: {e}")
        return False

    def start_heartbeat_loop(self):
        """启动心跳循环"""
        while self.running:
            self.send_heartbeat()
            time.sleep(5)  # 每5秒发送一次心跳

    def stop(self):
        """停止服务"""
        self.running = False


def start_registry():
    """启动服务注册中心"""
    server = HTTPServer(('localhost', 8000), RegistryHandler)
    print("🚀 服务注册中心启动在 http://localhost:8000")
    print("   支持的API:")
    print("   • POST /register - 注册服务")
    print("   • POST /heartbeat - 发送心跳")
    print("   • GET /discover?service=xxx - 发现服务")
    print("   • GET /services - 查看所有服务")
    server.serve_forever()


def simulate_services():
    """模拟多个微服务注册和运行"""
    print("\n" + "="*50)
    print("🧪 模拟微服务注册和发现")
    print("="*50)

    # 创建模拟服务
    user_service = MockService('user-service', 'localhost', 8001)
    order_service = MockService('order-service', 'localhost', 8002)
    product_service = MockService('product-service', 'localhost', 8003)

    services = [user_service, order_service, product_service]

    # 注册所有服务
    for service in services:
        service.register()

    # 启动心跳线程
    heartbeat_threads = []
    for service in services:
        thread = threading.Thread(target=service.start_heartbeat_loop)
        thread.daemon = True
        thread.start()
        heartbeat_threads.append(thread)

    # 演示服务发现
    time.sleep(2)
    print("\n🔍 发现用户服务:")
    try:
        with urllib.request.urlopen('http://localhost:8000/discover?service=user-service') as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"   可用实例: {data['instances']}")
    except Exception as e:
        print(f"   发现失败: {e}")

    print("\n🔍 发现所有服务:")
    try:
        with urllib.request.urlopen('http://localhost:8000/services') as response:
            services_info = json.loads(response.read().decode('utf-8'))
            for service_name, instances in services_info.items():
                print(f"   {service_name}: {len(instances)} 个实例")
    except Exception as e:
        print(f"   获取所有服务失败: {e}")

    # 模拟一个服务停止（不发送心跳）
    print("\n⏰ 模拟用户服务停止发送心跳...")
    user_service.stop()
    time.sleep(12)  # 等待超过心跳超时时间

    print("\n🔍 再次发现用户服务（应该为空）:")
    try:
        with urllib.request.urlopen('http://localhost:8000/discover?service=user-service') as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"   可用实例: {data['instances']}")
    except Exception as e:
        print(f"   发现失败: {e}")


if __name__ == '__main__':
    print("📚 服务发现机制演示")
    print("本示例展示了服务注册、心跳检测、服务发现和健康检查")

    # 在后台线程中启动注册中心
    registry_thread = threading.Thread(target=start_registry)
    registry_thread.daemon = True
    registry_thread.start()

    # 等待注册中心启动
    time.sleep(1)

    # 运行模拟
    simulate_services()

    print("\n💡 关键概念理解:")
    print("   • 服务注册：服务启动时向注册中心注册自己")
    print("   • 心跳检测：定期发送心跳证明服务存活")
    print("   • 健康检查：注册中心移除超时的实例")
    print("   • 服务发现：客户端查询可用的服务实例")

    # 保持程序运行以便观察
    time.sleep(5)
    print("\n👋 演示结束")