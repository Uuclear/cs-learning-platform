#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3：GitOps vs 传统 DevOps 完整对比

这个脚本深入对比了两种部署模式的根本差异：
1. 命令式（推送式）vs 声明式（拉取式）
2. 直接操作 vs 状态协调
3. 权限模型和安全特性
4. 审计跟踪和回滚机制
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class TraditionalDevOpsSystem:
    """传统 DevOps 系统（命令式/推送式）"""

    def __init__(self, env_path: Path):
        self.env_path = env_path
        self.env_path.mkdir(exist_ok=True)
        self.state_file = self.env_path / "state.json"
        self.operation_log = []
        self._initialize_state()

    def _initialize_state(self):
        """初始化系统状态"""
        initial_state = {
            "services": [],
            "deployment_history": [],
            "last_operation": None
        }
        self._save_state(initial_state)

    def _save_state(self, state: Dict[str, Any]):
        """保存状态"""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _load_state(self) -> Dict[str, Any]:
        """加载状态"""
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def deploy_service(self, service_name: str, image: str, replicas: int, operator: str = "admin"):
        """直接部署服务（命令式操作）"""
        print(f"🚀 传统 DevOps: {operator} 直接部署 {service_name}")

        state = self._load_state()

        # 查找现有服务
        existing_service = None
        for i, svc in enumerate(state["services"]):
            if svc["name"] == service_name:
                existing_service = i
                break

        operation = {
            "timestamp": datetime.now().isoformat(),
            "operator": operator,
            "action": "update" if existing_service is not None else "create",
            "service": service_name,
            "image": image,
            "replicas": replicas
        }

        if existing_service is not None:
            # 更新现有服务
            state["services"][existing_service].update({
                "image": image,
                "replicas": replicas,
                "last_updated": datetime.now().isoformat()
            })
            print(f"   ↳ 更新服务: {service_name} -> {image} (副本数: {replicas})")
        else:
            # 创建新服务
            new_service = {
                "name": service_name,
                "image": image,
                "replicas": replicas,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            state["services"].append(new_service)
            print(f"   ↳ 创建服务: {service_name} -> {image} (副本数: {replicas})")

        # 记录操作历史
        state["deployment_history"].append(operation)
        state["last_operation"] = operation
        self._save_state(state)
        self.operation_log.append(operation)

        print("✅ 部署完成\n")

    def get_state_summary(self) -> Dict[str, Any]:
        """获取状态摘要"""
        state = self._load_state()
        return {
            "service_count": len(state["services"]),
            "deployment_count": len(state["deployment_history"]),
            "last_operation_time": state["last_operation"]["timestamp"] if state["last_operation"] else None
        }


class GitOpsSystem:
    """GitOps 系统（声明式/拉取式）"""

    def __init__(self, repo_path: Path, env_path: Path):
        self.repo_path = repo_path
        self.env_path = env_path
        self.repo_path.mkdir(exist_ok=True)
        self.env_path.mkdir(exist_ok=True)

        self.desired_file = self.repo_path / "desired_state.json"
        self.actual_file = self.env_path / "actual_state.json"
        self.commit_history = []

        self._initialize_states()

    def _initialize_states(self):
        """初始化 Git 仓库和环境状态"""
        # 初始化 Git 仓库（期望状态）
        desired_state = {
            "services": [],
            "metadata": {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "author": "developer"
            }
        }
        self._save_desired_state(desired_state)

        # 初始化环境（实际状态）
        actual_state = {
            "services": [],
            "sync_metadata": {
                "last_synced": None,
                "synced_version": None,
                "status": "initialized"
            }
        }
        self._save_actual_state(actual_state)

    def _save_desired_state(self, state: Dict[str, Any]):
        """保存期望状态到 Git 仓库"""
        with open(self.desired_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _save_actual_state(self, state: Dict[str, Any]):
        """保存实际状态到环境"""
        with open(self.actual_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _load_desired_state(self) -> Dict[str, Any]:
        """加载期望状态"""
        with open(self.desired_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_actual_state(self) -> Dict[str, Any]:
        """加载实际状态"""
        with open(self.actual_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def commit_to_git(self, services: List[Dict], author: str = "developer", message: str = "Update desired state"):
        """提交变更到 Git 仓库（声明式更新）"""
        print(f"📝 GitOps: {author} 提交变更到 Git 仓库")

        current_desired = self._load_desired_state()

        # 创建新版本
        current_version = current_desired["metadata"]["version"]
        version_parts = current_version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)

        new_desired = {
            "services": services,
            "metadata": {
                "version": new_version,
                "created_at": datetime.now().isoformat(),
                "author": author,
                "message": message,
                "previous_version": current_version
            }
        }

        self._save_desired_state(new_desired)

        # 记录提交历史
        commit_info = {
            "timestamp": datetime.now().isoformat(),
            "author": author,
            "version": new_version,
            "message": message,
            "service_count": len(services)
        }
        self.commit_history.append(commit_info)

        print(f"✅ 提交完成，新版本: {new_version}\n")

    def reconcile(self):
        """执行状态协调（拉取式同步）"""
        print("🔄 GitOps: 执行状态协调...")

        desired_state = self._load_desired_state()
        actual_state = self._load_actual_state()

        # 比较状态
        if self._states_match(desired_state["services"], actual_state["services"]):
            print("   ↳ 状态已经同步，无需操作\n")
            return False

        # 执行协调
        new_actual = {
            "services": desired_state["services"].copy(),
            "sync_metadata": {
                "last_synced": datetime.now().isoformat(),
                "synced_version": desired_state["metadata"]["version"],
                "status": "synced",
                "commit_author": desired_state["metadata"]["author"]
            }
        }

        self._save_actual_state(new_actual)
        print(f"✅ 协调完成，同步到版本 {desired_state['metadata']['version']}\n")
        return True

    def _states_match(self, desired_services: List[Dict], actual_services: List[Dict]) -> bool:
        """比较两个服务列表是否匹配"""
        if len(desired_services) != len(actual_services):
            return False

        desired_dict = {svc["name"]: svc for svc in desired_services}
        actual_dict = {svc["name"]: svc for svc in actual_services}

        for name, desired_svc in desired_dict.items():
            if name not in actual_dict:
                return False
            if actual_dict[name] != desired_svc:
                return False

        return True

    def get_state_summary(self) -> Dict[str, Any]:
        """获取状态摘要"""
        actual_state = self._load_actual_state()
        desired_state = self._load_desired_state()
        return {
            "service_count": len(actual_state["services"]),
            "commit_count": len(self.commit_history),
            "current_version": desired_state["metadata"]["version"],
            "last_synced": actual_state["sync_metadata"]["last_synced"]
        }


def comprehensive_comparison():
    """全面对比两种部署模式"""
    print("🎯 GitOps vs 传统 DevOps 全面对比")
    print("=" * 60)

    # 初始化系统
    traditional_env = Path("traditional-system")
    gitops_repo = Path("gitops-repo-comparison")
    gitops_env = Path("gitops-env-comparison")

    traditional = TraditionalDevOpsSystem(traditional_env)
    gitops = GitOpsSystem(gitops_repo, gitops_env)

    print("🔧 场景 1: 初始部署")
    print("-" * 30)

    # 传统方式
    traditional.deploy_service("web", "nginx:1.21", 3, "ops-team")

    # GitOps 方式
    initial_services = [{"name": "web", "image": "nginx:1.21", "replicas": 3}]
    gitops.commit_to_git(initial_services, "developer", "Initial deployment")
    gitops.reconcile()

    print("🔧 场景 2: 版本升级")
    print("-" * 30)

    # 传统方式
    traditional.deploy_service("web", "nginx:1.22", 5, "senior-dev")

    # GitOps 方式
    updated_services = [{"name": "web", "image": "nginx:1.22", "replicas": 5}]
    gitops.commit_to_git(updated_services, "developer", "Upgrade to nginx 1.22")
    gitops.reconcile()

    print("🔧 场景 3: 多服务部署")
    print("-" * 30)

    # 传统方式
    traditional.deploy_service("api", "myapi:v2.0", 2, "backend-team")
    traditional.deploy_service("cache", "redis:7.0", 1, "infra-team")

    # GitOps 方式
    final_services = [
        {"name": "web", "image": "nginx:1.22", "replicas": 5},
        {"name": "api", "image": "myapi:v2.0", "replicas": 2},
        {"name": "cache", "image": "redis:7.0", "replicas": 1}
    ]
    gitops.commit_to_git(final_services, "team", "Add api and cache services")
    gitops.reconcile()

    print("📊 最终状态对比:")
    print("-" * 30)
    traditional_summary = traditional.get_state_summary()
    gitops_summary = gitops.get_state_summary()

    print(f"传统 DevOps:")
    print(f"  • 服务数量: {traditional_summary['service_count']}")
    print(f"  • 部署次数: {traditional_summary['deployment_count']}")
    print(f"  • 操作者: 直接访问环境")
    print(f"  • 审计: 操作日志")

    print(f"\nGitOps:")
    print(f"  • 服务数量: {gitops_summary['service_count']}")
    print(f"  • 提交次数: {gitops_summary['commit_count']}")
    print(f"  • 操作者: 通过 Git 提交")
    print(f"  • 审计: 完整的 Git 历史")
    print(f"  • 当前版本: {gitops_summary['current_version']}")

    print("\n🔑 核心差异总结:")
    print("• 权限模型: 传统需要环境访问权限，GitOps 只需 Git 权限")
    print("• 部署方式: 传统是推送式，GitOps 是拉取式")
    print("• 状态管理: 传统是命令式，GitOps 是声明式")
    print("• 回滚机制: 传统需要手动回滚，GitOps 通过 Git revert")
    print("• 一致性: GitOps 提供更强的一致性保证")
    print("• 安全性: GitOps 更好的凭证隔离和最小权限原则")


if __name__ == "__main__":
    comprehensive_comparison()