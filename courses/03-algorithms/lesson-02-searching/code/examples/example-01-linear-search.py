# 线性查找：大海捞针的朴素方法
# 算法思想：从头开始，一个一个找，找到了就停下

def linear_search(arr, target):
    """
    线性查找算法
    参数:
        arr - 待查找的列表
        target - 要查找的目标值
    返回:
        目标值的索引，如果没找到返回-1
    """
    comparisons = 0  # 记录比较次数

    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            print(f"  找到了！在索引 {i}，比较了 {comparisons} 次")
            return i

    print(f"  没找到目标值，比较了 {comparisons} 次")
    return -1


def linear_search_with_trace(arr, target):
    """
    带追踪的线性查找
    展示查找过程，帮助理解算法
    """
    print(f"  在列表中查找 {target}...")
    print(f"  列表: {arr}")

    for i in range(len(arr)):
        # 可视化查找过程
        indicator = " " * (i * 5) + "^ 当前"
        if i == 0:
            indicator = " " + "^ 当前"

        if arr[i] == target:
            print(f"  步骤 {i+1}: 检查 arr[{i}] = {arr[i]} ← 找到了！")
            return i
        else:
            print(f"  步骤 {i+1}: 检查 arr[{i}] = {arr[i]} ← 不是，继续")

    print(f"  列表中不存在 {target}")
    return -1


def linear_search_all(arr, target):
    """
    查找所有匹配的位置
    返回列表中所有等于目标值的索引
    """
    positions = []
    for i in range(len(arr)):
        if arr[i] == target:
            positions.append(i)
    return positions


if __name__ == "__main__":
    print("=" * 50)
    print("示例1: 线性查找基础")
    print("=" * 50)

    # 场景1：查找存在的元素
    numbers = [3, 7, 1, 9, 5, 2, 8, 4]
    print(f"\n列表: {numbers}")

    print("\n查找 5:")
    linear_search(numbers, 5)

    print("\n查找 1:")
    linear_search(numbers, 1)

    print("\n查找 10（不存在的元素）:")
    linear_search(numbers, 10)

    # 场景2：查找过程的可视化追踪
    print("\n" + "=" * 50)
    print("示例1-B: 查找过程追踪")
    print("=" * 50)

    small_list = [7, 2, 9, 4, 6]
    print(f"\n列表: {small_list}")

    print("\n查找 9:")
    linear_search_with_trace(small_list, 9)

    # 场景3：查找所有匹配项
    print("\n" + "=" * 50)
    print("示例1-C: 查找所有匹配项")
    print("=" * 50)

    duplicates = ["苹果", "香蕉", "苹果", "橙子", "苹果", "葡萄"]
    print(f"\n水果列表: {duplicates}")
    positions = linear_search_all(duplicates, "苹果")
    print(f"'苹果'出现在位置: {positions}")

    # 场景4：最好、最坏、平均情况分析
    print("\n" + "=" * 50)
    print("示例1-D: 最好/最坏/平均情况分析")
    print("=" * 50)

    test_list = [50, 23, 77, 12, 88, 44, 66, 33, 99, 11]

    print("\n最好情况（目标在第一个）:")
    linear_search(test_list, 50)  # 1次比较

    print("\n最坏情况（目标在最后或不存在）:")
    linear_search(test_list, 11)  # 10次比较
    linear_search(test_list, 100)  # 10次比较，没找到

# 输出:
# ==================================================
# 示例1: 线性查找基础
# ==================================================
#
# 列表: [3, 7, 1, 9, 5, 2, 8, 4]
#
# 查找 5:
#   找到了！在索引 4，比较了 5 次
#
# 查找 1:
#   找到了！在索引 2，比较了 3 次
#
# 查找 10（不存在的元素）:
#   没找到目标值，比较了 8 次
#
# ==================================================
# 示例1-B: 查找过程追踪
# ==================================================
#
# 列表: [7, 2, 9, 4, 6]
#
# 查找 9:
#   步骤 1: 检查 arr[0] = 7 ← 不是，继续
#   步骤 2: 检查 arr[1] = 2 ← 不是，继续
#   步骤 3: 检查 arr[2] = 9 ← 找到了！
#
# ==================================================
# 示例1-C: 查找所有匹配项
# ==================================================
#
# 水果列表: ['苹果', '香蕉', '苹果', '橙子', '苹果', '葡萄']
# '苹果'出现在位置: [0, 2, 4]
#
# ==================================================
# 示例1-D: 最好/最坏/平均情况分析
# ==================================================
#
# 最好情况（目标在第一个）:
#   找到了！在索引 0，比较了 1 次
#
# 最坏情况（目标在最后或不存在）:
#   找到了！在索引 9，比较了 10 次
#   没找到目标值，比较了 10 次
