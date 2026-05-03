# 示例3：边缘节点编排和负载均衡模拟
import random
import math
from collections import defaultdict

class EdgeNode:
    """边缘节点类"""

    def __init__(self, node_id, location, capacity):
        """
        初始化边缘节点

        :param node_id: 节点ID
        :param location: 位置坐标 (x, y)
        :param capacity: 计算容量
        """
        self.node_id = node_id
        self.location = location
        self.capacity = capacity
        self.current_load = 0
        self.tasks = []

    def get_utilization(self):
        """获取当前利用率"""
        return self.current_load / self.capacity if self.capacity > 0 else 1.0

    def can_accept_task(self, task_demand):
        """检查是否能接受新任务"""
        return self.current_load + task_demand <= self.capacity

    def assign_task(self, task_id, task_demand, user_location):
        """分配任务给节点"""
        if self.can_accept_task(task_demand):
            self.current_load += task_demand
            self.tasks.append({
                'task_id': task_id,
                'demand': task_demand,
                'user_location': user_location,
                'distance': self.calculate_distance(user_location)
            })
            return True
        return False

    def calculate_distance(self, other_location):
        """计算到用户位置的距离"""
        return math.sqrt((self.location[0] - other_location[0])**2 +
                        (self.location[1] - other_location[1])**2)

class EdgeOrchestrator:
    """边缘编排器"""

    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        """添加边缘节点"""
        self.nodes.append(node)

    def find_best_node(self, task_demand, user_location, strategy="load_balancing"):
        """
        根据策略找到最佳节点

        :param task_demand: 任务需求
        :param user_location: 用户位置
        :param strategy: 策略 ("load_balancing", "proximity", "hybrid")
        :return: 最佳节点
        """
        available_nodes = [node for node in self.nodes if node.can_accept_task(task_demand)]

        if not available_nodes:
            return None

        if strategy == "load_balancing":
            # 选择负载最低的节点
            return min(available_nodes, key=lambda x: x.get_utilization())

        elif strategy == "proximity":
            # 选择距离最近的节点
            return min(available_nodes, key=lambda x: x.calculate_distance(user_location))

        elif strategy == "hybrid":
            # 综合考虑负载和距离
            scores = []
            for node in available_nodes:
                load_score = node.get_utilization()
                distance_score = node.calculate_distance(user_location) / 100  # 归一化距离
                hybrid_score = 0.6 * load_score + 0.4 * distance_score
                scores.append((hybrid_score, node))

            return min(scores, key=lambda x: x[0])[1]

    def distribute_tasks(self, tasks, strategy="hybrid"):
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
                    'latency_estimate': best_node.calculate_distance(location) * 0.1
                })
            else:
                failed_tasks.append(task_id)

        return results, failed_tasks

def simulate_edge_orchestration():
    """模拟边缘编排场景"""
    # 创建边缘节点（模拟城市中的边缘服务器）
    orchestrator = EdgeOrchestrator()
    node_locations = [(0, 0), (50, 0), (0, 50), (50, 50), (25, 25)]

    for i, loc in enumerate(node_locations):
        node = EdgeNode(f"edge_node_{i+1}", loc, capacity=100)
        orchestrator.add_node(node)

    # 生成随机任务（模拟用户请求）
    random.seed(42)
    tasks = []
    for i in range(20):
        task_id = f"task_{i+1}"
        demand = random.randint(5, 25)
        location = (random.randint(0, 60), random.randint(0, 60))
        tasks.append((task_id, demand, location))

    # 使用不同策略分发任务
    strategies = ["load_balancing", "proximity", "hybrid"]

    print("边缘节点编排和负载均衡模拟")
    print("=" * 80)

    for strategy in strategies:
        # 重置节点状态
        for node in orchestrator.nodes:
            node.current_load = 0
            node.tasks = []

        results, failed = orchestrator.distribute_tasks(tasks, strategy)

        # 计算统计信息
        success_rate = len(results) / len(tasks) * 100
        avg_latency = sum(r['latency_estimate'] for r in results) / len(results) if results else 0
        utilization = [node.get_utilization() for node in orchestrator.nodes]
        avg_utilization = sum(utilization) / len(utilization)

        print(f"\n策略: {strategy}")
        print(f"  成功率: {success_rate:.1f}%")
        print(f"  平均延迟估计: {avg_latency:.2f} ms")
        print(f"  平均节点利用率: {avg_utilization:.2f}")
        print(f"  失败任务数: {len(failed)}")

if __name__ == "__main__":
    simulate_edge_orchestration()