#include <stdio.h>
#include <string.h>
#include <ctype.h>

// 统计元音字母的函数
int count_vowels(const char *str) {
    int count = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        char c = tolower(str[i]);
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            count++;
        }
    }
    return count;
}

// 字符串反转函数
void reverse_string(char *str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        char temp = str[i];
        str[i] = str[len - 1 - i];
        str[len - 1 - i] = temp;
    }
}

// 检查回文字符串
int is_palindrome(const char *str) {
    int len = strlen(str);
    for (int i = 0; i < len / 2; i++) {
        if (tolower(str[i]) != tolower(str[len - 1 - i])) {
            return 0; // 不是回文
        }
    }
    return 1; // 是回文
}

// 安全的字符串连接函数
char* safe_strcat(char *dest, size_t dest_size, const char *src) {
    if (dest == NULL || src == NULL || dest_size == 0) {
        return NULL;
    }

    size_t dest_len = strlen(dest);
    size_t src_len = strlen(src);

    // 检查是否有足够的空间
    if (dest_len + src_len >= dest_size) {
        // 空间不足，只复制能容纳的部分
        strncat(dest, src, dest_size - dest_len - 1);
    } else {
        strcat(dest, src);
    }

    return dest;
}

int main() {
    printf("=== 字符串处理解决方案 ===\n\n");

    // 元音字母统计
    char text1[] = "Hello World Programming";
    int vowels = count_vowels(text1);
    printf("1. '%s' 中的元音字母数量: %d\n", text1, vowels);

    // 字符串反转
    char text2[] = "Hello World";
    printf("\n2. 字符串反转:\n");
    printf("   原字符串: '%s'\n", text2);
    reverse_string(text2);
    printf("   反转后: '%s'\n", text2);

    // 回文检查
    char palindrome[] = "A man a plan a canal Panama";
    char non_palindrome[] = "Hello World";

    // 移除空格和标点符号用于回文检查（简化版本）
    char clean_palindrome[100];
    int j = 0;
    for (int i = 0; palindrome[i] != '\0'; i++) {
        if (isalpha(palindrome[i])) {
            clean_palindrome[j++] = tolower(palindrome[i]);
        }
    }
    clean_palindrome[j] = '\0';

    printf("\n3. 回文检查:\n");
    printf("   '%s' -> 清理后: '%s'\n", palindrome, clean_palindrome);
    if (is_palindrome(clean_palindrome)) {
        printf("   这是一个回文！\n");
    } else {
        printf("   这不是回文。\n");
    }

    printf("   '%s' -> ", non_palindrome);
    if (is_palindrome(non_palindrome)) {
        printf("这是一个回文！\n");
    } else {
        printf("这不是回文。\n");
    }

    // 安全字符串连接演示
    char buffer[20] = "Hello";
    printf("\n4. 安全字符串连接:\n");
    printf("   初始: '%s'\n", buffer);
    safe_strcat(buffer, sizeof(buffer), " Beautiful World!");
    printf("   连接后: '%s'\n", buffer);

    return 0;
}