# 总线仲裁算法演示
# 当多个设备同时想使用总线时，谁先用？


class BusArbiter:
    """
    总线仲裁器
    决定哪个设备获得总线使用权
    """
    def __init__(self, algorithm="round_robin"):
        self.algorithm = algorithm    # 仲裁算法
        self.current_index = 0        # 轮询起始位置
        self.busy = False             # 总线是否被占用
        self.current_master = None    # 当前总线主人

    def grant_access(self, devices):
        """
        授予总线使用权
        支持三种算法：轮询、优先级、固定优先级
        """
        if self.busy:
            print(f"  总线正被 {self.current_master} 占用，等待...")
            return None

        if self.algorithm == "round_robin":
            return self._round_robin(devices)
        elif self.algorithm == "priority":
            return self._priority(devices)
        elif self.algorithm == "fixed_priority":
            return self._fixed_priority(devices)
        return None

    def _round_robin(self, devices):
        """轮询算法：公平轮转，一人一次"""
        if not devices:
            return None

        # 从当前位置开始找下一个请求者
        for i in range(len(devices)):
            idx = (self.current_index + i) % len(devices)
            if devices[idx]["requesting"]:
                self.current_index = (idx + 1) % len(devices)
                winner = devices[idx]
                self.busy = True
                self.current_master = winner["name"]
                return winner
        return None

    def _priority(self, devices):
        """动态优先级：高优先级先用，用完降优先级"""
        # 按优先级排序，选最高的请求者
        requesting = [d for d in devices if d["requesting"]]
        if not requesting:
            return None
        winner = max(requesting, key=lambda d: d["priority"])
        self.busy = True
        self.current_master = winner["name"]
        # 降低获胜者优先级（让其他设备也有机会）
        winner["priority"] = max(1, winner["priority"] - 1)
        return winner

    def _fixed_priority(self, devices):
        """固定优先级：CPU永远第一，依次递减"""
        for device in sorted(devices, key=lambda d: d["fixed_priority"], reverse=True):
            if device["requesting"]:
                self.busy = True
                self.current_master = device["name"]
                return device
        return None

    def release(self):
        """释放总线"""
        self.busy = False
        print(f"  {self.current_master} 释放了总线")
        self.current_master = None


def simulate_arbitration():
    """模拟总线仲裁过程"""
    print("=== 总线仲裁模拟 ===\n")

    # 定义三个设备
    devices = [
        {"name": "CPU",         "requesting": True,  "priority": 10, "fixed_priority": 3},
        {"name": "DMA控制器",    "requesting": True,  "priority": 7,  "fixed_priority": 2},
        {"name": "显卡GPU",     "requesting": True,  "priority": 5,  "fixed_priority": 1},
    ]

    # 场景1: 轮询算法
    print("场景1: 轮询仲裁（Round Robin）")
    print("-" * 40)
    arbiter = BusArbiter("round_robin")

    for round_num in range(1, 6):
        print(f"\n第 {round_num} 轮:")
        winner = arbiter.grant_access(devices)
        if winner:
            print(f"  {winner['name']} 获得总线使用权")
            arbiter.release()
            # 每轮每个设备都请求
            for d in devices:
                d["requesting"] = True

    # 场景2: 优先级算法
    print("\n\n场景2: 动态优先级仲裁")
    print("-" * 40)

    # 重置设备
    devices = [
        {"name": "CPU",         "requesting": True,  "priority": 10, "fixed_priority": 3},
        {"name": "DMA控制器",    "requesting": True,  "priority": 7,  "fixed_priority": 2},
        {"name": "显卡GPU",     "requesting": True,  "priority": 5,  "fixed_priority": 1},
    ]

    arbiter2 = BusArbiter("priority")

    for round_num in range(1, 6):
        print(f"\n第 {round_num} 轮 (优先级: CPU={devices[0]['priority']}, DMA={devices[1]['priority']}, GPU={devices[2]['priority']}):")
        winner = arbiter2.grant_access(devices)
        if winner:
            print(f"  {winner['name']} 获得总线使用权 (优先级: {winner['priority']+1})")
            arbiter2.release()

    # 场景3: 对比总结
    print("\n\n仲裁算法对比:")
    print("-" * 40)
    print("  算法          | 公平性 | 实时性 | 复杂度")
    print("  " + "-" * 35)
    print("  轮询          | 5星    | 3星    | 低")
    print("  动态优先级     | 4星    | 4星    | 中")
    print("  固定优先级     | 2星    | 5星    | 低")
    print("\n实际系统中，CPU通常有最高优先级，")
    print("但也会用超时机制防止其他设备饿死。")


if __name__ == "__main__":
    simulate_arbitration()
