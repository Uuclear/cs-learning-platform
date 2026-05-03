# 示例1：常见面试编码模式实现
from typing import List, Optional

def two_sum_sorted(arr: List[int], target: int) -> Optional[tuple]:
    """
    两数之和（已排序数组）- 双指针模式
    时间复杂度: O(n)
    空间复杂度: O(1)

    :param arr: 已排序的整数数组
    :param target: 目标和
    :return: 找到的两个数的索引元组，未找到返回None
    """
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1  # 和太小，移动左指针
        else:
            right -= 1  # 和太大，移动右指针

    return None

def max_subarray_sum(arr: List[int]) -> int:
    """
    最大子数组和 - 滑动窗口模式
    时间复杂度: O(n)
    空间复杂度: O(1)

    :param arr: 整数数组
    :return: 最大子数组和
    """
    if not arr:
        return 0

    max_sum = current_sum = arr[0]

    for i in range(1, len(arr)):
        # 要么扩展当前子数组，要么重新开始
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)

    return max_sum

def has_cycle(head) -> bool:
    """
    检测链表环 - 快慢指针模式
    时间复杂度: O(n)
    空间复杂度: O(1)

    :param head: 链表头节点
    :return: 是否存在环
    """
    if not head or not head.next:
        return False

    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True  # 快慢指针相遇，存在环

    return False

# 测试示例
if __name__ == "__main__":
    # 测试双指针
    sorted_arr = [2, 7, 11, 15]
    result = two_sum_sorted(sorted_arr, 9)
    print(f"双指针示例 - 数组 {sorted_arr}, 目标 9: {result}")

    # 测试滑动窗口
    arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    max_sum = max_subarray_sum(arr)
    print(f"滑动窗口示例 - 数组 {arr}: 最大子数组和 = {max_sum}")

    # 快慢指针需要链表实现，这里仅展示概念
    print("快慢指针示例: 用于检测链表中的环")