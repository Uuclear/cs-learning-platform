# 示例2：快速排序 —— 分治思想的经典代表
# 核心思想：选一个基准，小的放左边，大的放右边，递归搞定

def quick_sort(arr):
    """
    快速排序（简洁版）
    核心：分治法 —— 选基准、分两边、递归排
    就像你当裁判：比我矮的站左边，比我高的站右边
    """
    # 基准情况：空列表或单元素列表已经有序
    if len(arr) <= 1:
        return arr

    # 选择基准（这里选中间元素）
    pivot = arr[len(arr) // 2]

    # 分成三部分：小于、等于、大于基准
    left = [x for x in arr if x < pivot]    # 左边：比基准小的
    middle = [x for x in arr if x == pivot] # 中间：等于基准的
    right = [x for x in arr if x > pivot]   # 右边：比基准大的

    # 递归排序左右两边，然后拼接
    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_verbose(arr, depth=0):
    """
    快速排序（详细版，带过程打印）
    方便理解递归过程
    """
    indent = "  " * depth
    if len(arr) <= 1:
        print(f"{indent}-> [{arr}] 已有序，直接返回")
        return arr

    pivot = arr[len(arr) // 2]
    print(f"{indent}选基准: {pivot}, 当前数组: {arr}")

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    print(f"{indent}  左边: {left} | 中间: {middle} | 右边: {right}")

    sorted_left = quick_sort_verbose(left, depth + 1)
    sorted_right = quick_sort_verbose(right, depth + 1)

    result = sorted_left + middle + sorted_right
    print(f"{indent}<-- 合并: {result}")
    return result


if __name__ == "__main__":
    print("=" * 50)
    print("【快速排序 —— 简洁版】")
    test_arr = [3, 6, 8, 10, 1, 2, 1]
    print(f"原始数组: {test_arr}")
    result = quick_sort(test_arr)
    print(f"排序结果: {result}")

    print("\n" + "=" * 50)
    print("【快速排序 —— 详细版（带递归过程）】")
    test_arr2 = [5, 2, 9, 1, 7, 3]
    print(f"原始数组: {test_arr2}")
    quick_sort_verbose(test_arr2)
    print(f"\n最终结果: {sorted(test_arr2)}")


# 输出:
# ==================================================
# 【快速排序 —— 简洁版】
# 原始数组: [3, 6, 8, 10, 1, 2, 1]
# 排序结果: [1, 1, 2, 3, 6, 8, 10]
#
# ==================================================
# 【快速排序 —— 详细版（带递归过程）】
# 原始数组: [5, 2, 9, 1, 7, 3]
# 选基准: 1, 当前数组: [5, 2, 9, 1, 7, 3]
#   左边: [] | 中间: [1] | 右边: [5, 2, 9, 7, 3]
#   -> [[]] 已有序，直接返回
#   选基准: 9, 当前数组: [5, 2, 9, 7, 3]
#     左边: [5, 2, 7, 3] | 中间: [9] | 右边: []
#     选基准: 7, 当前数组: [5, 2, 7, 3]
#       左边: [5, 2, 3] | 中间: [7] | 右边: []
#       选基准: 2, 当前数组: [5, 2, 3]
#         左边: [] | 中间: [2] | 右边: [5, 3]
#         -> [[]] 已有序，直接返回
#         -> [[2]] 已有序，直接返回
#         选基准: 3, 当前数组: [5, 3]
#           左边: [] | 中间: [3] | 右边: [5]
#           -> [[]] 已有序，直接返回
#           -> [[5]] 已有序，直接返回
#         <-- 合并: [3, 5]
#       <-- 合并: [2, 3, 5, 7]
#     <-- 合并: [2, 3, 5, 7, 9]
#   <-- 合并: [1, 2, 3, 5, 7, 9]
#
# 最终结果: [1, 2, 3, 5, 7, 9]
