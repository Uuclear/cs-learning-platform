#include <stdio.h>

/**
 * 解决方案1：指针基础练习
 * 找到数组中的最大值和最小值，并通过指针参数返回
 */

void find_min_max(int *arr, int size, int *min, int *max) {
    // 基本错误检查
    if (arr == NULL || size <= 0 || min == NULL || max == NULL) {
        return;
    }

    // 初始化为第一个元素
    *min = *max = arr[0];

    // 遍历数组找到最小值和最大值
    for (int i = 1; i < size; i++) {
        if (arr[i] < *min) {
            *min = arr[i];
        }
        if (arr[i] > *max) {
            *max = arr[i];
        }
    }
}

int main() {
    int numbers[] = {64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    int min_val, max_val;

    printf("原始数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    find_min_max(numbers, size, &min_val, &max_val);

    printf("最小值: %d\n", min_val);
    printf("最大值: %d\n", max_val);

    return 0;
}