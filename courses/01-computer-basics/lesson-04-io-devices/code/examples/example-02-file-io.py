# 文件I/O操作演示
# 文件I/O是最常见的I/O操作之一

import os

print("=" * 50)
print("📁 文件I/O操作演示")
print("=" * 50)

# 定义文件名
filename = "demo_data.txt"

# 1. 写入文件（输出操作）
print("\n📝 步骤1: 写入文件")
print("-" * 30)

data_to_write = """Hello, I/O World!
这是第二行数据。
这是第三行，文件I/O很有趣！"""

# 使用 with 语句确保文件正确关闭
with open(filename, 'w', encoding='utf-8') as file:
    # 'w' 模式：写入模式（write）
    bytes_written = file.write(data_to_write)
    print(f"✅ 成功写入 {bytes_written} 个字符到 '{filename}'")

# 2. 读取文件（输入操作）
print("\n📖 步骤2: 读取文件")
print("-" * 30)

with open(filename, 'r', encoding='utf-8') as file:
    # 'r' 模式：读取模式（read）
    content = file.read()
    print(f"✅ 读取到的内容:\n{'-'*30}")
    print(content)
    print(f"{'-'*30}")

# 3. 追加写入（在文件末尾添加）
print("\n➕ 步骤3: 追加写入")
print("-" * 30)

with open(filename, 'a', encoding='utf-8') as file:
    # 'a' 模式：追加模式（append）
    file.write("\n这是追加的第四行！")
    print(f"✅ 成功追加内容到文件末尾")

# 4. 逐行读取
print("\n📋 步骤4: 逐行读取")
print("-" * 30)

with open(filename, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    print(f"✅ 文件共有 {len(lines)} 行:")
    for i, line in enumerate(lines, 1):
        print(f"  第{i}行: {line.strip()}")

# 5. 获取文件信息
print("\n📊 步骤5: 文件信息")
print("-" * 30)

file_size = os.path.getsize(filename)
print(f"✅ 文件大小: {file_size} 字节")
print(f"✅ 文件路径: {os.path.abspath(filename)}")

# 清理：删除演示文件
os.remove(filename)
print(f"\n🗑️ 演示完成，已删除临时文件 '{filename}'")

# 输出:
# ==================================================
# 📁 文件I/O操作演示
# ==================================================
#
# 📝 步骤1: 写入文件
# ------------------------------
# ✅ 成功写入 63 个字符到 'demo_data.txt'
#
# 📖 步骤2: 读取文件
# ------------------------------
# ✅ 读取到的内容:
# ------------------------------
# Hello, I/O World!
# 这是第二行数据。
# 这是第三行，文件I/O很有趣！
# ------------------------------
#
# ➕ 步骤3: 追加写入
# ------------------------------
# ✅ 成功追加内容到文件末尾
#
# 📋 步骤4: 逐行读取
# ------------------------------
# ✅ 文件共有 4 行:
#   第1行: Hello, I/O World!
#   第2行: 这是第二行数据。
#   第3行: 这是第三行，文件I/O很有趣！
#   第4行: 这是追加的第四行！
#
# 📊 步骤5: 文件信息
# ------------------------------
# ✅ 文件大小: 85 字节
# ✅ 文件路径: /xxx/demo_data.txt
#
# 🗑️ 演示完成，已删除临时文件 'demo_data.txt'
