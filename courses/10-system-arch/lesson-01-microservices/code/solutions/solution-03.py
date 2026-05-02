#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：服务健康检查与负载均衡器

这个脚本实现了一个简单的服务健康检查和负载均衡器，演示了微服务架构中的
高可用性和容错机制。

功能包括：
- 定期健康检查服务实例
- 基于轮询的负载均衡算法
- 自动移除不健康的实例
- 故障转移和恢复检测
"""

import json
import threading
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from typing import List, Dict, Optional
from collections import deque


class ServiceInstance:
    """服务实例表示"""

    def __init__(self, host: str, port: int, service_name: str):
        self.host = host
        self.port = port
        self.service_name = service_name
        self.healthy = True
        self.last_health_check = 0
        self.failures = 0
        self.successes = 0

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def __str__(self):
        status = "✅" if self.healthy else "❌"
        return f"{status} {self.host}:{self.port}"


class LoadBalancer:
    """负载均衡器"""

    def __init__(self):
        self.services: Dict[str, List[ServiceInstance]] = {}
        self.instance_queues: Dict[str, deque] = {}  # 用于轮询
        self.lock = threading.Lock()

    def add_instance(self, service_name: str, host: str, port: int):
        """添加服务实例"""
        with self.lock:
            instance = ServiceInstance(host, port, service_name)
            if service_name not in self.services:
                self.services[service_name] = []
                self.instance_queues[service_name] = deque()

            self.services[service_name].append(instance)
            self.instance_queues[service_name].append(instance)
            print(f"➕ 添加服务实例: {service_name} @ {host}:{port}")

    def remove_instance(self, service_name: str, host: str, port: int):
        """移除服务实例"""
        with self.lock:
            if service_name in self.services:
                self.services[service_name] = [
                    inst for inst in self.services[service_name]
                    if not (inst.host == host and inst.port == port)
                ]
                # 重建轮询队列
                self.instance_queues[service_name] = deque([
                    inst for inst in self.instance_queues[service_name]
                    if not (inst.host == host and inst.port == port)
                ])
                print(f"➖ 移除服务实例: {service_name} @ {host}:{port}")

    def get_next_instance(self, service_name: str) -> Optional[ServiceInstance]:
        """获取下一个健康的服务实例（轮询）"""
        with self.lock:
            if service_name not in self.instance_queues:
                return None

            queue = self.instance_queues[service_name]
            if not queue:
                return None

            # 轮询获取实例
            for _ in range(len(queue)):
                instance = queue.popleft()
                queue.append(instance)  # 放回队尾

                if instance.healthy:
                    return instance

            return None  # 没有健康实例

    def mark_instance_healthy(self, service_name: str, host: str, port: int):
        """标记实例为健康"""
        with self.lock:
            for instance in self.services.get(service_name, []):
                if instance.host == host and instance.port == port:
                    instance.healthy = True
                    instance.failures = 0
                    instance.successes += 1
                    break

    def mark_instance_unhealthy(self, service_name: str, host: str, port: int):
        """标记实例为不健康"""
        with self.lock:
            for instance in self.services.get(service_name, []):
                if instance.host == host and instance.port == port:
                    instance.healthy = False
                    instance.failures += 1
                    break

    def get_service_status(self, service_name: str) -> Dict:
        """获取服务状态信息"""
        with self.lock:
            instances = self.services.get(service_name, [])
            healthy_count = sum(1 for inst in instances if inst.healthy)
            total_count = len(instances)

            return {
                'service_name': service_name,
                'healthy_instances': healthy_count,
                'total_instances': total_count,
                'instances': [str(inst) for inst in instances]
            }


class HealthChecker:
    """健康检查器"""

    def __init__(self, load_balancer: LoadBalancer, check_interval: int = 5):
        self.load_balancer = load_balancer
        self.check_interval = check_interval
        self.running = True

    def start_health_check_loop(self):
        """启动健康检查循环"""
        while self.running:
            self._perform_health_checks()
            time.sleep(self.check_interval)

    def stop(self):
        """停止健康检查"""
        self.running = False

    def _perform_health_checks(self):
        """执行健康检查"""
        print(f"\n🏥 执行健康检查...")

        with self.load_balancer.lock:
            all_services = list(self.load_balancer.services.keys())

        for service_name in all_services:
            self._check_service_health(service_name)

    def _check_service_health(self, service_name: str):
        """检查单个服务的健康状态"""
        with self.load_balancer.lock:
            instances = self.load_balancer.services.get(service_name, [])

        for instance in instances:
            healthy = self._check_instance_health(instance)

            if healthy:
                self.load_balancer.mark_instance_healthy(
                    service_name, instance.host, instance.port
                )
                print(f"   ✅ {instance.service_name} @ {instance.host}:{instance.port} 健康")
            else:
                self.load_balancer.mark_instance_unhealthy(
                    service_name, instance.host, instance.port
                )
                print(f"   ❌ {instance.service_name} @ {instance.host}:{instance.port} 不健康")

    def _check_instance_health(self, instance: ServiceInstance) -> bool:
        """检查单个实例的健康状态"""
        try:
            # 尝试访问健康检查端点
            req = urllib.request.Request(f"{instance.url}/health")
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    return data.get('status') == 'healthy'
        except Exception as e:
            print(f"      健康检查异常 {instance.url}: {e}")
            return False


class LoadBalancerHandler(BaseHTTPRequestHandler):
    """负载均衡器HTTP处理器"""

    def do_GET(self):
        self._handle_request('GET')

    def do_POST(self):
        self._handle_request('POST')

    def do_PUT(self):
        self._handle_request('PUT')

    def do_DELETE(self):
        self._handle_request('DELETE')

    def _handle_request(self, method: str):
        """处理请求并转发到后端服务"""
        # 解析路径以确定目标服务
        path_parts = self.path.strip('/').split('/')
        if not path_parts or path_parts[0] != 'api':
            self._send_error(404, "无效的API路径")
            return

        if len(path_parts) < 2:
            self._send_error(404, "缺少服务名称")
            return

        service_name = path_parts[1]
        target_path = '/' + '/'.join(path_parts[1:])  # 保留原始路径结构

        # 获取健康的服务实例
        instance = self.server.load_balancer.get_next_instance(service_name)
        if not instance:
            self._send_error(503, f"没有可用的 {service_name} 实例")
            return

        # 转发请求
        backend_url = instance.url + target_path
        try:
            response = self._forward_request(method, backend_url)
            if response:
                self.send_response(response.status)
                for header, value in response.headers.items():
                    if header.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.read())
            else:
                raise Exception("空响应")

        except Exception as e:
            # 标记实例为不健康
            self.server.load_balancer.mark_instance_unhealthy(
                service_name, instance.host, instance.port
            )
            self._send_error(502, f"后端服务调用失败: {e}")

    def _forward_request(self, method: str, url: str):
        """转发请求到后端服务"""
        data = None
        if method in ['POST', 'PUT'] and 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)

        req = urllib.request.Request(url, data=data, method=method)

        # 复制请求头
        for header, value in self.headers.items():
            if header.lower() != 'host':
                req.add_header(header, value)

        return urllib.request.urlopen(req, timeout=10)

    def _send_error(self, status_code: int, message: str):
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


def start_load_balancer(port: int = 8080):
    """启动负载均衡器"""
    # 创建负载均衡器
    lb = LoadBalancer()

    # 添加服务实例（模拟多个实例）
    lb.add_instance('user-service', 'localhost', 9001)
    lb.add_instance('user-service', 'localhost', 9002)
    lb.add_instance('order-service', 'localhost', 9003)
    lb.add_instance('order-service', 'localhost', 9004)
    lb.add_instance('product-service', 'localhost', 9005)

    # 创建健康检查器
    health_checker = HealthChecker(lb)
    health_thread = threading.Thread(target=health_checker.start_health_check_loop)
    health_thread.daemon = True
    health_thread.start()

    # 创建服务器
    server = HTTPServer(('localhost', port), LoadBalancerHandler)
    server.load_balancer = lb  # 注入负载均衡器

    print(f"🚀 负载均衡器启动在 http://localhost:{port}")
    print("   支持的服务:")
    for service_name in lb.services:
        status = lb.get_service_status(service_name)
        print(f"   • {service_name}: {status['total_instances']} 实例")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        health_checker.stop()
        print("\n👋 负载均衡器已停止")


def simulate_backend_services():
    """模拟后端服务实例（用于演示）"""

    class MockServiceHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, service_name="unknown", instance_id="1", **kwargs):
            self.service_name = service_name
            self.instance_id = instance_id
            super().__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == '/health':
                # 模拟健康检查 - 偶尔返回不健康状态用于演示
                import random
                if random.random() < 0.1:  # 10%概率不健康
                    self._send_response(500, {'status': 'unhealthy'})
                else:
                    self._send_response(200, {
                        'status': 'healthy',
                        'service': self.service_name,
                        'instance': self.instance_id,
                        'timestamp': time.time()
                    })
            else:
                self._send_response(200, {
                    'message': f'来自 {self.service_name}-{self.instance_id} 的响应',
                    'path': self.path
                })

        def do_POST(self):
            self._send_response(201, {
                'message': f'创建成功 - {self.service_name}-{self.instance_id}',
                'path': self.path
            })

        def _send_response(self, status_code, data):
            self.send_response(status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    # 创建不同服务的工厂函数
    def create_handler(service_name, instance_id):
        def handler(*args, **kwargs):
            MockServiceHandler(*args, service_name=service_name, instance_id=instance_id, **kwargs)
        return handler

    # 启动模拟服务实例
    ports_config = [
        ('user-service', 9001, '1'),
        ('user-service', 9002, '2'),
        ('order-service', 9003, '1'),
        ('order-service', 9004, '2'),
        ('product-service', 9005, '1')
    ]

    for service_name, port, instance_id in ports_config:
        handler_class = type(
            f'{service_name.capitalize()}Handler{instance_id}',
            (BaseHTTPRequestHandler,),
            {
                '__init__': lambda self, *args, **kwargs: MockServiceHandler.__init__(
                    self, *args, service_name=service_name, instance_id=instance_id, **kwargs
                )
            }
        )

        thread = threading.Thread(
            target=lambda p=port, h=handler_class: HTTPServer(('localhost', p), h).serve_forever()
        )
        thread.daemon = True
        thread.start()
        print(f"🧪 模拟服务启动: {service_name}-{instance_id} @ http://localhost:{port}")


def test_load_balancer():
    """测试负载均衡器"""
    print("\n" + "="*50)
    print("🧪 测试负载均衡器")
    print("="*50)

    # 测试请求分发
    services_to_test = ['user-service', 'order-service', 'product-service']

    for service in services_to_test:
        print(f"\n测试 {service}:")
        for i in range(3):  # 发送3个请求
            try:
                req = urllib.request.Request(f'http://localhost:8080/api/{service}/test')
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    print(f"   请求 {i+1}: {data['message']}")
            except Exception as e:
                print(f"   请求 {i+1} 失败: {e}")
            time.sleep(0.5)

    # 显示负载均衡状态
    print(f"\n📊 负载均衡状态:")
    try:
        req = urllib.request.Request('http://localhost:8080/status')
        # 注意：我们的负载均衡器没有/status端点，这里只是演示概念
        # 在实际实现中，可以添加管理端点来查看状态
    except:
        pass


if __name__ == '__main__':
    print("📚 服务健康检查与负载均衡器解决方案演示")
    print("本示例展示了如何实现服务健康检查、自动故障转移和负载均衡")

    # 启动模拟后端服务
    simulate_backend_services()
    time.sleep(1)

    # 启动负载均衡器
    start_load_balancer()