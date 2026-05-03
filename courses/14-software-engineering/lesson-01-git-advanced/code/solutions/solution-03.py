#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: Git 分支图生成器

创建一个可视化工具，显示 Git 分支的合并和 rebase 历史。
"""

import subprocess
import sys
from typing import List, Dict, Optional, Tuple


class CommitNode:
    """提交节点"""

    def __init__(self, sha: str, message: str, author: str, timestamp: int):
        self.sha = sha
        self.message = message
        self.author = author
        self.timestamp = timestamp
        self.parents: List['CommitNode'] = []
        self.children: List['CommitNode'] = []
        self.branches: List[str] = []

    def add_parent(self, parent: 'CommitNode'):
        """添加父节点"""
        if parent not in self.parents:
            self.parents.append(parent)
            parent.children.append(self)

    def __str__(self):
        return f"{self.sha[:8]} - {self.message[:50]}"


class BranchGraphGenerator:
    """分支图生成器"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.commits: Dict[str, CommitNode] = {}
        self.branch_heads: Dict[str, CommitNode] = {}

    def _run_git_command(self, args: List[str]) -> str:
        """运行 Git 命令"""
        try:
            result = subprocess.run(
                ['git'] + args,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git 命令失败: {' '.join(args)} - {e.stderr}")

    def load_commits(self, max_commits: int = 50):
        """加载提交历史"""
        # 获取所有分支信息
        branch_info = self._run_git_command(['branch', '-v'])
        branches = {}
        for line in branch_info.strip().split('\n'):
            if line.startswith('*'):
                line = line[1:].strip()
            parts = line.split()
            if len(parts) >= 2:
                branch_name = parts[0]
                commit_sha = parts[1]
                branches[branch_name] = commit_sha

        # 获取提交历史（包括所有分支）
        log_format = '%H|%P|%s|%an|%at'
        log_output = self._run_git_command([
            'log', '--all', '--format=' + log_format,
            f'--max-count={max_commits}'
        ])

        # 解析提交
        for line in log_output.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|')
            sha = parts[0]
            parents = parts[1].split() if parts[1] else []
            message = parts[2]
            author = parts[3]
            timestamp = int(parts[4])

            if sha not in self.commits:
                self.commits[sha] = CommitNode(sha, message, author, timestamp)

            # 设置父节点关系
            commit_node = self.commits[sha]
            for parent_sha in parents:
                if parent_sha not in self.commits:
                    # 获取父提交信息
                    parent_log = self._run_git_command([
                        'log', '--format=' + log_format, '-1', parent_sha
                    ]).strip()
                    if parent_log:
                        parent_parts = parent_log.split('|')
                        parent_node = CommitNode(
                            parent_parts[0],
                            parent_parts[2],
                            parent_parts[3],
                            int(parent_parts[4])
                        )
                        self.commits[parent_sha] = parent_node
                    else:
                        # 如果无法获取父提交，创建占位符
                        parent_node = CommitNode(parent_sha, "Unknown", "Unknown", 0)
                        self.commits[parent_sha] = parent_node

                parent_node = self.commits[parent_sha]
                commit_node.add_parent(parent_node)

        # 设置分支头
        for branch_name, commit_sha in branches.items():
            if commit_sha in self.commits:
                self.branch_heads[branch_name] = self.commits[commit_sha]
                # 标记提交所属的分支
                self._mark_branch_commits(branch_name, self.commits[commit_sha])

    def _mark_branch_commits(self, branch_name: str, head: CommitNode):
        """标记分支中的所有提交"""
        visited = set()
        stack = [head]

        while stack:
            node = stack.pop()
            if node.sha in visited:
                continue
            visited.add(node.sha)
            node.branches.append(branch_name)

            # 添加父节点到栈中
            for parent in node.parents:
                if parent.sha not in visited:
                    stack.append(parent)

    def generate_ascii_graph(self) -> str:
        """生成 ASCII 分支图"""
        if not self.commits:
            return "没有提交历史"

        # 按时间排序提交（最新的在前面）
        sorted_commits = sorted(
            self.commits.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )

        # 创建提交到行号的映射
        commit_to_line = {}
        lines = []

        for i, commit in enumerate(sorted_commits):
            commit_to_line[commit.sha] = i

            # 确定分支标签
            branch_labels = []
            for branch_name, head in self.branch_heads.items():
                if head.sha == commit.sha:
                    branch_labels.append(f"[{branch_name}]")

            branch_str = " ".join(branch_labels) if branch_labels else ""

            # 提交信息
            message = commit.message
            if len(message) > 40:
                message = message[:37] + "..."

            # 父提交引用
            parent_refs = []
            for parent in commit.parents:
                if parent.sha in commit_to_line:
                    parent_line = commit_to_line[parent.sha]
                    parent_refs.append(f"L{parent_line}")
                else:
                    parent_refs.append("...")

            parent_str = ", ".join(parent_refs) if parent_refs else "root"

            line = f"L{i}: {commit.sha[:8]} - {message} {branch_str} <- {parent_str}"
            lines.append(line)

        return "\n".join(lines)

    def generate_mermaid_graph(self) -> str:
        """生成 Mermaid 流程图"""
        if not self.commits:
            return "没有提交历史"

        mermaid_lines = ["graph TD"]
        mermaid_lines.append("    classDef branchHead fill:#f9f,stroke:#333,stroke-width:2px;")
        mermaid_lines.append("    classDef mergeCommit fill:#bbf,stroke:#333;")
        mermaid_lines.append("    classDef regularCommit fill:#fff,stroke:#333;")

        # 添加节点
        for commit in self.commits.values():
            label = commit.message
            if len(label) > 20:
                label = label[:17] + "..."

            # 确定节点样式
            classes = []
            if commit.sha in [head.sha for head in self.branch_heads.values()]:
                classes.append("branchHead")
            if len(commit.parents) > 1:
                classes.append("mergeCommit")
            if not classes:
                classes.append("regularCommit")

            class_str = f":::{','.join(classes)}"
            node_id = f"commit_{commit.sha[:8]}"
            mermaid_lines.append(f"    {node_id}[\"{label}<br/>{commit.sha[:8]}\"]{class_str}")

        # 添加边（从子节点指向父节点）
        for commit in self.commits.values():
            child_id = f"commit_{commit.sha[:8]}"
            for parent in commit.parents:
                parent_id = f"commit_{parent.sha[:8]}"
                if parent.sha in self.commits:
                    mermaid_lines.append(f"    {child_id} --> {parent_id}")

        return "\n".join(mermaid_lines)

    def detect_workflow_pattern(self) -> str:
        """检测工作流模式"""
        if not self.commits:
            return "未知"

        # 统计不同类型的提交
        merge_commits = [c for c in self.commits.values() if len(c.parents) > 1]
        total_commits = len(self.commits)
        merge_ratio = len(merge_commits) / total_commits if total_commits > 0 else 0

        # 检查分支数量
        all_branches = set()
        for commit in self.commits.values():
            all_branches.update(commit.branches)
        branch_count = len(all_branches)

        # 检查是否有特定的分支命名模式
        has_develop = any('develop' in branch.lower() for branch in all_branches)
        has_feature = any('feature' in branch.lower() or branch.startswith(('feat/', 'feature/'))
                         for branch in all_branches)
        has_release = any('release' in branch.lower() or branch.startswith('release/')
                         for branch in all_branches)

        if has_develop and has_feature and has_release:
            return "Git Flow"
        elif branch_count <= 2 and merge_ratio < 0.3:
            return "GitHub Flow (squash merges)"
        elif branch_count > 2 and merge_ratio > 0.5:
            return "GitHub Flow (merge commits)"
        elif merge_ratio < 0.1:
            return "Linear history (rebase workflow)"
        else:
            return "混合工作流"

    def analyze_merge_vs_rebase(self) -> Dict:
        """分析合并 vs rebase 的使用情况"""
        merge_commits = [c for c in self.commits.values() if len(c.parents) > 1]
        linear_commits = [c for c in self.commits.values() if len(c.parents) <= 1]

        # 检测 rebase 模式：连续的线性提交可能来自 rebase
        recent_commits = sorted(
            self.commits.values(),
            key=lambda x: x.timestamp,
            reverse=True
        )[:20]  # 最近20个提交

        linear_recent = [c for c in recent_commits if len(c.parents) <= 1]
        linear_ratio_recent = len(linear_recent) / len(recent_commits) if recent_commits else 0

        return {
            'total_commits': len(self.commits),
            'merge_commits': len(merge_commits),
            'linear_commits': len(linear_commits),
            'merge_ratio': len(merge_commits) / len(self.commits) if self.commits else 0,
            'recent_linear_ratio': linear_ratio_recent,
            'workflow_tendency': 'rebase' if linear_ratio_recent > 0.8 else 'merge'
        }


def main():
    """主函数"""
    print("=== Git 分支图生成器 ===\n")

    try:
        generator = BranchGraphGenerator()

        print("正在加载提交历史...")
        generator.load_commits(max_commits=30)

        print(f"\n📊 工作流分析:")
        workflow = generator.detect_workflow_pattern()
        print(f"   检测到的工作流: {workflow}")

        analysis = generator.analyze_merge_vs_rebase()
        print(f"   提交总数: {analysis['total_commits']}")
        print(f"   合并提交: {analysis['merge_commits']} ({analysis['merge_ratio']:.1%})")
        print(f"   最近提交线性比例: {analysis['recent_linear_ratio']:.1%}")
        print(f"   倾向: {analysis['workflow_tendency']} 工作流")

        print(f"\n🔤 ASCII 分支图:")
        ascii_graph = generator.generate_ascii_graph()
        print(ascii_graph)

        print(f"\n🔧 Mermaid 图表代码:")
        print("可以将以下代码粘贴到支持 Mermaid 的编辑器中查看可视化图表:")
        print("\n" + generator.generate_mermaid_graph())

    except RuntimeError as e:
        print(f"❌ 错误: {e}")
        print("\n💡 提示: 请确保在 Git 仓库中运行此脚本")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未预期的错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()