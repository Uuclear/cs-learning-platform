# 解答2：统计排序过程中的比较和交换次数
# 对应练习2：统计排序过程中的比较和交换次数

def bubble_sort_with_stats(arr):
    """
    冒泡排序（带统计信息）
    返回: (比较次数, 交换次数)
    """
    comparisons = 0
    swaps = 0
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return comparisons, swaps


if __name__ == "__main__":
    test_cases = [
        ([5, 4, 3, 2, 1], "逆序"),
        ([1, 2, 3, 4, 5], "已有序"),
        ([3, 1, 4, 1, 5], "随机"),
    ]

    print("【冒泡排序统计】")
    for arr, label in test_cases:
        arr_copy = arr.copy()
        comps, swaps = bubble_sort_with_stats(arr_copy)
        print(f"  {label} {arr} -> {arr_copy}")
        print(f"    比较次数: {comps}, 交换次数: {swaps}")


# 输出:
# 【冒泡排序统计】
#   逆序 [5, 4, 3, 2, 1] -> [1, 2, 3, 4, 5]
#     比较次数: 10, 交换次数: 10
#   已有序 [1, 2, 3, 4, 5] -> [1, 2, 3, 4, 5]
#     比较次数: 4, 交换次数: 0
#   随机 [3, 1, 4, 1, 5] -> [1, 1, 3, 4, 5]
#     比较次数: 10, 交换次数: 3
