#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: Terraform 状态管理模拟
这是 example-02-state-management.py 的简化解决方案
"""

from typing import Dict, Any


class SimpleStateManager:
    """简化的状态管理器"""

    def __init__(self):
        self.current_state = {}
        self.desired_state = {}

    def detect_drift(self) -> Dict[str, str]:
        """检测漂移"""
        drifts = {}

        # 检查缺失的资源
        for resource_id in self.desired_state:
            if resource_id not in self.current_state:
                drifts[resource_id] = "缺失资源"

        # 检查意外的资源
        for resource_id in self.current_state:
            if resource_id not in self.desired_state:
                drifts[resource_id] = "意外资源"

        return drifts

    def sync_state(self):
        """同步状态"""
        self.current_state = self.desired_state.copy()


def main():
    """主函数"""
    state_manager = SimpleStateManager()

    # 设置当前状态（模拟现有基础设施）
    state_manager.current_state = {
        "vpc-1": {"type": "aws_vpc", "cidr": "10.0.0.0/16"}
    }

    # 设置期望状态（来自配置）
    state_manager.desired_state = {
        "vpc-1": {"type": "aws_vpc", "cidr": "10.0.0.0/16"},
        "subnet-1": {"type": "aws_subnet", "cidr": "10.0.1.0/24"}
    }

    # 检测漂移
    drifts = state_manager.detect_drift()
    print("检测到的漂移:", drifts)

    # 同步状态
    state_manager.sync_state()
    print("同步后的状态:", state_manager.current_state)


if __name__ == "__main__":
    main()