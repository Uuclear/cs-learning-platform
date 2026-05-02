# 二分查找的实际应用
# 展示二分查找在真实场景中的用法

import bisect


def find_first_occurrence(arr, target):
    """
    查找第一个出现的位置
    即使有重复元素，也返回最左边的那个
    """
    left = 0
    right = len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid     # 记录当前位置
            right = mid - 1  # 继续向左找，看有没有更早出现的
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def find_last_occurrence(arr, target):
    """
    查找最后一个出现的位置
    即使有重复元素，也返回最右边的那个
    """
    left = 0
    right = len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid     # 记录当前位置
            left = mid + 1   # 继续向右找，看有没有更晚出现的
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def search_insert_position(arr, target):
    """
    查找插入位置
    如果目标存在，返回其索引
    如果不存在，返回它应该插入的位置（保持有序）
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    # left就是应该插入的位置
    return left


def count_occurrences(arr, target):
    """
    统计目标值在有序数组中出现的次数
    利用find_first和find_last，O(log n)复杂度
    """
    first = find_first_occurrence(arr, target)
    if first == -1:
        return 0
    last = find_last_occurrence(arr, target)
    return last - first + 1


if __name__ == "__main__":
    print("=" * 50)
    print("示例3: 二分查找的实际应用")
    print("=" * 50)

    # 场景1：查找重复元素的第一个和最后一个位置
    print("\n--- 场景1：重复元素的边界查找 ---")
    numbers = [1, 2, 2, 2, 3, 4, 5, 5, 5, 5, 6]
    print(f"列表: {numbers}")

    print(f"\n查找第一个 2 的位置: {find_first_occurrence(numbers, 2)}")
    print(f"查找最后一个 2 的位置: {find_last_occurrence(numbers, 2)}")
    print(f"查找第一个 5 的位置: {find_first_occurrence(numbers, 5)}")
    print(f"查找最后一个 5 的位置: {find_last_occurrence(numbers, 5)}")
    print(f"查找第一个 7 的位置（不存在）: {find_first_occurrence(numbers, 7)}")

    # 场景2：插入位置
    print("\n" + "=" * 50)
    print("示例3-B: 插入位置查找")
    print("=" * 50)

    scores = [55, 60, 65, 70, 75, 80, 85, 90, 95]
    print(f"\n成绩列表（已排序）: {scores}")

    new_score = 73
    pos = search_insert_position(scores, new_score)
    print(f"新成绩 {new_score} 应该插入位置 {pos}")
    print(f"插入后: {scores[:pos]} + [{new_score}] + {scores[pos:]}")

    # 场景3：统计出现次数
    print("\n" + "=" * 50)
    print("示例3-C: 统计有序数组中元素出现次数")
    print("=" * 50)

    data = [1, 1, 2, 3, 3, 3, 3, 4, 5, 5, 5, 6, 6]
    print(f"数据: {data}")

    for target in [1, 3, 5, 7]:
        count = count_occurrences(data, target)
        print(f"数字 {target} 出现了 {count} 次")

    # 场景4：Python内置的bisect模块
    print("\n" + "=" * 50)
    print("示例3-D: 使用Python内置bisect模块")
    print("=" * 50)

    words = ["apple", "banana", "cherry", "date", "fig", "grape"]
    print(f"\n单词列表: {words}")

    # bisect_left 返回插入位置（左边）
    pos = bisect.bisect_left(words, "cherry")
    print(f"'cherry' 的位置: {pos}")

    pos = bisect.bisect_left(words, "elderberry")
    print(f"'elderberry' 的插入位置: {pos}")

    # 插入后保持有序
    bisect.insort(words, "elderberry")
    print(f"插入 'elderberry' 后: {words}")

# 输出:
# ==================================================
# 示例3: 二分查找的实际应用
# ==================================================
#
# --- 场景1：重复元素的边界查找 ---
# 列表: [1, 2, 2, 2, 3, 4, 5, 5, 5, 5, 6]
#
# 查找第一个 2 的位置: 1
# 查找最后一个 2 的位置: 3
# 查找第一个 5 的位置: 6
# 查找最后一个 5 的位置: 9
# 查找第一个 7 的位置（不存在）: -1
#
# ==================================================
# 示例3-B: 插入位置查找
# ==================================================
#
# 成绩列表（已排序）: [55, 60, 65, 70, 75, 80, 85, 90, 95]
# 新成绩 73 应该插入位置 3
# 插入后: [55, 60, 65] + [73] + [70, 75, 80, 85, 90, 95]
#
# ==================================================
# 示例3-C: 统计有序数组中元素出现次数
# ==================================================
# 数据: [1, 1, 2, 3, 3, 3, 3, 4, 5, 5, 5, 6, 6]
# 数字 1 出现了 2 次
# 数字 3 出现了 4 次
# 数字 5 出现了 3 次
# 数字 7 出现了 0 次
#
# ==================================================
# 示例3-D: 使用Python内置bisect模块
# ==================================================
#
# 单词列表: ['apple', 'banana', 'cherry', 'date', 'fig', 'grape']
# 'cherry' 的位置: 2
# 'elderberry' 的插入位置: 4
# 插入 'elderberry' 后: ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape']
