# 分数背包问题 - 贪心算法经典示例
# 问题：你有一个容量有限的背包，有多个物品可以选择
# 与0-1背包不同，分数背包允许拿走物品的一部分（比如拿走一半的黄金）
# 目标：在不超过背包容量的前提下，最大化总价值

# 贪心策略：按"单位价值"（价值/重量）从高到低排序，优先拿单位价值最高的

class Item:
    """物品类"""
    def __init__(self, name, value, weight):
        self.name = name
        self.value = value       # 物品总价值
        self.weight = weight     # 物品总重量
        self.ratio = value / weight  # 单位价值（价值密度）

    def __repr__(self):
        return f"{self.name}(价值:{self.value}, 重量:{self.weight}, 单位价值:{self.ratio:.2f})"


def fractional_knapsack(items, capacity):
    """
    分数背包问题 - 贪心算法
    参数: items - 物品列表
          capacity - 背包容量
    返回: (总价值, 选择的物品及数量列表)
    """
    # 按单位价值从高到低排序
    items_sorted = sorted(items, key=lambda x: x.ratio, reverse=True)

    total_value = 0
    selected = []  # 记录选择了哪些物品，以及选择了多少
    remaining_capacity = capacity

    print("选择过程:")
    print("-" * 60)

    for item in items_sorted:
        if remaining_capacity <= 0:
            break

        # 能拿多少就拿多少
        if item.weight <= remaining_capacity:
            # 全部拿走
            take_weight = item.weight
            total_value += item.value
            remaining_capacity -= item.weight
            selected.append((item.name, take_weight, item.weight))  # (名称, 拿走重量, 总重量)
            print(f"  选择 {item.name}: 全部拿走 {take_weight}kg, 价值 {item.value}")
        else:
            # 只拿一部分（分数）
            take_weight = remaining_capacity
            take_value = item.ratio * take_weight
            total_value += take_value
            fraction = take_weight / item.weight
            selected.append((item.name, take_weight, item.weight))
            print(f"  选择 {item.name}: 拿走 {take_weight}kg ({fraction*100:.0f}%), 价值 {take_value:.1f}")
            remaining_capacity = 0

    print("-" * 60)
    return total_value, selected


if __name__ == "__main__":
    # 测试数据：黄金、白银、铜、铁、木头
    items = [
        Item("黄金", 60, 10),    # 单位价值: 6.0
        Item("白银", 100, 20),   # 单位价值: 5.0
        Item("铜",   120, 30),   # 单位价值: 4.0
        Item("铁",   50, 15),    # 单位价值: 3.33
        Item("木头", 10, 50),    # 单位价值: 0.2
    ]

    capacity = 50  # 背包容量50kg

    print("所有物品:")
    for item in items:
        print(f"  {item}")

    print(f"\n背包容量: {capacity}kg")
    print("=" * 60)

    total_value, selected = fractional_knapsack(items, capacity)

    print(f"\n最终结果:")
    print(f"  背包总价值: {total_value}")
    print(f"  选择的物品:")
    for name, taken, total in selected:
        if taken < total:
            print(f"    {name}: {taken}/{total}kg ({taken/total*100:.0f}%)")
        else:
            print(f"    {name}: 全部 {taken}kg")

# 输出:
# 所有物品:
#   黄金(价值:60, 重量:10, 单位价值:6.00)
#   白银(价值:100, 重量:20, 单位价值:5.00)
#   铜(价值:120, 重量:30, 单位价值:4.00)
#   铁(价值:50, 重量:15, 单位价值:3.33)
#   木头(价值:10, 重量:50, 单位价值:0.20)
#
# 背包容量: 50kg
# ============================================================
# 选择过程:
# ------------------------------------------------------------
#   选择 黄金: 全部拿走 10kg, 价值 60
#   选择 白银: 全部拿走 20kg, 价值 100
#   选择 铜: 拿走 20kg (67%), 价值 80.0
# ------------------------------------------------------------
#
# 最终结果:
#   背包总价值: 240.0
#   选择的物品:
#     黄金: 全部 10kg
#     白银: 全部 20kg
#     铜: 20/30kg (67%)
