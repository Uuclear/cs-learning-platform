#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI/CD 流水线阶段模拟示例

本示例模拟一个完整的 CI/CD 流水线，包含以下阶段：
1. 代码检查 (lint)
2. 单元测试 (test)
3. 构建 (build)
4. 部署 (deploy)

每个阶段都会进行验证，如果失败则整个流水线停止。
"""

import time
import random
import sys


def lint_code():
    """代码检查阶段 - 模拟代码风格检查"""
    print("🔍 正在执行代码检查...")
    time.sleep(1)

    # 模拟 90% 的成功率
    if random.random() < 0.9:
        print("✅ 代码检查通过！")
        return True
    else:
        print("❌ 代码检查失败：发现代码风格问题")
        return False


def run_tests():
    """单元测试阶段 - 模拟运行测试套件"""
    print("🧪 正在运行单元测试...")
    time.sleep(2)

    # 模拟 85% 的成功率
    if random.random() < 0.85:
        print("✅ 所有测试通过！")
        return True
    else:
        print("❌ 测试失败：发现功能缺陷")
        return False


def build_artifact():
    """构建阶段 - 模拟创建可部署的制品"""
    print("🔨 正在构建应用...")
    time.sleep(1.5)

    # 模拟 95% 的成功率
    if random.random() < 0.95:
        print("✅ 构建成功！生成了部署包")
        return True
    else:
        print("❌ 构建失败：编译错误")
        return False


def deploy_to_staging():
    """部署到预发布环境"""
    print("🚀 正在部署到预发布环境...")
    time.sleep(1)

    # 模拟 98% 的成功率
    if random.random() < 0.98:
        print("✅ 预发布环境部署成功！")
        return True
    else:
        print("❌ 预发布环境部署失败")
        return False


def main():
    """主函数 - 执行完整的 CI/CD 流水线"""
    print("🏗️  开始 CI/CD 流水线执行")
    print("=" * 50)

    # 阶段 1: 代码检查
    if not lint_code():
        print("\n❌ 流水线在代码检查阶段失败")
        sys.exit(1)

    print()

    # 阶段 2: 单元测试
    if not run_tests():
        print("\n❌ 流水线在测试阶段失败")
        sys.exit(1)

    print()

    # 阶段 3: 构建
    if not build_artifact():
        print("\n❌ 流水线在构建阶段失败")
        sys.exit(1)

    print()

    # 阶段 4: 部署到预发布环境
    if not deploy_to_staging():
        print("\n❌ 流水线在部署阶段失败")
        sys.exit(1)

    print()
    print("🎉 CI/CD 流水线执行成功！")
    print("✅ 应用已成功部署到预发布环境")


if __name__ == "__main__":
    main()