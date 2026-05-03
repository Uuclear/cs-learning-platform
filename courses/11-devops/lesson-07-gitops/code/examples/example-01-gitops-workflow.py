#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1：GitOps 工作流程模拟

这个脚本模拟了 GitOps 的拉取式部署工作流程：
1. 开发者提交代码到 Git 仓库（模拟为文件变更）
2. GitOps 代理检测到变更
3. 代理从 Git 仓库拉取最新的期望状态
4. 代理将变更应用到目标环境
"""

import os
import time
import json
from pathlib import Path


def simulate_git_repository():
    """模拟 Git 仓库，存储期望状态"""
    repo_path = Path("git-repo")
    repo_path.mkdir(exist_ok=True)

    # 初始期望状态
    desired_state = {
        "version": "1.0.0",
        "replicas": 3,
        "image": "nginx:1.21",
        "last_updated": time.time()
    }

    with open(repo_path / "deployment.json", "w", encoding="utf-8") as f:
        json.dump(desired_state, f, indent=2, ensure_ascii=False)

    return repo_path


def simulate_target_environment():
    """模拟目标环境，存储实际状态"""
    env_path = Path("target-env")
    env_path.mkdir(exist_ok=True)

    # 初始实际状态（可能与期望状态不同）
    actual_state = {
        "version": "0.9.0",
        "replicas": 2,
        "image": "nginx:1.20",
        "last_updated": time.time()
    }

    with open(env_path / "deployment.json", "w", encoding="utf-8") as f:
        json.dump(actual_state, f, indent=2, ensure_ascii=False)

    return env_path


def detect_git_changes(repo_path):
    """检测 Git 仓库是否有变更"""
    # 在真实场景中，这会检查 Git 提交历史
    # 这里我们简单地检查文件修改时间
    deployment_file = repo_path / "deployment.json"
    if not hasattr(detect_git_changes, "last_check"):
        detect_git_changes.last_check = 0

    current_mtime = deployment_file.stat().st_mtime
    has_changed = current_mtime > detect_git_changes.last_check
    detect_git_changes.last_check = current_mtime

    return has_changed


def pull_from_git(repo_path):
    """从 Git 仓库拉取最新的期望状态"""
    print("🔄 从 Git 仓库拉取最新的期望状态...")
    with open(repo_path / "deployment.json", "r", encoding="utf-8") as f:
        desired_state = json.load(f)
    print(f"✅ 拉取成功: 版本 {desired_state['version']}, 副本数 {desired_state['replicas']}")
    return desired_state


def apply_to_environment(desired_state, env_path):
    """将期望状态应用到目标环境"""
    print("🚀 将变更应用到目标环境...")

    # 在真实场景中，这会调用 kubectl 或其他工具
    # 这里我们直接更新文件
    with open(env_path / "deployment.json", "w", encoding="utf-8") as f:
        json.dump(desired_state, f, indent=2, ensure_ascii=False)

    print(f"✅ 应用成功: 环境现在运行版本 {desired_state['version']}")


def gitops_workflow_simulation():
    """模拟完整的 GitOps 工作流程"""
    print("🎯 开始 GitOps 工作流程模拟")
    print("=" * 50)

    # 初始化 Git 仓库和目标环境
    repo_path = simulate_git_repository()
    env_path = simulate_target_environment()

    print("📁 初始化完成:")
    print(f"   Git 仓库: {repo_path}")
    print(f"   目标环境: {env_path}")
    print()

    # 模拟开发者提交新版本
    print("💻 开发者提交新版本到 Git 仓库...")
    with open(repo_path / "deployment.json", "r", encoding="utf-8") as f:
        new_state = json.load(f)

    new_state["version"] = "1.1.0"
    new_state["replicas"] = 5
    new_state["last_updated"] = time.time()

    with open(repo_path / "deployment.json", "w", encoding="utf-8") as f:
        json.dump(new_state, f, indent=2, ensure_ascii=False)

    print("✅ 新版本提交完成!")
    print()

    # GitOps 代理工作流程
    print("🤖 GitOps 代理开始工作...")

    # 步骤 1: 检测变更
    if detect_git_changes(repo_path):
        print("🔍 检测到 Git 仓库有变更")

        # 步骤 2: 拉取期望状态
        desired_state = pull_from_git(repo_path)

        # 步骤 3: 应用到环境
        apply_to_environment(desired_state, env_path)

        print("\n🎉 GitOps 工作流程完成!")
        print("系统现在处于期望状态 ✨")
    else:
        print("❌ 未检测到任何变更")


if __name__ == "__main__":
    gitops_workflow_simulation()