#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 示例3: 内存泄漏演示与Valgrind分析指南

// 函数1: 简单的内存泄漏
void simple_memory_leak() {
    printf("函数simple_memory_leak: 分配内存但不释放\n");
    int* ptr = (int*)malloc(sizeof(int));
    *ptr = 42;
    // 故意不调用free - 这就是内存泄漏!
}

// 函数2: 隐蔽的内存泄漏（丢失指针）
void hidden_memory_leak() {
    printf("函数hidden_memory_leak: 丢失指针导致的内存泄漏\n");
    int* ptr1 = (int*)malloc(sizeof(int));
    int* ptr2 = (int*)malloc(sizeof(int));

    *ptr1 = 100;
    *ptr2 = 200;

    ptr1 = ptr2; // ptr1原来的地址丢失了！
    // 只能释放ptr2指向的内存，ptr1原来指向的内存无法释放
    free(ptr1); // 这实际上释放的是ptr2的内存
    // ptr1原来指向的内存泄漏了！
}

// 函数3: 条件分支中的内存泄漏
void conditional_memory_leak(int condition) {
    printf("函数conditional_memory_leak: 条件分支中的内存泄漏\n");
    int* ptr = (int*)malloc(sizeof(int));
    *ptr = 300;

    if (condition) {
        // 在某些条件下忘记释放内存
        printf("条件为真，不释放内存\n");
        return; // 直接返回，内存泄漏！
    }

    free(ptr);
    printf("条件为假，正确释放内存\n");
}

// 函数4: 数组内存泄漏
void array_memory_leak() {
    printf("函数array_memory_leak: 数组相关的内存泄漏\n");
    int** matrix = (int**)malloc(3 * sizeof(int*));

    for (int i = 0; i < 3; i++) {
        matrix[i] = (int*)malloc(3 * sizeof(int));
        for (int j = 0; j < 3; j++) {
            matrix[i][j] = i * j;
        }
    }

    // 只释放了第一行，其他行泄漏！
    free(matrix[0]);
    free(matrix); // 释放指针数组，但matrix[1]和matrix[2]仍然泄漏
    printf("只部分释放了二维数组内存\n");
}

// 函数5: 正确的内存管理示例（用于对比）
void correct_memory_management() {
    printf("函数correct_memory_management: 正确的内存管理\n");
    int* ptr = (int*)malloc(sizeof(int));
    if (ptr == NULL) {
        printf("内存分配失败\n");
        return;
    }

    *ptr = 500;
    printf("值: %d\n", *ptr);
    free(ptr);
    ptr = NULL; // 良好习惯
    printf("内存已正确释放\n");
}

// 函数6: realloc相关的内存泄漏
void realloc_memory_leak() {
    printf("函数realloc_memory_leak: realloc相关的内存泄漏\n");
    int* ptr = (int*)malloc(5 * sizeof(int));
    for (int i = 0; i < 5; i++) {
        ptr[i] = i + 1;
    }

    // 错误的realloc使用方式
    ptr = (int*)realloc(ptr, 10 * sizeof(int));
    // 如果realloc失败，ptr变成NULL，原来的内存就丢失了！
    // 正确的方式应该是：
    // int* new_ptr = (int*)realloc(ptr, 10 * sizeof(int));
    // if (new_ptr == NULL) { /* 处理错误 */ }
    // else { ptr = new_ptr; }

    if (ptr != NULL) {
        // 假设realloc成功
        for (int i = 5; i < 10; i++) {
            ptr[i] = i + 1;
        }
        free(ptr);
    }
    // 如果realloc失败，这里会有内存泄漏！
}

int main() {
    printf("=== C语言内存管理示例3: 内存泄漏演示 ===\n\n");
    printf("编译此程序后，请使用以下命令运行Valgrind进行分析:\n");
    printf("gcc -g -o example-03 example-03.c\n");
    printf("valgrind --leak-check=full --show-leak-kinds=all ./example-03\n\n");

    // 演示各种内存泄漏情况
    simple_memory_leak();
    printf("\n");

    hidden_memory_leak();
    printf("\n");

    conditional_memory_leak(1); // 触发内存泄漏
    printf("\n");

    array_memory_leak();
    printf("\n");

    correct_memory_management();
    printf("\n");

    realloc_memory_leak();
    printf("\n");

    printf("=== Valgrind分析指南 ===\n");
    printf("Valgrind输出中关键信息解释:\n");
    printf("- definitely lost: 肯定的内存泄漏（最严重）\n");
    printf("- indirectly lost: 间接泄漏（通过其他泄漏的指针引用）\n");
    printf("- possibly lost: 可能的泄漏\n");
    printf("- still reachable: 程序结束时仍可访问的内存\n");
    printf("- suppressed: 被抑制的报告（通常是系统库的问题）\n\n");

    printf("修复内存泄漏的步骤:\n");
    printf("1. 编译时加上-g选项以包含调试信息\n");
    printf("2. 使用Valgrind运行程序\n");
    printf("3. 根据Valgrind报告定位泄漏位置\n");
    printf("4. 确保每个malloc/calloc/realloc都有对应的free\n");
    printf("5. 注意错误处理路径中的内存释放\n");
    printf("6. 对于复杂数据结构，确保递归释放所有节点\n\n");

    printf("=== 示例3结束 ===\n");
    return 0;
}