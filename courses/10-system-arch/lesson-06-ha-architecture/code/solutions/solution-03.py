#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混沌工程实验解决方案

模拟混沌工程实验来测试系统弹性。
"""

import time
import random
from enum import Enum
from typing import List, Dict, Any


class ComponentType(Enum):
    DATABASE = "database"
    CACHE = "cache"
    API_GATEWAY = "api_gateway"
    WORKER = "worker"


class SystemComponent:
    def __init__(self, name: str, component_type: ComponentType):
        self.name = name
        self.component_type = component_type
        self.is_healthy = True
        self.failure_mode = None

    def introduce_failure(self, failure_type: str):
        self.failure_mode = failure_type
        self.is_healthy = False

    def recover(self):
        self.failure_mode = None
        self.is_healthy = True


class WebServiceSystem:
    def __init__(self):
        self.components: List[SystemComponent] = []
        self._setup_components()

    def _setup_components(self):
        self.components.append(SystemComponent("MainDB", ComponentType.DATABASE))
        self.components.append(SystemComponent("ReplicaDB", ComponentType.DATABASE))
        self.components.append(SystemComponent("Redis", ComponentType.CACHE))
        self.components.append(SystemComponent("Gateway1", ComponentType.API_GATEWAY))
        self.components.append(SystemComponent("Gateway2", ComponentType.API_GATEWAY))
        for i in range(3):
            self.components.append(SystemComponent(f"Worker{i+1}", ComponentType.WORKER))

    def get_healthy_components(self) -> List[SystemComponent]:
        return [comp for comp in self.components if comp.is_healthy]

    def get_component_by_type(self, component_type: ComponentType) -> List[SystemComponent]:
        return [comp for comp in self.components if comp.component_type == component_type]

    def simulate_traffic(self, duration: int = 5) -> Dict[str, Any]:
        start_time = time.time()
        total_requests = 0
        successful_requests = 0

        while time.time() - start_time < duration:
            total_requests += 1
            healthy_gateways = len(self.get_component_by_type(ComponentType.API_GATEWAY))
            healthy_workers = len(self.get_component_by_type(ComponentType.WORKER))
            healthy_db = len(self.get_component_by_type(ComponentType.DATABASE)) > 0

            if healthy_gateways > 0 and healthy_workers > 0 and healthy_db:
                successful_requests += 1

            time.sleep(0.1)

        return {
            "success_rate": successful_requests / total_requests if total_requests > 0 else 0
        }


class ChaosExperiment:
    def __init__(self, system: WebServiceSystem):
        self.system = system

    def run_experiment(self, failure_scenarios: List[Dict[str, Any]]) -> bool:
        # Baseline
        baseline = self.system.simulate_traffic()

        # Inject failures
        affected_components = []
        for scenario in failure_scenarios:
            components = self.system.get_component_by_type(scenario["component_type"])
            if components:
                target = random.choice(components)
                target.introduce_failure(scenario["failure_type"])
                affected_components.append(target)

        time.sleep(1)

        # During failure
        during_failure = self.system.simulate_traffic()

        # Recover
        for component in affected_components:
            component.recover()

        time.sleep(1)

        # After recovery
        after_recovery = self.system.simulate_traffic()

        return (
            during_failure["success_rate"] < baseline["success_rate"] and
            after_recovery["success_rate"] >= baseline["success_rate"] * 0.9
        )


def test_chaos_engineering():
    system = WebServiceSystem()
    chaos = ChaosExperiment(system)

    # Test single database failure
    result = chaos.run_experiment([
        {"component_type": ComponentType.DATABASE, "failure_type": "timeout"}
    ])

    print(f"Chaos experiment result: {'PASS' if result else 'FAIL'}")


if __name__ == "__main__":
    test_chaos_engineering()