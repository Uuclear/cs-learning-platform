#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2：状态协调模拟

这个脚本模拟了 GitOps 中的核心概念——状态协调（Reconciliation）：
- 期望状态（Desired State）：来自 Git 仓库的配置
- 实际状态（Actual State）：运行环境中当前的状态
- 协调过程：持续比较两者并执行必要的变更来使实际状态匹配期望状态
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List


def load_desired_state(repo_path: Path) -> Dict[str, Any]:
    """从 Git 仓库加载期望状态"""
    with open(repo_path / "desired.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_actual_state(env_path: Path) -> Dict[str, Any]:
    """从目标环境加载实际状态"""
    actual_file = env_path / "actual.json"
    if actual_file.exists():
        with open(actual_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 如果没有实际状态，返回空状态
        return {"services": []}


def save_actual_state(state: Dict[str, Any], env_path: Path):
    """保存实际状态到目标环境"""
    with open(env_path / "actual.json", "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def compare_states(desired: Dict[str, Any], actual: Dict[str, Any]) -> List[str]:
    """比较期望状态和实际状态，返回需要执行的操作列表"""
    operations = []

    # 比较服务列表
    desired_services = {svc["name"]: svc for svc in desired.get("services", [])}
    actual_services = {svc["name"]: svc for svc in actual.get("services", [])}

    # 检查需要创建的服务
    for name, svc in desired_services.items():
        if name not in actual_services:
            operations.append(f"CREATE service '{name}' (image: {svc['image']}, replicas: {svc['replicas']})")
        elif actual_services[name] != svc:
            operations.append(f"UPDATE service '{name}' (new image: {svc['image']}, new replicas: {svc['replicas']})")

    # 检查需要删除的服务
    for name in actual_services:
        if name not in desired_services:
            operations.append(f"DELETE service '{name}'")

    return operations


def execute_operations(operations: List[str], actual_state: Dict[str, Any], desired_state: Dict[str, Any]):
    """执行协调操作，更新实际状态"""
    print("🔧 执行协调操作:")
    for op in operations:
        print(f"  - {op}")

    # 在真实场景中，这里会调用实际的部署工具
    # 这里我们直接更新状态
    actual_state["services"] = desired_state.get("services", []).copy()
    actual_state["last_reconciled"] = time.time()


def simulate_reconciliation_loop(repo_path: Path, env_path: Path, max_cycles: int = 3):
    """模拟状态协调循环"""
    print("🔄 开始状态协调模拟")
    print("=" * 50)

    # 初始化 Git 仓库（期望状态）
    desired_state = {
        "services": [
            {"name": "web", "image": "nginx:1.21", "replicas": 3},
            {"name": "api", "image": "myapi:v1.0", "replicas": 2}
        ],
        "last_updated": time.time()
    }
    with open(repo_path / "desired.json", "w", encoding="utf-8") as f:
        json.dump(desired_state, f, indent=2, ensure_ascii=False)

    # 初始化目标环境（实际状态）
    env_path.mkdir(exist_ok=True)
    actual_state = {
        "services": [
            {"name": "web", "image": "nginx:1.20", "replicas": 2}  # 与期望状态不同
        ],
        "last_reconciled": time.time()
    }
    save_actual_state(actual_state, env_path)

    print("📁 初始状态:")
    print(f"   期望状态: {len(desired_state['services'])} 个服务")
    print(f"   实际状态: {len(actual_state['services'])} 个服务")
    print()

    for cycle in range(max_cycles):
        print(f"🔁 协调周期 {cycle + 1}:")

        # 加载当前状态
        current_desired = load_desired_state(repo_path)
        current_actual = load_actual_state(env_path)

        # 比较状态
        operations = compare_states(current_desired, current_actual)

        if not operations:
            print("✅ 状态已经同步，无需操作")
            break
        else:
            # 执行协调
            execute_operations(operations, current_actual, current_desired)
            save_actual_state(current_actual, env_path)
            print(f"✅ 协调完成，实际状态已更新")

        # 模拟在协调过程中开发者提交了新变更
        if cycle == 0:
            print("\n💡 开发者在协调过程中提交了新变更...")
            updated_desired = current_desired.copy()
            updated_desired["services"].append(
                {"name": "cache", "image": "redis:7.0", "replicas": 1}
            )
            updated_desired["last_updated"] = time.time()
            with open(repo_path / "desired.json", "w", encoding="utf-8") as f:
                json.dump(updated_desired, f, indent=2, ensure_ascii=False)
            print("✅ 新服务 'cache' 已添加到期望状态")

        print()

    print("🏁 状态协调模拟完成!")
    final_actual = load_actual_state(env_path)
    print(f"最终实际状态包含 {len(final_actual['services'])} 个服务")


if __name__ == "__main__":
    repo_path = Path("git-repo")
    env_path = Path("target-env")
    repo_path.mkdir(exist_ok=True)
    simulate_reconciliation_loop(repo_path, env_path)