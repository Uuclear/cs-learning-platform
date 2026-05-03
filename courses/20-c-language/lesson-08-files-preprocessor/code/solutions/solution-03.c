#include <stdio.h>
#include <stdlib.h>

// 跨平台问候程序
int main() {
    printf("=== 跨平台问候程序 ===\n");

#ifdef _WIN32
    printf("Hello Windows!\n");
    printf("您正在使用 Windows 系统。\n");
#elif defined(__linux__)
    printf("Hello Linux!\n");
    printf("您正在使用 Linux 系统。\n");
#elif defined(__APPLE__)
    printf("Hello macOS!\n");
    printf("您正在使用 macOS 系统。\n");
#else
    printf("Hello Unknown Platform!\n");
    printf("您正在使用未知的操作系统。\n");
#endif

    // 根据平台显示不同的特性信息
#ifdef _WIN32
    printf("Windows 特性: 使用 \\ 作为路径分隔符\n");
#elif defined(__unix__) || defined(__APPLE__)
    printf("Unix-like 特性: 使用 / 作为路径分隔符\n");
#endif

    // 条件编译调试信息
#ifdef DEBUG
    printf("[DEBUG] 编译时启用了调试模式\n");
#endif

    return 0;
}