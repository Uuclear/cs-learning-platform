// solution-01.c - 函数声明与定义分离的完整解决方案

// calculator.h
#ifndef CALCULATOR_H
#define CALCULATOR_H

// 函数声明
double add(double a, double b);
double subtract(double a, double b);
double multiply(double a, double b);
double divide(double a, double b);
int power(int base, int exponent);
double square_root(double x);

#endif

// calculator.c
#include "calculator.h"
#include <stdio.h>
#include <math.h>

double add(double a, double b) {
    return a + b;
}

double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double divide(double a, double b) {
    if (b == 0.0) {
        fprintf(stderr, "Error: Division by zero!\n");
        return 0.0;
    }
    return a / b;
}

int power(int base, int exponent) {
    if (exponent == 0) return 1;
    if (exponent < 0) return 0; // 简化处理，不支持负指数
    
    int result = 1;
    for (int i = 0; i < exponent; i++) {
        result *= base;
    }
    return result;
}

double square_root(double x) {
    if (x < 0) {
        fprintf(stderr, "Error: Cannot calculate square root of negative number!\n");
        return 0.0;
    }
    return sqrt(x);
}

// main.c
#include <stdio.h>
#include "calculator.h"

int main() {
    double a = 15.5, b = 4.2;
    
    printf("=== Advanced Calculator Demo ===\n");
    printf("%.1f + %.1f = %.2f\n", a, b, add(a, b));
    printf("%.1f - %.1f = %.2f\n", a, b, subtract(a, b));
    printf("%.1f * %.1f = %.2f\n", a, b, multiply(a, b));
    printf("%.1f / %.1f = %.2f\n", a, b, divide(a, b));
    
    int base = 3, exp = 4;
    printf("%d^%d = %d\n", base, exp, power(base, exp));
    
    double num = 25.0;
    printf("√%.1f = %.2f\n", num, square_root(num));
    
    return 0;
}
