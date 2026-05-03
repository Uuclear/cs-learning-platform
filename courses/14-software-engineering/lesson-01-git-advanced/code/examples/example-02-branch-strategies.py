#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: 分支策略模拟

本示例模拟两种主流的 Git 工作流：
1. Git Flow - 适用于有固定发布周期的项目
2. GitHub Flow - 适用于持续交付的项目

通过可视化的方式展示不同工作流下的分支合并模式。
"""

from typing import List, Dict, Optional
import time


class Commit:
    """提交对象"""

    def __init__(self, sha: str, message: str, timestamp: float):
        self.sha = sha
        self.message = message
        self.timestamp = timestamp
        self.parents: List['Commit'] = []

    def add_parent(self, parent: 'Commit'):
        """添加父提交"""
        self.parents.append(parent)


class Branch:
    """分支对象"""

    def __init__(self, name: str, head: Optional[Commit] = None):
        self.name = name
        self.head = head
        self.commits: List[Commit] = []
        if head:
            self.commits.append(head)

    def add_commit(self, commit: Commit):
        """向分支添加提交"""
        self.head = commit
        self.commits.append(commit)


class GitFlowSimulator:
    """Git Flow 工作流模拟器"""

    def __init__(self):
        self.branches: Dict[str, Branch] = {}
        self.commit_counter = 0

    def _create_commit(self, message: str) -> Commit:
        """创建新的提交"""
        self.commit_counter += 1
        sha = f"abcdef{self.commit_counter:04d}"
        return Commit(sha, message, time.time())

    def initialize(self):
        """初始化 Git Flow 结构"""
        # 创建初始提交
        initial_commit = self._create_commit("初始提交")

        # 创建 main 分支（生产环境）
        main_branch = Branch("main", initial_commit)
        self.branches["main"] = main_branch

        # 创建 develop 分支（开发环境）
        develop_branch = Branch("develop", initial_commit)
        self.branches["develop"] = develop_branch

        print("=== Git Flow 初始化 ===")
        print(f"✓ 创建 main 分支: {initial_commit.sha[:8]}")
        print(f"✓ 创建 develop 分支: {initial_commit.sha[:8]}")
        print()

    def create_feature_branch(self, feature_name: str):
        """创建特性分支"""
        if "develop" not in self.branches:
            raise ValueError("必须先初始化 develop 分支")

        feature_branch_name = f"feature/{feature_name}"
        develop_head = self.branches["develop"].head
        feature_branch = Branch(feature_branch_name, develop_head)
        self.branches[feature_branch_name] = feature_branch

        print(f"✓ 创建特性分支: {feature_branch_name} (基于 {develop_head.sha[:8]})")

    def work_on_feature(self, feature_name: str, commits: List[str]):
        """在特性分支上工作"""
        feature_branch_name = f"feature/{feature_name}"
        if feature_branch_name not in self.branches:
            raise ValueError(f"特性分支 {feature_branch_name} 不存在")

        branch = self.branches[feature_branch_name]
        for message in commits:
            new_commit = self._create_commit(message)
            if branch.head:
                new_commit.add_parent(branch.head)
            branch.add_commit(new_commit)
            print(f"  → 提交: {new_commit.sha[:8]} - {message}")

    def finish_feature(self, feature_name: str):
        """完成特性开发，合并到 develop"""
        feature_branch_name = f"feature/{feature_name}"
        if feature_branch_name not in self.branches:
            raise ValueError(f"特性分支 {feature_branch_name} 不存在")

        feature_branch = self.branches[feature_branch_name]
        develop_branch = self.branches["develop"]

        # 创建合并提交
        merge_message = f"Merge branch '{feature_branch_name}' into develop"
        merge_commit = self._create_commit(merge_message)
        merge_commit.add_parent(develop_branch.head)
        merge_commit.add_parent(feature_branch.head)

        develop_branch.add_commit(merge_commit)
        print(f"✓ 合并 {feature_branch_name} 到 develop: {merge_commit.sha[:8]}")

        # 删除特性分支
        del self.branches[feature_branch_name]
        print(f"✓ 删除分支: {feature_branch_name}")
        print()

    def create_release(self, version: str):
        """创建发布分支"""
        if "develop" not in self.branches:
            raise ValueError("必须先有 develop 分支")

        release_branch_name = f"release/{version}"
        develop_head = self.branches["develop"].head
        release_branch = Branch(release_branch_name, develop_head)
        self.branches[release_branch_name] = release_branch

        print(f"✓ 创建发布分支: {release_branch_name} (基于 {develop_head.sha[:8]})")

    def finish_release(self, version: str):
        """完成发布，合并到 main 和 develop"""
        release_branch_name = f"release/{version}"
        if release_branch_name not in self.branches:
            raise ValueError(f"发布分支 {release_branch_name} 不存在")

        release_branch = self.branches[release_branch_name]

        # 合并到 main
        main_branch = self.branches["main"]
        main_merge_message = f"Merge branch 'release/{version}'"
        main_merge_commit = self._create_commit(main_merge_message)
        main_merge_commit.add_parent(main_branch.head)
        main_merge_commit.add_parent(release_branch.head)
        main_branch.add_commit(main_merge_commit)

        # 合并到 develop
        develop_branch = self.branches["develop"]
        develop_merge_message = f"Merge branch 'release/{version}' into develop"
        develop_merge_commit = self._create_commit(develop_merge_message)
        develop_merge_commit.add_parent(develop_branch.head)
        develop_merge_commit.add_parent(release_branch.head)
        develop_branch.add_commit(develop_merge_commit)

        print(f"✓ 发布 {version} 完成:")
        print(f"  → 合并到 main: {main_merge_commit.sha[:8]}")
        print(f"  → 合并到 develop: {develop_merge_commit.sha[:8]}")

        # 删除发布分支
        del self.branches[release_branch_name]
        print(f"✓ 删除分支: {release_branch_name}")
        print()

    def show_branch_structure(self):
        """显示当前分支结构"""
        print("=== 当前分支结构 ===")
        for branch_name, branch in sorted(self.branches.items()):
            commits = [commit.sha[:8] for commit in branch.commits[-3:]]  # 显示最近3个提交
            if len(branch.commits) > 3:
                commits.insert(0, "...")
            print(f"{branch_name:15}: {' <- '.join(commits)}")
        print()


class GitHubFlowSimulator:
    """GitHub Flow 工作流模拟器"""

    def __init__(self):
        self.branches: Dict[str, Branch] = {}
        self.commit_counter = 0

    def _create_commit(self, message: str) -> Commit:
        """创建新的提交"""
        self.commit_counter += 1
        sha = f"ghflow{self.commit_counter:04d}"
        return Commit(sha, message, time.time())

    def initialize(self):
        """初始化 GitHub Flow 结构"""
        initial_commit = self._create_commit("初始提交")
        main_branch = Branch("main", initial_commit)
        self.branches["main"] = main_branch

        print("=== GitHub Flow 初始化 ===")
        print(f"✓ 创建 main 分支: {initial_commit.sha[:8]}")
        print()

    def create_feature_branch(self, feature_name: str):
        """创建特性分支"""
        main_head = self.branches["main"].head
        feature_branch = Branch(feature_name, main_head)
        self.branches[feature_name] = feature_branch

        print(f"✓ 创建特性分支: {feature_name} (基于 {main_head.sha[:8]})")

    def work_on_feature(self, feature_name: str, commits: List[str]):
        """在特性分支上工作"""
        if feature_name not in self.branches:
            raise ValueError(f"特性分支 {feature_name} 不存在")

        branch = self.branches[feature_name]
        for message in commits:
            new_commit = self._create_commit(message)
            if branch.head:
                new_commit.add_parent(branch.head)
            branch.add_commit(new_commit)
            print(f"  → 提交: {new_commit.sha[:8]} - {message}")

    def merge_to_main(self, feature_name: str, squash: bool = False):
        """合并特性分支到 main"""
        if feature_name not in self.branches:
            raise ValueError(f"特性分支 {feature_name} 不存在")

        feature_branch = self.branches[feature_name]
        main_branch = self.branches["main"]

        if squash:
            # Squash 合并：将所有提交压缩为一个
            squash_message = f"实现 {feature_name.replace('-', ' ')}"
            squash_commit = self._create_commit(squash_message)
            squash_commit.add_parent(main_branch.head)
            main_branch.add_commit(squash_commit)
            print(f"✓ Squash 合并 {feature_name} 到 main: {squash_commit.sha[:8]}")
        else:
            # 普通合并
            merge_message = f"Merge branch '{feature_name}'"
            merge_commit = self._create_commit(merge_message)
            merge_commit.add_parent(main_branch.head)
            merge_commit.add_parent(feature_branch.head)
            main_branch.add_commit(merge_commit)
            print(f"✓ 合并 {feature_name} 到 main: {merge_commit.sha[:8]}")

        # 删除特性分支
        del self.branches[feature_name]
        print(f"✓ 删除分支: {feature_name}")
        print()

    def show_branch_structure(self):
        """显示当前分支结构"""
        print("=== 当前分支结构 ===")
        for branch_name, branch in sorted(self.branches.items()):
            commits = [commit.sha[:8] for commit in branch.commits[-3:]]  # 显示最近3个提交
            if len(branch.commits) > 3:
                commits.insert(0, "...")
            print(f"{branch_name:15}: {' <- '.join(commits)}")
        print()


def demonstrate_branch_strategies():
    """演示不同的分支策略"""
    print("=== 分支策略对比演示 ===\n")

    # 演示 Git Flow
    print("1. Git Flow 工作流:")
    git_flow = GitFlowSimulator()
    git_flow.initialize()

    # 开发用户管理功能
    git_flow.create_feature_branch("user-management")
    git_flow.work_on_feature("user-management", [
        "添加用户模型",
        "实现用户注册接口",
        "添加用户认证逻辑"
    ])
    git_flow.finish_feature("user-management")

    # 创建发布
    git_flow.create_release("v1.0.0")
    git_flow.finish_release("v1.0.0")

    git_flow.show_branch_structure()

    print("\n" + "="*50 + "\n")

    # 演示 GitHub Flow
    print("2. GitHub Flow 工作流:")
    github_flow = GitHubFlowSimulator()
    github_flow.initialize()

    # 开发搜索功能
    github_flow.create_feature_branch("search-feature")
    github_flow.work_on_feature("search-feature", [
        "添加搜索API端点",
        "实现全文搜索逻辑",
        "优化搜索性能"
    ])
    github_flow.merge_to_main("search-feature", squash=True)

    github_flow.show_branch_structure()


if __name__ == "__main__":
    demonstrate_branch_strategies()