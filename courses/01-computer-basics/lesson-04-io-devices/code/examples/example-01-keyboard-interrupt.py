# 模拟键盘输入处理和中断机制
# 想象这是一个简单的文字处理器

class KeyboardInputHandler:
    """键盘输入处理器 - 模拟中断处理"""
    
    def __init__(self):
        self.buffer = []  # 输入缓冲区
        self.interrupt_enabled = True  # 中断使能标志
    
    def key_pressed(self, key):
        """模拟按键被按下（触发中断）"""
        if self.interrupt_enabled:
            print(f"🚨 [中断] 检测到按键: '{key}'")
            self.handle_interrupt(key)
        else:
            print(f"⚠️ 中断被禁用，忽略按键: '{key}'")
    
    def handle_interrupt(self, key):
        """处理中断 - 保存按键到缓冲区"""
        # 保存当前状态（简化版）
        print(f"   → 保存CPU状态...")
        
        # 处理输入
        if key == 'BACKSPACE':
            if self.buffer:
                removed = self.buffer.pop()
                print(f"   → 删除字符 '{removed}'")
        elif key == 'ENTER':
            print(f"   → 换行！当前行: {''.join(self.buffer)}")
            self.buffer.clear()
        else:
            self.buffer.append(key)
            print(f"   → 缓冲区: {''.join(self.buffer)}")
        
        # 恢复状态（简化版）
        print(f"   → 恢复CPU状态，继续原任务\n")
    
    def get_buffer_content(self):
        """获取缓冲区内容"""
        return ''.join(self.buffer)


# 演示键盘输入处理
print("=" * 50)
print("🎹 键盘输入处理模拟器")
print("=" * 50)

keyboard = KeyboardInputHandler()

# 模拟用户输入 "Hello"
print("用户想输入 'Hello'...\n")
for char in ['H', 'e', 'l', 'l', 'o']:
    keyboard.key_pressed(char)

# 模拟按回车
keyboard.key_pressed('ENTER')

# 模拟输入 "World" 然后退格
print("用户想输入 'World' 但打错字...\n")
for char in ['W', 'o', 'r', 'l', 'x']:
    keyboard.key_pressed(char)
keyboard.key_pressed('BACKSPACE')  # 删除 'x'
keyboard.key_pressed('d')  # 输入正确的 'd'

print(f"\n最终缓冲区内容: '{keyboard.get_buffer_content()}'")

# 输出:
# ==================================================
# 🎹 键盘输入处理模拟器
# ==================================================
# 用户想输入 'Hello'...
#
# 🚨 [中断] 检测到按键: 'H'
#    → 保存CPU状态...
#    → 缓冲区: H
#    → 恢复CPU状态，继续原任务
#
# 🚨 [中断] 检测到按键: 'e'
#    → 保存CPU状态...
#    → 缓冲区: He
#    → 恢复CPU状态，继续原任务
#
# 🚨 [中断] 检测到按键: 'l'
#    → 保存CPU状态...
#    → 缓冲区: Hel
#    → 恢复CPU状态，继续原任务
#
# 🚨 [中断] 检测到按键: 'l'
#    → 保存CPU状态...
#    → 缓冲区: Hell
#    → 恢复CPU状态，继续原任务
#
# 🚨 [中断] 检测到按键: 'o'
#    → 保存CPU状态...
#    → 缓冲区: Hello
#    → 恢复CPU状态，继续原任务
#
# 🚨 [中断] 检测到按键: 'ENTER'
#    → 换行！当前行: Hello
#    → 恢复CPU状态，继续原任务
#
# 用户想输入 'World' 但打错字...
#
# 🚨 [中断] 检测到按键: 'W'
#    → 保存CPU状态...
#    → 缓冲区: W
#    → 恢复CPU状态，继续原任务
# ...
# 🚨 [中断] 检测到按键: 'BACKSPACE'
#    → 删除字符 'x'
#    → 恢复CPU状态，继续原任务
#
# 🚨 [中断] 检测到按键: 'd'
#    → 保存CPU状态...
#    → 缓冲区: World
#    → 恢复CPU状态，继续原任务
#
# 最终缓冲区内容: 'World'
