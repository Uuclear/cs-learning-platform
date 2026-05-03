# 实现简化的Git commit系统

## 背景

Git 的核心是一个内容寻址的文件系统，通过对象模型（blob、tree、commit）来存储和管理版本历史。理解这些基本概念有助于我们更好地使用 Git。

## 任务

实现一个简化的 Git commit 系统，支持以下功能：

1. **创建 blob 对象**：将文件内容存储为 blob 对象，并计算 SHA-1 哈希值
2. **创建 tree 对象**：将目录结构存储为 tree 对象，包含文件名、模式和对应的 blob SHA-1
3. **创建 commit 对象**：将提交信息、作者、时间戳和 tree 引用组合成 commit 对象
4. **基本的版本控制**：能够创建多个提交，并维护父子关系

## 要求

- 使用 Python 标准库实现（hashlib、os、time 等）
- 遵循 Git 对象格式：`"类型 长度\0内容"`
- 支持基本的文件和目录结构
- 提交信息应包含作者、时间戳和提交说明
- 能够显示提交历史（至少显示最近3个提交）

## 示例输出

```
$ python challenge-01-solution.py
初始化仓库...
创建提交: abc123 - 初始提交
创建提交: def456 - 添加用户认证功能
创建提交: ghi789 - 修复登录bug

提交历史:
commit ghi789
Author: User <user@example.com>
Date:   Mon May 3 10:30:45 2026

    修复登录bug

commit def456
Author: User <user@example.com>  
Date:   Mon May 3 10:25:30 2026

    添加用户认证功能

commit abc123
Author: User <user@example.com>
Date:   Mon May 3 10:20:15 2026

    初始提交
```

## 提示

1. 参考 `example-01-git-internals.py` 中的对象模型实现
2. Git 对象存储在 `.git/objects/` 目录下，按前两个字符分目录
3. 提交对象包含 tree 引用、父提交引用、作者信息和提交消息
4. 时间戳使用 Unix 时间戳格式

## 扩展挑战（可选）

- 支持分支功能（维护 HEAD 和 refs/heads/）
- 实现基本的 checkout 功能，能够恢复到指定提交的状态
- 添加简单的 diff 功能，显示两个提交之间的差异

⭐⭐ 难度：中等
预计完成时间：45-60分钟