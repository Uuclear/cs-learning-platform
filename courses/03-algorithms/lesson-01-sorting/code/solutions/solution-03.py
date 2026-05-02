# 解答3：合并两个已排序的数组
# 对应练习3：合并两个已排序的数组（归并排序的merge函数）

def merge_sorted_arrays(arr1, arr2):
    """
    合并两个已排序的数组
    参数: arr1, arr2 - 两个已排序的列表
    返回: 合并后的有序列表
    """
    result = []
    i = j = 0

    # 比较两个数组的当前元素，把小的放进去
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    # 把剩余元素直接追加
    result.extend(arr1[i:])
    result.extend(arr2[j:])

    return result


if __name__ == "__main__":
    a = [1, 3, 5, 7]
    b = [2, 4, 6, 8, 10]
    print(f"数组1: {a}")
    print(f"数组2: {b}")
    result = merge_sorted_arrays(a, b)
    print(f"合并结果: {result}")


# 输出:
# 数组1: [1, 3, 5, 7]
# 数组2: [2, 4, 6, 8, 10]
# 合并结果: [1, 2, 3, 4, 5, 6, 7, 8, 10]
