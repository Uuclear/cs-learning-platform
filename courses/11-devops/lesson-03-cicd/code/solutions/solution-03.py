#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 03: GitHub Actions 工作流优化

这个解决方案展示了一个更完整和优化的 GitHub Actions 工作流，
包含缓存、并行作业、条件执行等最佳实践。
"""

import yaml
from typing import Dict, List


def create_optimized_workflow():
    """创建一个优化的 GitHub Actions 工作流"""
    workflow = {
        "name": "优化的 Python CI/CD",
        "on": {
            "push": {
                "branches": ["main", "develop"]
            },
            "pull_request": {
                "branches": ["main"]
            },
            "workflow_dispatch": {}  # 允许手动触发
        },
        "env": {
            "PYTHON_VERSION": "3.11"
        },
        "jobs": {
            "lint": {
                "name": "代码检查",
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"name": "检出代码", "uses": "actions/checkout@v4"},
                    {"name": "设置 Python", "uses": "actions/setup-python@v5", "with": {"python-version": "${{ env.PYTHON_VERSION }}"}},
                    {"name": "缓存依赖", "uses": "actions/cache@v4", "with": {"path": "~/.cache/pip", "key": "${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}"}},
                    {"name": "安装依赖", "run": "pip install flake8 black"},
                    {"name": "运行代码检查", "run": "flake8 . --count --show-source --statistics"}
                ]
            },
            "test": {
                "name": "运行测试",
                "runs-on": "ubuntu-latest",
                "needs": ["lint"],
                "strategy": {
                    "matrix": {
                        "python-version": ["3.9", "3.10", "3.11"],
                        "os": ["ubuntu-latest", "windows-latest"]
                    }
                },
                "steps": [
                    {"name": "检出代码", "uses": "actions/checkout@v4"},
                    {"name": "设置 Python", "uses": "actions/setup-python@v5", "with": {"python-version": "${{ matrix.python-version }}"}},
                    {"name": "缓存依赖", "uses": "actions/cache@v4", "with": {"path": "~/.cache/pip", "key": "${{ runner.os }}-pip-${{ matrix.python-version }}-${{ hashFiles('**/requirements.txt') }}", "restore-keys": "${{ runner.os }}-pip-"}},
                    {"name": "安装依赖", "run": "pip install -r requirements.txt"},
                    {"name": "运行测试", "run": "python -m pytest tests/ --cov=src --cov-report=xml"},
                    {"name": "上传覆盖率报告", "uses": "codecov/codecov-action@v4", "if": "matrix.os == 'ubuntu-latest' && matrix.python-version == '3.11'"}
                ]
            },
            "build": {
                "name": "构建制品",
                "runs-on": "ubuntu-latest",
                "needs": ["test"],
                "if": "github.ref == 'refs/heads/main'",
                "steps": [
                    {"name": "检出代码", "uses": "actions/checkout@v4"},
                    {"name": "设置 Python", "uses": "actions/setup-python@v5", "with": {"python-version": "${{ env.PYTHON_VERSION }}"}},
                    {"name": "安装构建工具", "run": "pip install build twine"},
                    {"name": "构建包", "run": "python -m build"},
                    {"name": "上传制品", "uses": "actions/upload-artifact@v4", "with": {"name": "python-package", "path": "dist/"}}
                ]
            },
            "deploy-staging": {
                "name": "部署到预发布环境",
                "runs-on": "ubuntu-latest",
                "needs": ["build"],
                "environment": "staging",
                "steps": [
                    {"name": "下载制品", "uses": "actions/download-artifact@v4", "with": {"name": "python-package", "path": "dist/"}},
                    {"name": "部署到预发布", "run": "echo 'Deploying to staging environment...'", "env": {"ENV": "staging"}}
                ]
            },
            "deploy-production": {
                "name": "部署到生产环境",
                "runs-on": "ubuntu-latest",
                "needs": ["deploy-staging"],
                "environment": "production",
                "if": "github.ref == 'refs/heads/main'",
                "steps": [
                    {"name": "下载制品", "uses": "actions/download-artifact@v4", "with": {"name": "python-package", "path": "dist/"}},
                    {"name": "部署到生产", "run": "echo 'Deploying to production environment...'", "env": {"ENV": "production"}}
                ]
            }
        }
    }
    return workflow


def validate_workflow_completeness(workflow: Dict) -> List[str]:
    """验证工作流的完整性并返回建议"""
    issues = []

    # 检查是否有适当的触发器
    triggers = workflow.get("on", {})
    if not any(key in triggers for key in ["push", "pull_request", "schedule", "workflow_dispatch"]):
        issues.append("缺少适当的触发器配置")

    # 检查是否有并行作业
    jobs = workflow.get("jobs", {})
    if len(jobs) == 1:
        issues.append("考虑将独立的步骤拆分为并行作业以提高效率")

    # 检查是否使用了缓存
    uses_cache = False
    for job in jobs.values():
        steps = job.get("steps", [])
        for step in steps:
            if isinstance(step, dict) and step.get("uses", "").startswith("actions/cache"):
                uses_cache = True
                break
    if not uses_cache:
        issues.append("建议添加依赖缓存以加速工作流执行")

    # 检查是否有环境变量管理
    if "env" not in workflow and not any("env" in job for job in jobs.values()):
        issues.append("考虑使用环境变量来管理配置")

    return issues


def main():
    """主函数 - 创建、验证并展示优化的工作流"""
    print("🚀 GitHub Actions 工作流优化示例")
    print("=" * 50)

    # 创建优化的工作流
    workflow = create_optimized_workflow()
    print("✅ 创建了优化的工作流")

    # 验证工作流
    issues = validate_workflow_completeness(workflow)
    if issues:
        print("\n⚠️  发现以下改进建议:")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("\n✅ 工作流符合最佳实践")

    # 显示工作流统计信息
    job_count = len(workflow["jobs"])
    matrix_jobs = sum(1 for job in workflow["jobs"].values() if "strategy" in job)

    print(f"\n📊 工作流统计:")
    print(f"  • 作业数量: {job_count}")
    print(f"  • 矩阵作业: {matrix_jobs}")
    print(f"  • 触发器: {list(workflow['on'].keys())}")

    # 保存工作流
    try:
        with open(".github/workflows/optimized-ci-cd.yml", "w", encoding="utf-8") as f:
            yaml.dump(workflow, f, default_flow_style=False, allow_unicode=True, indent=2)
        print("\n✅ 优化的工作流已保存到 .github/workflows/optimized-ci-cd.yml")
    except Exception as e:
        print(f"\n❌ 保存失败: {e}")


if __name__ == "__main__":
    main()