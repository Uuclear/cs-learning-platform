#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3: inode模拟演示
展示inode的核心概念：文件名与数据分离，硬链接共享inode
"""

import time
from datetime import datetime

class Inode:
    """模拟inode结构 - 文件的元数据容器"""
    def __init__(self, inode_id, file_type='file'):
        """
        初始化inode

        Args:
            inode_id (int): inode的唯一标识符
            file_type (str): 文件类型 ('file', 'directory', 'symlink')
        """
        self.inode_id = inode_id
        self.file_type = file_type
        self.permissions = 0o644    # 默认权限: rw-r--r--
        self.owner = "user"
        self.group = "user"
        self.size = 0
        self.hard_links = 1         # 硬链接计数
        self.data_content = ""      # 简化：直接存储文件内容（实际系统中是指向数据块的指针）
        self.timestamps = {
            'created': datetime.now(),
            'modified': datetime.now(),
            'accessed': datetime.now()
        }

    def update_access_time(self):
        """更新访问时间"""
        self.timestamps['accessed'] = datetime.now()

    def update_modify_time(self):
        """更新修改时间"""
        self.timestamps['modified'] = datetime.now()
        self.update_access_time()   # 修改时也会访问

    def __str__(self):
        """字符串表示"""
        return (f"Inode({self.inode_id}): type={self.file_type}, "
                f"size={self.size}B, links={self.hard_links}")

class FileSystemSimulator:
    """简单的文件系统模拟器"""
    def __init__(self):
        self.inodes = {}           # inode_id -> Inode对象
        self.directory_entries = {} # 路径 -> inode_id映射
        self.next_inode_id = 1
        print("💾 初始化文件系统模拟器...")

    def create_file(self, path, content=""):
        """创建文件"""
        # 验证路径
        if path in self.directory_entries:
            print(f"❌ 文件已存在: {path}")
            return None

        # 创建新的inode
        inode_id = self.next_inode_id
        self.next_inode_id += 1

        inode = Inode(inode_id, 'file')
        inode.size = len(content.encode('utf-8'))
        inode.data_content = content
        inode.update_modify_time()

        # 保存inode
        self.inodes[inode_id] = inode

        # 在目录中创建条目
        self.directory_entries[path] = inode_id

        print(f"✅ 创建文件 {path} (inode {inode_id})")
        return inode_id

    def create_directory(self, path):
        """创建目录"""
        if path in self.directory_entries:
            print(f"❌ 目录已存在: {path}")
            return None

        inode_id = self.next_inode_id
        self.next_inode_id += 1

        inode = Inode(inode_id, 'directory')
        self.inodes[inode_id] = inode
        self.directory_entries[path] = inode_id

        print(f"📁 创建目录 {path} (inode {inode_id})")
        return inode_id

    def read_file(self, path):
        """读取文件内容"""
        if path not in self.directory_entries:
            print(f"❌ 文件不存在: {path}")
            return None

        inode_id = self.directory_entries[path]
        inode = self.inodes[inode_id]

        # 更新访问时间
        inode.update_access_time()

        print(f"📄 读取文件 {path} (inode {inode_id})")
        return inode.data_content

    def write_file(self, path, content):
        """写入文件内容"""
        if path not in self.directory_entries:
            print(f"❌ 文件不存在: {path}")
            return False

        inode_id = self.directory_entries[path]
        inode = self.inodes[inode_id]

        inode.data_content = content
        inode.size = len(content.encode('utf-8'))
        inode.update_modify_time()

        print(f"✍️  写入文件 {path} (inode {inode_id})")
        return True

    def get_file_info(self, path):
        """获取文件信息"""
        if path not in self.directory_entries:
            print(f"❌ 文件不存在: {path}")
            return None

        inode_id = self.directory_entries[path]
        inode = self.inodes[inode_id]
        return inode

    def create_hard_link(self, existing_path, new_path):
        """创建硬链接"""
        if existing_path not in self.directory_entries:
            print(f"❌ 源文件不存在: {existing_path}")
            return False

        if new_path in self.directory_entries:
            print(f"❌ 目标路径已存在: {new_path}")
            return False

        # 硬链接共享同一个inode
        inode_id = self.directory_entries[existing_path]
        self.directory_entries[new_path] = inode_id

        # 增加硬链接计数
        self.inodes[inode_id].hard_links += 1

        print(f"🔗 创建硬链接 {new_path} -> {existing_path} (inode {inode_id})")
        return True

    def delete_file(self, path):
        """删除文件（减少硬链接计数）"""
        if path not in self.directory_entries:
            print(f"❌ 文件不存在: {path}")
            return False

        inode_id = self.directory_entries[path]
        inode = self.inodes[inode_id]

        # 减少硬链接计数
        inode.hard_links -= 1
        del self.directory_entries[path]

        print(f"🗑️  删除文件 {path} (硬链接数: {inode.hard_links})")

        # 如果硬链接数为0，真正删除inode
        if inode.hard_links == 0:
            del self.inodes[inode_id]
            print(f"🧹 真正删除inode {inode_id} (无剩余硬链接)")

        return True

def demonstrate_inode_concepts():
    """演示inode核心概念"""
    print("=" * 50)
    print("🧠 示例3: inode模拟演示")
    print("=" * 50)

    # 创建文件系统模拟器
    fs = FileSystemSimulator()

    # 创建目录结构
    print("\n📂 创建目录结构:")
    fs.create_directory("/home")
    fs.create_directory("/home/user")

    # 创建文件
    print("\n📄 创建文件:")
    fs.create_file("/home/user/document.txt", "这是重要文档！\n包含敏感信息。")
    fs.create_file("/home/user/photo.jpg", "图片二进制数据...")

    # 查看文件信息
    print("\n📊 查看文件信息:")
    doc_inode = fs.get_file_info("/home/user/document.txt")
    if doc_inode:
        print(f"   文档inode信息: {doc_inode}")
        print(f"   创建时间: {doc_inode.timestamps['created']}")
        print(f"   权限: {oct(doc_inode.permissions)}")

    # 读取文件
    print("\n🔍 读取文件内容:")
    content = fs.read_file("/home/user/document.txt")
    if content:
        print(f"   内容: {repr(content)}")

    # 创建硬链接
    print("\n🔗 创建硬链接:")
    fs.create_hard_link("/home/user/document.txt", "/home/user/backup.txt")

    # 再次查看，硬链接数应该增加了
    print("\n📊 查看inode信息（创建硬链接后）:")
    doc_inode = fs.get_file_info("/home/user/document.txt")
    if doc_inode:
        print(f"   文档inode信息: {doc_inode}")

    # 验证硬链接共享数据
    print("\n🔄 验证硬链接共享数据:")
    backup_content = fs.read_file("/home/user/backup.txt")
    if backup_content:
        print(f"   备份文件内容: {repr(backup_content)}")

    # 修改原文件，验证硬链接同步
    print("\n✏️  修改原文件:")
    fs.write_file("/home/user/document.txt", "这是修改后的文档！")

    # 读取备份文件，应该看到相同的内容
    print("\n🔍 读取备份文件（应该同步更新）:")
    backup_content = fs.read_file("/home/user/backup.txt")
    if backup_content:
        print(f"   备份文件内容: {repr(backup_content)}")

    # 删除一个硬链接
    print("\n🗑️  删除原文件:")
    fs.delete_file("/home/user/document.txt")

    # 验证备份文件仍然存在
    print("\n🔍 验证备份文件仍然可访问:")
    backup_content = fs.read_file("/home/user/backup.txt")
    if backup_content:
        print(f"   备份文件内容: {repr(backup_content)}")
        print("✅ 硬链接机制工作正常！")

    # 删除最后一个硬链接
    print("\n🗑️  删除备份文件（最后一个硬链接）:")
    fs.delete_file("/home/user/backup.txt")

if __name__ == "__main__":
    demonstrate_inode_concepts()