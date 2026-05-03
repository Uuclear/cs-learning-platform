// example-01.c - 函数声明与定义分离（多文件结构演示）

// math_operations.h - 函数声明头文件
#ifndef MATH_OPERATIONS_H
#define MATH_OPERATIONS_H

// 函数声明
int add(int a, int b);
int subtract(int a, int b);
int multiply(int a, int b);
double divide(double a, double b);

#endif

// math_operations.c - 函数实现文件
#include "math_operations.h"
#include <stdio.h>

// 函数定义
int add(int a, int b) {
    return a + b;
}

int subtract(int a, int b) {
    return a - b;
}

int multiply(int a, int b) {
    return a * b;
}

double divide(double a, double b) {
    if (b == 0) {
        printf("Error: Division by zero!\n");
        return 0.0;
    }
    return a / b;
}

// main.c - 主程序文件
#include <stdio.h>
#include "math_operations.h"

int main() {
    int x = 10, y = 5;

    printf("Addition: %d + %d = %d\n", x, y, add(x, y));
    printf("Subtraction: %d - %d = %d\n", x, y, subtract(x, y));
    printf("Multiplication: %d * %d = %d\n", x, y, multiply(x, y));
    printf("Division: %.1f / %.1f = %.2f\n", (double)x, (double)y, divide((double)x, (double)y));

    return 0;
}
