# 解决方案3：考虑能源效率的边缘编排策略
import random
import math
from collections import defaultdict

class EnergyAwareEdgeNode:
    """支持能源感知的边缘节点"""

    def __init__(self, node_id, location, capacity, energy_efficiency=1.0):
        """
        初始化边缘节点

        :param node_id: 节点ID
        :param location: 位置坐标 (x, y)
        :param capacity: 计算容量
        :param energy_efficiency: 能源效率（越高越节能）
        """
        self.node_id = node_id
        self.location = location
        self.capacity = capacity
        self.energy_efficiency = energy_efficiency
        self.current_load = 0
        self.tasks = []
        self.total_energy_consumed = 0.0

    def get_utilization(self):
        """获取当前利用率"""
        return self.current_load / self.capacity if self.capacity > 0 else 1.0

    def can_accept_task(self, task_demand):
        """检查是否能接受新任务"""
        return self.current_load + task_demand <= self.capacity

    def assign_task(self, task_id, task_demand, user_location):
        """分配任务给节点（计算能耗）"""
        if self.can_accept_task(task_demand):
            self.current_load += task_demand

            # 计算能耗（基于负载和能源效率）
            energy_per_unit = 0.1 / self.energy_efficiency  # 基础能耗
            task_energy = task_demand * energy_per_unit
            self.total_energy_consumed += task_energy

            self.tasks.append({
                'task_id': task_id,
                'demand': task_demand,
                'user_location': user_location,
                'distance': self.calculate_distance(user_location),
                'energy_consumed': task_energy
            })
            return True
        return False

    def calculate_distance(self, other_location):
        """计算到用户位置的距离"""
        return math.sqrt((self.location[0] - other_location[0])**2 +
                        (self.location[1] - other_location[1])**2)

class EnergyAwareEdgeOrchestrator:
    """能源感知的边缘编排器"""

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        """添加边缘节点"""
        self.nodes.append(node)

    def find_best_node(self, task_demand, user_location, strategy="energy_aware"):
        """
        根据策略找到最佳节点

        :param task_demand: 任务需求
        :param user_location: 用户位置
        :param strategy: 策略 ("load_balancing", "proximity", "hybrid", "energy_aware")
        :return: 最佳节点
        """
        available_nodes = [node for node in self.nodes if node.can_accept_task(task_demand)]

        if not available_nodes:
            return None

        if strategy == "energy_aware":
            # 能源感知策略：在满足延迟要求的前提下最小化能耗
            latency_threshold = 10.0  # 最大可接受延迟（ms）

            # 过滤满足延迟要求的节点
            feasible_nodes = []
            for node in available_nodes:
                distance = node.calculate_distance(user_location)
                estimated_latency = distance * 0.1
                if estimated_latency <= latency_threshold:
                    feasible_nodes.append(node)

            if feasible_nodes:
                # 选择能耗最低的节点
                return min(feasible_nodes, key=lambda x: x.energy_efficiency)
            else:
                # 如果没有满足延迟要求的节点，退回到混合策略
                return self.find_best_node(task_demand, user_location, "hybrid")

        elif strategy == "hybrid":
            # 综合考虑负载、距离和能耗
            scores = []
            for node in available_nodes:
                load_score = node.get_utilization()
                distance_score = node.calculate_distance(user_location) / 100
                energy_score = 1.0 / node.energy_efficiency  # 能源效率越高，分数越低

                # 加权综合评分
                hybrid_score = 0.4 * load_score + 0.3 * distance_score + 0.3 * energy_score
                scores.append((hybrid_score, node))

            return min(scores, key=lambda x: x[0])[1]

        else:
            # 复用原始策略
            if strategy == "load_balancing":
                return min(available_nodes, key=lambda x: x.get_utilization())
            elif strategy == "proximity":
                return min(available_nodes, key=lambda x: x.calculate_distance(user_location))

    def distribute_tasks(self, tasks, strategy="energy_aware"):
        """
        分发任务到边缘节点

        :param tasks: 任务列表 [(task_id, demand, user_location), ...]
        :param strategy: 分发策略
        :return: 分发结果
        """
        results = []
        failed_tasks = []

        for task_id, demand, location in tasks:
            best_node = self.find_best_node(demand, location, strategy)

            if best_node and best_node.assign_task(task_id, demand, location):
                results.append({
                    'task_id': task_id,
                    'assigned_to': best_node.node_id,
                    'latency_estimate': best_node.calculate_distance(location) * 0.1,
                    'energy_estimate': demand * 0.1 / best_node.energy_efficiency
                })
            else:
                failed_tasks.append(task_id)

        return results, failed_tasks

def simulate_energy_aware_orchestration():
    """模拟能源感知的边缘编排"""
    # 创建具有不同能源效率的边缘节点
    orchestrator = EnergyAwareEdgeOrchestrator()
    node_locations = [(0, 0), (50, 0), (0, 50), (50, 50), (25, 25)]
    energy_efficiencies = [1.2, 0.8, 1.0, 1.5, 0.9]  # 不同节点的能源效率

    for i, (loc, eff) in enumerate(zip(node_locations, energy_efficiencies)):
        node = EnergyAwareEdgeNode(f"edge_node_{i+1}", loc, capacity=100, energy_efficiency=eff)
        orchestrator.add_node(node)

    # 生成随机任务
    random.seed(42)
    tasks = []
    for i in range(20):
        task_id = f"task_{i+1}"
        demand = random.randint(5, 25)
        location = (random.randint(0, 60), random.randint(0, 60))
        tasks.append((task_id, demand, location))

    # 测试不同策略
    strategies = ["load_balancing", "proximity", "hybrid", "energy_aware"]

    print("能源感知边缘编排模拟")
    print("=" * 80)

    for strategy in strategies:
        # 重置节点状态
        for node in orchestrator.nodes:
            node.current_load = 0
            node.tasks = []
            node.total_energy_consumed = 0.0

        results, failed = orchestrator.distribute_tasks(tasks, strategy)

        # 计算统计信息
        success_rate = len(results) / len(tasks) * 100
        avg_latency = sum(r['latency_estimate'] for r in results) / len(results) if results else 0
        total_energy = sum(node.total_energy_consumed for node in orchestrator.nodes)
        utilization = [node.get_utilization() for node in orchestrator.nodes]
        avg_utilization = sum(utilization) / len(utilization)

        print(f"\n策略: {strategy}")
        print(f"  成功率: {success_rate:.1f}%")
        print(f"  平均延迟估计: {avg_latency:.2f} ms")
        print(f"  总能耗: {total_energy:.2f} 单位")
        print(f"  平均节点利用率: {avg_utilization:.2f}")
        print(f"  失败任务数: {len(failed)}")

if __name__ == "__main__":
    simulate_energy_aware_orchestration()