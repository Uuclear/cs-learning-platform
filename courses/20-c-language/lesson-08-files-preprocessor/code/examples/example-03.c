#include <stdio.h>
#include <stdlib.h>

// 简单的宏定义
#define PI 3.1415926
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))

// 调试宏
#ifdef DEBUG
    #define DEBUG_PRINT(fmt, ...) printf("DEBUG: " fmt "\n", ##__VA_ARGS__)
#else
    #define DEBUG_PRINT(fmt, ...)
#endif

// 平台相关的条件编译
#ifdef _WIN32
    #define CLEAR_SCREEN "cls"
#elif defined(__linux__) || defined(__APPLE__)
    #define CLEAR_SCREEN "clear"
#else
    #define CLEAR_SCREEN "echo -n"
#endif

int main() {
    int x = 5, y = 3;

    printf("PI = %.6f\n", PI);
    printf("MAX(%d, %d) = %d\n", x, y, MAX(x, y));
    printf("%d 的平方 = %d\n", x, SQUARE(x));

    // 调试输出（只有在定义了DEBUG时才会显示）
    DEBUG_PRINT("程序开始执行，x=%d, y=%d", x, y);

    // 清屏命令（根据平台选择）
    system(CLEAR_SCREEN);

    return 0;
}