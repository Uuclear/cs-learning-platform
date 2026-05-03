#include <stdio.h>
#include <limits.h>

int main() {
    // 打印各种基本数据类型的大小（以字节为单位）
    printf("=== C语言数据类型大小 ===\n");
    printf("char:        %zu 字节\n", sizeof(char));
    printf("short:       %zu 字节\n", sizeof(short));
    printf("int:         %zu 字节\n", sizeof(int));
    printf("long:        %zu 字节\n", sizeof(long));
    printf("long long:   %zu 字节\n", sizeof(long long));
    printf("float:       %zu 字节\n", sizeof(float));
    printf("double:      %zu 字节\n", sizeof(double));
    printf("long double: %zu 字节\n", sizeof(long double));

    // 演示有符号和无符号的区别
    printf("\n=== 有符号 vs 无符号范围 ===\n");
    printf("signed char 范围: %d 到 %d\n", SCHAR_MIN, SCHAR_MAX);
    printf("unsigned char 范围: 0 到 %u\n", UCHAR_MAX);
    printf("signed int 范围: %d 到 %d\n", INT_MIN, INT_MAX);
    printf("unsigned int 范围: 0 到 %u\n", UINT_MAX);

    // 额外：计算数组大小
    int arr[10];
    printf("\n=== 数组大小计算 ===\n");
    printf("单个int大小: %zu 字节\n", sizeof(int));
    printf("数组arr总大小: %zu 字节\n", sizeof(arr));
    printf("数组元素个数: %zu\n", sizeof(arr) / sizeof(arr[0]));

    return 0;
}