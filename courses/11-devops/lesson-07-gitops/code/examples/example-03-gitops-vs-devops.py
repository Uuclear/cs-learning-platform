#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3：GitOps vs 传统 DevOps 部署模式对比

这个脚本对比了两种不同的部署模式：
1. 传统 DevOps（命令式/推送式）：直接对目标环境执行命令
2. GitOps（声明式/拉取式）：通过 Git 仓库管理期望状态
"""

import json
import time
from pathlib import Path
from typing import Dict, Any


class TraditionalDevOpsDeployment:
    """传统 DevOps 部署模拟（命令式/推送式）"""

    def __init__(self, env_path: Path):
        self.env_path = env_path
        self.env_path.mkdir(exist_ok=True)
        # 初始化环境状态
        self.state = {"services": [], "last_deployed": None}
        self.save_state()

    def save_state(self):
        """保存当前环境状态"""
        with open(self.env_path / "state.json", "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def deploy_service(self, service_name: str, image: str, replicas: int):
        """直接部署服务到环境（命令式操作）"""
        print(f"🚀 传统 DevOps: 直接部署 {service_name} 到环境")

        # 查找现有服务
        existing_service = None
        for svc in self.state["services"]:
            if svc["name"] == service_name:
                existing_service = svc
                break

        if existing_service:
            # 更新现有服务
            existing_service.update({
                "image": image,
                "replicas": replicas,
                "updated_at": time.time()
            })
            print(f"   ↳ 更新服务: {service_name} -> {image} (副本数: {replicas})")
        else:
            # 创建新服务
            new_service = {
                "name": service_name,
                "image": image,
                "replicas": replicas,
                "created_at": time.time(),
                "updated_at": time.time()
            }
            self.state["services"].append(new_service)
            print(f"   ↳ 创建服务: {service_name} -> {image} (副本数: {replicas})")

        self.state["last_deployed"] = time.time()
        self.save_state()
        print("✅ 部署完成\n")

    def get_state(self) -> Dict[str, Any]:
        """获取当前环境状态"""
        return self.state.copy()


class GitOpsDeployment:
    """GitOps 部署模拟（声明式/拉取式）"""

    def __init__(self, repo_path: Path, env_path: Path):
        self.repo_path = repo_path
        self.env_path = env_path
        self.repo_path.mkdir(exist_ok=True)
        self.env_path.mkdir(exist_ok=True)

        # 初始化 Git 仓库（期望状态）
        self.desired_state = {"services": [], "last_updated": None}
        self.save_desired_state()

        # 初始化环境状态
        self.actual_state = {"services": [], "last_reconciled": None}
        self.save_actual_state()

    def save_desired_state(self):
        """保存期望状态到 Git 仓库"""
        with open(self.repo_path / "desired.json", "w", encoding="utf-8") as f:
            json.dump(self.desired_state, f, indent=2, ensure_ascii=False)

    def save_actual_state(self):
        """保存实际状态到环境"""
        with open(self.env_path / "actual.json", "w", encoding="utf-8") as f:
            json.dump(self.actual_state, f, indent=2, ensure_ascii=False)

    def update_desired_state(self, services: list):
        """更新 Git 仓库中的期望状态（开发者提交变更）"""
        print(f"📝 GitOps: 开发者更新 Git 仓库中的期望状态")
        self.desired_state = {
            "services": services,
            "last_updated": time.time()
        }
        self.save_desired_state()
        print("✅ 期望状态已更新\n")

    def reconcile(self):
        """协调过程：使实际状态匹配期望状态"""
        print("🔄 GitOps: 执行状态协调...")

        # 在真实场景中，这会由 ArgoCD 或 Flux 自动执行
        # 这里我们手动触发协调

        operations = []
        desired_services = {svc["name"]: svc for svc in self.desired_state["services"]}
        actual_services = {svc["name"]: svc for svc in self.actual_state["services"]}

        # 创建或更新服务
        for name, desired_svc in desired_services.items():
            if name not in actual_services:
                operations.append(f"CREATE {name}")
                self.actual_state["services"].append(desired_svc.copy())
            elif actual_services[name] != desired_svc:
                operations.append(f"UPDATE {name}")
                # 找到并更新服务
                for svc in self.actual_state["services"]:
                    if svc["name"] == name:
                        svc.update(desired_svc)
                        break

        # 删除多余的服务
        for name in list(actual_services.keys()):
            if name not in desired_services:
                operations.append(f"DELETE {name}")
                self.actual_state["services"] = [
                    svc for svc in self.actual_state["services"] if svc["name"] != name
                ]

        if operations:
            print(f"   ↳ 执行操作: {', '.join(operations)}")
            self.actual_state["last_reconciled"] = time.time()
            self.save_actual_state()
            print("✅ 协调完成\n")
        else:
            print("   ↳ 状态已经同步，无需操作\n")

    def get_desired_state(self) -> Dict[str, Any]:
        """获取期望状态"""
        return self.desired_state.copy()

    def get_actual_state(self) -> Dict[str, Any]:
        """获取实际状态"""
        return self.actual_state.copy()


def compare_deployment_patterns():
    """对比两种部署模式"""
    print("🎯 GitOps vs 传统 DevOps 部署模式对比")
    print("=" * 60)

    # 设置路径
    traditional_env = Path("traditional-env")
    gitops_repo = Path("gitops-repo")
    gitops_env = Path("gitops-env")

    # 初始化两种部署方式
    traditional = TraditionalDevOpsDeployment(traditional_env)
    gitops = GitOpsDeployment(gitops_repo, gitops_env)

    print("🔧 场景 1: 部署初始服务")
    print("-" * 30)

    # 传统 DevOps 方式
    traditional.deploy_service("web", "nginx:1.21", 3)

    # GitOps 方式
    initial_services = [{"name": "web", "image": "nginx:1.21", "replicas": 3}]
    gitops.update_desired_state(initial_services)
    gitops.reconcile()

    print("🔧 场景 2: 更新服务版本")
    print("-" * 30)

    # 传统 DevOps 方式
    traditional.deploy_service("web", "nginx:1.22", 5)

    # GitOps 方式
    updated_services = [{"name": "web", "image": "nginx:1.22", "replicas": 5}]
    gitops.update_desired_state(updated_services)
    gitops.reconcile()

    print("🔧 场景 3: 添加新服务")
    print("-" * 30)

    # 传统 DevOps 方式
    traditional.deploy_service("api", "myapi:v2.0", 2)

    # GitOps 方式
    final_services = [
        {"name": "web", "image": "nginx:1.22", "replicas": 5},
        {"name": "api", "image": "myapi:v2.0", "replicas": 2}
    ]
    gitops.update_desired_state(final_services)
    gitops.reconcile()

    print("📊 最终状态对比:")
    print("-" * 30)
    traditional_state = traditional.get_state()
    gitops_actual = gitops.get_actual_state()

    print(f"传统 DevOps 服务数: {len(traditional_state['services'])}")
    print(f"GitOps 实际服务数: {len(gitops_actual['services'])}")
    print()

    print("🔑 关键差异:")
    print("• 传统 DevOps: 直接操作环境，需要环境访问权限")
    print("• GitOps: 通过 Git 提交变更，环境自动同步")
    print("• GitOps 提供完整的审计跟踪和版本历史")
    print("• GitOps 支持自动回滚（Git revert）")
    print("• 传统 DevOps 更简单但缺乏一致性保证")


if __name__ == "__main__":
    compare_deployment_patterns()