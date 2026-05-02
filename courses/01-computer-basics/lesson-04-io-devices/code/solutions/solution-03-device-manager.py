# 练习3解答：设备管理器
# 实现一个简单的设备管理器，支持设备注册、请求队列、优先级调度

import heapq
import time
from dataclasses import dataclass, field

print("=" * 60)
print("⚙️ 优先级设备管理器")
print("=" * 60)

@dataclass(order=True)
class IORequest:
    """I/O请求类 - 支持优先级排序"""
    priority: int  # 优先级（1-5，5最高）
    timestamp: float = field(compare=True)  # 时间戳，用于相同优先级的FIFO
    device_name: str = field(compare=False)
    operation: str = field(compare=False)
    data: str = field(compare=False)
    
    def __repr__(self):
        return f"[{self.device_name}] {self.operation}('{self.data}') P={self.priority}"


class Device:
    """设备类"""
    def __init__(self, name, device_type, speed):
        self.name = name
        self.device_type = device_type
        self.speed = speed  # 处理速度（毫秒）
        self.status = "空闲"
        self.processed_count = 0
    
    def process(self, request):
        """处理请求"""
        self.status = "忙碌"
        print(f"    [{self.name}] 正在处理: {request.operation}({request.data})")
        time.sleep(self.speed / 1000)  # 模拟处理时间
        self.status = "空闲"
        self.processed_count += 1
        return f"{request.operation}完成"


class DeviceManager:
    """设备管理器 - 支持优先级调度"""
    def __init__(self):
        self.devices = {}  # 设备字典
        self.request_queue = []  # 优先级队列（用堆实现）
        self.completed_requests = []
        self.counter = 0  # 用于保证相同优先级时的FIFO顺序
    
    def register_device(self, device):
        """注册设备"""
        self.devices[device.name] = device
        print(f"✅ 注册设备: {device.name} (类型: {device.device_type}, 速度: {device.speed}ms)")
    
    def submit_request(self, device_name, operation, data, priority=3):
        """提交I/O请求"""
        if device_name not in self.devices:
            print(f"❌ 错误: 未找到设备 '{device_name}'")
            return
        
        # 优先级反转（heapq是最小堆，所以用6-priority实现最大堆效果）
        heap_priority = 6 - priority
        
        request = IORequest(
            priority=heap_priority,
            timestamp=time.time() + self.counter * 0.0001,  # 确保FIFO
            device_name=device_name,
            operation=operation,
            data=data
        )
        self.counter += 1
        
        heapq.heappush(self.request_queue, request)
        print(f"📨 提交请求: [{device_name}] {operation}('{data}') 优先级:{priority}")
    
    def process_all(self):
        """处理所有请求（按优先级）"""
        print(f"\n🚀 开始处理 {len(self.request_queue)} 个请求（按优先级）...")
        print("-" * 60)
        
        while self.request_queue:
            # 取出优先级最高的请求
            request = heapq.heappop(self.request_queue)
            device = self.devices[request.device_name]
            
            # 显示优先级（转换回1-5）
            actual_priority = 6 - request.priority
            print(f"\n  [优先级 {actual_priority}] {request}")
            
            # 处理请求
            result = device.process(request)
            
            self.completed_requests.append({
                'request': request,
                'result': result,
                'priority': actual_priority
            })
        
        print("-" * 60)
        print(f"✅ 所有请求处理完成！共完成 {len(self.completed_requests)} 个\n")
    
    def show_statistics(self):
        """显示统计信息"""
        print("📊 设备统计:")
        print("-" * 60)
        for name, device in self.devices.items():
            print(f"  {device.name}: 处理了 {device.processed_count} 个请求")
        
        print("\n📋 请求处理顺序:")
        print("-" * 60)
        for i, item in enumerate(self.completed_requests, 1):
            req = item['request']
            print(f"  {i}. [P{item['priority']}] [{req.device_name}] {req.operation}('{req.data}')")


# 创建设备管理器
manager = DeviceManager()

# 注册设备
manager.register_device(Device("键盘", "输入设备", 30))
manager.register_device(Device("鼠标", "输入设备", 20))
manager.register_device(Device("硬盘", "存储设备", 100))
manager.register_device(Device("打印机", "输出设备", 300))

print()

# 提交各种优先级的请求
manager.submit_request("键盘", "读取输入", "紧急命令", priority=5)
manager.submit_request("硬盘", "读取文件", "系统配置", priority=4)
manager.submit_request("鼠标", "点击事件", "打开应用", priority=3)
manager.submit_request("打印机", "打印文档", "普通报告", priority=2)
manager.submit_request("键盘", "读取输入", "普通文字", priority=3)
manager.submit_request("硬盘", "写入日志", "错误日志", priority=5)  # 高优先级
manager.submit_request("打印机", "打印文档", "紧急合同", priority=5)  # 高优先级

# 处理所有请求
manager.process_all()

# 显示统计
manager.show_statistics()

# 示例运行：
# ============================================================
# ⚙️ 优先级设备管理器
# ============================================================
# ✅ 注册设备: 键盘 (类型: 输入设备, 速度: 30ms)
# ✅ 注册设备: 鼠标 (类型: 输入设备, 速度: 20ms)
# ✅ 注册设备: 硬盘 (类型: 存储设备, 速度: 100ms)
# ✅ 注册设备: 打印机 (类型: 输出设备, 速度: 300ms)
#
# 📨 提交请求: [键盘] 读取输入('紧急命令') 优先级:5
# 📨 提交请求: [硬盘] 读取文件('系统配置') 优先级:4
# 📨 提交请求: [鼠标] 点击事件('打开应用') 优先级:3
# 📨 提交请求: [打印机] 打印文档('普通报告') 优先级:2
# 📨 提交请求: [键盘] 读取输入('普通文字') 优先级:3
# 📨 提交请求: [硬盘] 写入日志('错误日志') 优先级:5
# 📨 提交请求: [打印机] 打印文档('紧急合同') 优先级:5
#
# 🚀 开始处理 7 个请求（按优先级）...
# ------------------------------------------------------------
#
#   [优先级 5] [键盘] 读取输入('紧急命令') P=1
#     [键盘] 正在处理: 读取输入(紧急命令)
#     [键盘] 完成
#
#   [优先级 5] [硬盘] 写入日志('错误日志') P=1
#     [硬盘] 正在处理: 写入日志(错误日志)
#     [硬盘] 完成
#
#   [优先级 5] [打印机] 打印文档('紧急合同') P=1
#     [打印机] 正在处理: 打印文档(紧急合同)
#     [打印机] 完成
#
#   [优先级 4] [硬盘] 读取文件('系统配置') P=2
# ...
# ------------------------------------------------------------
# ✅ 所有请求处理完成！共完成 7 个
#
# 📊 设备统计:
# ------------------------------------------------------------
#   键盘: 处理了 2 个请求
#   鼠标: 处理了 1 个请求
#   硬盘: 处理了 2 个请求
#   打印机: 处理了 2 个请求
#
# 📋 请求处理顺序:
# ------------------------------------------------------------
#   1. [P5] [键盘] 读取输入('紧急命令')
#   2. [P5] [硬盘] 写入日志('错误日志')
#   3. [P5] [打印机] 打印文档('紧急合同')
#   4. [P4] [硬盘] 读取文件('系统配置')
# ...
