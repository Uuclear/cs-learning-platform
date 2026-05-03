#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1：GitOps 工作流程完整实现

这个脚本实现了 GitOps 的完整工作流程，包括：
1. Git 仓库作为单一事实源
2. 拉取式部署机制
3. 自动化状态同步
4. 完整的审计跟踪
"""

import os
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime


class GitRepository:
    """模拟 Git 仓库，作为单一事实源"""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo_path.mkdir(exist_ok=True)
        self.state_file = self.repo_path / "desired_state.json"

    def initialize_state(self, initial_state: dict):
        """初始化期望状态"""
        initial_state["metadata"] = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "commit_hash": self._generate_commit_hash(initial_state)
        }
        self._save_state(initial_state)
        print(f"✅ Git 仓库初始化完成，初始版本: {initial_state['metadata']['version']}")

    def update_state(self, new_state: dict, version: str):
        """更新期望状态（模拟开发者提交）"""
        current_state = self.get_state()
        new_state["metadata"] = {
            "created_at": datetime.now().isoformat(),
            "version": version,
            "previous_version": current_state.get("metadata", {}).get("version", "none"),
            "commit_hash": self._generate_commit_hash(new_state)
        }
        self._save_state(new_state)
        print(f"📝 开发者提交新版本到 Git: {version}")
        return new_state

    def get_state(self) -> dict:
        """获取当前期望状态"""
        if self.state_file.exists():
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_state(self, state: dict):
        """保存状态到文件"""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _generate_commit_hash(self, state: dict) -> str:
        """生成模拟的 commit hash"""
        state_str = json.dumps(state, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(state_str.encode()).hexdigest()[:8]


class TargetEnvironment:
    """模拟目标环境"""

    def __init__(self, env_path: Path):
        self.env_path = env_path
        self.env_path.mkdir(exist_ok=True)
        self.state_file = self.env_path / "actual_state.json"

    def initialize_state(self, initial_state: dict):
        """初始化实际状态"""
        initial_state["sync_metadata"] = {
            "last_synced": None,
            "synced_version": None,
            "status": "initialized"
        }
        self._save_state(initial_state)
        print("🎯 目标环境初始化完成")

    def get_state(self) -> dict:
        """获取当前实际状态"""
        if self.state_file.exists():
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def apply_state(self, desired_state: dict):
        """应用期望状态到环境"""
        actual_state = self.get_state()

        # 复制期望状态的内容（除了 metadata）
        applied_state = {}
        for key, value in desired_state.items():
            if key != "metadata":
                applied_state[key] = value

        # 更新同步元数据
        applied_state["sync_metadata"] = {
            "last_synced": datetime.now().isoformat(),
            "synced_version": desired_state["metadata"]["version"],
            "status": "synced",
            "commit_hash": desired_state["metadata"]["commit_hash"]
        }

        self._save_state(applied_state)
        print(f"🚀 成功应用版本 {desired_state['metadata']['version']} 到目标环境")

    def _save_state(self, state: dict):
        """保存状态到文件"""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)


class GitOpsAgent:
    """GitOps 代理，负责协调工作"""

    def __init__(self, repo: GitRepository, env: TargetEnvironment):
        self.repo = repo
        self.env = env
        self.last_processed_hash = None

    def detect_changes(self) -> bool:
        """检测 Git 仓库是否有变更"""
        current_state = self.repo.get_state()
        if not current_state:
            return False

        current_hash = current_state["metadata"]["commit_hash"]
        if self.last_processed_hash != current_hash:
            self.last_processed_hash = current_hash
            return True
        return False

    def sync_to_environment(self):
        """同步 Git 仓库状态到目标环境"""
        if self.detect_changes():
            desired_state = self.repo.get_state()
            self.env.apply_state(desired_state)
            print("✅ GitOps 同步完成")
        else:
            print("ℹ️  无变更需要同步")


def main():
    """主函数：演示完整的 GitOps 工作流程"""
    print("🎯 GitOps 工作流程完整解决方案")
    print("=" * 50)

    # 初始化组件
    repo_path = Path("git-repo-solution")
    env_path = Path("target-env-solution")

    git_repo = GitRepository(repo_path)
    target_env = TargetEnvironment(env_path)
    gitops_agent = GitOpsAgent(git_repo, target_env)

    # 步骤 1: 初始化 Git 仓库和目标环境
    initial_desired = {
        "application": "web-app",
        "version": "1.0.0",
        "replicas": 3,
        "image": "nginx:1.21",
        "config": {
            "port": 80,
            "health_check": "/health"
        }
    }

    git_repo.initialize_state(initial_desired)
    target_env.initialize_state({})

    # 步骤 2: 首次同步
    print("\n🔄 执行首次同步...")
    gitops_agent.sync_to_environment()

    # 步骤 3: 模拟开发者提交新版本
    print("\n" + "="*50)
    print("💻 开发者工作流：提交新版本")

    new_desired = {
        "application": "web-app",
        "version": "1.1.0",
        "replicas": 5,
        "image": "nginx:1.22",
        "config": {
            "port": 8080,
            "health_check": "/healthz",
            "new_feature": True
        }
    }

    git_repo.update_state(new_desired, "1.1.0")

    # 步骤 4: GitOps 代理自动同步
    print("\n🤖 GitOps 代理检测并同步变更...")
    gitops_agent.sync_to_environment()

    # 步骤 5: 验证最终状态
    print("\n" + "="*50)
    print("🔍 验证最终状态:")
    final_actual = target_env.get_state()
    print(f"   应用版本: {final_actual.get('version', 'unknown')}")
    print(f"   副本数: {final_actual.get('replicas', 'unknown')}")
    print(f"   同步状态: {final_actual['sync_metadata']['status']}")
    print(f"   最后同步时间: {final_actual['sync_metadata']['last_synced']}")

    print("\n🎉 GitOps 工作流程演示完成!")
    print("关键优势:")
    print("• Git 作为单一事实源")
    print("• 自动化拉取式部署")
    print("• 完整的版本历史和审计跟踪")
    print("• 声明式配置确保一致性")


if __name__ == "__main__":
    main()