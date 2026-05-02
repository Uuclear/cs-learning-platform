# 挑战2：文件复制器

## 难度
⭐⭐

## 描述

实现一个文件复制程序，支持显示复制进度。程序应该能够读取源文件，写入目标文件，并在复制过程中显示进度百分比。

## 输入

程序接收两个参数：
- `src`: 源文件路径
- `dst`: 目标文件路径

## 输出

程序输出复制进度：
- 文件信息（大小、路径）
- 进度条和百分比
- 复制完成提示
- 错误提示（如文件不存在）

## 示例

**示例 1:**
```
源文件: test.txt
目标文件: test_copy.txt
文件大小: 10240 字节 (10.00 KB)
--------------------------------------------------
[████████████████████████████░░░░░░░░░░░░] 75.0% (7680/10240 字节)
--------------------------------------------------
✅ 复制完成！
```

**示例 2（错误情况）:**
```
源文件: not_exist.txt
输出: ❌ 错误: 源文件 'not_exist.txt' 不存在
```

## 约束条件

- 每次读取固定大小（如1024字节）
- 显示进度条（用 `█` 和 `░` 表示）
- 处理文件不存在、权限不足等错误
- 支持二进制文件复制

## 提示

- 用 `os.path.getsize()` 获取文件大小
- 用 `os.path.exists()` 检查文件是否存在
- 用 `read(1024)` 分块读取
- 用 `try-except` 处理异常
- 进度 = 已复制字节数 / 总字节数 × 100%
- 用 `\r` 和 `end=''` 实现单行更新进度

## 进阶思考

- 如何实现断点续传？（提示：记录已复制的位置）
- 如何支持复制整个目录？（提示：递归遍历目录）
- 如何计算复制速度？（提示：记录开始时间和当前时间）

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

1. 检查源文件是否存在
2. 获取文件大小
3. 以二进制模式打开源文件和目标文件
4. 循环读取固定大小的块，写入目标文件
5. 每次写入后更新并显示进度
6. 处理可能的异常

### 代码

```python
import os

def copy_file_with_progress(src, dst):
    """复制文件并显示进度"""
    # 检查源文件
    if not os.path.exists(src):
        print(f"❌ 错误: 源文件 '{src}' 不存在")
        return False
    
    if not os.path.isfile(src):
        print(f"❌ 错误: '{src}' 不是文件")
        return False
    
    # 获取文件大小
    total_size = os.path.getsize(src)
    print(f"📊 源文件: {src}")
    print(f"📊 目标文件: {dst}")
    print(f"📊 文件大小: {total_size} 字节 ({total_size/1024:.2f} KB)")
    print("-" * 50)
    
    block_size = 1024
    copied = 0
    
    try:
        with open(src, 'rb') as f_src, open(dst, 'wb') as f_dst:
            while True:
                block = f_src.read(block_size)
                if not block:
                    break
                
                f_dst.write(block)
                copied += len(block)
                
                # 显示进度
                progress = (copied / total_size) * 100
                bar_length = 30
                filled = int(bar_length * copied / total_size)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                print(f"\r[{bar}] {progress:.1f}% ({copied}/{total_size} 字节)", 
                      end='', flush=True)
        
        print()
        print("-" * 50)
        print(f"✅ 复制完成！")
        return True
        
    except PermissionError:
        print(f"\n❌ 错误: 权限不足")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


# 使用示例
if __name__ == "__main__":
    # 创建测试文件
    test_content = "测试内容 " * 1000
    with open("test.txt", 'w') as f:
        f.write(test_content)
    
    # 复制文件
    copy_file_with_progress("test.txt", "test_copy.txt")
    
    # 清理
    os.remove("test.txt")
    os.remove("test_copy.txt")
```

### 复杂度分析

- 时间复杂度: O(n)，其中n是文件大小（需要遍历整个文件）
- 空间复杂度: O(1)，只使用固定大小的缓冲区

</details>
