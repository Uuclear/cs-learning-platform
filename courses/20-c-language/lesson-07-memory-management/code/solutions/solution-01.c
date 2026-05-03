#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 解决方案1: malloc/free 正确使用示例

int main() {
    printf("=== C语言内存管理解决方案1: 正确的malloc/free使用 ===\n\n");

    // 1. 始终检查malloc返回值
    printf("1. 安全的malloc使用:\n");
    int* ptr1 = (int*)malloc(sizeof(int));
    if (ptr1 == NULL) {
        fprintf(stderr, "内存分配失败!\n");
        return 1;
    }
    *ptr1 = 42;
    printf("分配的值: %d\n", *ptr1);
    free(ptr1);
    ptr1 = NULL; // 避免悬空指针
    printf("内存已安全释放\n\n");

    // 2. calloc的正确使用（自动初始化）
    printf("2. calloc使用（自动初始化为0）:\n");
    int* arr = (int*)calloc(5, sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "calloc分配失败!\n");
        return 1;
    }

    printf("calloc数组内容: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", arr[i]); // 全部为0
    }
    printf("\n");
    free(arr);
    arr = NULL;
    printf("calloc内存已释放\n\n");

    // 3. realloc的安全使用
    printf("3. 安全的realloc使用:\n");
    int* dynamic_arr = (int*)malloc(3 * sizeof(int));
    if (dynamic_arr == NULL) {
        fprintf(stderr, "初始分配失败!\n");
        return 1;
    }

    // 初始化
    for (int i = 0; i < 3; i++) {
        dynamic_arr[i] = i + 1;
    }

    printf("原始数组: ");
    for (int i = 0; i < 3; i++) {
        printf("%d ", dynamic_arr[i]);
    }
    printf("\n");

    // 安全的realloc - 使用临时指针
    int* temp = (int*)realloc(dynamic_arr, 6 * sizeof(int));
    if (temp == NULL) {
        fprintf(stderr, "realloc失败!\n");
        free(dynamic_arr); // 释放原来的内存
        return 1;
    }
    dynamic_arr = temp;

    // 初始化新增的元素
    for (int i = 3; i < 6; i++) {
        dynamic_arr[i] = i + 1;
    }

    printf("扩容后数组: ");
    for (int i = 0; i < 6; i++) {
        printf("%d ", dynamic_arr[i]);
    }
    printf("\n");

    free(dynamic_arr);
    dynamic_arr = NULL;
    printf("realloc内存已释放\n\n");

    // 4. 字符串处理的正确方式
    printf("4. 字符串动态分配:\n");
    const char* source = "Hello, Dynamic Memory!";
    size_t len = strlen(source) + 1; // +1 for null terminator

    char* str_copy = (char*)malloc(len);
    if (str_copy == NULL) {
        fprintf(stderr, "字符串分配失败!\n");
        return 1;
    }

    strcpy(str_copy, source);
    printf("复制的字符串: %s\n", str_copy);

    free(str_copy);
    str_copy = NULL;
    printf("字符串内存已释放\n\n");

    // 5. 多级指针的正确管理
    printf("5. 二维数组的正确分配和释放:\n");
    int rows = 3, cols = 4;

    // 分配行指针数组
    int** matrix = (int**)malloc(rows * sizeof(int*));
    if (matrix == NULL) {
        fprintf(stderr, "行指针分配失败!\n");
        return 1;
    }

    // 分配每行的数据
    int allocation_failed = 0;
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
        if (matrix[i] == NULL) {
            fprintf(stderr, "第%d行分配失败!\n", i);
            allocation_failed = 1;
            break;
        }
        // 初始化数据
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = i * cols + j;
        }
    }

    if (allocation_failed) {
        // 清理已分配的内存
        for (int i = 0; i < rows && matrix[i] != NULL; i++) {
            free(matrix[i]);
        }
        free(matrix);
        return 1;
    }

    // 打印矩阵
    printf("二维数组内容:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }

    // 正确释放二维数组
    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
    printf("二维数组内存已正确释放\n\n");

    printf("=== 解决方案1结束 - 所有内存都已正确管理! ===\n");
    return 0;
}