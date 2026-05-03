#include <stdio.h>

// 冒泡排序函数
void bubble_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // 交换元素
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

// 线性查找函数
int linear_search(int arr[], int n, int target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) {
            return i; // 返回找到的索引
        }
    }
    return -1; // 未找到
}

int main() {
    // 初始化数组
    int numbers[] = {64, 34, 25, 12, 22, 11, 90};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printf("原始数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // 查找示例
    int target = 25;
    int found_index = linear_search(numbers, size, target);
    if (found_index != -1) {
        printf("找到了 %d，位置在索引 %d\n", target, found_index);
    } else {
        printf("未找到 %d\n", target);
    }

    // 排序示例
    bubble_sort(numbers, size);
    printf("排序后数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    return 0;
}