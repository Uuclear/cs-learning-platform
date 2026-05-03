// main.c - 主程序文件
#include <stdio.h>
#include "utils.h"

/**
 * 多文件C程序演示
 *
 * 这个例子展示了如何将程序分割成多个文件：
 * - main.c: 包含主函数和程序逻辑
 * - utils.h: 头文件，声明函数接口
 * - utils.c: 实现文件，包含函数的具体实现
 *
 * 编译命令：gcc main.c utils.c -o program
 */

int main() {
    printf("欢迎使用多文件C程序演示！\n");

    // 调用utils.h中声明的函数
    greet_user("学习者");
    int result = add_numbers(10, 20);
    printf("10 + 20 = %d\n", result);

    return 0;
}