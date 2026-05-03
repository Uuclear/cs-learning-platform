#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 3: Git 钩子应用

本示例演示如何创建实用的 Git 钩子：
1. 预提交钩子：验证提交信息格式
2. 后提交钩子：发送通知
3. 预推送钩子：运行测试

这些钩子可以帮助团队维护代码质量和提交规范。
"""

import os
import re
import sys
import subprocess
from typing import List, Tuple


class GitHookSimulator:
    """Git 钩子模拟器"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def validate_commit_message(self, message: str) -> Tuple[bool, str]:
        """
        验证提交信息格式

        要求格式: type(scope): description
        例如: feat(auth): 添加用户登录功能
        """
        # 常见的提交类型
        valid_types = ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']

        # 提交信息格式正则表达式
        pattern = r'^([a-z]+)(?:$([^)]+)$)?: (.+)$'
        match = re.match(pattern, message.strip())

        if not match:
            return False, "提交信息格式错误。应为: type(scope): description"

        commit_type = match.group(1)
        if commit_type not in valid_types:
            return False, f"无效的提交类型: {commit_type}。有效类型: {', '.join(valid_types)}"

        description = match.group(3)
        if len(description) < 10:
            return False, "描述太短，至少需要10个字符"

        if description.endswith('.'):
            return False, "描述不应以句号结尾"

        return True, "提交信息格式正确"

    def pre_commit_hook(self, commit_message_file: str) -> bool:
        """
        预提交钩子 - 验证提交信息

        Args:
            commit_message_file: 提交信息文件路径

        Returns:
            bool: True 表示通过验证，False 表示拒绝提交
        """
        print("🔍 执行预提交钩子...")

        try:
            with open(commit_message_file, 'r', encoding='utf-8') as f:
                message = f.read()

            # 跳过空行和注释行
            lines = [line.strip() for line in message.split('\n')
                    if line.strip() and not line.strip().startswith('#')]

            if not lines:
                print("❌ 提交信息为空")
                return False

            first_line = lines[0]
            is_valid, reason = self.validate_commit_message(first_line)

            if is_valid:
                print(f"✅ {reason}")
                return True
            else:
                print(f"❌ {reason}")
                print("\n提交信息示例:")
                print("  ✅ feat(auth): 添加用户登录功能")
                print("  ✅ fix(api): 修复用户信息获取接口的空指针异常")
                print("  ✅ docs(readme): 更新安装说明")
                return False

        except Exception as e:
            print(f"❌ 读取提交信息文件失败: {e}")
            return False

    def post_commit_hook(self) -> bool:
        """
        后提交钩子 - 发送通知

        Returns:
            bool: True 表示成功，False 表示失败
        """
        print("📨 执行后提交钩子...")

        try:
            # 获取最新提交信息
            result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%h - %s (%an)'],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )

            if result.returncode != 0:
                print(f"❌ 获取提交信息失败: {result.stderr}")
                return False

            commit_info = result.stdout.strip()
            print(f"✅ 已记录提交: {commit_info}")

            # 模拟发送通知（实际项目中可以集成 Slack、邮件等）
            print("✅ 通知已发送到团队频道")
            return True

        except Exception as e:
            print(f"❌ 后提交钩子执行失败: {e}")
            return False

    def pre_push_hook(self) -> bool:
        """
        预推送钩子 - 运行测试

        Returns:
            bool: True 表示测试通过，False 表示测试失败
        """
        print("🧪 执行预推送钩子...")

        try:
            # 检查是否有未暂存的更改
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )

            if result.returncode != 0:
                print(f"❌ 检查工作区状态失败: {result.stderr}")
                return False

            if result.stdout.strip():
                print("⚠️  工作区有未暂存的更改:")
                for line in result.stdout.strip().split('\n'):
                    print(f"   {line}")
                response = input("是否继续推送？(y/N): ")
                if response.lower() != 'y':
                    return False

            # 模拟运行测试（实际项目中会运行真实的测试命令）
            print("   运行单元测试...")
            # 这里可以替换为实际的测试命令，如 pytest、npm test 等
            time.sleep(1)  # 模拟测试时间

            # 模拟测试结果（在实际项目中，这里会检查测试命令的返回码）
            test_passed = True  # 假设测试通过

            if test_passed:
                print("✅ 所有测试通过")
                return True
            else:
                print("❌ 测试失败，推送被阻止")
                return False

        except KeyboardInterrupt:
            print("\n❌ 推送被用户中断")
            return False
        except Exception as e:
            print(f"❌ 预推送钩子执行失败: {e}")
            return False

    def install_hooks(self, hook_names: List[str]) -> bool:
        """
        安装 Git 钩子到仓库

        Args:
            hook_names: 要安装的钩子名称列表

        Returns:
            bool: True 表示安装成功
        """
        hooks_dir = os.path.join(self.repo_path, '.git', 'hooks')
        if not os.path.exists(hooks_dir):
            print(f"❌ 未找到 Git hooks 目录: {hooks_dir}")
            return False

        # 简化的钩子脚本模板
        hook_templates = {
            'pre-commit': '''#!/bin/sh
# 预提交钩子 - 验证提交信息格式
python3 -c "
import sys
from pathlib import Path

# 简化的提交信息验证
with open(sys.argv[1] if len(sys.argv) > 1 else '.git/COMMIT_EDITMSG', 'r') as f:
    message = f.read().strip()

# 跳过注释行
lines = [line for line in message.split('\\n') if line and not line.startswith('#')]
if lines:
    first_line = lines[0]
    if not re.match(r'^[a-z]+($[^)]+$)?: .{10,}$', first_line):
        print('❌ 提交信息格式错误！')
        print('格式: type(scope): description (至少10个字符)')
        sys.exit(1)
print('✅ 提交信息格式正确')
"
''',
            'post-commit': '''#!/bin/sh
# 后提交钩子 - 记录提交信息
echo "✅ 新提交: $(git log -1 --pretty=format:'%h - %s (%an)')"
echo "✅ 通知已发送到团队频道"
''',
            'pre-push': '''#!/bin/sh
# 预推送钩子 - 运行测试
echo "🧪 运行测试..."
# 在实际项目中，这里会运行真实的测试命令
sleep 1
echo "✅ 所有测试通过"
'''
        }

        success_count = 0
        for hook_name in hook_names:
            if hook_name not in hook_templates:
                print(f"⚠️  不支持的钩子: {hook_name}")
                continue

            hook_path = os.path.join(hooks_dir, hook_name)
            try:
                with open(hook_path, 'w') as f:
                    f.write(hook_templates[hook_name])
                os.chmod(hook_path, 0o755)  # 添加执行权限
                print(f"✅ 安装钩子: {hook_name}")
                success_count += 1
            except Exception as e:
                print(f"❌ 安装钩子失败 {hook_name}: {e}")

        print(f"\n🎉 成功安装 {success_count}/{len(hook_names)} 个钩子")
        return success_count > 0


def demonstrate_git_hooks():
    """演示 Git 钩子的使用"""
    print("=== Git 钩子应用演示 ===\n")

    simulator = GitHookSimulator()

    # 演示提交信息验证
    print("1. 提交信息格式验证:")
    test_messages = [
        "feat(auth): 添加用户登录功能",  # 正确
        "fix: 修复bug",  # 错误：描述太短
        "invalid message format",  # 错误：格式不对
        "docs(readme): 更新安装说明和使用指南，包含详细的配置步骤。"  # 正确但有句号
    ]

    for msg in test_messages:
        is_valid, reason = simulator.validate_commit_message(msg)
        status = "✅" if is_valid else "❌"
        print(f"   {status} '{msg}' -> {reason}")

    print()

    # 演示钩子安装
    print("2. 钩子安装演示:")
    # 注意：这只是一个模拟，在真实环境中需要在 Git 仓库中运行
    print("   在实际项目中，可以运行以下命令安装钩子:")
    print("   $ python example-03-git-hooks.py --install pre-commit post-commit")
    print()

    # 演示钩子执行流程
    print("3. 钩子执行流程:")
    print("   开发者执行 git commit -> 触发 pre-commit 钩子")
    print("   pre-commit 验证通过 -> 创建提交 -> 触发 post-commit 钩子")
    print("   开发者执行 git push -> 触发 pre-push 钩子")
    print("   pre-push 测试通过 -> 允许推送")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        # 安装模式
        hook_names = sys.argv[2:] if len(sys.argv) > 2 else ['pre-commit', 'post-commit', 'pre-push']
        simulator = GitHookSimulator()
        simulator.install_hooks(hook_names)
    else:
        # 演示模式
        demonstrate_git_hooks()