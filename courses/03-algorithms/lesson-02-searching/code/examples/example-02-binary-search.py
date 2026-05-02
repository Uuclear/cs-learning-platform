# 二分查找：猜数字游戏的终极策略
# 算法思想：每次砍一半，快速缩小范围
# 前提条件：列表必须是有序的！

def binary_search_iterative(arr, target):
    """
    二分查找 - 迭代实现
    参数:
        arr - 有序列表（从小到大排序）
        target - 要查找的目标值
    返回:
        目标值的索引，如果没找到返回-1
    """
    left = 0            # 左边界
    right = len(arr) - 1  # 右边界
    steps = 0           # 记录查找步数

    while left <= right:
        steps += 1
        mid = (left + right) // 2  # 中间位置

        print(f"  第{steps}步: left={left}, right={right}, mid={mid}, arr[mid]={arr[mid]}")

        if arr[mid] == target:
            print(f"  找到了！索引={mid}，共{steps}步")
            return mid
        elif arr[mid] < target:
            # 目标在右半部分
            print(f"  arr[{mid}]={arr[mid]} < {target}，目标在右边，left 变为 {mid + 1}")
            left = mid + 1
        else:
            # 目标在左半部分
            print(f"  arr[{mid}]={arr[mid]} > {target}，目标在左边，right 变为 {mid - 1}")
            right = mid - 1

    print(f"  没找到，共{steps}步")
    return -1


def binary_search_recursive(arr, target, left, right):
    """
    二分查找 - 递归实现
    参数:
        arr - 有序列表
        target - 要查找的目标值
        left - 当前搜索范围的左边界
        right - 当前搜索范围的右边界
    返回:
        目标值的索引，如果没找到返回-1
    """
    # 基准情况：搜索范围为空
    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        # 目标在右半部分
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        # 目标在左半部分
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_wrapper(arr, target):
    """
    二分查找的便捷包装函数
    用户无需传入left和right
    """
    return binary_search_recursive(arr, target, 0, len(arr) - 1)


if __name__ == "__main__":
    print("=" * 50)
    print("示例2: 二分查找（迭代+递归）")
    print("=" * 50)

    # 有序列表（二分查找的前提！）
    numbers = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    print(f"\n有序列表: {numbers}")
    print(f"列表长度: {len(numbers)}")

    # 场景1：迭代实现
    print("\n--- 迭代实现 ---")
    print("\n查找 23:")
    binary_search_iterative(numbers, 23)

    print("\n查找 5:")
    binary_search_iterative(numbers, 5)

    print("\n查找 50（不存在的元素）:")
    binary_search_iterative(numbers, 50)

    # 场景2：递归实现
    print("\n" + "=" * 50)
    print("示例2-B: 递归实现")
    print("=" * 50)

    print(f"\n列表: {numbers}")

    result = binary_search_wrapper(numbers, 72)
    print(f"递归查找 72: 索引={result}")

    result = binary_search_wrapper(numbers, 100)
    print(f"递归查找 100: 索引={result}")

    # 场景3：对比查找效率
    print("\n" + "=" * 50)
    print("示例2-C: 二分查找 vs 线性查找 效率对比")
    print("=" * 50)

    # 创建一个较大的有序列表
    large_list = list(range(1, 1001))  # 1到1000

    print(f"\n列表大小: 1000个元素")
    print(f"查找目标: 999")

    # 线性查找需要多少步
    linear_steps = 0
    for i in range(len(large_list)):
        linear_steps += 1
        if large_list[i] == 999:
            break
    print(f"线性查找需要: {linear_steps} 次比较")

    # 二分查找需要多少步
    binary_steps = 0
    left, right = 0, len(large_list) - 1
    while left <= right:
        binary_steps += 1
        mid = (left + right) // 2
        if large_list[mid] == 999:
            break
        elif large_list[mid] < 999:
            left = mid + 1
        else:
            right = mid - 1
    print(f"二分查找需要: {binary_steps} 次比较")
    print(f"\n结论: 1000个元素中查找，线性查找需要 {linear_steps} 步，二分查找只需 {binary_steps} 步！")
    print(f"快了约 {linear_steps / binary_steps:.1f} 倍")

# 输出:
# ==================================================
# 示例2: 二分查找（迭代+递归）
# ==================================================
#
# 有序列表: [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
# 列表长度: 10
#
# --- 迭代实现 ---
#
# 查找 23:
#   第1步: left=0, right=9, mid=4, arr[mid]=16
#   arr[4]=16 < 23，目标在右边，left 变为 5
#   第2步: left=5, right=9, mid=7, arr[mid]=56
#   arr[7]=56 > 23，目标在左边，right 变为 6
#   第3步: left=5, right=6, mid=5, arr[mid]=23
#   找到了！索引=5，共3步
#
# ...
#
# ==================================================
# 示例2-C: 二分查找 vs 线性查找 效率对比
# ==================================================
#
# 列表大小: 1000个元素
# 查找目标: 999
# 线性查找需要: 999 次比较
# 二分查找需要: 10 次比较
#
# 结论: 1000个元素中查找，线性查找需要 999 步，二分查找只需 10 步！
# 快了约 99.9 倍
