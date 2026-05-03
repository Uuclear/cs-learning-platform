#include <stdio.h>
#include <string.h>

// 危险的缓冲区溢出演示
void dangerous_overflow() {
    printf("=== 危险的缓冲区溢出示例 ===\n");
    char small_buffer[10];

    // 这会导致缓冲区溢出！
    strcpy(small_buffer, "This string is way too long for the buffer!");

    printf("溢出后的结果: '%s'\n", small_buffer);
    printf("注意：这可能导致程序崩溃或未定义行为！\n\n");
}

// 安全的字符串操作演示
void safe_string_operations() {
    printf("=== 安全的字符串操作示例 ===\n");
    char safe_buffer[20];
    const char *long_string = "This is a long string";

    // 方法1: 使用 strncpy 并确保 null 结尾
    printf("方法1 - strncpy:\n");
    strncpy(safe_buffer, long_string, sizeof(safe_buffer) - 1);
    safe_buffer[sizeof(safe_buffer) - 1] = '\0';
    printf("   结果: '%s'\n", safe_buffer);

    // 方法2: 先检查长度再复制
    printf("\n方法2 - 长度检查:\n");
    if (strlen(long_string) < sizeof(safe_buffer)) {
        strcpy(safe_buffer, long_string);
        printf("   安全复制: '%s'\n", safe_buffer);
    } else {
        printf("   字符串太长，无法安全复制！\n");
        // 只复制前一部分
        strncpy(safe_buffer, long_string, sizeof(safe_buffer) - 1);
        safe_buffer[sizeof(safe_buffer) - 1] = '\0';
        printf("   截断后: '%s'\n", safe_buffer);
    }

    // 方法3: 使用 snprintf (推荐)
    printf("\n方法3 - snprintf:\n");
    snprintf(safe_buffer, sizeof(safe_buffer), "%s", long_string);
    printf("   snprintf 结果: '%s'\n", safe_buffer);
}

// 自定义安全字符串复制函数
char* safe_strcpy(char *dest, size_t dest_size, const char *src) {
    if (dest == NULL || src == NULL || dest_size == 0) {
        return NULL;
    }

    // 计算可以安全复制的最大字符数
    size_t max_copy = dest_size - 1;
    strncpy(dest, src, max_copy);
    dest[max_copy] = '\0'; // 确保以 null 结尾

    return dest;
}

int main() {
    printf("本程序演示缓冲区溢出的危险性和安全编码实践。\n\n");

    // 注意：在实际生产代码中，永远不要运行危险的溢出示例！
    // 这里仅用于教育目的，在受控环境中演示。
    printf("警告：接下来的溢出示例可能导致程序崩溃！\n");
    printf("按 Enter 继续...\n");
    getchar();

    // dangerous_overflow(); // 注释掉以避免实际溢出

    safe_string_operations();

    // 演示自定义安全函数
    printf("\n=== 自定义安全函数演示 ===\n");
    char custom_buffer[15];
    const char *test_string = "Hello, World!";

    if (safe_strcpy(custom_buffer, sizeof(custom_buffer), test_string) != NULL) {
        printf("自定义安全复制: '%s'\n", custom_buffer);
    }

    return 0;
}