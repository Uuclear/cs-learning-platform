#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 解决方案3: 修复内存泄漏的正确实现

// 函数1: 修复简单的内存泄漏
void fixed_simple_memory_leak() {
    printf("函数fixed_simple_memory_leak: 正确释放内存\n");
    int* ptr = (int*)malloc(sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "内存分配失败!\n");
        return;
    }
    *ptr = 42;
    // 正确释放
    free(ptr);
    ptr = NULL;
    printf("内存已正确释放\n");
}

// 函数2: 修复隐蔽的内存泄漏
void fixed_hidden_memory_leak() {
    printf("函数fixed_hidden_memory_leak: 避免指针丢失\n");
    int* ptr1 = (int*)malloc(sizeof(int));
    int* ptr2 = (int*)malloc(sizeof(int));

    if (ptr1 == NULL || ptr2 == NULL) {
        // 错误处理：确保释放已分配的内存
        if (ptr1 != NULL) free(ptr1);
        if (ptr2 != NULL) free(ptr2);
        fprintf(stderr, "内存分配失败!\n");
        return;
    }

    *ptr1 = 100;
    *ptr2 = 200;

    // 不要让ptr1丢失原来的地址
    // 如果需要交换，先保存或直接使用ptr2
    printf("ptr1=%d, ptr2=%d\n", *ptr1, *ptr2);

    // 正确释放两个指针
    free(ptr1);
    free(ptr2);
    ptr1 = NULL;
    ptr2 = NULL;
    printf("两个内存块都已正确释放\n");
}

// 函数3: 修复条件分支中的内存泄漏
void fixed_conditional_memory_leak(int condition) {
    printf("函数fixed_conditional_memory_leak: 所有路径都释放内存\n");
    int* ptr = (int*)malloc(sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "内存分配失败!\n");
        return;
    }

    *ptr = 300;

    if (condition) {
        printf("条件为真\n");
        // 即使在条件分支中也要释放内存
        free(ptr);
        ptr = NULL;
        return;
    }

    free(ptr);
    ptr = NULL;
    printf("条件为假\n");
}

// 函数4: 修复数组内存泄漏
void fixed_array_memory_management() {
    printf("函数fixed_array_memory_management: 正确管理二维数组\n");
    int rows = 3, cols = 3;

    // 分配行指针数组
    int** matrix = (int**)malloc(rows * sizeof(int*));
    if (matrix == NULL) {
        fprintf(stderr, "行指针分配失败!\n");
        return;
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
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = i * cols + j;
        }
    }

    if (allocation_failed) {
        // 清理已成功分配的内存
        for (int i = 0; i < rows; i++) {
            if (matrix[i] != NULL) {
                free(matrix[i]);
            }
        }
        free(matrix);
        return;
    }

    // 使用矩阵
    printf("矩阵内容:\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }

    // 正确释放所有内存
    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);
    printf("二维数组内存已完全释放\n");
}

// 函数5: 安全的realloc使用
void safe_realloc_usage() {
    printf("函数safe_realloc_usage: 安全的realloc使用\n");
    int* ptr = (int*)malloc(5 * sizeof(int));
    if (ptr == NULL) {
        fprintf(stderr, "初始分配失败!\n");
        return;
    }

    for (int i = 0; i < 5; i++) {
        ptr[i] = i + 1;
    }

    printf("原始数组: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", ptr[i]);
    }
    printf("\n");

    // 安全的realloc - 使用临时指针
    int* new_ptr = (int*)realloc(ptr, 10 * sizeof(int));
    if (new_ptr == NULL) {
        fprintf(stderr, "realloc失败!\n");
        // 原来的ptr仍然有效，需要释放
        free(ptr);
        return;
    }

    ptr = new_ptr;
    // 初始化新增的元素
    for (int i = 5; i < 10; i++) {
        ptr[i] = i + 1;
    }

    printf("扩容后数组: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", ptr[i]);
    }
    printf("\n");

    free(ptr);
    ptr = NULL;
    printf("realloc内存已安全释放\n");
}

// 函数6: 内存泄漏检测辅助函数
void demonstrate_valgrind_clean_code() {
    printf("函数demonstrate_valgrind_clean_code: Valgrind友好的代码\n");

    // 1. 字符串复制
    const char* source = "Clean memory management";
    char* copy = (char*)malloc(strlen(source) + 1);
    if (copy != NULL) {
        strcpy(copy, source);
        printf("字符串: %s\n", copy);
        free(copy);
        copy = NULL;
    }

    // 2. 动态结构体
    typedef struct {
        int id;
        char* name;
    } Person;

    Person* person = (Person*)malloc(sizeof(Person));
    if (person != NULL) {
        person->id = 123;
        person->name = (char*)malloc(20 * sizeof(char));
        if (person->name != NULL) {
            strcpy(person->name, "John Doe");
            printf("Person: ID=%d, Name=%s\n", person->id, person->name);
            free(person->name);
            person->name = NULL;
        }
        free(person);
        person = NULL;
    }

    printf("所有动态分配的内存都已正确释放\n");
}

int main() {
    printf("=== C语言内存管理解决方案3: 修复内存泄漏 ===\n\n");
    printf("此程序展示了如何编写Valgrind干净的代码\n");
    printf("编译并运行Valgrind验证:\n");
    printf("gcc -g -o solution-03 solution-03.c\n");
    printf("valgrind --leak-check=full --show-leak-kinds=all ./solution-03\n\n");

    // 测试所有修复后的函数
    fixed_simple_memory_leak();
    printf("\n");

    fixed_hidden_memory_leak();
    printf("\n");

    fixed_conditional_memory_leak(1);
    printf("\n");

    fixed_array_memory_management();
    printf("\n");

    safe_realloc_usage();
    printf("\n");

    demonstrate_valgrind_clean_code();
    printf("\n");

    printf("=== 最佳实践总结 ===\n");
    printf("1. 每个malloc/calloc/realloc都要有对应的free\n");
    printf("2. 使用临时指针处理realloc\n");
    printf("3. 所有代码路径都要考虑内存释放（包括错误路径）\n");
    printf("4. 复杂数据结构要递归释放\n");
    printf("5. free后将指针设为NULL\n");
    printf("6. 使用Valgrind等工具定期检查\n");
    printf("7. 在函数开始处规划好内存释放策略\n\n");

    printf("=== 解决方案3结束 - 内存泄漏已全部修复! ===\n");
    return 0;
}