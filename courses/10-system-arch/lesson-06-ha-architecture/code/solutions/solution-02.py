#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故障转移模拟解决方案

实现主动-被动架构的健康检查和自动故障转移。
"""

import time
import random
import threading
from typing import Optional


class Server:
    def __init__(self, name: str, failure_rate: float = 0.0):
        self.name = name
        self.failure_rate = failure_rate
        self.is_healthy = True
        self.request_count = 0

    def handle_request(self) -> bool:
        self.request_count += 1
        if random.random() < self.failure_rate:
            return False
        time.sleep(0.01)
        return True

    def health_check(self) -> bool:
        try:
            success = self.handle_request()
            self.is_healthy = success
            return success
        except:
            self.is_healthy = False
            return False


class FailoverManager:
    def __init__(self, primary: Server, secondary: Server, check_interval: float = 2.0):
        self.primary = primary
        self.secondary = secondary
        self.active_server = primary
        self.check_interval = check_interval
        self.failover_count = 0
        self.is_running = False

    def start_monitoring(self):
        self.is_running = True
        monitor_thread = threading.Thread(target=self._monitor_health)
        monitor_thread.daemon = True
        monitor_thread.start()

    def stop_monitoring(self):
        self.is_running = False

    def _monitor_health(self):
        while self.is_running:
            if not self.active_server.health_check():
                new_active = self.secondary if self.active_server == self.primary else self.primary
                if new_active.health_check():
                    self.active_server = new_active
                    self.failover_count += 1
            time.sleep(self.check_interval)

    def process_request(self) -> bool:
        if not self.active_server.is_healthy:
            return False
        return self.active_server.handle_request()


def test_failover():
    primary = Server("Primary", failure_rate=0.5)
    secondary = Server("Secondary", failure_rate=0.1)

    manager = FailoverManager(primary, secondary, check_interval=1.0)
    manager.start_monitoring()

    # 模拟请求
    success_count = 0
    for _ in range(10):
        if manager.process_request():
            success_count += 1
        time.sleep(0.1)

    manager.stop_monitoring()
    print(f"Failover test completed. Success rate: {success_count}/10")
    print(f"Failover count: {manager.failover_count}")


if __name__ == "__main__":
    test_failover()