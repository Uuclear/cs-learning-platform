// utils.c - 工具函数实现文件
#include "utils.h"

/**
 * 实现头文件中声明的函数
 */

// 打印欢迎信息
void greet_user(const char* name) {
    printf("你好，%s！欢迎学习C语言！\n", name);
}

// 计算两个整数的和
int add_numbers(int a, int b) {
    return a + b;
}