#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// 安全的字符串复制函数（返回实际复制的字符数）
size_t safe_strcpy_with_count(char *dest, size_t dest_size, const char *src) {
    if (dest == NULL || src == NULL || dest_size == 0) {
        return 0;
    }

    size_t src_len = strlen(src);
    size_t copy_len = (src_len < dest_size - 1) ? src_len : dest_size - 1;

    memcpy(dest, src, copy_len);
    dest[copy_len] = '\0';

    return copy_len;
}

// 动态分配安全字符串复制
char* dynamic_safe_strcpy(const char *src) {
    if (src == NULL) {
        return NULL;
    }

    size_t len = strlen(src);
    char *dest = malloc(len + 1);
    if (dest == NULL) {
        return NULL; // 内存分配失败
    }

    strcpy(dest, src);
    return dest;
}

// 安全的输入函数（防止缓冲区溢出）
char* safe_gets(char *buffer, size_t buffer_size) {
    if (buffer == NULL || buffer_size == 0) {
        return NULL;
    }

    if (fgets(buffer, buffer_size, stdin) == NULL) {
        return NULL; // 读取失败
    }

    // 移除换行符（如果存在）
    size_t len = strlen(buffer);
    if (len > 0 && buffer[len - 1] == '\n') {
        buffer[len - 1] = '\0';
    }

    return buffer;
}

// 演示各种安全实践
void demonstrate_safe_practices() {
    printf("=== 安全编码实践演示 ===\n\n");

    // 1. 使用动态内存分配
    printf("1. 动态内存分配:\n");
    const char *long_string = "This is a very long string that we want to copy safely";
    char *dynamic_copy = dynamic_safe_strcpy(long_string);
    if (dynamic_copy != NULL) {
        printf("   动态复制成功: '%s'\n", dynamic_copy);
        free(dynamic_copy); // 记得释放内存
    }

    // 2. 带计数的安全复制
    printf("\n2. 带计数的安全复制:\n");
    char small_buffer[15];
    const char *source = "Hello, World!";
    size_t copied = safe_strcpy_with_count(small_buffer, sizeof(small_buffer), source);
    printf("   复制了 %zu 个字符: '%s'\n", copied, small_buffer);

    // 3. 安全输入
    printf("\n3. 安全输入演示:\n");
    char input_buffer[20];
    printf("   请输入一段文本（最多19个字符）: ");
    if (safe_gets(input_buffer, sizeof(input_buffer)) != NULL) {
        printf("   您输入的是: '%s'\n", input_buffer);
    } else {
        printf("   输入失败\n");
    }

    // 4. 边界检查的数组访问
    printf("\n4. 边界检查的数组访问:\n");
    int numbers[] = {1, 2, 3, 4, 5};
    int array_size = sizeof(numbers) / sizeof(numbers[0]);
    int index = 10; // 超出边界

    if (index >= 0 && index < array_size) {
        printf("   numbers[%d] = %d\n", index, numbers[index]);
    } else {
        printf("   错误：索引 %d 超出数组边界 [0, %d]\n", index, array_size - 1);
    }
}

// 安全的字符串格式化函数
int safe_snprintf_demo() {
    printf("\n5. 安全格式化演示:\n");
    char buffer[50];
    int num = 42;
    const char *name = "Alice";

    // snprintf 确保不会溢出
    int result = snprintf(buffer, sizeof(buffer), "Hello %s, your number is %d!", name, num);
    if (result < 0) {
        printf("   格式化错误\n");
        return -1;
    } else if (result >= sizeof(buffer)) {
        printf("   警告：输出被截断\n");
    }
    printf("   格式化结果: '%s'\n", buffer);

    return 0;
}

int main() {
    printf("本程序演示C语言中的安全编码最佳实践。\n\n");

    demonstrate_safe_practices();
    safe_snprintf_demo();

    printf("\n记住这些安全原则：\n");
    printf("- 始终检查数组和缓冲区边界\n");
    printf("- 使用安全的字符串函数（strncpy, strncat, snprintf）\n");
    printf("- 考虑使用动态内存分配来适应实际需求\n");
    printf("- 对所有输入进行验证和清理\n");
    printf("- 编译时启用安全检查选项（如 -fstack-protector）\n");

    return 0;
}