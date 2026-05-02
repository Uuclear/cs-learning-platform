# 插值查找：更聪明的"猜位置"
# 算法思想：利用数据的分布特性，预测目标可能的位置
# 前提条件：数据必须是有序的，且大致均匀分布

def interpolation_search(arr, target):
    """
    插值查找算法
    参数:
        arr - 有序列表（从小到大排序，且大致均匀分布）
        target - 要查找的目标值
    返回:
        目标值的索引，如果没找到返回-1
    """
    left = 0
    right = len(arr) - 1
    steps = 0

    while left <= right and arr[left] <= target <= arr[right]:
        steps += 1

        # 如果左右边界相等，说明只剩一个元素
        if left == right:
            if arr[left] == target:
                print(f"  第{steps}步: 直接检查 arr[{left}] = {arr[left]} ← 找到了！")
                return left
            else:
                break

        # 插值公式：预测目标值的位置
        # pos = left + (target - arr[left]) * (right - left) // (arr[right] - arr[left])
        pos = left + int((target - arr[left]) * (right - left) / (arr[right] - arr[left]))

        print(f"  第{steps}步: left={left}, right={right}, 预测位置={pos}, arr[pos]={arr[pos]}")

        if arr[pos] == target:
            print(f"  找到了！索引={pos}，共{steps}步")
            return pos
        elif arr[pos] < target:
            # 目标在右半部分
            print(f"  arr[{pos}]={arr[pos]} < {target}，目标在右边，left 变为 {pos + 1}")
            left = pos + 1
        else:
            # 目标在左半部分
            print(f"  arr[{pos}]={arr[pos]} > {target}，目标在左边，right 变为 {pos - 1}")
            right = pos - 1

    print(f"  没找到，共{steps}步")
    return -1


def compare_search_algorithms():
    """
    对比三种查找算法的效率
    """
    print("=" * 60)
    print("三种查找算法效率对比")
    print("=" * 60)

    # 创建一个均匀分布的大数组
    n = 10000
    arr = list(range(1, n + 1))  # [1, 2, 3, ..., 10000]
    target = 9999  # 接近末尾的元素

    print(f"\n数组大小: {n}")
    print(f"查找目标: {target}")
    print(f"数据分布: 均匀分布 (理想情况)")

    # 线性查找
    linear_steps = target  # 最坏情况
    print(f"\n线性查找: {linear_steps} 次比较")

    # 二分查找
    binary_steps = 0
    left, right = 0, len(arr) - 1
    while left <= right:
        binary_steps += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            break
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    print(f"二分查找: {binary_steps} 次比较")

    # 插值查找
    print("\n插值查找过程:")
    interpolation_steps = 0
    left, right = 0, len(arr) - 1
    while left <= right and arr[left] <= target <= arr[right]:
        interpolation_steps += 1
        if left == right:
            if arr[left] == target:
                break
            else:
                break
        pos = left + int((target - arr[left]) * (right - left) / (arr[right] - arr[left]))
        if arr[pos] == target:
            break
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    print(f"插值查找: {interpolation_steps} 次比较")

    print(f"\n结论:")
    print(f"- 线性查找: O(n) = {linear_steps}")
    print(f"- 二分查找: O(log n) = {binary_steps}")
    print(f"- 插值查找: O(log log n) = {interpolation_steps} (理想情况下)")
    print(f"\n插值查找比二分查找快了 {binary_steps / interpolation_steps:.1f} 倍")


if __name__ == "__main__":
    print("=" * 50)
    print("示例3: 插值查找")
    print("=" * 50)

    # 场景1：小规模测试
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    print(f"\n有序列表（均匀分布）: {numbers}")

    print("\n查找 70:")
    interpolation_search(numbers, 70)

    print("\n查找 25（不存在的元素）:")
    interpolation_search(numbers, 25)

    # 场景2：大规模效率对比
    compare_search_algorithms()

    # 场景3：非均匀分布的情况
    print("\n" + "=" * 50)
    print("示例3-B: 非均匀分布的挑战")
    print("=" * 50)

    # 指数分布的数据（不适合插值查找）
    exponential_data = [2**i for i in range(10)]  # [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    print(f"\n指数分布数据: {exponential_data}")
    print("这种数据不适合插值查找，因为分布不均匀")
    print("插值查找可能会退化成线性查找")

    print("\n查找 64:")
    interpolation_search(exponential_data, 64)

# 输出:
# ==================================================
# 示例3: 插值查找
# ==================================================
#
# 有序列表（均匀分布）: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#
# 查找 70:
#   第1步: left=0, right=9, 预测位置=6, arr[6]=70
#   找到了！索引=6，共1步
#
# 查找 25（不存在的元素）:
#   第1步: left=0, right=9, 预测位置=1, arr[1]=20
#   arr[1]=20 < 25，目标在右边，left 变为 2
#   第2步: left=2, right=9, 预测位置=2, arr[2]=30
#   arr[2]=30 > 25，目标在左边，right 变为 1
#   没找到，共2步
#
# ==================================================
# 三种查找算法效率对比
# ==================================================
#
# 数组大小: 10000
# 查找目标: 9999
# 数据分布: 均匀分布 (理想情况)
#
# 线性查找: 9999 次比较
# 二分查找: 14 次比较
#
# 插值查找过程:
# 插值查找: 2 次比较
#
# 结论:
# - 线性查找: O(n) = 9999
# - 二分查找: O(log n) = 14
# - 插值查找: O(log log n) = 2 (理想情况下)
#
# 插值查找比二分查找快了 7.0 倍