#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
部署策略模拟示例

本示例演示两种常见的部署策略：
1. 蓝绿部署 (Blue-Green Deployment)
2. 金丝雀发布 (Canary Release)

通过模拟用户流量分配来展示不同策略的特点。
"""

import time
import random


class ApplicationVersion:
    """应用版本类"""
    def __init__(self, version_name, success_rate=0.95):
        self.version_name = version_name
        self.success_rate = success_rate
        self.requests_handled = 0
        self.errors = 0

    def handle_request(self):
        """处理请求，有一定概率失败"""
        self.requests_handled += 1
        if random.random() < self.success_rate:
            return True
        else:
            self.errors += 1
            return False

    def get_error_rate(self):
        """计算错误率"""
        if self.requests_handled == 0:
            return 0
        return self.errors / self.requests_handled


def blue_green_deployment():
    """蓝绿部署模拟

    蓝绿部署同时维护两个相同的生产环境（蓝色和绿色），
    新版本部署到非活动环境中，测试通过后切换流量。
    """
    print("🔵🟢 蓝绿部署模拟")
    print("-" * 30)

    # 创建两个版本
    blue_version = ApplicationVersion("v1.0 (蓝色)", success_rate=0.98)
    green_version = ApplicationVersion("v2.0 (绿色)", success_rate=0.92)  # 新版本有更多问题

    print(f"当前活动环境: {blue_version.version_name}")
    print(f"新版本环境: {green_version.version_name}")

    # 在绿色环境进行测试
    print("\n🧪 在绿色环境进行预发布测试...")
    test_requests = 100
    for _ in range(test_requests):
        green_version.handle_request()

    error_rate = green_version.get_error_rate()
    print(f"绿色环境测试结果: 错误率 {error_rate:.2%}")

    if error_rate > 0.05:  # 如果错误率超过5%，回滚
        print("❌ 新版本问题太多，保持使用蓝色环境")
        active_version = blue_version
    else:
        print("✅ 新版本测试通过，切换到绿色环境")
        active_version = green_version

    # 模拟生产流量
    print(f"\n🚀 切换所有流量到 {active_version.version_name}")
    production_requests = 1000
    for _ in range(production_requests):
        active_version.handle_request()

    final_error_rate = active_version.get_error_rate()
    print(f"最终生产环境错误率: {final_error_rate:.2%}")


def canary_release():
    """金丝雀发布模拟

    金丝雀发布逐步将流量从旧版本转移到新版本，
    先让一小部分用户使用新版本，监控稳定性后再逐步扩大。
    """
    print("\n🐦 金丝雀发布模拟")
    print("-" * 30)

    old_version = ApplicationVersion("v1.0 (旧版本)", success_rate=0.98)
    new_version = ApplicationVersion("v2.0 (新版本)", success_rate=0.92)

    # 阶段1: 5% 流量到新版本
    print("阶段 1: 分配 5% 流量到新版本")
    total_requests = 1000
    canary_requests = int(total_requests * 0.05)
    main_requests = total_requests - canary_requests

    for _ in range(canary_requests):
        new_version.handle_request()
    for _ in range(main_requests):
        old_version.handle_request()

    canary_error_rate = new_version.get_error_rate()
    print(f"金丝雀版本错误率: {canary_error_rate:.2%}")

    if canary_error_rate > 0.1:  # 如果金丝雀版本错误率太高，停止发布
        print("❌ 金丝雀版本问题严重，停止发布")
        return

    # 阶段2: 25% 流量到新版本
    print("\n阶段 2: 分配 25% 流量到新版本")
    additional_requests = 1000
    canary_requests = int(additional_requests * 0.25)
    main_requests = additional_requests - canary_requests

    for _ in range(canary_requests):
        new_version.handle_request()
    for _ in range(main_requests):
        old_version.handle_request()

    canary_error_rate = new_version.get_error_rate()
    print(f"金丝雀版本累计错误率: {canary_error_rate:.2%}")

    if canary_error_rate > 0.08:
        print("⚠️  金丝雀版本仍有问题，暂停发布")
        return

    # 阶段3: 100% 流量到新版本
    print("\n阶段 3: 全量切换到新版本")
    final_requests = 1000
    for _ in range(final_requests):
        new_version.handle_request()

    final_error_rate = new_version.get_error_rate()
    print(f"新版本最终错误率: {final_error_rate:.2%}")


def main():
    """主函数 - 运行两种部署策略的模拟"""
    print("🎯 部署策略对比模拟")
    print("=" * 50)

    blue_green_deployment()
    canary_release()

    print("\n📊 部署策略总结:")
    print("• 蓝绿部署: 快速回滚，但需要双倍资源")
    print("• 金丝雀发布: 渐进式风险控制，但发布周期较长")


if __name__ == "__main__":
    main()