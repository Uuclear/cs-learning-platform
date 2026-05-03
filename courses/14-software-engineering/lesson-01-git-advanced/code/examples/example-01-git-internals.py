#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 1: Git 内部对象模型演示

本示例演示 Git 的核心对象模型：
- Blob 对象：存储文件内容
- Tree 对象：存储目录结构
- Commit 对象：存储提交信息

通过手动创建这些对象，我们可以理解 Git 如何存储和组织数据。
"""

import hashlib
import json
import os
import time


class GitObject:
    """Git 对象基类"""

    def __init__(self, content: bytes):
        self.content = content
        self.sha1 = self._calculate_sha1()

    def _calculate_sha1(self) -> str:
        """计算对象的 SHA-1 哈希值"""
        # Git 对象格式: "类型 长度\0内容"
        header = f"{self.object_type} {len(self.content)}".encode() + b'\0'
        data = header + self.content
        return hashlib.sha1(data).hexdigest()

    @property
    def object_type(self) -> str:
        raise NotImplementedError


class Blob(GitObject):
    """Blob 对象 - 存储文件内容"""

    @property
    def object_type(self) -> str:
        return "blob"


class Tree(GitObject):
    """Tree 对象 - 存储目录结构"""

    def __init__(self, entries: list):
        """
        entries: 目录条目列表，每个条目包含 (mode, name, sha1)
        mode: 文件模式 (如 '100644' 表示普通文件)
        """
        self.entries = entries
        # 构建 tree 内容: "mode name\0sha1" 的序列
        content_parts = []
        for mode, name, sha1 in sorted(entries, key=lambda x: x[1]):
            entry = f"{mode} {name}".encode() + b'\0' + bytes.fromhex(sha1)
            content_parts.append(entry)

        content = b''.join(content_parts)
        super().__init__(content)

    @property
    def object_type(self) -> str:
        return "tree"


class Commit(GitObject):
    """Commit 对象 - 存储提交信息"""

    def __init__(self, tree_sha1: str, parent_sha1s: list, author: str,
                 committer: str, message: str):
        """
        tree_sha1: 树对象的 SHA-1
        parent_sha1s: 父提交的 SHA-1 列表
        author: 作者信息 "姓名 <邮箱> 时间戳 时区"
        committer: 提交者信息
        message: 提交信息
        """
        self.tree_sha1 = tree_sha1
        self.parent_sha1s = parent_sha1s
        self.author = author
        self.committer = committer
        self.message = message

        # 构建 commit 内容
        content_parts = [f"tree {tree_sha1}"]
        for parent in parent_sha1s:
            content_parts.append(f"parent {parent}")
        content_parts.extend([
            f"author {author}",
            f"committer {committer}",
            "",  # 空行分隔头部和消息
            message
        ])

        content = "\n".join(content_parts).encode()
        super().__init__(content)

    @property
    def object_type(self) -> str:
        return "commit"


def demonstrate_git_objects():
    """演示 Git 对象的创建和关系"""
    print("=== Git 内部对象模型演示 ===\n")

    # 创建一个简单的文件内容
    file_content = b"Hello, Git World!\nThis is a sample file."
    blob = Blob(file_content)
    print(f"1. 创建 Blob 对象:")
    print(f"   内容: {file_content.decode()}")
    print(f"   SHA-1: {blob.sha1}")
    print()

    # 创建 Tree 对象，包含我们的 blob
    tree_entries = [
        ("100644", "sample.txt", blob.sha1)  # 100644 = 普通文件
    ]
    tree = Tree(tree_entries)
    print(f"2. 创建 Tree 对象:")
    print(f"   条目: {tree_entries[0][1]} ({tree_entries[0][0]}) -> {tree_entries[0][2][:8]}...")
    print(f"   SHA-1: {tree.sha1}")
    print()

    # 创建 Commit 对象
    current_time = int(time.time())
    author_info = f"张三 <zhangsan@example.com> {current_time} +0800"
    committer_info = f"张三 <zhangsan@example.com> {current_time} +0800"

    commit = Commit(
        tree_sha1=tree.sha1,
        parent_sha1s=[],  # 初始提交没有父提交
        author=author_info,
        committer=committer_info,
        message="初始提交\n\n添加示例文件"
    )

    print(f"3. 创建 Commit 对象:")
    print(f"   Tree: {commit.tree_sha1[:8]}...")
    print(f"   作者: {commit.author}")
    print(f"   提交信息: {commit.message.split(chr(10))[0]}")
    print(f"   SHA-1: {commit.sha1}")
    print()

    # 展示对象之间的引用关系
    print("4. 对象引用关系:")
    print(f"   Commit ({commit.sha1[:8]}...) -> Tree ({tree.sha1[:8]}...) -> Blob ({blob.sha1[:8]}...)")
    print()

    # 验证 SHA-1 计算的正确性
    print("5. 验证 SHA-1 计算:")
    # 手动计算 blob 的 SHA-1 进行验证
    blob_header = f"blob {len(file_content)}".encode() + b'\0'
    blob_data = blob_header + file_content
    manual_blob_sha1 = hashlib.sha1(blob_data).hexdigest()
    print(f"   手动计算 Blob SHA-1: {manual_blob_sha1}")
    print(f"   对象计算 Blob SHA-1: {blob.sha1}")
    print(f"   验证结果: {'✓ 正确' if manual_blob_sha1 == blob.sha1 else '✗ 错误'}")


if __name__ == "__main__":
    demonstrate_git_objects()