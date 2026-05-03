#include <stdio.h>
#include <limits.h>
#include <math.h>

int main() {
    // 创建整数溢出的情况
    printf("=== 整数溢出检测 ===\n");

    // 方法1: 检测有符号整数加法溢出
    int a = INT_MAX;
    int b = 1;
    // 检查是否会发生溢出
    if (a > INT_MAX - b) {
        printf("警告: %d + %d 会导致溢出!\n", a, b);
    } else {
        printf("%d + %d = %d\n", a, b, a + b);
    }

    // 方法2: 使用无符号整数（回绕是定义良好的）
    unsigned int ua = UINT_MAX;
    unsigned int ub = 1;
    unsigned int result = ua + ub;
    printf("UINT_MAX + 1 = %u (回绕到0)\n", result);

    // 方法3: 溢出后的检测
    int overflow_result = a + b;
    if (overflow_result < a) { // 对于正数加法，结果变小说明溢出
        printf("检测到溢出: 结果 %d 小于操作数 %d\n", overflow_result, a);
    }

    // 浮点精度问题演示和解决方案
    printf("\n=== 浮点精度问题及解决方案 ===\n");

    float x = 0.1f;
    float y = 0.2f;
    float z = x + y;

    printf("直接比较 0.1f + 0.2f == 0.3f: %s\n", (z == 0.3f) ? "true" : "false");

    // 正确的浮点比较方法
    #define FLOAT_EPSILON 1e-6f
    if (fabsf(z - 0.3f) < FLOAT_EPSILON) {
        printf("使用epsilon比较: 认为相等 (差值 = %.10f)\n", fabsf(z - 0.3f));
    } else {
        printf("使用epsilon比较: 不相等 (差值 = %.10f)\n", fabsf(z - 0.3f));
    }

    // 不同精度的比较
    double dx = 0.1;
    double dy = 0.2;
    double dz = dx + dy;
    #define DOUBLE_EPSILON 1e-15

    printf("\n=== 双精度浮点比较 ===\n");
    printf("直接比较 0.1 + 0.2 == 0.3: %s\n", (dz == 0.3) ? "true" : "false");
    if (fabs(dz - 0.3) < DOUBLE_EPSILON) {
        printf("使用双精度epsilon比较: 认为相等 (差值 = %.17f)\n", fabs(dz - 0.3));
    } else {
        printf("使用双精度epsilon比较: 不相等 (差值 = %.17f)\n", fabs(dz - 0.3));
    }

    // 实际应用：安全的整数运算函数示例
    printf("\n=== 安全整数运算示例 ===\n");

    // 安全加法函数（简化版）
    int safe_add(int x, int y, int *result) {
        if (y > 0 && x > INT_MAX - y) return 0; // 溢出
        if (y < 0 && x < INT_MIN - y) return 0; // 下溢
        *result = x + y;
        return 1; // 成功
    }

    int test_result;
    if (safe_add(INT_MAX, 1, &test_result)) {
        printf("安全加法成功: %d\n", test_result);
    } else {
        printf("安全加法检测到溢出，拒绝执行\n");
    }

    return 0;
}