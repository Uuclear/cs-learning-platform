#include <stdio.h>

// 冒泡排序函数（优化版本）
void bubble_sort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // 交换元素
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = 1;
            }
        }
        // 如果没有发生交换，说明数组已经有序
        if (!swapped) break;
    }
}

// 二分查找函数（要求输入数组已排序）
int binary_search(int arr[], int n, int target) {
    int left = 0, right = n - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return -1; // 未找到
}

// 计算数组平均值
double calculate_average(int arr[], int n) {
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        sum += arr[i];
    }
    return (double)sum / n;
}

int main() {
    // 初始化数组
    int numbers[] = {64, 34, 25, 12, 22, 11, 90, 88, 76, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printf("原始数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // 找到最大值和最小值
    int max = numbers[0], min = numbers[0];
    for (int i = 1; i < size; i++) {
        if (numbers[i] > max) max = numbers[i];
        if (numbers[i] < min) min = numbers[i];
    }
    printf("最大值: %d\n", max);
    printf("最小值: %d\n", min);

    // 计算平均值
    double avg = calculate_average(numbers, size);
    printf("平均值: %.2f\n", avg);

    // 排序
    bubble_sort(numbers, size);
    printf("排序后数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // 二分查找示例
    int target = 25;
    int found_index = binary_search(numbers, size, target);
    if (found_index != -1) {
        printf("通过二分查找找到了 %d，位置在索引 %d\n", target, found_index);
    } else {
        printf("未找到 %d\n", target);
    }

    return 0;
}