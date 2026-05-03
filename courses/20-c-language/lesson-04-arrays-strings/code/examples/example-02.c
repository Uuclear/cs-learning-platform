#include <stdio.h>
#include <string.h>

int main() {
    char source[] = "Hello";
    char destination[50];
    char str1[] = "apple";
    char str2[] = "banana";

    printf("=== 字符串函数演示 ===\n\n");

    // strcpy - 复制字符串
    printf("1. strcpy 演示:\n");
    strcpy(destination, source);
    printf("   复制 '%s' 到 destination: '%s'\n", source, destination);

    // strcat - 连接字符串
    printf("\n2. strcat 演示:\n");
    strcat(destination, " World!");
    printf("   连接 ' World!' 后: '%s'\n", destination);

    // strlen - 计算字符串长度
    printf("\n3. strlen 演示:\n");
    printf("   '%s' 的长度: %lu\n", destination, strlen(destination));
    printf("   注意：长度不包括结束符 \\0\n");

    // strcmp - 比较字符串
    printf("\n4. strcmp 演示:\n");
    int result1 = strcmp(str1, str2);
    printf("   strcmp('%s', '%s') = %d\n", str1, str2, result1);
    printf("   (%d 表示 '%s' 在字典序中小于 '%s')\n", result1, str1, str2);

    int result2 = strcmp("hello", "hello");
    printf("   strcmp('hello', 'hello') = %d\n", result2);
    printf("   (0 表示两个字符串相等)\n");

    // strchr - 查找字符
    printf("\n5. strchr 演示:\n");
    char text[] = "Hello, World!";
    char *found = strchr(text, 'W');
    if (found != NULL) {
        printf("   在 '%s' 中找到了 'W'，位置: %ld\n", text, found - text);
        printf("   从该位置开始的子字符串: '%s'\n", found);
    }

    // strncpy - 安全复制（指定最大长度）
    printf("\n6. strncpy 演示:\n");
    char safe_dest[10];
    strncpy(safe_dest, "This is a long string", sizeof(safe_dest) - 1);
    safe_dest[sizeof(safe_dest) - 1] = '\0'; // 确保以 null 结尾
    printf("   使用 strncpy 截断后: '%s'\n", safe_dest);

    return 0;
}