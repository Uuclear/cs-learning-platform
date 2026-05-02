# 练习1解答：简易文本编辑器
# 实现一个支持基本输入、退格、显示的简易文本编辑器

print("=" * 50)
print("📝 简易文本编辑器")
print("=" * 50)
print("命令说明：")
print("  - 直接输入：添加文字到编辑器")
print("  - 'back'：删除最后一个字符（退格）")
print("  - 'show'：显示当前内容")
print("  - 'quit'：退出程序")
print("-" * 50)

class SimpleEditor:
    """简易文本编辑器"""
    def __init__(self):
        self.buffer = []  # 用列表存储字符
    
    def insert(self, text):
        """插入文字"""
        for char in text:
            self.buffer.append(char)
        print(f"✅ 已添加: '{text}'")
    
    def backspace(self):
        """退格删除"""
        if self.buffer:
            removed = self.buffer.pop()
            print(f"✅ 已删除: '{removed}'")
        else:
            print("⚠️ 缓冲区为空，无法删除")
    
    def show(self):
        """显示内容"""
        content = ''.join(self.buffer)
        print(f"📄 当前内容: '{content}'")
        print(f"   长度: {len(self.buffer)} 字符")
    
    def clear(self):
        """清空内容"""
        self.buffer.clear()
        print("✅ 已清空")


# 创建编辑器实例
editor = SimpleEditor()

# 主循环
while True:
    # 获取用户输入
    user_input = input("\n> ").strip()
    
    # 处理命令
    if user_input.lower() == 'quit':
        print("👋 再见！")
        break
    elif user_input.lower() == 'back':
        editor.backspace()
    elif user_input.lower() == 'show':
        editor.show()
    elif user_input.lower() == 'clear':
        editor.clear()
    elif user_input == '':
        print("⚠️ 请输入内容或命令")
    else:
        editor.insert(user_input)

# 示例运行：
# ==================================================
# 📝 简易文本编辑器
# ==================================================
# 命令说明：
#   - 直接输入：添加文字到编辑器
#   - 'back'：删除最后一个字符（退格）
#   - 'show'：显示当前内容
#   - 'quit'：退出程序
# --------------------------------------------------
#
# > Hello
# ✅ 已添加: 'Hello'
#
# >  World
# ✅ 已添加: ' World'
#
# > show
# 📄 当前内容: 'Hello World'
#    长度: 11 字符
#
# > back
# ✅ 已删除: 'd'
#
# > show
# 📄 当前内容: 'Hello Worl'
#    长度: 10 字符
#
# > quit
# 👋 再见！
