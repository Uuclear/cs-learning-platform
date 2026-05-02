# 挑战1: 总线带宽计算器

## 难度
⭐⭐

## 描述
编写一个交互式总线带宽计算器，支持多种总线类型的快速查询和自定义计算。

## 输入
- 用户可以选择预设总线类型，或手动输入频率和位宽
- 支持指定是否为DDR模式

## 输出
- 显示理论带宽（MB/s 和 Gbps）
- 显示传输一个指定大小文件所需的时间

## 示例

**示例 1:**
```
输入: DDR4-3200
输出:
  总线: DDR4-3200
  频率: 1600 MHz
  位宽: 64 位
  DDR: 是
  带宽: 25,600.00 MB/s (204.80 Gbps)
  传输1GB文件约需: 0.04 秒
```

**示例 2:**
```
输入: 频率=8000, 位宽=16, DDR=否
输出:
  带宽: 16,000.00 MB/s (128.00 Gbps)
  传输1GB文件约需: 0.06 秒
```

## 约束条件
- 预设总线类型至少包含5种（PCIe各版本、DDR、USB、SATA）
- 自定义输入时验证参数合法性（频率>0，位宽>0）

## 提示
- 用字典存储预设总线参数
- 带宽公式: 带宽 = 频率 × 位宽 / 8 × (2 if DDR else 1)
- 传输时间 = 文件大小 / 带宽

## 进阶思考
- 如何计算"实际"带宽而非"理论"带宽？（考虑编码开销，如8b/10b编码）
- 如果要考虑延迟而非只看带宽，应该如何建模？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
1. 定义预设总线参数表
2. 实现带宽计算函数
3. 计算传输时间

### 代码
```python
def calculate_bandwidth(freq_mhz, width_bits, ddr=False):
    """计算带宽"""
    multiplier = 2 if ddr else 1
    bandwidth_mbps = (freq_mhz * 1_000_000 * width_bits / 8 * multiplier) / 1_000_000
    bandwidth_gbps = bandwidth_mbps * 8 / 1000
    return bandwidth_mbps, bandwidth_gbps

PRESET_BUSES = {
    "DDR4-3200": (1600, 64, True),
    "DDR5-6000": (3000, 64, True),
    "PCIe 3.0 x16": (8000, 16, False),
    "PCIe 4.0 x16": (16000, 16, False),
    "PCIe 5.0 x16": (32000, 16, False),
    "USB 3.0": (5000, 1, False),
    "SATA 3.0": (6000, 1, False),
}

def print_bandwidth(name, freq, width, ddr, file_size_gb=1):
    mbps, gbps = calculate_bandwidth(freq, width, ddr)
    time_sec = (file_size_gb * 1000) / mbps
    print(f"  总线: {name}")
    print(f"  频率: {freq} MHz, 位宽: {width} 位, DDR: {'是' if ddr else '否'}")
    print(f"  带宽: {mbps:,.2f} MB/s ({gbps:.2f} Gbps)")
    print(f"  传输{file_size_gb}GB文件约需: {time_sec:.2f} 秒")

# 使用示例
for name, (freq, width, ddr) in PRESET_BUSES.items():
    print_bandwidth(name, freq, width, ddr)
    print()
```

### 复杂度分析
- 时间复杂度: O(1)，纯数学计算
- 空间复杂度: O(1)，常数空间

</details>

---

# 挑战2: 总线争用模拟器

## 难度
⭐⭐⭐

## 描述
模拟多个设备争抢共享总线的场景，分析不同仲裁算法下的性能差异。

## 输入
- 设备列表（名称、请求频率、数据大小）
- 仲裁算法选择（round_robin / priority / fixed_priority）
- 模拟时间（总周期数）

## 输出
- 每个设备的总线使用率（获得次数 / 总请求次数）
- 平均等待时间
- 总线空闲率
- 是否有设备"饿死"（长时间未获得总线）

## 示例
```
输入:
  设备: CPU(请求率90%), GPU(请求率70%), DMA(请求率50%), 网卡(请求率20%)
  算法: round_robin
  模拟: 200轮

输出:
  CPU:   获得45次/180请求 = 25.0%使用率, 平均等待2.1轮
  GPU:   获得42次/140请求 = 30.0%使用率, 平均等待1.8轮
  DMA:   得到35次/100请求 = 35.0%使用率, 平均等待1.2轮
  网卡:  获得33次/40请求  = 82.5%使用率, 平均等待0.3轮
  总线空闲率: 5.0%
  饿死设备: 无
```

## 约束条件
- 模拟至少100轮
- 需要支持至少3种仲裁算法
- "饿死"判定标准：连续超过50轮未获得总线但有请求

## 提示
- 用random.random() < request_rate来模拟设备是否发出请求
- 每个算法单独实现一个方法
- 维护每个设备的请求队列和等待计数器

## 进阶思考
- 如果设备有不同"紧急程度"（如实时音频 vs 后台下载），如何设计更智能的仲裁？
- 真实PCIe总线使用什么仲裁方式？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
1. 用随机数模拟设备请求行为
2. 分别实现三种仲裁策略
3. 统计每个设备的获得率、等待时间、饿死情况

### 代码
```python
import random

class BusContentionSimulator:
    def __init__(self, algorithm="round_robin"):
        self.algorithm = algorithm
        self.round_robin_idx = 0
        self.stats = {}

    def _grant_round_robin(self, devices):
        n = len(devices)
        for i in range(n):
            idx = (self.round_robin_idx + i) % n
            if devices[idx]["requesting"]:
                self.round_robin_idx = (idx + 1) % n
                return idx
        return -1

    def _grant_priority(self, devices):
        best = -1
        best_pri = -1
        for i, d in enumerate(devices):
            if d["requesting"] and d["priority"] > best_pri:
                best_pri = d["priority"]
                best = i
        return best

    def _grant_fixed(self, devices):
        for i, d in enumerate(devices):
            if d["requesting"]:
                return i
        return -1

    def simulate(self, devices, rounds=200):
        for name in devices:
            self.stats[name] = {"granted": 0, "requested": 0, "total_wait": 0,
                                 "starved": False, "consecutive_denied": 0}

        for _ in range(rounds):
            # 生成请求
            for d in devices:
                d["requesting"] = random.random() < d["rate"]
                if d["requesting"]:
                    self.stats[d["name"]]["requested"] += 1

            # 仲裁
            if self.algorithm == "round_robin":
                winner = self._grant_round_robin(devices)
            elif self.algorithm == "priority":
                winner = self._grant_priority(devices)
            else:
                winner = self._grant_fixed(devices)

            # 更新统计
            for i, d in enumerate(devices):
                if d["requesting"]:
                    if i == winner:
                        self.stats[d["name"]]["granted"] += 1
                        self.stats[d["name"]]["consecutive_denied"] = 0
                    else:
                        self.stats[d["name"]]["consecutive_denied"] += 1
                        if self.stats[d["name"]]["consecutive_denied"] > 50:
                            self.stats[d["name"]]["starved"] = True

    def print_results(self):
        print(f"仲裁算法: {self.algorithm}")
        for name, s in self.stats.items():
            rate = s["granted"] / max(s["requested"], 1) * 100
            starved = " (饿死!)" if s["starved"] else ""
            print(f"  {name}: {s['granted']}/{s['requested']} = {rate:.1f}%{starved}")
```

### 复杂度分析
- 时间复杂度: O(rounds × 设备数)，每轮遍历所有设备
- 空间复杂度: O(设备数)，统计信息

</details>

---

# 挑战3: 总线延迟与吞吐量建模

## 难度
⭐⭐⭐⭐

## 描述
建立一个简化的总线性能模型，分析不同负载下总线的延迟和吞吐量变化。

## 输入
- 总线参数：带宽（MB/s）、基础延迟（微秒）
- 负载参数：请求率（请求/秒）、每个请求的数据量（KB）
- 排队模型：M/M/1队列（简单排队论模型）

## 输出
- 不同负载下的平均延迟
- 不同负载下的实际吞吐量
- 绘制"负载-延迟"曲线（用字符图表示）
- 找出总线饱和点（利用率>90%时的负载）

## 示例
```
输入:
  总线带宽: 10000 MB/s
  基础延迟: 100 μs
  数据量: 每请求 64 KB

输出:
  负载(MB/s)    利用率    平均延迟(μs)    实际吞吐量(MB/s)
  -----------------------------------------------------
  1000          10%       111             1000
  3000          30%       143             3000
  5000          50%       200             5000
  7000          70%       333             7000
  9000          90%       1000            9000
  9500          95%       2000            9500
  9900          99%       10000           9900

  ⚠️ 总线饱和点: 约 9000 MB/s (利用率 90%)
```

## 约束条件
- 使用M/M/1排队论模型：平均延迟 = 基础延迟 / (1 - 利用率)
- 利用率 = 负载带宽 / 总线带宽
- 负载范围从10%到99%，步进5%

## 提示
- M/M/1模型公式：W = W0 / (1 - ρ)，其中W0是基础延迟，ρ是利用率
- 当ρ接近1时，延迟趋向无穷（这就是"堵车"的数学表达）
- 用字符画绘制延迟曲线会更直观

## 进阶思考
- 真实总线的延迟模型比M/M/1更复杂，还有哪些因素会影响？
- 为什么PCIe使用"信用制"（Credit-based）流量控制而非简单排队？

---

## 参考解答

<details>
<summary>点击查看解答（先自己尝试！）</summary>

### 思路
1. 根据M/M/1排队论模型计算不同负载下的延迟
2. 计算实际吞吐量
3. 用字符图绘制延迟曲线

### 代码
```python
def simulate_bus_performance(bandwidth_mbps, base_latency_us, data_kb_per_request=64):
    """模拟总线性能"""
    print("=== 总线延迟与吞吐量建模 ===\n")
    print(f"总线带宽: {bandwidth_mbps:,} MB/s")
    print(f"基础延迟: {base_latency_us} μs")
    print(f"每请求数据量: {data_kb_per_request} KB\n")

    print(f"{'负载(MB/s)':>12} {'利用率':>8} {'平均延迟(μs)':>14} {'吞吐量(MB/s)':>14}")
    print("-" * 54)

    max_delay = 0
    saturation_point = None

    for util_pct in range(10, 100, 5):
        util = util_pct / 100.0
        load = bandwidth_mbps * util

        # M/M/1模型: 延迟 = 基础延迟 / (1 - 利用率)
        if util < 1.0:
            avg_delay = base_latency_us / (1 - util)
        else:
            avg_delay = float('inf')

        throughput = load  # M/M/1模型中吞吐量=负载（稳定状态）

        if avg_delay < float('inf'):
            print(f"{load:>12,.0f} {util*100:>7.0f}% {avg_delay:>14,.0f} {throughput:>14,.0f}")
        else:
            print(f"{load:>12,.0f} {util*100:>7.0f} {'无穷大':>14} {throughput:>14,.0f}")

        if util_pct >= 90 and saturation_point is None:
            saturation_point = load
            print(f"\n  ⚠️ 总线饱和点: 约 {saturation_point:,.0f} MB/s (利用率 90%)")

    # 绘制字符延迟曲线
    print("\n延迟曲线:")
    for util_pct in range(10, 100, 10):
        util = util_pct / 100.0
        delay = base_latency_us / (1 - util)
        bar_len = min(int(delay / base_latency_us), 50)
        bar = "#" * bar_len
        print(f"  {util_pct:3d}%: {bar} ({delay:,.0f} μs)")

# 运行模拟
simulate_bus_performance(10000, 100)
```

### 复杂度分析
- 时间复杂度: O(n)，n为负载采样点数
- 空间复杂度: O(1)

</details>
