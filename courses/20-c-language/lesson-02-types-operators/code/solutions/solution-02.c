#include <stdio.h>

int main() {
    // 验证运算符优先级
    printf("=== 运算符优先级验证 ===\n");

    // 表达式1: 5 + 3 * 2
    int expr1 = 5 + 3 * 2;  // 乘法优先，所以是 5 + 6 = 11
    printf("5 + 3 * 2 = %d\n", expr1);
    printf("解释: 乘法(*)优先级高于加法(+), 所以先计算 3*2=6, 再计算 5+6=11\n");

    // 表达式2: 10 - 4 / 2
    int expr2 = 10 - 4 / 2; // 除法优先，所以是 10 - 2 = 8
    printf("10 - 4 / 2 = %d\n", expr2);
    printf("解释: 除法(/)优先级高于减法(-), 所以先计算 4/2=2, 再计算 10-2=8\n");

    // 表达式3: (5 + 3) * 2
    int expr3 = (5 + 3) * 2; // 括号优先，所以是 8 * 2 = 16
    printf("(5 + 3) * 2 = %d\n", expr3);
    printf("解释: 括号()具有最高优先级, 所以先计算 5+3=8, 再计算 8*2=16\n");

    // 类型转换实验
    printf("\n=== 类型转换实验 ===\n");

    // 隐式类型转换示例
    int int_val = 100;
    float float_val = 3.14f;
    double result_implicit = int_val + float_val; // int被隐式转换为float，然后提升为double
    printf("隐式转换: %d + %.2f = %.2f\n", int_val, float_val, result_implicit);

    // 显式类型转换示例
    double double_val = 99.99;
    int result_explicit = (int)double_val; // 显式转换，截断小数部分
    printf("显式转换: (int)%.2f = %d\n", double_val, result_explicit);

    // 比较两种转换的结果差异
    float f1 = 10.0f / 3.0f;           // 浮点除法
    int i1 = 10 / 3;                   // 整数除法（截断）
    float f2 = (float)10 / 3;          // 显式转换后的浮点除法

    printf("\n=== 转换结果比较 ===\n");
    printf("10.0f / 3.0f = %.6f (浮点除法)\n", f1);
    printf("10 / 3 = %d (整数除法，截断)\n", i1);
    printf("(float)10 / 3 = %.6f (显式转换后浮点除法)\n", f2);

    return 0;
}