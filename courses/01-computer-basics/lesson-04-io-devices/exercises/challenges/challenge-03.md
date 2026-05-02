# 挑战3：优先级设备管理器

## 难度
⭐⭐⭐

## 描述

实现一个简单的设备管理器，支持设备注册、请求队列、优先级调度。模拟操作系统如何管理多个I/O设备的请求。

## 输入

程序通过方法调用接收输入：
- `register_device(device)`: 注册设备
- `submit_request(device_name, operation, data, priority)`: 提交I/O请求

## 输出

程序输出处理过程：
- 设备注册信息
- 请求提交确认
- 按优先级处理请求的过程
- 处理完成统计

## 示例

**示例 1:**
```
✅ 注册设备: 键盘 (类型: 输入设备, 速度: 30ms)
✅ 注册设备: 硬盘 (类型: 存储设备, 速度: 100ms)

📨 提交请求: [键盘] 读取输入('紧急命令') 优先级:5
📨 提交请求: [硬盘] 读取文件('普通文件') 优先级:2

🚀 开始处理 2 个请求（按优先级）...
------------------------------------------------------------

  [优先级 5] [键盘] 读取输入('紧急命令')
    [键盘] 正在处理: 读取输入(紧急命令)
    [键盘] 完成

  [优先级 2] [硬盘] 读取文件('普通文件')
    [硬盘] 正在处理: 读取文件(普通文件)
    [硬盘] 完成
------------------------------------------------------------
✅ 所有请求处理完成！共完成 2 个

📊 设备统计:
------------------------------------------------------------
  键盘: 处理了 1 个请求
  硬盘: 处理了 1 个请求
```

## 约束条件

- 优先级范围 1-5（5为最高优先级）
- 相同优先级的请求按FIFO（先进先出）处理
- 每个设备有处理速度（模拟处理时间）
- 使用堆（heap）或排序实现优先级队列

## 提示

- 用 `dataclass` 定义请求类，包含优先级和时间戳
- 用 `heapq` 模块实现优先级队列
- 注意：Python的 `heapq` 是最小堆，可以用 `6-priority` 实现最大堆效果
- 时间戳用于保证相同优先级的FIFO顺序
- 用 `time.sleep()` 模拟设备处理时间

## 进阶思考

- 如何实现设备忙等待？（提示：检查设备状态）
- 如何实现抢占式调度？（提示：高优先级可以中断低优先级）
- 如何支持批量请求的原子性？（提示：事务概念）

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路

1. 定义 `IORequest` 类，包含优先级、时间戳、设备名等信息
2. 定义 `Device` 类，包含名称、类型、速度等属性
3. 定义 `DeviceManager` 类，管理设备和请求队列
4. 使用堆实现优先级队列
5. 处理时按优先级取出请求，分配给相应设备

### 代码

```python
import heapq
import time
from dataclasses import dataclass, field

@dataclass(order=True)
class IORequest:
    """I/O请求类"""
    priority: int  # 堆优先级（越小越高）
    timestamp: float = field(compare=True)
    device_name: str = field(compare=False)
    operation: str = field(compare=False)
    data: str = field(compare=False)

class Device:
    """设备类"""
    def __init__(self, name, device_type, speed):
        self.name = name
        self.device_type = device_type
        self.speed = speed
        self.processed_count = 0
    
    def process(self, request):
        print(f"    [{self.name}] 正在处理: {request.operation}({request.data})")
        time.sleep(self.speed / 1000)
        self.processed_count += 1
        return f"{request.operation}完成"

class DeviceManager:
    """设备管理器"""
    def __init__(self):
        self.devices = {}
        self.request_queue = []
        self.completed_requests = []
        self.counter = 0
    
    def register_device(self, device):
        self.devices[device.name] = device
        print(f"✅ 注册设备: {device.name}")
    
    def submit_request(self, device_name, operation, data, priority=3):
        if device_name not in self.devices:
            print(f"❌ 错误: 未找到设备 '{device_name}'")
            return
        
        # 转换优先级（堆是最小堆，所以反转）
        heap_priority = 6 - priority
        
        request = IORequest(
            priority=heap_priority,
            timestamp=time.time() + self.counter * 0.0001,
            device_name=device_name,
            operation=operation,
            data=data
        )
        self.counter += 1
        
        heapq.heappush(self.request_queue, request)
        print(f"📨 提交请求: [{device_name}] {operation}('{data}') 优先级:{priority}")
    
    def process_all(self):
        print(f"\n🚀 开始处理 {len(self.request_queue)} 个请求...")
        print("-" * 60)
        
        while self.request_queue:
            request = heapq.heappop(self.request_queue)
            device = self.devices[request.device_name]
            actual_priority = 6 - request.priority
            
            print(f"\n  [优先级 {actual_priority}] [{request.device_name}] {request.operation}")
            result = device.process(request)
            
            self.completed_requests.append({
                'request': request,
                'result': result,
                'priority': actual_priority
            })
        
        print("-" * 60)
        print(f"✅ 所有请求处理完成！\n")
    
    def show_statistics(self):
        print("📊 设备统计:")
        for name, device in self.devices.items():
            print(f"  {device.name}: 处理了 {device.processed_count} 个请求")


# 使用示例
manager = DeviceManager()
manager.register_device(Device("键盘", "输入设备", 30))
manager.register_device(Device("硬盘", "存储设备", 100))

manager.submit_request("键盘", "读取输入", "紧急命令", priority=5)
manager.submit_request("硬盘", "读取文件", "普通文件", priority=2)

manager.process_all()
manager.show_statistics()
```

### 复杂度分析

- 提交请求时间复杂度: O(log n)，n是队列中请求数（堆插入）
- 处理请求时间复杂度: O(n log n)，需要取出所有请求
- 空间复杂度: O(n)，存储请求队列

</details>
