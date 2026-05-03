#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 1: 简化的 Git 版本控制系统

实现一个微型的 Git-like 版本控制系统，支持基本的 commit、branch、checkout 操作。
"""

import hashlib
import json
import os
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional


class MiniGit:
    """简化的 Git 版本控制系统"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.git_dir = self.repo_path / ".minigit"
        self.objects_dir = self.git_dir / "objects"
        self.refs_dir = self.git_dir / "refs"
        self.head_file = self.git_dir / "HEAD"

        # 初始化仓库结构
        self._init_repo()

    def _init_repo(self):
        """初始化仓库目录结构"""
        if not self.git_dir.exists():
            self.git_dir.mkdir()
            self.objects_dir.mkdir()
            self.refs_dir.mkdir()
            self.refs_dir.joinpath("heads").mkdir()

            # 初始化 HEAD 指向 main 分支
            self.head_file.write_text("ref: refs/heads/main\n")

            # 创建初始分支
            self._create_branch("main", None)

    def _hash_object(self, content: bytes, obj_type: str = "blob") -> str:
        """计算对象哈希值并存储对象"""
        header = f"{obj_type} {len(content)}".encode() + b'\0'
        data = header + content
        sha1 = hashlib.sha1(data).hexdigest()

        # 存储对象
        obj_dir = self.objects_dir / sha1[:2]
        obj_dir.mkdir(exist_ok=True)
        obj_file = obj_dir / sha1[2:]
        if not obj_file.exists():
            obj_file.write_bytes(data)

        return sha1

    def _read_object(self, sha1: str) -> tuple:
        """读取对象内容和类型"""
        obj_file = self.objects_dir / sha1[:2] / sha1[2:]
        if not obj_file.exists():
            raise ValueError(f"对象不存在: {sha1}")

        data = obj_file.read_bytes()
        null_idx = data.find(b'\0')
        header = data[:null_idx].decode()
        content = data[null_idx + 1:]

        obj_type, size = header.split(' ')
        return obj_type, content

    def _create_tree(self, path: Path, base_path: Path = None) -> str:
        """递归创建树对象"""
        if base_path is None:
            base_path = path

        entries = []

        for item in sorted(path.iterdir()):
            if item.name == ".minigit":
                continue

            rel_path = item.relative_to(base_path)
            if item.is_file():
                # 创建 blob 对象
                content = item.read_bytes()
                blob_sha1 = self._hash_object(content, "blob")
                entries.append(("100644", str(rel_path), blob_sha1))
            elif item.is_dir():
                # 递归创建子树
                subtree_sha1 = self._create_tree(item, base_path)
                entries.append(("40000", str(rel_path), subtree_sha1))

        # 创建树对象内容
        tree_content = b""
        for mode, name, sha1 in entries:
            entry = f"{mode} {name}".encode() + b'\0' + bytes.fromhex(sha1)
            tree_content += entry

        return self._hash_object(tree_content, "tree")

    def commit(self, message: str) -> str:
        """创建提交"""
        # 创建当前工作目录的树对象
        tree_sha1 = self._create_tree(self.repo_path)

        # 获取当前分支的 HEAD
        current_ref = self._get_current_ref()
        parent_sha1 = None
        if current_ref and (self.refs_dir / current_ref).exists():
            parent_sha1 = (self.refs_dir / current_ref).read_text().strip()

        # 创建提交对象
        timestamp = int(time.time())
        author = f"User <user@example.com> {timestamp} +0000"
        commit_content = f"""tree {tree_sha1}
{f"parent {parent_sha1}" if parent_sha1 else ""}
author {author}
committer {author}

{message}""".encode()

        commit_sha1 = self._hash_object(commit_content, "commit")

        # 更新当前分支指向新的提交
        current_branch = self._get_current_branch()
        branch_ref = self.refs_dir / "heads" / current_branch
        branch_ref.write_text(commit_sha1 + "\n")

        print(f"✅ 提交成功: {commit_sha1[:8]} - {message}")
        return commit_sha1

    def _get_current_ref(self) -> Optional[str]:
        """获取当前 HEAD 引用"""
        head_content = self.head_file.read_text().strip()
        if head_content.startswith("ref: "):
            return head_content[5:]  # 移除 "ref: " 前缀
        return None

    def _get_current_branch(self) -> str:
        """获取当前分支名称"""
        current_ref = self._get_current_ref()
        if current_ref and current_ref.startswith("refs/heads/"):
            return current_ref[11:]  # 移除 "refs/heads/" 前缀
        return "main"

    def _create_branch(self, branch_name: str, target_commit: Optional[str]):
        """创建分支"""
        branch_ref = self.refs_dir / "heads" / branch_name
        if branch_ref.exists():
            raise ValueError(f"分支已存在: {branch_name}")

        if target_commit is None:
            # 如果没有指定目标提交，使用当前 HEAD
            current_ref = self._get_current_ref()
            if current_ref and (self.refs_dir / current_ref).exists():
                target_commit = (self.refs_dir / current_ref).read_text().strip()
            else:
                target_commit = ""

        branch_ref.write_text(target_commit + "\n")
        print(f"✅ 创建分支: {branch_name}")

    def branch(self, branch_name: str):
        """创建新分支"""
        self._create_branch(branch_name, None)

    def checkout(self, ref: str):
        """切换到指定分支或提交"""
        # 首先检查是否是分支
        branch_ref = self.refs_dir / "heads" / ref
        if branch_ref.exists():
            # 切换到分支
            commit_sha1 = branch_ref.read_text().strip()
            self.head_file.write_text(f"ref: refs/heads/{ref}\n")
            print(f"✅ 切换到分支: {ref}")
        else:
            # 检查是否是提交 SHA1
            try:
                self._read_object(ref)
                # 直接检出提交（分离 HEAD 状态）
                self.head_file.write_text(ref + "\n")
                print(f"✅ 检出提交: {ref[:8]}")
            except ValueError:
                raise ValueError(f"引用不存在: {ref}")

        # 恢复工作目录文件（简化版：只恢复根目录文件）
        self._restore_working_directory(ref)

    def _restore_working_directory(self, ref: str):
        """恢复工作目录到指定提交状态（简化实现）"""
        # 获取提交对应的树对象
        if len(ref) == 40:  # 完整的 SHA1
            commit_sha1 = ref
        else:
            # 分支名称
            branch_ref = self.refs_dir / "heads" / ref
            if branch_ref.exists():
                commit_sha1 = branch_ref.read_text().strip()
            else:
                return

        try:
            _, commit_content = self._read_object(commit_sha1)
            commit_lines = commit_content.decode().split('\n')
            tree_sha1 = commit_lines[0].split()[1]

            # 读取树对象并恢复文件
            self._restore_tree_files(tree_sha1, self.repo_path)
        except Exception as e:
            print(f"⚠️  恢复工作目录失败: {e}")

    def _restore_tree_files(self, tree_sha1: str, base_path: Path):
        """递归恢复树中的文件"""
        try:
            _, tree_content = self._read_object(tree_sha1)
            # 解析树对象内容（简化处理）
            i = 0
            while i < len(tree_content):
                # 找到下一个 null 字符
                null_pos = tree_content.find(b'\0', i)
                if null_pos == -1:
                    break

                # 解析条目头
                entry_header = tree_content[i:null_pos].decode()
                mode, name = entry_header.split(' ', 1)
                sha1 = tree_content[null_pos + 1:null_pos + 21].hex()

                file_path = base_path / name
                if mode == "100644":  # 普通文件
                    _, file_content = self._read_object(sha1)
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_bytes(file_content)
                elif mode == "40000":  # 目录
                    file_path.mkdir(exist_ok=True)
                    self._restore_tree_files(sha1, file_path)

                i = null_pos + 21
        except Exception as e:
            print(f"⚠️  恢复树文件失败: {e}")

    def log(self, max_commits: int = 10):
        """显示提交历史"""
        current_ref = self._get_current_ref()
        if not current_ref:
            current_commit = self.head_file.read_text().strip()
        else:
            current_commit = (self.refs_dir / current_ref).read_text().strip()

        if not current_commit:
            print("暂无提交历史")
            return

        print("提交历史:")
        commits_shown = 0
        current = current_commit

        while current and commits_shown < max_commits:
            try:
                _, commit_content = self._read_object(current)
                commit_lines = commit_content.decode().split('\n')

                # 解析提交信息
                tree_line = commit_lines[0]
                parent_line = commit_lines[1] if len(commit_lines) > 1 and commit_lines[1].startswith('parent') else None
                author_line = None
                message_start = 0

                for i, line in enumerate(commit_lines):
                    if line.startswith('author '):
                        author_line = line
                    if line == '':
                        message_start = i + 1
                        break

                message = '\n'.join(commit_lines[message_start:]).strip()
                author = author_line.split(' ', 1)[1] if author_line else "Unknown"

                print(f"commit {current}")
                print(f"Author: {author}")
                print(f"Date:   {time.ctime(int(author.split()[-2])) if author_line else 'Unknown'}")
                print(f"\n    {message}\n")

                # 移动到父提交
                if parent_line:
                    current = parent_line.split()[1]
                else:
                    current = None

                commits_shown += 1

            except Exception as e:
                print(f"读取提交 {current[:8]} 失败: {e}")
                break

    def status(self):
        """显示仓库状态"""
        current_branch = self._get_current_branch()
        print(f"当前分支: {current_branch}")

        # 检查工作目录更改（简化版）
        tracked_files = self._get_tracked_files()
        modified_files = []

        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file() and ".minigit" not in str(file_path):
                rel_path = file_path.relative_to(self.repo_path)
                if str(rel_path) not in tracked_files:
                    modified_files.append(str(rel_path))

        if modified_files:
            print("\n未跟踪的文件:")
            for file in modified_files[:5]:  # 只显示前5个
                print(f"  {file}")
            if len(modified_files) > 5:
                print(f"  ... 还有 {len(modified_files) - 5} 个文件")
        else:
            print("\n工作目录干净")

    def _get_tracked_files(self) -> set:
        """获取已跟踪的文件列表"""
        tracked = set()
        current_ref = self._get_current_ref()
        if current_ref and (self.refs_dir / current_ref).exists():
            current_commit = (self.refs_dir / current_ref).read_text().strip()
            try:
                _, commit_content = self._read_object(current_commit)
                commit_lines = commit_content.decode().split('\n')
                tree_sha1 = commit_lines[0].split()[1]
                tracked = self._get_files_from_tree(tree_sha1)
            except Exception:
                pass
        return tracked

    def _get_files_from_tree(self, tree_sha1: str) -> set:
        """从树对象获取文件列表"""
        files = set()
        try:
            _, tree_content = self._read_object(tree_sha1)
            i = 0
            while i < len(tree_content):
                null_pos = tree_content.find(b'\0', i)
                if null_pos == -1:
                    break
                entry_header = tree_content[i:null_pos].decode()
                mode, name = entry_header.split(' ', 1)
                if mode == "100644":
                    files.add(name)
                elif mode == "40000":
                    subdir_files = self._get_files_from_tree(tree_content[null_pos + 1:null_pos + 21].hex())
                    for f in subdir_files:
                        files.add(f"{name}/{f}")
                i = null_pos + 21
        except Exception:
            pass
        return files


def main():
    """主函数 - 演示 MiniGit 的使用"""
    print("=== 简化的 Git 版本控制系统演示 ===\n")

    # 创建临时测试目录
    test_dir = Path("test_minigit")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir()

    try:
        # 初始化 MiniGit 仓库
        minigit = MiniGit(str(test_dir))

        # 创建一些测试文件
        (test_dir / "README.md").write_text("# 测试项目\n\n这是一个 MiniGit 测试项目。")
        (test_dir / "main.py").write_text('print("Hello, MiniGit!")\n')

        # 首次提交
        minigit.commit("初始提交")

        # 创建新分支
        minigit.branch("feature-login")
        minigit.checkout("feature-login")

        # 在特性分支上工作
        (test_dir / "auth.py").write_text('def login():\n    return "logged in"\n')
        minigit.commit("添加用户认证功能")

        # 切换回主分支
        minigit.checkout("main")

        # 显示状态和日志
        print()
        minigit.status()
        print()
        minigit.log(5)

    finally:
        # 清理测试目录
        if test_dir.exists():
            shutil.rmtree(test_dir)


if __name__ == "__main__":
    main()