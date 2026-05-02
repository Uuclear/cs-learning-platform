# 模拟I/O调度器
# 展示操作系统如何管理多个I/O请求

import time
from collections import deque

print("=" * 50)
print("⚙️ I/O调度器模拟")
print("=" * 50)

class IODevice:
    """模拟I/O设备"""
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed  # 处理速度（毫秒/请求）
        self.busy = False
    
    def process(self, request):
        """处理I/O请求"""
        print(f"  [{self.name}] 正在处理: {request}")
        time.sleep(self.speed / 1000)  # 模拟处理时间
        print(f"  [{self.name}] 完成: {request}")
        return f"{request} 的结果"

class IOScheduler:
    """I/O调度器 - 管理多个设备的I/O请求"""
    def __init__(self):
        self.devices = {}  # 设备字典
        self.request_queue = deque()  # 请求队列
        self.completed = []  # 已完成的请求
    
    def add_device(self, device):
        """添加设备"""
        self.devices[device.name] = device
        print(f"✅ 注册设备: {device.name} (速度: {device.speed}ms/请求)")
    
    def submit_request(self, device_name, operation, data):
        """提交I/O请求"""
        request = {
            'device': device_name,
            'operation': operation,
            'data': data,
            'timestamp': time.time()
        }
        self.request_queue.append(request)
        print(f"📨 提交请求: [{device_name}] {operation} - '{data}'")
    
    def process_all(self):
        """处理队列中的所有请求"""
        print(f"\n🚀 开始处理 {len(self.request_queue)} 个请求...")
        print("-" * 40)
        
        while self.request_queue:
            request = self.request_queue.popleft()
            device_name = request['device']
            
            if device_name not in self.devices:
                print(f"❌ 错误: 未知设备 '{device_name}'")
                continue
            
            device = self.devices[device_name]
            result = device.process(f"{request['operation']}({request['data']})")
            
            self.completed.append({
                'request': request,
                'result': result
            })
        
        print("-" * 40)
        print(f"✅ 所有请求处理完成！共完成 {len(self.completed)} 个\n")


# 创建设备
keyboard = IODevice("键盘", 50)      # 键盘响应快
printer = IODevice("打印机", 200)    # 打印机较慢
disk = IODevice("硬盘", 100)         # 硬盘中等速度

# 创建调度器并注册设备
scheduler = IOScheduler()
scheduler.add_device(keyboard)
scheduler.add_device(printer)
scheduler.add_device(disk)

print()

# 提交各种I/O请求
scheduler.submit_request("键盘", "读取输入", "Hello")
scheduler.submit_request("硬盘", "读取文件", "data.txt")
scheduler.submit_request("打印机", "打印文档", "报告.pdf")
scheduler.submit_request("键盘", "读取输入", "World")
scheduler.submit_request("硬盘", "写入文件", "output.txt")

# 处理所有请求
scheduler.process_all()

# 显示完成摘要
print("📊 处理摘要:")
print("-" * 40)
for item in scheduler.completed:
    req = item['request']
    print(f"  [{req['device']}] {req['operation']}: {item['result']}")

# 输出:
# ==================================================
# ⚙️ I/O调度器模拟
# ==================================================
# ✅ 注册设备: 键盘 (速度: 50ms/请求)
# ✅ 注册设备: 打印机 (速度: 200ms/请求)
# ✅ 注册设备: 硬盘 (速度: 100ms/请求)
#
# 📨 提交请求: [键盘] 读取输入 - 'Hello'
# 📨 提交请求: [硬盘] 读取文件 - 'data.txt'
# 📨 提交请求: [打印机] 打印文档 - '报告.pdf'
# 📨 提交请求: [键盘] 读取输入 - 'World'
# 📨 提交请求: [硬盘] 写入文件 - 'output.txt'
#
# 🚀 开始处理 5 个请求...
# ----------------------------------------
#   [键盘] 正在处理: 读取输入(Hello)
#   [键盘] 完成: 读取输入(Hello)
#   [硬盘] 正在处理: 读取文件(data.txt)
#   [硬盘] 完成: 读取文件(data.txt)
#   [打印机] 正在处理: 打印文档(报告.pdf)
#   [打印机] 完成: 打印文档(报告.pdf)
#   [键盘] 正在处理: 读取输入(World)
#   [键盘] 完成: 读取输入(World)
#   [硬盘] 正在处理: 写入文件(output.txt)
#   [硬盘] 完成: 写入文件(output.txt)
# ----------------------------------------
# ✅ 所有请求处理完成！共完成 5 个
#
# 📊 处理摘要:
# ----------------------------------------
#   [键盘] 读取输入: 读取输入(Hello) 的结果
#   [硬盘] 读取文件: 读取文件(data.txt) 的结果
#   [打印机] 打印文档: 打印文档(报告.pdf) 的结果
#   [键盘] 读取输入: 读取输入(World) 的结果
#   [硬盘] 写入文件: 写入文件(output.txt) 的结果
