#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions 工作流生成和验证示例

本示例演示如何生成和验证 GitHub Actions 工作流 YAML 文件。
"""

import yaml
import json
from typing import Dict, List


def generate_github_actions_workflow():
    """生成一个典型的 Python 应用 CI/CD 工作流"""
    workflow = {
        "name": "Python CI/CD Pipeline",
        "on": {
            "push": {
                "branches": ["main"]
            },
            "pull_request": {
                "branches": ["main"]
            }
        },
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "检出代码",
                        "uses": "actions/checkout@v4"
                    },
                    {
                        "name": "设置 Python",
                        "uses": "actions/setup-python@v5",
                        "with": {
                            "python-version": "3.11"
                        }
                    },
                    {
                        "name": "安装依赖",
                        "run": "pip install -r requirements.txt"
                    },
                    {
                        "name": "运行测试",
                        "run": "python -m pytest tests/"
                    }
                ]
            },
            "deploy": {
                "needs": "test",
                "runs-on": "ubuntu-latest",
                "if": "github.ref == 'refs/heads/main'",
                "steps": [
                    {
                        "name": "检出代码",
                        "uses": "actions/checkout@v4"
                    },
                    {
                        "name": "部署到生产环境",
                        "run": "echo 'Deploying to production...'"
                    }
                ]
            }
        }
    }
    return workflow


def validate_workflow_structure(workflow: Dict) -> bool:
    """验证工作流结构是否符合基本要求"""
    required_keys = ["name", "on", "jobs"]

    # 检查必需的顶层键
    for key in required_keys:
        if key not in workflow:
            print(f"❌ 缺少必需的键: {key}")
            return False

    # 检查触发器配置
    if "push" not in workflow["on"] and "pull_request" not in workflow["on"]:
        print("❌ 工作流必须至少有一个触发器 (push 或 pull_request)")
        return False

    # 检查是否有作业
    if not workflow["jobs"]:
        print("❌ 工作流必须至少包含一个作业")
        return False

    # 检查每个作业是否有步骤
    for job_name, job_config in workflow["jobs"].items():
        if "steps" not in job_config:
            print(f"❌ 作业 {job_name} 必须包含 steps")
            return False
        if not job_config["steps"]:
            print(f"❌ 作业 {job_name} 的 steps 不能为空")
            return False

    return True


def save_workflow_to_yaml(workflow: Dict, filename: str):
    """将工作流保存为 YAML 文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(workflow, f, default_flow_style=False, allow_unicode=True, indent=2)
        print(f"✅ 工作流已保存到 {filename}")
    except Exception as e:
        print(f"❌ 保存工作流失败: {e}")


def main():
    """主函数 - 生成、验证并保存 GitHub Actions 工作流"""
    print("🤖 GitHub Actions 工作流生成器")
    print("=" * 40)

    # 生成工作流
    workflow = generate_github_actions_workflow()
    print("✅ 工作流生成完成")

    # 验证工作流结构
    print("\n🔍 验证工作流结构...")
    if validate_workflow_structure(workflow):
        print("✅ 工作流结构验证通过")
    else:
        print("❌ 工作流结构验证失败")
        return

    # 显示工作流概览
    print(f"\n📋 工作流名称: {workflow['name']}")
    print(f"🎯 触发器: {list(workflow['on'].keys())}")
    print(f"🔧 作业数量: {len(workflow['jobs'])}")

    # 保存为 YAML 文件
    workflow_file = ".github/workflows/ci-cd.yml"
    save_workflow_to_yaml(workflow, workflow_file)

    # 显示 YAML 内容预览
    print(f"\n📄 {workflow_file} 内容预览:")
    print("-" * 50)
    yaml_content = yaml.dump(workflow, default_flow_style=False, allow_unicode=True, indent=2)
    lines = yaml_content.split('\n')
    for i, line in enumerate(lines[:15]):  # 只显示前15行
        print(line)
    if len(lines) > 15:
        print("... (内容被截断)")


if __name__ == "__main__":
    main()