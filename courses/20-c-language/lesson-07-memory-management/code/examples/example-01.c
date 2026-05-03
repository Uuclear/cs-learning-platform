#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 示例1: malloc/free 基础与常见错误演示

int main() {
    printf("=== C语言内存管理示例1: malloc/free基础 ===\n\n");

    // 1. 正确的malloc使用
    printf("1. 正确的malloc使用:\n");
    int* ptr1 = (int*)malloc(sizeof(int));
    if (ptr1 == NULL) {
        printf("内存分配失败!\n");
        return 1;
    }
    *ptr1 = 42;
    printf("分配的值: %d\n", *ptr1);
    free(ptr1);  // 正确释放
    ptr1 = NULL; // 避免悬空指针
    printf("内存已正确释放\n\n");

    // 2. 忘记检查malloc返回值的危险
    printf("2. malloc返回NULL的情况:\n");
    // 尝试分配超大内存（可能会失败）
    size_t huge_size = (size_t)-1; // 最大可能的size_t值
    int* ptr2 = (int*)malloc(huge_size);
    if (ptr2 == NULL) {
        printf("分配超大内存失败 - 这是正常的!\n");
    } else {
        printf("意外成功分配了超大内存!\n");
        free(ptr2);
    }
    printf("\n");

    // 3. 内存泄漏示例（故意不释放）
    printf("3. 内存泄漏示例:\n");
    int* ptr3 = (int*)malloc(sizeof(int));
    *ptr3 = 100;
    printf("分配了内存但不释放 - 这就是内存泄漏!\n");
    // 注意：这里故意不调用free(ptr3)
    printf("(程序结束后操作系统会回收内存，但在长时间运行的程序中这很危险)\n\n");

    // 4. 双重释放的危险
    printf("4. 双重释放示例:\n");
    int* ptr4 = (int*)malloc(sizeof(int));
    *ptr4 = 200;
    free(ptr4);
    printf("第一次free完成\n");
    // free(ptr4); // 这行被注释掉了，因为会导致未定义行为！
    printf("注意：双重释放会导致程序崩溃或安全漏洞!\n\n");

    // 5. calloc vs malloc
    printf("5. calloc vs malloc:\n");
    int* malloc_arr = (int*)malloc(5 * sizeof(int));
    int* calloc_arr = (int*)calloc(5, sizeof(int));

    printf("malloc分配的数组内容: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", malloc_arr[i]); // 可能是随机值
    }
    printf("\n");

    printf("calloc分配的数组内容: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", calloc_arr[i]); // 一定是0
    }
    printf("\n");

    free(malloc_arr);
    free(calloc_arr);
    printf("calloc和malloc内存都已释放\n\n");

    // 6. realloc示例
    printf("6. realloc示例:\n");
    int* ptr6 = (int*)malloc(3 * sizeof(int));
    for (int i = 0; i < 3; i++) {
        ptr6[i] = i + 1;
    }
    printf("原始数组: ");
    for (int i = 0; i < 3; i++) {
        printf("%d ", ptr6[i]);
    }
    printf("\n");

    // 扩容到5个元素
    int* new_ptr6 = (int*)realloc(ptr6, 5 * sizeof(int));
    if (new_ptr6 != NULL) {
        ptr6 = new_ptr6;
        // 新增的元素内容是未定义的
        ptr6[3] = 4;
        ptr6[4] = 5;
        printf("扩容后数组: ");
        for (int i = 0; i < 5; i++) {
            printf("%d ", ptr6[i]);
        }
        printf("\n");
        free(ptr6);
    } else {
        printf("realloc失败!\n");
        free(ptr6);
    }

    printf("\n=== 示例1结束 ===\n");
    return 0;
}