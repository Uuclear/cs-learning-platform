# 示例3：归并排序 —— 分治法的另一种优雅实现
# 核心思想：先拆到最小单位，再两两合并排序
# 就像整理两堆已经排好序的扑克牌，从每堆顶部选小的

def merge_sort(arr):
    """
    归并排序
    核心：分而治之 —— 先拆后合，合的时候排序
    就像把一副乱牌分成两半，各自排好，再合并
    """
    # 基准情况：单个元素天然有序
    if len(arr) <= 1:
        return arr

    # 从中间切开
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # 递归排序左半边
    right = merge_sort(arr[mid:])  # 递归排序右半边

    # 合并两个已排序的数组
    return merge(left, right)


def merge(left, right):
    """
    合并两个已排序的数组
    核心：两个指针，谁小谁先走
    """
    result = []
    i = j = 0

    # 比较两个数组的当前元素，把小的放进去
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 把剩余元素直接追加（只剩一边没处理完）
    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort_verbose(arr, depth=0):
    """
    归并排序（详细版，带过程打印）
    """
    indent = "  " * depth
    if len(arr) <= 1:
        print(f"{indent}-> [{arr}] 单个元素，返回")
        return arr

    mid = len(arr) // 2
    print(f"{indent}拆分: {arr} -> 左{arr[:mid]} | 右{arr[mid:]}")

    left = merge_sort_verbose(arr[:mid], depth + 1)
    right = merge_sort_verbose(arr[mid:], depth + 1)

    result = merge(left, right)
    print(f"{indent}<-- 合并: {left} + {right} -> {result}")
    return result


if __name__ == "__main__":
    print("=" * 50)
    print("【归并排序 —— 简洁版】")
    test_arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"原始数组: {test_arr}")
    result = merge_sort(test_arr)
    print(f"排序结果: {result}")

    print("\n" + "=" * 50)
    print("【归并排序 —— 详细版（带拆分合并过程）】")
    test_arr2 = [5, 3, 8, 1]
    print(f"原始数组: {test_arr2}")
    merge_sort_verbose(test_arr2)
    print(f"\n最终结果: {sorted(test_arr2)}")


# 输出:
# ==================================================
# 【归并排序 —— 简洁版】
# 原始数组: [38, 27, 43, 3, 9, 82, 10]
# 排序结果: [3, 9, 10, 27, 38, 43, 82]
#
# ==================================================
# 【归并排序 —— 详细版（带拆分合并过程）】
# 原始数组: [5, 3, 8, 1]
# 拆分: [5, 3, 8, 1] -> 左[5, 3] | 右[8, 1]
#   拆分: [5, 3] -> 左[5] | 右[3]
#   -> [5] 单个元素，返回
#   -> [3] 单个元素，返回
#   <-- 合并: [5] + [3] -> [3, 5]
#   拆分: [8, 1] -> 左[8] | 右[1]
#   -> [8] 单个元素，返回
#   -> [1] 单个元素，返回
#   <-- 合并: [8] + [1] -> [1, 8]
# <-- 合并: [3, 5] + [1, 8] -> [1, 3, 5, 8]
#
# 最终结果: [1, 3, 5, 8]
