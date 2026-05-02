# 练习1解答：实现线性查找

def linear_search(arr, target):
    """
    线性查找
    返回目标值的索引，记录比较次数
    """
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            print(f"  找到目标 {target}，索引={i}，比较了 {comparisons} 次")
            return i
    print(f"  未找到目标 {target}，比较了 {comparisons} 次")
    return -1


# 测试
if __name__ == "__main__":
    arr = [34, 7, 23, 32, 5, 62]

    # 查找存在的元素
    linear_search(arr, 23)  # 输出: 2（比较了3次）

    # 查找不存在的元素
    linear_search(arr, 100)  # 输出: -1（比较了6次）

    # 查找第一个元素
    linear_search(arr, 34)  # 输出: 0（比较了1次）
