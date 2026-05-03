#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2：状态协调完整实现

这个脚本实现了 GitOps 中的核心概念——状态协调（Reconciliation）：
- 持续比较期望状态和实际状态
- 自动执行必要的操作来使实际状态匹配期望状态
- 支持复杂的服务拓扑和配置变更
"""

import json
import time
import copy
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple


class StateReconciler:
    """状态协调器，负责比较和同步状态"""

    def __init__(self, repo_path: Path, env_path: Path):
        self.repo_path = repo_path
        self.env_path = env_path
        self.repo_path.mkdir(exist_ok=True)
        self.env_path.mkdir(exist_ok=True)

        # 状态文件路径
        self.desired_file = self.repo_path / "desired_state.json"
        self.actual_file = self.env_path / "actual_state.json"

    def initialize_states(self):
        """初始化期望状态和实际状态"""
        # 初始期望状态
        desired_state = {
            "services": [
                {"name": "web", "image": "nginx:1.21", "replicas": 3, "port": 80},
                {"name": "api", "image": "myapi:v1.0", "replicas": 2, "port": 8080}
            ],
            "config_maps": {
                "app-config": {"LOG_LEVEL": "info", "DB_HOST": "db.example.com"}
            },
            "metadata": {"version": "1.0.0", "created_at": datetime.now().isoformat()}
        }

        # 初始实际状态（与期望状态不同）
        actual_state = {
            "services": [
                {"name": "web", "image": "nginx:1.20", "replicas": 2, "port": 80},  # 版本和副本数不同
                {"name": "cache", "image": "redis:6.2", "replicas": 1, "port": 6379}  # 多余的服务
            ],
            "config_maps": {
                "app-config": {"LOG_LEVEL": "debug", "DB_HOST": "old-db.example.com"}  # 配置不同
            },
            "reconciliation_metadata": {"last_synced": None, "status": "out_of_sync"}
        }

        self._save_desired_state(desired_state)
        self._save_actual_state(actual_state)

        print("✅ 状态初始化完成")
        print(f"   期望服务数: {len(desired_state['services'])}")
        print(f"   实际服务数: {len(actual_state['services'])}")

    def _save_desired_state(self, state: Dict[str, Any]):
        """保存期望状态"""
        with open(self.desired_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def _save_actual_state(self, state: Dict[str, Any]):
        """保存实际状态"""
        with open(self.actual_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def load_desired_state(self) -> Dict[str, Any]:
        """加载期望状态"""
        if self.desired_file.exists():
            with open(self.desired_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"services": [], "config_maps": {}}

    def load_actual_state(self) -> Dict[str, Any]:
        """加载实际状态"""
        if self.actual_file.exists():
            with open(self.actual_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"services": [], "config_maps": {}, "reconciliation_metadata": {}}

    def compare_service_states(self, desired_services: List[Dict], actual_services: List[Dict]) -> Tuple[List[str], bool]:
        """比较服务状态，返回操作列表和是否需要协调"""
        operations = []
        needs_reconciliation = False

        # 转换为字典以便查找
        desired_dict = {svc["name"]: svc for svc in desired_services}
        actual_dict = {svc["name"]: svc for svc in actual_services}

        # 检查需要创建或更新的服务
        for name, desired_svc in desired_dict.items():
            if name not in actual_dict:
                operations.append(f"CREATE service '{name}' (image: {desired_svc['image']}, replicas: {desired_svc['replicas']})")
                needs_reconciliation = True
            elif actual_dict[name] != desired_svc:
                # 比较具体字段
                actual_svc = actual_dict[name]
                changes = []
                if actual_svc["image"] != desired_svc["image"]:
                    changes.append(f"image {actual_svc['image']} → {desired_svc['image']}")
                if actual_svc["replicas"] != desired_svc["replicas"]:
                    changes.append(f"replicas {actual_svc['replicas']} → {desired_svc['replicas']}")
                if actual_svc["port"] != desired_svc["port"]:
                    changes.append(f"port {actual_svc['port']} → {desired_svc['port']}")

                if changes:
                    operations.append(f"UPDATE service '{name}' ({', '.join(changes)})")
                    needs_reconciliation = True

        # 检查需要删除的服务
        for name in actual_dict:
            if name not in desired_dict:
                operations.append(f"DELETE service '{name}'")
                needs_reconciliation = True

        return operations, needs_reconciliation

    def compare_config_maps(self, desired_configs: Dict, actual_configs: Dict) -> Tuple[List[str], bool]:
        """比较配置映射，返回操作列表和是否需要协调"""
        operations = []
        needs_reconciliation = False

        # 检查需要创建或更新的配置
        for name, desired_config in desired_configs.items():
            if name not in actual_configs:
                operations.append(f"CREATE config_map '{name}'")
                needs_reconciliation = True
            elif actual_configs[name] != desired_config:
                operations.append(f"UPDATE config_map '{name}'")
                needs_reconciliation = True

        # 检查需要删除的配置
        for name in actual_configs:
            if name not in desired_configs:
                operations.append(f"DELETE config_map '{name}'")
                needs_reconciliation = True

        return operations, needs_reconciliation

    def reconcile(self) -> bool:
        """执行完整的状态协调"""
        print("\n🔄 开始状态协调...")

        # 加载当前状态
        desired_state = self.load_desired_state()
        actual_state = self.load_actual_state()

        # 比较服务状态
        service_ops, service_needs = self.compare_service_states(
            desired_state.get("services", []),
            actual_state.get("services", [])
        )

        # 比较配置状态
        config_ops, config_needs = self.compare_config_maps(
            desired_state.get("config_maps", {}),
            actual_state.get("config_maps", {})
        )

        all_operations = service_ops + config_ops
        needs_reconciliation = service_needs or config_needs

        if not needs_reconciliation:
            print("✅ 状态已经同步，无需操作")
            actual_state["reconciliation_metadata"] = {
                "last_synced": datetime.now().isoformat(),
                "status": "synced",
                "operations_performed": []
            }
            self._save_actual_state(actual_state)
            return False

        # 执行协调操作
        print("🔧 执行以下协调操作:")
        for op in all_operations:
            print(f"  - {op}")

        # 更新实际状态以匹配期望状态
        new_actual_state = {
            "services": copy.deepcopy(desired_state.get("services", [])),
            "config_maps": copy.deepcopy(desired_state.get("config_maps", {})),
            "reconciliation_metadata": {
                "last_synced": datetime.now().isoformat(),
                "status": "synced",
                "operations_performed": all_operations,
                "desired_version": desired_state.get("metadata", {}).get("version", "unknown")
            }
        }

        self._save_actual_state(new_actual_state)
        print("✅ 状态协调完成!")
        return True

    def simulate_developer_updates(self):
        """模拟开发者在协调过程中提交新变更"""
        print("\n💡 开发者提交新变更...")

        desired_state = self.load_desired_state()

        # 添加新服务
        desired_state["services"].append({
            "name": "cache",
            "image": "redis:7.0",
            "replicas": 2,
            "port": 6379
        })

        # 更新配置
        desired_state["config_maps"]["app-config"]["NEW_FEATURE"] = "enabled"
        desired_state["config_maps"]["app-config"]["LOG_LEVEL"] = "warn"

        # 更新版本
        current_version = desired_state.get("metadata", {}).get("version", "1.0.0")
        version_parts = current_version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        desired_state["metadata"]["version"] = new_version
        desired_state["metadata"]["updated_at"] = datetime.now().isoformat()

        self._save_desired_state(desired_state)
        print(f"✅ 新版本 {new_version} 已提交到 Git")


def main():
    """主函数：演示状态协调解决方案"""
    print("🎯 状态协调完整解决方案")
    print("=" * 50)

    # 初始化协调器
    reconciler = StateReconciler(
        Path("git-repo-reconciliation"),
        Path("target-env-reconciliation")
    )

    # 初始化状态
    reconciler.initialize_states()

    # 第一次协调
    print("\n🔁 第一次协调循环:")
    reconciler.reconcile()

    # 模拟开发者提交新变更
    reconciler.simulate_developer_updates()

    # 第二次协调（处理新变更）
    print("\n🔁 第二次协调循环（处理新变更）:")
    reconciler.reconcile()

    # 验证最终状态
    print("\n" + "="*50)
    print("🔍 最终状态验证:")
    final_actual = reconciler.load_actual_state()
    final_desired = reconciler.load_desired_state()

    print(f"   服务数量: {len(final_actual['services'])} (期望: {len(final_desired['services'])})")
    print(f"   配置数量: {len(final_actual['config_maps'])} (期望: {len(final_desired['config_maps'])})")
    print(f"   协调状态: {final_actual['reconciliation_metadata']['status']}")
    print(f"   最后同步时间: {final_actual['reconciliation_metadata']['last_synced']}")

    print("\n🎉 状态协调解决方案演示完成!")
    print("关键特性:")
    print("• 持续比较期望状态和实际状态")
    print("• 自动识别差异并生成操作计划")
    print("• 支持复杂资源类型（服务、配置等）")
    print("• 幂等性保证：多次协调产生相同结果")


if __name__ == "__main__":
    main()