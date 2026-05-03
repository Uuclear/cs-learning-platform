#include <stdio.h>

int main() {
    // 演示运算符优先级
    printf("=== 运算符优先级演示 ===\n");
    int a = 5, b = 3, c = 2;

    // 乘法优先级高于加法
    int result1 = a + b * c;  // 5 + (3 * 2) = 11
    printf("a + b * c = %d\n", result1);

    // 使用括号改变优先级
    int result2 = (a + b) * c; // (5 + 3) * 2 = 16
    printf("(a + b) * c = %d\n", result2);

    // 演示类型转换
    printf("\n=== 类型转换演示 ===\n");
    int int_num = 10;
    float float_num = 3.5f;
    double double_num = 2.7;

    // 隐式类型转换（提升）
    double mixed_result = int_num + float_num + double_num;
    printf("混合类型计算: %d + %.1f + %.1f = %.2f\n",
           int_num, float_num, double_num, mixed_result);

    // 显式类型转换（强制转换）
    int truncated = (int)float_num;  // 截断小数部分
    printf("(int)%.1f = %d\n", float_num, truncated);

    // 整数除法 vs 浮点除法
    int dividend = 7, divisor = 3;
    int int_division = dividend / divisor;           // 整数除法，结果为2
    float float_division = (float)dividend / divisor; // 浮点除法，结果为2.333...

    printf("\n=== 除法演示 ===\n");
    printf("%d / %d = %d (整数除法)\n", dividend, divisor, int_division);
    printf("(float)%d / %d = %.3f (浮点除法)\n", dividend, divisor, float_division);

    return 0;
}