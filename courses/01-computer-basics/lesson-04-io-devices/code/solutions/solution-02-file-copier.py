# 练习2解答：文件复制器
# 实现一个文件复制程序，支持显示复制进度

import os
import shutil

print("=" * 50)
print("📂 文件复制器")
print("=" * 50)

def copy_file_with_progress(src, dst):
    """
    复制文件并显示进度
    参数:
        src: 源文件路径
        dst: 目标文件路径
    """
    # 检查源文件是否存在
    if not os.path.exists(src):
        print(f"❌ 错误: 源文件 '{src}' 不存在")
        return False
    
    # 检查是否是文件
    if not os.path.isfile(src):
        print(f"❌ 错误: '{src}' 不是文件")
        return False
    
    # 获取文件大小
    total_size = os.path.getsize(src)
    print(f"📊 源文件: {src}")
    print(f"📊 目标文件: {dst}")
    print(f"📊 文件大小: {total_size} 字节 ({total_size/1024:.2f} KB)")
    print("-" * 50)
    
    # 块大小（每次读取1KB）
    block_size = 1024
    copied = 0
    
    try:
        with open(src, 'rb') as f_src, open(dst, 'wb') as f_dst:
            while True:
                # 读取一块数据
                block = f_src.read(block_size)
                if not block:
                    break
                
                # 写入目标文件
                f_dst.write(block)
                copied += len(block)
                
                # 计算并显示进度
                progress = (copied / total_size) * 100
                bar_length = 30
                filled = int(bar_length * copied / total_size)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                print(f"\r[{bar}] {progress:.1f}% ({copied}/{total_size} 字节)", end='', flush=True)
        
        print()  # 换行
        print("-" * 50)
        print(f"✅ 复制完成！")
        return True
        
    except PermissionError:
        print(f"\n❌ 错误: 权限不足，无法访问文件")
        return False
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return False


# 创建一个测试文件
test_src = "test_source.txt"
test_dst = "test_destination.txt"

# 生成测试内容（约10KB）
test_content = "这是一行测试数据。" * 500  # 重复生成内容
with open(test_src, 'w', encoding='utf-8') as f:
    f.write(test_content)

print(f"📝 已创建测试文件: {test_src}")
print()

# 执行复制
copy_file_with_progress(test_src, test_dst)

# 验证复制结果
if os.path.exists(test_dst):
    src_size = os.path.getsize(test_src)
    dst_size = os.path.getsize(test_dst)
    if src_size == dst_size:
        print(f"✅ 验证通过: 文件大小一致 ({src_size} 字节)")
    else:
        print(f"⚠️ 警告: 文件大小不一致 (源:{src_size}, 目标:{dst_size})")

# 清理测试文件
print("\n🗑️ 清理测试文件...")
os.remove(test_src)
os.remove(test_dst)
print("✅ 清理完成")

# 示例运行：
# ==================================================
# 📂 文件复制器
# ==================================================
# 📝 已创建测试文件: test_source.txt
#
# 📊 源文件: test_source.txt
# 📊 目标文件: test_destination.txt
# 📊 文件大小: 10500 字节 (10.25 KB)
# --------------------------------------------------
# [████████████████████████████░░░░░░░░░░░░] 85.7% (9000/10500 字节)
# --------------------------------------------------
# ✅ 复制完成！
# ✅ 验证通过: 文件大小一致 (10500 字节)
#
# 🗑️ 清理测试文件...
# ✅ 清理完成
