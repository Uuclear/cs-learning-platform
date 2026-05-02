# 练习2解答：实现二分查找（迭代+递归）

def binary_search_iterative(arr, target):
    """
    二分查找 - 迭代实现
    打印查找过程
    """
    left = 0
    right = len(arr) - 1
    steps = 0

    while left <= right:
        steps += 1
        mid = (left + right) // 2
        print(f"  步骤{steps}: left={left}, right={right}, mid={mid}, arr[mid]={arr[mid]}")

        if arr[mid] == target:
            print(f"  找到 {target}，索引={mid}")
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    print(f"  未找到 {target}")
    return -1


def binary_search_recursive(arr, target, left=None, right=None):
    """
    二分查找 - 递归实现
    """
    if left is None:
        left = 0
        right = len(arr) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


# 测试
if __name__ == "__main__":
    arr = [1, 3, 5, 7, 9, 11, 13, 15]
    print(f"有序数组: {arr}\n")

    # 迭代实现
    print("--- 迭代实现 ---")
    binary_search_iterative(arr, 11)

    # 递归实现
    print("\n--- 递归实现 ---")
    result = binary_search_recursive(arr, 7)
    print(f"递归查找7: 索引={result}")

    result = binary_search_recursive(arr, 4)
    print(f"递归查找4: 索引={result}")
