// example-03.c - 递归函数（阶乘、斐波那契）

#include <stdio.h>

// 阶乘函数 - 递归实现
long long factorial(int n) {
    // 基础情况：递归终止条件
    if (n <= 1) {
        return 1;
    }
    // 递归情况：函数调用自身
    return n * factorial(n - 1);
}

// 斐波那契数列 - 递归实现（注意：效率较低，仅用于演示）
int fibonacci(int n) {
    // 基础情况
    if (n <= 1) {
        return n;
    }
    // 递归情况
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 计算数字各位数之和 - 递归实现
int digit_sum(int n) {
    if (n == 0) {
        return 0;
    }
    return (n % 10) + digit_sum(n / 10);
}

// 打印数字的逆序 - 递归实现
void print_reverse(int n) {
    if (n == 0) {
        return;
    }
    printf("%d", n % 10);
    print_reverse(n / 10);
}

int main() {
    printf("=== 阶乘计算 ===\n");
    for (int i = 0; i <= 10; i++) {
        printf("%d! = %lld\n", i, factorial(i));
    }
    
    printf("\n=== 斐波那契数列 ===\n");
    for (int i = 0; i <= 10; i++) {
        printf("F(%d) = %d\n", i, fibonacci(i));
    }
    
    printf("\n=== 数字各位数之和 ===\n");
    int numbers[] = {123, 456, 789, 1000};
    int size = sizeof(numbers) / sizeof(numbers[0]);
    for (int i = 0; i < size; i++) {
        printf("Sum of digits in %d = %d\n", numbers[i], digit_sum(numbers[i]));
    }
    
    printf("\n=== 数字逆序打印 ===\n");
    for (int i = 0; i < size; i++) {
        printf("Reverse of %d = ", numbers[i]);
        print_reverse(numbers[i]);
        printf("\n");
    }
    
    return 0;
}
