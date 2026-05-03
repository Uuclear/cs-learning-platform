#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: 提交信息格式验证器

实现一个提交信息 linter，强制执行 conventional commit 格式规范。
"""

import re
import sys
from typing import List, Tuple, Optional


class CommitMessageLinter:
    """提交信息格式验证器"""

    def __init__(self):
        # Conventional Commits 规范
        # https://www.conventionalcommits.org/
        self.valid_types = {
            'feat': '新功能',
            'fix': 'bug 修复',
            'docs': '文档变更',
            'style': '代码格式调整（不影响代码逻辑）',
            'refactor': '代码重构（既不是新增功能也不是修复 bug）',
            'perf': '性能优化',
            'test': '添加缺失的测试或修正现有测试',
            'build': '影响构建系统或外部依赖的变更',
            'ci': '持续集成相关的变更',
            'chore': '其他不修改 src 或 test 文件的变更',
            'revert': '撤销之前的提交'
        }

        self.valid_scopes = [
            'auth', 'api', 'ui', 'db', 'config', 'deps', 'docs', 'tests',
            'ci', 'build', 'perf', 'security', 'i18n', 'a11y'
        ]

        # 提交信息格式正则表达式
        # type(scope)!: description
        # type(scope): description
        # type!: description
        # type: description
        self.commit_pattern = re.compile(
            r'^(?P<type>[a-z]+)'
            r'(?:$(?P<scope>[^)]+)$)?'
            r'(?P<breaking>!)?'
            r':\s*'
            r'(?P<description>.+)$'
        )

    def validate_commit_message(self, message: str) -> Tuple[bool, List[str]]:
        """
        验证提交信息格式

        Args:
            message: 提交信息

        Returns:
            Tuple[是否有效, 错误信息列表]
        """
        errors = []

        # 移除注释行和空行
        lines = []
        for line in message.split('\n'):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                lines.append(stripped)

        if not lines:
            return False, ["提交信息不能为空"]

        # 只检查第一行（标题行）
        title = lines[0]

        # 检查长度
        if len(title) > 72:
            errors.append(f"标题行过长 ({len(title)} 字符)，建议不超过 72 字符")

        # 检查格式
        match = self.commit_pattern.match(title)
        if not match:
            errors.append(
                "提交信息格式不符合 Conventional Commits 规范\n"
                "正确格式: type(scope)!: description\n"
                "示例: feat(auth): 添加用户登录功能"
            )
            return False, errors

        # 验证类型
        commit_type = match.group('type')
        if commit_type not in self.valid_types:
            valid_types_str = ', '.join(self.valid_types.keys())
            errors.append(f"无效的提交类型 '{commit_type}'。有效类型: {valid_types_str}")

        # 验证 scope（如果存在）
        scope = match.group('scope')
        if scope:
            # 允许自定义 scope，但提供常见 scope 的建议
            if scope.lower() not in [s.lower() for s in self.valid_scopes]:
                common_scopes_str = ', '.join(self.valid_scopes[:5])  # 只显示前5个
                errors.append(
                    f"Scope '{scope}' 不在常见范围内。常见 scope: {common_scopes_str}... "
                    "(自定义 scope 是允许的)"
                )

        # 验证描述
        description = match.group('description')
        if not description:
            errors.append("描述不能为空")
        elif len(description) < 5:
            errors.append("描述太短，至少需要 5 个字符")
        elif description[0].isupper():
            errors.append("描述不应以大写字母开头")
        elif description.endswith('.'):
            errors.append("描述不应以句号结尾")

        # 检查是否有正文（如果有，应该与标题用空行分隔）
        if len(lines) > 1:
            if lines[1].strip() != '':
                errors.append("标题和正文之间应该用空行分隔")

        # 检查正文行长度（如果有正文）
        for i, line in enumerate(lines[2:], start=2):
            if len(line) > 80:
                errors.append(f"正文第 {i-1} 行过长 ({len(line)} 字符)，建议不超过 80 字符")

        return len(errors) == 0, errors

    def get_suggestions(self, message: str) -> List[str]:
        """
        为无效的提交信息提供建议

        Args:
            message: 提交信息

        Returns:
            建议列表
        """
        suggestions = []
        lines = [line.strip() for line in message.split('\n')
                if line.strip() and not line.strip().startswith('#')]

        if not lines:
            return ["请输入提交信息"]

        title = lines[0]

        # 检查是否缺少冒号
        if ':' not in title:
            # 尝试猜测类型
            first_word = title.split()[0].lower() if title.split() else ""
            if first_word in self.valid_types:
                suggestions.append(f"添加冒号和空格: '{first_word}: {title[len(first_word):].strip()}'")
            else:
                suggestions.append("使用格式: type: description")

        # 检查是否只有类型没有描述
        parts = title.split(':', 1)
        if len(parts) == 2 and not parts[1].strip():
            suggestions.append("添加描述，说明做了什么以及为什么")

        return suggestions

    def format_error_message(self, errors: List[str], suggestions: List[str]) -> str:
        """格式化错误信息"""
        output = ["❌ 提交信息验证失败:\n"]

        for error in errors:
            output.append(f"  • {error}")

        if suggestions:
            output.append("\n💡 建议:")
            for suggestion in suggestions:
                output.append(f"  • {suggestion}")

        output.append("\n📋 Conventional Commits 格式示例:")
        examples = [
            "feat(auth): 添加 OAuth2 登录支持",
            "fix(api): 修复用户信息接口的空指针异常",
            "docs(readme): 更新安装和配置说明",
            "refactor(ui)!: 重写组件 API（破坏性变更）",
            "perf(db): 优化数据库查询性能"
        ]
        for example in examples:
            output.append(f"  • {example}")

        return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python solution-02.py <commit-message-file>")
        print("或者: echo 'commit message' | python solution-02.py -")
        sys.exit(1)

    if sys.argv[1] == '-':
        # 从标准输入读取
        commit_message = sys.stdin.read()
    else:
        # 从文件读取
        try:
            with open(sys.argv[1], 'r', encoding='utf-8') as f:
                commit_message = f.read()
        except FileNotFoundError:
            print(f"错误: 文件 {sys.argv[1]} 不存在")
            sys.exit(1)
        except Exception as e:
            print(f"错误: 读取文件失败 - {e}")
            sys.exit(1)

    linter = CommitMessageLinter()
    is_valid, errors = linter.validate_commit_message(commit_message)

    if is_valid:
        print("✅ 提交信息格式正确")
        sys.exit(0)
    else:
        suggestions = linter.get_suggestions(commit_message)
        error_message = linter.format_error_message(errors, suggestions)
        print(error_message)
        sys.exit(1)


if __name__ == "__main__":
    main()