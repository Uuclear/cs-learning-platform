#include <stdio.h>

/**
 * 示例1：指针基础
 * 演示地址打印、解引用、NULL检查等基本指针操作
 */

int main() {
    // 基本变量声明
    int number = 42;
    char letter = 'A';
    double pi = 3.14159;

    // 指针声明和初始化
    int *int_ptr = &number;
    char *char_ptr = &letter;
    double *double_ptr = &pi;

    // 打印变量的值和地址
    printf("=== 变量信息 ===\n");
    printf("number: 值=%d, 地址=%p\n", number, &number);
    printf("letter: 值=%c, 地址=%p\n", letter, &letter);
    printf("pi: 值=%.5f, 地址=%p\n", pi, &pi);

    printf("\n=== 指针信息 ===\n");
    printf("int_ptr: 存储地址=%p, 解引用值=%d\n", int_ptr, *int_ptr);
    printf("char_ptr: 存储地址=%p, 解引用值=%c\n", char_ptr, *char_ptr);
    printf("double_ptr: 存储地址=%p, 解引用值=%.5f\n", double_ptr, *double_ptr);

    // NULL指针演示
    printf("\n=== NULL指针演示 ===\n");
    int *null_ptr = NULL;
    printf("null_ptr = %p\n", null_ptr);

    // 安全的NULL检查
    if (null_ptr != NULL) {
        printf("null_ptr的值: %d\n", *null_ptr);  // 这行不会执行
    } else {
        printf("null_ptr是空指针，不能解引用！\n");
    }

    // 修改通过指针的值
    printf("\n=== 通过指针修改值 ===\n");
    printf("修改前 number = %d\n", number);
    *int_ptr = 100;  // 通过指针修改number的值
    printf("修改后 number = %d\n", number);

    return 0;
}