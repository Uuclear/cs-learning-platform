#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混沌工程实验模拟

模拟混沌工程实验，通过有计划地注入故障来测试系统的弹性和恢复能力。
本示例模拟一个简单的Web服务系统，包含多个组件，通过实验验证
系统在各种故障场景下的表现。
"""

import time
import random
import threading
from typing import List, Dict, Any
from enum import Enum


class ComponentType(Enum):
    """组件类型枚举"""
    DATABASE = "database"
    CACHE = "cache"
    API_GATEWAY = "api_gateway"
    WORKER = "worker"


class SystemComponent:
    """系统组件基类"""

    def __init__(self, name: str, component_type: ComponentType):
        """
        初始化系统组件

        Args:
            name: 组件名称
            component_type: 组件类型
        """
        self.name = name
        self.component_type = component_type
        self.is_healthy = True
        self.failure_mode = None

    def introduce_failure(self, failure_type: str):
        """
        注入故障

        Args:
            failure_type: 故障类型
        """
        self.failure_mode = failure_type
        self.is_healthy = False
        print(f"💥 在 {self.name} ({self.component_type.value}) 中注入 {failure_type} 故障")

    def recover(self):
        """恢复组件"""
        self.failure_mode = None
        self.is_healthy = True
        print(f"✅ {self.name} 已恢复")


class WebServiceSystem:
    """Web服务系统"""

    def __init__(self):
        """初始化Web服务系统"""
        self.components: List[SystemComponent] = []
        self._setup_components()

    def _setup_components(self):
        """设置系统组件"""
        # 添加数据库组件
        self.components.append(SystemComponent("主数据库", ComponentType.DATABASE))
        self.components.append(SystemComponent("从数据库", ComponentType.DATABASE))

        # 添加缓存组件
        self.components.append(SystemComponent("Redis缓存", ComponentType.CACHE))

        # 添加API网关
        self.components.append(SystemComponent("API网关1", ComponentType.API_GATEWAY))
        self.components.append(SystemComponent("API网关2", ComponentType.API_GATEWAY))

        # 添加工作进程
        for i in range(3):
            self.components.append(SystemComponent(f"工作进程{i+1}", ComponentType.WORKER))

    def get_healthy_components(self) -> List[SystemComponent]:
        """获取健康的组件列表"""
        return [comp for comp in self.components if comp.is_healthy]

    def get_component_by_type(self, component_type: ComponentType) -> List[SystemComponent]:
        """根据类型获取组件"""
        return [comp for comp in self.components if comp.component_type == component_type]

    def simulate_traffic(self, duration: int = 10) -> Dict[str, Any]:
        """
        模拟流量并收集系统指标

        Args:
            duration: 模拟持续时间（秒）

        Returns:
            系统指标字典
        """
        start_time = time.time()
        total_requests = 0
        successful_requests = 0
        errors = []

        while time.time() - start_time < duration:
            total_requests += 1

            # 检查是否有足够的健康组件处理请求
            healthy_gateways = len(self.get_component_by_type(ComponentType.API_GATEWAY))
            healthy_workers = len(self.get_component_by_type(ComponentType.WORKER))
            healthy_db = len(self.get_component_by_type(ComponentType.DATABASE)) > 0

            if healthy_gateways > 0 and healthy_workers > 0 and healthy_db:
                successful_requests += 1
            else:
                errors.append("服务不可用")

            time.sleep(0.1)

        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "error_count": len(errors),
            "success_rate": successful_requests / total_requests if total_requests > 0 else 0,
            "healthy_components": len(self.get_healthy_components()),
            "total_components": len(self.components)
        }


class ChaosExperiment:
    """混沌工程实验"""

    def __init__(self, system: WebServiceSystem):
        """
        初始化混沌实验

        Args:
            system: 要测试的系统
        """
        self.system = system
        self.experiments_run = 0

    def run_experiment(self, experiment_name: str, failure_scenarios: List[Dict[str, Any]]):
        """
        运行混沌实验

        Args:
            experiment_name: 实验名称
            failure_scenarios: 故障场景列表
        """
        print(f"\n🧪 开始混沌实验: {experiment_name}")
        print("=" * 50)

        # 记录实验前的系统状态
        baseline_metrics = self.system.simulate_traffic(duration=5)
        print(f"基线指标: 成功率 {baseline_metrics['success_rate']:.2%}")

        # 注入故障
        affected_components = []
        for scenario in failure_scenarios:
            components = self.system.get_component_by_type(scenario["component_type"])
            if components:
                # 随机选择一个组件注入故障
                target_component = random.choice(components)
                target_component.introduce_failure(scenario["failure_type"])
                affected_components.append(target_component)

        # 等待故障生效
        time.sleep(2)

        # 测试故障期间的系统表现
        during_failure_metrics = self.system.simulate_traffic(duration=5)
        print(f"故障期间: 成功率 {during_failure_metrics['success_rate']:.2%}")

        # 恢复组件
        for component in affected_components:
            component.recover()

        # 等待系统恢复
        time.sleep(2)

        # 测试恢复后的系统表现
        after_recovery_metrics = self.system.simulate_traffic(duration=5)
        print(f"恢复后: 成功率 {after_recovery_metrics['success_rate']:.2%}")

        # 判断实验是否成功
        success = (
            during_failure_metrics["success_rate"] < baseline_metrics["success_rate"] and
            after_recovery_metrics["success_rate"] >= baseline_metrics["success_rate"] * 0.95
        )

        print(f"实验结果: {'✅ 通过' if success else '❌ 失败'}")
        self.experiments_run += 1

        return {
            "name": experiment_name,
            "success": success,
            "baseline": baseline_metrics,
            "during_failure": during_failure_metrics,
            "after_recovery": after_recovery_metrics
        }


def main():
    """主函数：演示混沌工程实验"""
    print("=== 混沌工程实验模拟 ===\n")

    # 创建Web服务系统
    system = WebServiceSystem()
    print(f"系统初始化完成，共 {len(system.components)} 个组件")

    # 创建混沌实验
    chaos = ChaosExperiment(system)

    # 定义实验场景
    experiments = [
        {
            "name": "单点数据库故障",
            "scenarios": [
                {"component_type": ComponentType.DATABASE, "failure_type": "连接超时"}
            ]
        },
        {
            "name": "API网关部分故障",
            "scenarios": [
                {"component_type": ComponentType.API_GATEWAY, "failure_type": "高延迟"}
            ]
        },
        {
            "name": "缓存失效",
            "scenarios": [
                {"component_type": ComponentType.CACHE, "failure_type": "内存溢出"}
            ]
        }
    ]

    # 运行所有实验
    results = []
    for experiment in experiments:
        result = chaos.run_experiment(experiment["name"], experiment["scenarios"])
        results.append(result)
        time.sleep(3)  # 实验间间隔

    # 总结实验结果
    print("\n" + "=" * 50)
    print("混沌工程实验总结")
    print("=" * 50)
    passed = sum(1 for r in results if r["success"])
    total = len(results)
    print(f"通过实验: {passed}/{total}")
    print(f"成功率: {passed/total:.2%}")

    if passed == total:
        print("🎉 系统展现出良好的弹性和恢复能力！")
    else:
        print("⚠️  需要改进系统的容错和恢复机制。")


if __name__ == "__main__":
    main()