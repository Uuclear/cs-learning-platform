#include <stdio.h>

/**
 * 示例3：指针作为函数参数（模拟传引用）
 * 演示如何通过指针在函数中修改调用者的变量
 */

// 交换两个整数的值
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 计算两个数的和与差，并通过指针返回结果
void calculate_sum_diff(int x, int y, int *sum, int *diff) {
    if (sum != NULL) {
        *sum = x + y;
    }
    if (diff != NULL) {
        *diff = x - y;
    }
}

// 安全地递增一个整数值
int safe_increment(int *value) {
    if (value == NULL) {
        return -1;  // 错误码：空指针
    }
    (*value)++;
    return 0;  // 成功
}

// 打印数组（只读，不修改）
void print_array(const int *arr, int size) {
    printf("数组内容: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);  // 可以使用数组下标语法
    }
    printf("\n");
}

// 修改数组元素
void modify_array(int *arr, int size, int multiplier) {
    for (int i = 0; i < size; i++) {
        arr[i] *= multiplier;  // 直接修改原数组
    }
}

int main() {
    printf("=== 交换函数演示 ===\n");
    int x = 5, y = 10;
    printf("交换前: x = %d, y = %d\n", x, y);
    swap(&x, &y);
    printf("交换后: x = %d, y = %d\n", x, y);

    printf("\n=== 多返回值演示 ===\n");
    int a = 15, b = 7;
    int sum_result, diff_result;
    calculate_sum_diff(a, b, &sum_result, &diff_result);
    printf("%d + %d = %d\n", a, b, sum_result);
    printf("%d - %d = %d\n", a, b, diff_result);

    // 也可以只获取其中一个结果
    int only_sum;
    calculate_sum_diff(a, b, &only_sum, NULL);
    printf("只计算和: %d + %d = %d\n", a, b, only_sum);

    printf("\n=== 安全递增演示 ===\n");
    int counter = 42;
    printf("计数器初始值: %d\n", counter);

    if (safe_increment(&counter) == 0) {
        printf("递增成功，新值: %d\n", counter);
    }

    // 测试空指针情况
    if (safe_increment(NULL) != 0) {
        printf("传递空指针时正确处理了错误！\n");
    }

    printf("\n=== 数组操作演示 ===\n");
    int data[] = {1, 2, 3, 4, 5};
    int data_size = sizeof(data) / sizeof(data[0]);

    printf("原始数组:\n");
    print_array(data, data_size);

    modify_array(data, data_size, 2);
    printf("乘以2后的数组:\n");
    print_array(data, data_size);

    return 0;
}