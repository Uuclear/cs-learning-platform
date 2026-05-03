// solution-03.c - 递归函数的完整解决方案

#include <stdio.h>

// 阶乘函数（带错误检查）
long long safe_factorial(int n) {
    if (n < 0) {
        printf("Error: Factorial not defined for negative numbers!\n");
        return -1;
    }
    if (n <= 1) {
        return 1;
    }
    return n * safe_factorial(n - 1);
}

// 斐波那契数列（优化版本，避免重复计算）
// 使用辅助函数实现尾递归优化
int fibonacci_helper(int n, int a, int b) {
    if (n == 0) return a;
    if (n == 1) return b;
    return fibonacci_helper(n - 1, b, a + b);
}

int optimized_fibonacci(int n) {
    if (n < 0) {
        printf("Error: Fibonacci not defined for negative numbers!\n");
        return -1;
    }
    return fibonacci_helper(n, 0, 1);
}

// 最大公约数（GCD）- 欧几里得算法递归实现
int gcd(int a, int b) {
    if (b == 0) {
        return a;
    }
    return gcd(b, a % b);
}

// 二分查找递归实现
int binary_search(int arr[], int left, int right, int target) {
    if (left > right) {
        return -1; // 未找到
    }
    
    int mid = left + (right - left) / 2;
    
    if (arr[mid] == target) {
        return mid;
    }
    
    if (arr[mid] > target) {
        return binary_search(arr, left, mid - 1, target);
    }
    
    return binary_search(arr, mid + 1, right, target);
}

// 打印数组元素（递归）
void print_array_recursive(int arr[], int size, int index) {
    if (index >= size) {
        return;
    }
    printf("%d ", arr[index]);
    print_array_recursive(arr, size, index + 1);
}

int main() {
    printf("=== 递归函数综合演示 ===\n\n");
    
    // 阶乘演示
    printf("--- 安全阶乘函数 ---\n");
    int factorial_tests[] = {-1, 0, 1, 5, 10};
    int factorial_size = sizeof(factorial_tests) / sizeof(factorial_tests[0]);
    for (int i = 0; i < factorial_size; i++) {
        long long result = safe_factorial(factorial_tests[i]);
        if (result != -1) {
            printf("%d! = %lld\n", factorial_tests[i], result);
        }
    }
    
    printf("\n--- 优化斐波那契数列 ---\n");
    for (int i = 0; i <= 15; i++) {
        printf("F(%d) = %d\n", i, optimized_fibonacci(i));
    }
    
    printf("\n--- 最大公约数（GCD）---\n");
    int pairs[][2] = {{48, 18}, {100, 25}, {17, 13}, {1071, 462}};
    int pairs_size = sizeof(pairs) / sizeof(pairs[0]);
    for (int i = 0; i < pairs_size; i++) {
        int a = pairs[i][0], b = pairs[i][1];
        printf("GCD(%d, %d) = %d\n", a, b, gcd(a, b));
    }
    
    printf("\n--- 二分查找 ---\n");
    int sorted_array[] = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19};
    int array_size = sizeof(sorted_array) / sizeof(sorted_array[0]);
    printf("Array: ");
    print_array_recursive(sorted_array, array_size, 0);
    printf("\n");
    
    int targets[] = {1, 7, 15, 20};
    int targets_size = sizeof(targets) / sizeof(targets[0]);
    for (int i = 0; i < targets_size; i++) {
        int index = binary_search(sorted_array, 0, array_size - 1, targets[i]);
        if (index != -1) {
            printf("Found %d at index %d\n", targets[i], index);
        } else {
            printf("%d not found in array\n", targets[i]);
        }
    }
    
    return 0;
}
