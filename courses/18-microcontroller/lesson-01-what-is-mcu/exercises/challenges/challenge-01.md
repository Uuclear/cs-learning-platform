# 挑战 1: 创建你自己的虚拟单片机环境

## 背景
在开始真实的硬件开发之前，创建一个软件模拟环境可以帮助你理解单片机的基本概念和编程模式。

## 任务要求
使用 Python 创建一个简单的虚拟单片机类，包含以下功能：

1. **GPIO 引脚模拟**：
   - 支持设置引脚为 INPUT 或 OUTPUT 模式
   - 支持读取/写入数字电平（HIGH/LOW）
   - 支持内部上拉/下拉电阻配置

2. **基本外设模拟**：
   - 简单的串口通信功能（发送和接收字符串）
   - 基本的延时功能

3. **程序结构模拟**：
   - 实现类似 Arduino 的 `setup()` 和 `loop()` 函数结构
   - 支持非阻塞式的定时操作

## 具体实现步骤

### 步骤 1: 创建基础 GPIO 类
```python
class VirtualPin:
    def __init__(self, pin_number):
        self.pin_number = pin_number
        self.mode = "INPUT"
        self.state = False
        self.pull_mode = None
    
    def set_mode(self, mode, pull_mode=None):
        # 实现引脚模式设置
        pass
    
    def write(self, state):
        # 实现数字输出
        pass
    
    def read(self):
        # 实现数字输入
        pass
```

### 步骤 2: 创建虚拟单片机类
```python
class VirtualMCU:
    def __init__(self):
        self.pins = {}  # 存储所有引脚对象
        self.serial_buffer = []
    
    def setup(self):
        # 初始化函数，在开始时调用一次
        pass
    
    def loop(self):
        # 主循环函数，重复调用
        pass
    
    def run(self):
        # 运行整个程序：先调用setup()，然后循环调用loop()
        pass
```

### 步骤 3: 实现 Blink 功能
创建一个继承自 `VirtualMCU` 的类，实现经典的 Blink 功能：
- 在 `setup()` 中初始化 LED 引脚为输出模式
- 在 `loop()` 中实现 LED 闪烁逻辑（亮1秒，灭1秒）

### 步骤 4: 扩展功能（可选）
- 添加按钮输入功能，实现按下按钮时改变 LED 闪烁频率
- 实现简单的串口通信，能够在控制台输出调试信息

## 提交要求
- 完整的 Python 代码文件
- 包含注释解释关键概念
- 一个简短的 README 说明如何运行你的代码

## 评估标准
- 代码结构清晰，符合面向对象设计原则
- 正确实现了要求的功能
- 包含适当的错误处理
- 注释充分，易于理解
- 创新性扩展（额外加分）

## 提示
- 参考课程中的 example-01.py 和 solution-01.py
- 考虑如何模拟硬件的并发行为
- 思考真实单片机的限制（内存、处理能力等）