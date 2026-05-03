#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * 解决方案2：动态字符串连接
 * 实现安全的字符串连接函数，返回新分配的内存
 */

char* safe_strcat(const char *str1, const char *str2) {
    // 错误检查
    if (str1 == NULL || str2 == NULL) {
        return NULL;
    }

    // 计算所需内存大小
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    size_t total_len = len1 + len2 + 1;  // +1 for null terminator

    // 分配内存
    char *result = malloc(total_len);
    if (result == NULL) {
        return NULL;  // 内存分配失败
    }

    // 复制第一个字符串
    strcpy(result, str1);
    // 连接第二个字符串
    strcat(result, str2);

    return result;
}

// 更高效的版本，避免多次遍历
char* efficient_strcat(const char *str1, const char *str2) {
    if (str1 == NULL || str2 == NULL) {
        return NULL;
    }

    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);
    size_t total_len = len1 + len2 + 1;

    char *result = malloc(total_len);
    if (result == NULL) {
        return NULL;
    }

    // 手动复制以避免额外的strlen调用
    char *ptr = result;
    while (*str1 != '\0') {
        *ptr++ = *str1++;
    }
    while (*str2 != '\0') {
        *ptr++ = *str2++;
    }
    *ptr = '\0';  // 添加字符串结束符

    return result;
}

int main() {
    const char *first = "Hello, ";
    const char *second = "World!";

    printf("字符串1: \"%s\"\n", first);
    printf("字符串2: \"%s\"\n", second);

    // 测试安全版本
    char *combined1 = safe_strcat(first, second);
    if (combined1 != NULL) {
        printf("安全连接结果: \"%s\"\n", combined1);
        free(combined1);  // 不要忘记释放内存！
    }

    // 测试高效版本
    char *combined2 = efficient_strcat(first, second);
    if (combined2 != NULL) {
        printf("高效连接结果: \"%s\"\n", combined2);
        free(combined2);  // 不要忘记释放内存！
    }

    // 测试边界情况
    char *empty_test = safe_strcat("", "Only second");
    if (empty_test != NULL) {
        printf("空字符串测试: \"%s\"\n", empty_test);
        free(empty_test);
    }

    return 0;
}