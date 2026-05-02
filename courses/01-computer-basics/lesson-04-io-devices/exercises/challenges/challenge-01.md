# 挑战1：简易文本编辑器

## 难度
⭐

## 描述

实现一个支持基本输入、退格、显示的简易文本编辑器。这个编辑器应该能够接收用户输入，支持删除操作，并随时显示当前内容。

## 输入

程序通过 `input()` 函数接收用户输入：
- 直接输入文字：添加到编辑器
- 输入 `back`：删除最后一个字符（退格）
- 输入 `show`：显示当前内容
- 输入 `quit`：退出程序

## 输出

根据命令输出相应信息：
- 添加文字后显示：`✅ 已添加: 'xxx'`
- 退格后显示：`✅ 已删除: 'x'` 或 `⚠️ 缓冲区为空，无法删除`
- 显示命令后显示：`📄 当前内容: 'xxx'` 和 `长度: n 字符`
- 退出时显示：`👋 再见！`

## 示例

**示例 1:**
```
输入: Hello
输出: ✅ 已添加: 'Hello'

输入:  World
输出: ✅ 已添加: ' World'

输入: show
输出: 📄 当前内容: 'Hello World'
       长度: 11 字符

输入: back
输出: ✅ 已删除: 'd'

输入: show
输出: 📄 当前内容: 'Hello Worl'
       长度: 10 字符

输入: quit
输出: 👋 再见！
```

**示例 2:**
```
输入: back
输出: ⚠️ 缓冲区为空，无法删除

输入: show
输出: 📄 当前内容: ''
       长度: 0 字符

输入: quit
输出: 👋 再见！
```

## 约束条件

- 使用列表存储字符（方便插入和删除）
- 支持任意可打印字符的输入
- 退格时如果缓冲区为空，给出提示

## 提示

- 用 `list.append()` 添加字符
- 用 `list.pop()` 删除最后一个字符
- 用 `''.join(list)` 将列表转换为字符串
- 使用 `while True` 循环持续接收输入
- 用条件判断处理不同命令

## 进阶思考

- 如何实现撤销（undo）功能？（提示：使用栈保存历史状态）
- 如何实现多行编辑？（提示：用二维列表或字符串列表）

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

1. 创建一个类来管理编辑器状态（缓冲区）
2. 在主循环中接收用户输入
3. 根据输入内容判断是命令还是普通文字
4. 执行相应操作并输出反馈

### 代码

```python
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


# 创建编辑器实例
editor = SimpleEditor()

# 主循环
while True:
    user_input = input("\n> ").strip()
    
    if user_input.lower() == 'quit':
        print("👋 再见！")
        break
    elif user_input.lower() == 'back':
        editor.backspace()
    elif user_input.lower() == 'show':
        editor.show()
    elif user_input == '':
        print("⚠️ 请输入内容或命令")
    else:
        editor.insert(user_input)
```

### 复杂度分析

- 时间复杂度: O(n)，其中n是输入文字的长度（每次添加字符需要遍历）
- 空间复杂度: O(m)，其中m是缓冲区中的字符数

</details>
