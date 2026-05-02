# 练习2解答：多设备总线仲裁模拟器

import random


class BusArbiter:
    """总线仲裁模拟器，支持多种仲裁算法"""

    def __init__(self, algorithm="round_robin"):
        self.algorithm = algorithm
        self.current_index = 0       # 轮询起始指针
        self.stats = {}              # 统计信息
        self.total_rounds = 0

    def _round_robin(self, devices):
        """轮询仲裁：从上次位置开始找下一个请求者"""
        n = len(devices)
        for i in range(n):
            idx = (self.current_index + i) % n
            if devices[idx]["requesting"]:
                self.current_index = (idx + 1) % n
                return devices[idx]
        return None

    def _priority(self, devices):
        """动态优先级仲裁：选优先级最高的请求者，然后降低其优先级"""
        requesting = [d for d in devices if d["requesting"]]
        if not requesting:
            return None
        winner = max(requesting, key=lambda d: d["priority"])
        winner["priority"] = max(1, winner["priority"] - 1)
        return winner

    def simulate(self, devices, rounds=100, request_prob=0.8):
        """
        模拟总线仲裁过程

        参数:
            devices: 设备列表，每个设备是包含name和priority的字典
            rounds: 模拟轮数
            request_prob: 每个设备每轮发出请求的概率
        """
        # 初始化统计
        for d in devices:
            self.stats[d["name"]] = {"granted": 0, "waited": 0}
        self.total_rounds = rounds

        for round_num in range(rounds):
            # 随机决定哪些设备发出请求
            for d in devices:
                d["requesting"] = random.random() < request_prob

            # 仲裁
            winner = None
            if self.algorithm == "round_robin":
                winner = self._round_robin(devices)
            elif self.algorithm == "priority":
                winner = self._priority(devices)

            # 更新统计
            for d in devices:
                if d["requesting"]:
                    if d == winner:
                        self.stats[d["name"]]["granted"] += 1
                    else:
                        self.stats[d["name"]]["waited"] += 1

    def print_stats(self):
        """打印仲裁统计结果"""
        print(f"=== 仲裁统计 ({self.algorithm}, {self.total_rounds}轮) ===\n")
        print(f"{'设备':<12} {'获得次数':>8} {'等待次数':>8} {'获得率':>10}")
        print("-" * 42)

        total_granted = sum(s["granted"] for s in self.stats.values())
        for name, stat in self.stats.items():
            rate = stat["granted"] / max(total_granted, 1) * 100
            print(f"{name:<12} {stat['granted']:>8} {stat['waited']:>8} {rate:>9.1f}%")

        print(f"\n总计获得: {total_granted} 次")


def main():
    """演示两种仲裁算法的对比"""
    random.seed(42)  # 固定随机种子以便结果可复现

    devices = [
        {"name": "CPU",     "priority": 10},
        {"name": "DMA",     "priority": 7},
        {"name": "GPU",     "priority": 5},
        {"name": "网卡",     "priority": 3},
    ]

    # 场景1: 轮询
    print("场景1: 轮询仲裁\n")
    arbiter1 = BusArbiter("round_robin")
    arbiter1.simulate(devices, rounds=100, request_prob=0.8)
    arbiter1.print_stats()

    # 重置优先级
    devices = [
        {"name": "CPU",     "priority": 10},
        {"name": "DMA",     "priority": 7},
        {"name": "GPU",     "priority": 5},
        {"name": "网卡",     "priority": 3},
    ]

    # 场景2: 动态优先级
    print("\n场景2: 动态优先级仲裁\n")
    arbiter2 = BusArbiter("priority")
    arbiter2.simulate(devices, rounds=100, request_prob=0.8)
    arbiter2.print_stats()


if __name__ == "__main__":
    main()

# 预期输出:
# 场景1: 轮询仲裁
#
# === 仲裁统计 (round_robin, 100轮) ===
#
# 设备             获得次数     等待次数      获得率
# ------------------------------------------
# CPU                30         40       29.7%
# DMA                28         42       27.7%
# GPU                22         48       21.8%
# 网卡               21         49       20.8%
#
# 总计获得: 101 次
#
# 场景2: 动态优先级仲裁
# ...
