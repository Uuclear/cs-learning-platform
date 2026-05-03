#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: Terraform 状态管理模拟
模拟 Terraform 的状态跟踪和漂移检测功能
"""

import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ResourceState:
    """资源状态数据类"""
    id: str
    type: str
    attributes: Dict[str, Any]
    dependencies: list


class StateManager:
    """Terraform 状态管理器模拟"""

    def __init__(self):
        self.current_state: Dict[str, ResourceState] = {}
        self.desired_state: Dict[str, ResourceState] = {}
        self.state_file_path = "terraform.tfstate"

    def save_state(self, state: Dict[str, ResourceState]):
        """保存状态到文件（模拟）"""
        print(f"💾 保存状态到 {self.state_file_path}")
        # 实际 Terraform 会将状态序列化为 JSON 并保存
        state_dict = {k: asdict(v) for k, v in state.items()}
        # 这里我们只是打印，不实际写入文件
        print(f"   状态包含 {len(state_dict)} 个资源")

    def load_state(self) -> Dict[str, ResourceState]:
        """从文件加载状态（模拟）"""
        print(f"📂 从 {self.state_file_path} 加载状态")
        # 模拟从文件加载状态
        return self.current_state.copy()

    def set_desired_state(self, resources: Dict[str, ResourceState]):
        """设置期望状态"""
        self.desired_state = resources

    def detect_drift(self) -> Dict[str, str]:
        """检测状态漂移"""
        drifts = {}

        # 检查当前状态中是否存在但期望状态中不存在的资源（意外删除）
        for resource_id in self.current_state:
            if resource_id not in self.desired_state:
                drifts[resource_id] = "意外删除 - 资源在基础设施中存在但在配置中不存在"

        # 检查期望状态中的资源是否与当前状态匹配
        for resource_id, desired in self.desired_state.items():
            if resource_id not in self.current_state:
                drifts[resource_id] = "缺失资源 - 配置中存在但基础设施中不存在"
            else:
                current = self.current_state[resource_id]
                if current.attributes != desired.attributes:
                    drifts[resource_id] = "属性漂移 - 资源属性与配置不匹配"
                if current.type != desired.type:
                    drifts[resource_id] = "类型漂移 - 资源类型与配置不匹配"

        return drifts

    def refresh_state(self, live_resources: Dict[str, ResourceState]):
        """刷新状态 - 从实际基础设施获取当前状态"""
        print("🔄 刷新状态 - 从实际基础设施获取当前状态")
        self.current_state = live_resources
        self.save_state(self.current_state)

    def apply_changes(self):
        """应用变更并更新状态"""
        print("⚡ 应用变更...")
        time.sleep(1)

        # 在真实场景中，这里会调用云提供商 API 创建/更新/删除资源
        # 现在我们假设所有变更都成功应用

        # 更新当前状态为期望状态
        self.current_state = self.desired_state.copy()
        self.save_state(self.current_state)
        print("✅ 变更应用成功!")


def simulate_infrastructure() -> Dict[str, ResourceState]:
    """模拟实际基础设施的当前状态"""
    return {
        "vpc-main": ResourceState(
            id="vpc-12345",
            type="aws_vpc",
            attributes={"cidr_block": "10.0.0.0/16", "tags": {"Name": "MainVPC"}},
            dependencies=[]
        ),
        "subnet-public": ResourceState(
            id="subnet-67890",
            type="aws_subnet",
            attributes={"cidr_block": "10.0.1.0/24", "availability_zone": "us-east-1a"},
            dependencies=["vpc-main"]
        )
    }


def main():
    """主函数 - 演示状态管理"""
    print("📊 Terraform 状态管理模拟器")
    print("本示例演示了 Terraform 如何跟踪状态和检测漂移\n")

    # 创建状态管理器
    state_manager = StateManager()

    # 模拟初始基础设施状态
    initial_infra = simulate_infrastructure()
    state_manager.refresh_state(initial_infra)

    print("\n=== 场景 1: 检测手动修改导致的漂移 ===")

    # 定义期望的配置状态（与当前基础设施不同）
    desired_config = {
        "vpc-main": ResourceState(
            id="vpc-12345",
            type="aws_vpc",
            attributes={"cidr_block": "10.0.0.0/16", "tags": {"Name": "ProductionVPC"}},  # 标签已更改
            dependencies=[]
        ),
        "subnet-public": ResourceState(
            id="subnet-67890",
            type="aws_subnet",
            attributes={"cidr_block": "10.0.1.0/24", "availability_zone": "us-east-1a"},
            dependencies=["vpc-main"]
        ),
        "security-group-web": ResourceState(  # 新增的安全组
            id="sg-abc123",
            type="aws_security_group",
            attributes={"description": "Web server security group"},
            dependencies=["vpc-main"]
        )
    }

    state_manager.set_desired_state(desired_config)
    drifts = state_manager.detect_drift()

    if drifts:
        print(f"\n⚠️  检测到 {len(drifts)} 个漂移:")
        for resource_id, reason in drifts.items():
            print(f"   • {resource_id}: {reason}")
    else:
        print("\n✅ 未检测到状态漂移")

    print("\n=== 场景 2: 应用修复变更 ===")
    state_manager.apply_changes()

    # 再次检查漂移
    final_drifts = state_manager.detect_drift()
    if not final_drifts:
        print("✅ 所有漂移已修复，状态同步完成!")
    else:
        print(f"❌ 仍有 {len(final_drifts)} 个漂移未解决")


if __name__ == "__main__":
    main()