#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主动-被动故障转移模拟

模拟一个主动-被动架构中的健康检查和自动故障转移过程。
系统包含一个主服务器和一个备用服务器，通过健康检查机制
在主服务器失败时自动切换到备用服务器。
"""

import time
import random
import threading
from typing import Optional, Callable


class Server:
    """服务器类，模拟服务实例"""

    def __init__(self, name: str, failure_rate: float = 0.0):
        """
        初始化服务器

        Args:
            name: 服务器名称
            failure_rate: 失败概率（0.0-1.0）
        """
        self.name = name
        self.failure_rate = failure_rate
        self.is_healthy = True
        self.request_count = 0

    def handle_request(self) -> bool:
        """
        处理请求

        Returns:
            是否成功处理请求
        """
        self.request_count += 1

        # 模拟随机失败
        if random.random() < self.failure_rate:
            return False

        # 模拟处理时间
        time.sleep(0.01)
        return True

    def health_check(self) -> bool:
        """
        健康检查

        Returns:
            服务器是否健康
        """
        # 简单的健康检查：尝试处理一个测试请求
        try:
            success = self.handle_request()
            self.is_healthy = success
            return success
        except:
            self.is_healthy = False
            return False


class FailoverManager:
    """故障转移管理器"""

    def __init__(self, primary: Server, secondary: Server, check_interval: float = 2.0):
        """
        初始化故障转移管理器

        Args:
            primary: 主服务器
            secondary: 备用服务器
            check_interval: 健康检查间隔（秒）
        """
        self.primary = primary
        self.secondary = secondary
        self.active_server = primary
        self.check_interval = check_interval
        self.failover_count = 0
        self.is_running = False

    def start_monitoring(self):
        """启动健康监控"""
        self.is_running = True
        monitor_thread = threading.Thread(target=self._monitor_health)
        monitor_thread.daemon = True
        monitor_thread.start()
        print(f"开始监控: 主服务器={self.primary.name}, 备用服务器={self.secondary.name}")

    def stop_monitoring(self):
        """停止健康监控"""
        self.is_running = False

    def _monitor_health(self):
        """健康监控循环"""
        while self.is_running:
            # 检查当前活跃服务器的健康状态
            if not self.active_server.health_check():
                print(f"\n⚠️  {self.active_server.name} 健康检查失败！")

                # 尝试切换到另一个服务器
                new_active = self.secondary if self.active_server == self.primary else self.primary

                if new_active.health_check():
                    print(f"✅ 切换到 {new_active.name}")
                    self.active_server = new_active
                    self.failover_count += 1
                else:
                    print(f"❌ 备用服务器 {new_active.name} 也不健康！")

            time.sleep(self.check_interval)

    def process_request(self) -> bool:
        """
        处理客户端请求

        Returns:
            是否成功处理请求
        """
        if not self.active_server.is_healthy:
            return False
        return self.active_server.handle_request()


def simulate_client_requests(manager: FailoverManager, duration: int = 30):
    """
    模拟客户端请求

    Args:
        manager: 故障转移管理器
        duration: 模拟持续时间（秒）
    """
    start_time = time.time()
    request_count = 0
    success_count = 0

    print(f"\n开始模拟客户端请求，持续 {duration} 秒...")

    while time.time() - start_time < duration:
        request_count += 1
        if manager.process_request():
            success_count += 1

        # 随机间隔发送请求
        time.sleep(random.uniform(0.1, 0.5))

    success_rate = success_count / request_count if request_count > 0 else 0
    print(f"\n请求统计:")
    print(f"  总请求数: {request_count}")
    print(f"  成功请求数: {success_count}")
    print(f"  成功率: {success_rate:.2%}")
    print(f"  故障转移次数: {manager.failover_count}")


def main():
    """主函数：演示故障转移模拟"""
    print("=== 主动-被动故障转移模拟 ===\n")

    # 创建服务器实例
    # 主服务器有较高的失败概率来触发故障转移
    primary_server = Server("主服务器", failure_rate=0.3)
    secondary_server = Server("备用服务器", failure_rate=0.1)

    # 创建故障转移管理器
    failover_manager = FailoverManager(primary_server, secondary_server, check_interval=3.0)

    try:
        # 启动监控
        failover_manager.start_monitoring()

        # 模拟客户端请求
        simulate_client_requests(failover_manager, duration=20)

    finally:
        failover_manager.stop_monitoring()

    print("\n模拟结束")


if __name__ == "__main__":
    main()