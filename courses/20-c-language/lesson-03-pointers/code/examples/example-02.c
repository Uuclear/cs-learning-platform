#include <stdio.h>

/**
 * 示例2：指针运算与数组遍历
 * 演示指针算术运算和使用指针遍历数组
 */

int main() {
    // 整数数组
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    printf("=== 数组基本信息 ===\n");
    printf("数组大小: %d 个元素\n", size);
    printf("每个int占用: %zu 字节\n", sizeof(int));
    printf("数组总大小: %zu 字节\n", sizeof(numbers));

    printf("\n=== 指针算术演示 ===\n");
    int *ptr = numbers;  // 数组名等价于 &numbers[0]

    for (int i = 0; i < size; i++) {
        printf("地址 ptr+%d = %p, 值 = %d\n",
               i, (void*)(ptr + i), *(ptr + i));
    }

    printf("\n=== 指针自增遍历 ===\n");
    ptr = numbers;  // 重置指针到数组开始
    printf("使用指针自增遍历数组: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", *ptr);
        ptr++;  // 指针自增，指向下一个元素
    }
    printf("\n");

    printf("\n=== 指针相减计算距离 ===\n");
    int *start = numbers;
    int *end = numbers + size - 1;  // 指向最后一个元素

    printf("起始地址: %p\n", (void*)start);
    printf("结束地址: %p\n", (void*)end);
    printf("元素个数: %td\n", end - start + 1);  // 指针相减得到元素个数

    printf("\n=== 字符数组指针操作 ===\n");
    char text[] = "Hello";
    char *char_ptr = text;

    printf("字符串: %s\n", text);
    printf("逐字符访问: ");
    while (*char_ptr != '\0') {
        printf("%c ", *char_ptr);
        char_ptr++;
    }
    printf("\n");

    return 0;
}